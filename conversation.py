from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)

# import icons
from states import *
import settings
from qiwi import check_pay, create_pay, p2p
from utils import get_obj_from_callback
import db
from methods import Bomber
from threading import Thread


def process_arbitrary_command(update, context):
    # это перехват инициативы пользователем: неожиданно другая команда введена
    message = update.message if update.message is not None else update.callback_query.message
    message.reply_text(
        text='Запуск других команд возможен после выхода из меню')


def process_arbitrary_message(update, context):
    # это перехват инициативы пользователем: неожиданное сообщение
    message = update.message if update.message is not None else update.callback_query.message
    text = 'Воспользуйтесь диалоговыми окнами'
    message.reply_text(text)


def process_arbitrary_callback(update, context):
    # необработанный callback - ошибка в структуре диалога - не нашлось подходящего обработчика
    message = update.message if update.message is not None else update.callback_query.message
    text = 'Взаимодействуйте с послденим диалоговым окном'
    message.reply_text(text)


def stop(update, context):
    message = update.message if update.message is not None else update.callback_query.message
    message.reply_text(text='До свидания, приходите ещё.')
    return STOPPING


def start(update, context):
    message = update.message if update.message \
        is not None else update.callback_query.message
    ud = context.user_data
    ud[ENGINE] = db.create_db()
    ud[USER_ID] = message.from_user.id
    ud[PHONE] = ''
    ud[TYPE] = ''
    ud[TIME] = ''
    db.create_row(ud[ENGINE], db.Promo, {
                  'bonus_id': 'BonusBest', 'bonus': 100})
    db.create_row(ud[ENGINE], db.User, {
                  'user_id': message.from_user.id, 'balance': 0})
    ud[BALANCE] = db.get_row(ud[ENGINE], db.User, {
                             'user_id': ud[USER_ID]}).balance
    return main_menu_dlg(update, context)


def main_menu_dlg(update, context):
    message = update.message if update.message is not None else update.callback_query.message

    buttons = [
        [
            InlineKeyboardButton(
                text='Звонки', callback_data=str(SPAM)),
            InlineKeyboardButton(
                text='Поддержка', callback_data=str(SUPPORT)),
            InlineKeyboardButton(
                text='Баланс', callback_data=str(BALANCE_MENU)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    message.reply_text(
        text=f"Ваш баланс: {context.user_data[BALANCE]}", reply_markup=keyboard)
    return MAIN_MENU


def show_support(update, context):
    message = update.message if update.message is not None else update.callback_query.message
    message.reply_text(
        text=f"Для обращения в поддержку перейдите по ссылкам, укажите id '{context.user_data[USER_ID]}' и опишите вашу проблему")
    return main_menu_dlg(update, context)


def return_to_menu(update, context):
    main_menu_dlg(update, context)
    return UP


def balannce_dlg(update, context):
    message = update.message if update.message is not None else update.callback_query.message

    buttons = [
        [
            InlineKeyboardButton(
                text='Пополнить баланс', callback_data=str(GET_PRICE_MENU)),
            InlineKeyboardButton(
                text='Ввести промокод', callback_data=str(GET_PROMO)),

        ],
        [
            InlineKeyboardButton(
                text='Вернуться в меню', callback_data=str(BACK_TO_MENU)),
        ]

    ]
    keyboard = InlineKeyboardMarkup(buttons)
    message.reply_text(
        text=f"Ваш баланс: {context.user_data[BALANCE]}", reply_markup=keyboard)
    return BALANCE_MENU


def get_price(update, context):
    message = update.message if update.message is not None else update.callback_query.message
    prices = [1, 100, 200, 300, 400, 500]
    price_button = []
    for price in prices:
        price_button.append(
            InlineKeyboardButton(text=f'{price}',
                                 callback_data=f'PRICE_{price}'))

    buttons = list(
        zip(price_button[:len(price_button) // 2],
            price_button[len(price_button) // 2:]))

    if len(price_button) % 2 == 1:
        buttons.append([price_button[-1]])

    keyboard = InlineKeyboardMarkup(buttons)
    message.reply_text(
        text='Выберите сумму для пополнения', reply_markup=keyboard)
    return GET_PRICE_MENU


def perform_pay(update, context):
    amount = get_obj_from_callback(update.callback_query.data)
    context.user_data[BILL_OBJ] = create_pay(amount=int(amount))
    context.user_data[AMOUNT] = int(amount)
    return fill_balance(update, context)


def fill_balance(update, context):
    message = update.message if update.message is not None else update.callback_query.message
    buttons = [
        [
            InlineKeyboardButton(
                text='Проверить', callback_data=str(CHECK_BALANCE)),
            InlineKeyboardButton(
                text='Отмена', callback_data=str(BACK_TO_BALANCE_MENU)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    message.reply_text(
        text='Что бы пополнить баланс перейдите по ссылке: '
        f'\n {context.user_data[BILL_OBJ].pay_url}', reply_markup=keyboard)
    return PAY_MENU


def check_balance(update, context):
    pay_status = check_pay(context.user_data[BILL_OBJ].bill_id)
    ud = context.user_data
    if pay_status:
        context.user_data[BILL_OBJ] = None
        db.update_balance(
            context.user_data[ENGINE], context.user_data[USER_ID],  ud[BALANCE] + ud[AMOUNT])

        ud[BALANCE] = db.get_row(ud[ENGINE], db.User, {
                                 'user_id': ud[USER_ID]}).balance

        db.create_log(ud[ENGINE], ud[USER_ID], 'fill_balance', f'{ud[AMOUNT]}')
        main_menu_dlg(update, context)
        return MAIN_MENU
    else:
        return fill_balance(update, context)


def perform_promo_save(update, context):
    message = update.message if update.message is not None else update.callback_query.message
    message.reply_text(text="Введите промокод")
    return SAVE_PROMO


def get_promo(update, context):
    message = update.message if update.message is not None else update.callback_query.message
    promo = db.get_row(context.user_data[ENGINE], db.Promo, {
                       'bonus_id': message.text})
    if promo:
        context.user_data[BALANCE] += promo.bonus
        db.update_balance(
            context.user_data[ENGINE], context.user_data[USER_ID], context.user_data[BALANCE])
        message.reply_text(text=f"Ваш баланс пополнен на {promo.bonus} рублей")
        main_menu_dlg(update, context)
        return UP

    message.reply_text(text="Не верный промокод")
    return balannce_dlg(update, context)


def return_to_balance_menu(update, context):
    p2p.reject(context.user_data[BILL_OBJ].bill_id)
    balannce_dlg(update, context)
    return BALANCE_MENU


def spam_dlg(update, context):
    message = update.message if update.message is not None else update.callback_query.message
    ud = context.user_data
    buttons = [
        [
            InlineKeyboardButton(
                text='Номер', callback_data=str(SAVE_PHONE)),
            InlineKeyboardButton(
                text='Тип', callback_data=str(TYPE_MENU)),
            InlineKeyboardButton(
                text='Время', callback_data=str(ATTEMP_MENU)),
        ],
        [
            InlineKeyboardButton(
                text='Вернуться в меню', callback_data=str(BACK_TO_MENU)),
            InlineKeyboardButton(
                text='Старт', callback_data=str(START_SPAM)),
        ]

    ]
    keyboard = InlineKeyboardMarkup(buttons)

    price = ''
    if ud[TYPE] and ud[TIME]:
        if ud[TYPE] == 'Смс':
            count = 20
        else:
            count = 100
        ud[PRICE] = ud[TIME]*count
        price = f"-Цена: {ud[PRICE]}"

    text = "Данные для пранка:\n"\
        f"-Ваш баланс: {ud[BALANCE]}\n"\
        f"-Номер: {ud[PHONE]}\n"\
        f"-Тип: {ud[TYPE]}\n"\
        f"-Время: {ud[TIME]}\n"

    message.reply_text(text=text + price, reply_markup=keyboard)
    return SPAM_MENU


def get_type_dlg(update, context):
    message = update.message if update.message is not None else update.callback_query.message
    buttons = [
        [
            InlineKeyboardButton(
                text='СМС', callback_data='TYPE_Смс'),
            InlineKeyboardButton(
                text='Звонки', callback_data='TYPE_Звонок'),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    message.reply_text(
        text='Выберите тип пранка', reply_markup=keyboard)
    return TYPE_MENU


def save_type(update, context):
    context.user_data[TYPE] = get_obj_from_callback(update.callback_query.data)
    return spam_dlg(update, context)


def perform_phone_save(update, context):
    message = update.message if update.message is not None else update.callback_query.message
    message.reply_text(text="Введите номер")
    return SAVE_PHONE


def save_phone(update, context):
    message = update.message if update.message is not None else update.callback_query.message
    context.user_data[PHONE] = message.text
    return spam_dlg(update, context)


def get_attemp_dlg(update, context):
    message = update.message if update.message is not None else update.callback_query.message
    minutes = [1, 10, 20, 30, 40, 50]
    minutes_button = []
    for minute in minutes:
        minutes_button.append(
            InlineKeyboardButton(text=f'{minute} минут',
                                 callback_data=f'ATTEMP_{minute}'))

    buttons = list(
        zip(minutes_button[:len(minutes_button) // 2],
            minutes_button[len(minutes_button) // 2:]))

    if len(minutes_button) % 2 == 1:
        buttons.append([minutes_button[-1]])

    keyboard = InlineKeyboardMarkup(buttons)
    message.reply_text(
        text='Выберите количество времени для пранка (смс 20 рублей, звонок 100 рублей за 1 минуту)', reply_markup=keyboard)
    return ATTEMP_MENU


def save_attemp(update, context):
    context.user_data[TIME] = int(
        get_obj_from_callback(update.callback_query.data))
    return spam_dlg(update, context)


def start_spam(update, context):
    message = update.message if update.message is not None else update.callback_query.message
    ud = context.user_data
    remainder = ud[BALANCE]-ud[PRICE]
    if remainder >= 0:
        db.update_balance(
            context.user_data[ENGINE], context.user_data[USER_ID], remainder)
        db.create_log(ud[ENGINE], ud[USER_ID], 'spam_start',
                      f'phone:{ud[PHONE]}/type:{ud[TYPE]}/time:{ud[TIME]}/price:{ud[PRICE]}')
        spam = Bomber(ud[PHONE])

        if ud[TYPE] == 'Смс':
            Thread(target=spam.sms, args=[ud[TIME]], daemon=True).start()

        else:
            Thread(target=spam.call, args=[ud[TIME]], daemon=True).start()

        ud[PHONE] = ''
        ud[TYPE] = ''
        ud[TIME] = ''
        ud[BALANCE] = remainder
        ud[PRICE] = ''

        text = f"Запускаю пранк на номер {ud[PHONE]}"
        message.reply_text(text=text)
        main_menu_dlg(update, context)
        return UP
    else:
        text = 'Не хватает средст для запуска пранка\n'\
            f'Ваш баланс: {ud[BALANCE]}'\
            f'Цена: {ud[PRICE]}'
        message.reply_text(text=text)
        return spam_dlg(update, context)
