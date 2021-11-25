from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)

# import icons
from states import *
import settings
from qiwi import check_pay, create_pay, p2p
from utils import get_obj_from_callback
import db
from methods import Bomber
from threading import Thread


def process_arbitrary_message_main(update, context):
    # это перехват инициативы пользователем: неожиданное сообщение
    return main_menu_dlg(update, context)


def process_arbitrary_callback_main(update, context):
    # необработанный callback - ошибка в структуре диалога - не нашлось подходящего обработчика
    return main_menu_dlg(update, context)


def process_arbitrary_message_sub(update, context):
    # это перехват инициативы пользователем: неожиданное сообщение
    return return_to_menu(update, context)


def process_arbitrary_callback_sub(update, context):
    # необработанный callback - ошибка в структуре диалога - не нашлось подходящего обработчика
    return return_to_menu(update, context)


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
    ud[ADMINS_ID] = [476947760, 622806461, 643516740]
    ud[TIME] = ''
    ud[PRICE] = ''
    db.create_row(ud[ENGINE], db.Promo, {
                  'bonus_id': 'FurInU', 'bonus': 100, 'data': 'test'})
    db.create_row(ud[ENGINE], db.User, {
                  'user_id': message.from_user.id, 'balance': 0})
    ud[BALANCE] = db.get_row(ud[ENGINE], db.User, {
                             'user_id': ud[USER_ID]}).balance
    return main_menu_dlg(update, context)


def main_menu_dlg(update, context):
    message = update.message if update.message is not None else update.callback_query.message

    buttons = [
        [InlineKeyboardButton(
            text=f'Звонки {emoji_hi}', callback_data=str(SPAM))],
        [InlineKeyboardButton(
            text=f'Поддержка {emoji_sup}', callback_data=str(SUPPORT))],
        [InlineKeyboardButton(
            text=f'Баланс {emoji_money}', callback_data=str(BALANCE_MENU))],
    ]
    if context.user_data[USER_ID] in context.user_data[ADMINS_ID]:
        buttons.append([InlineKeyboardButton(
            text='Админка', callback_data=str(ADMIN_DLG))])
    keyboard = InlineKeyboardMarkup(buttons)
    message.reply_text(
        text=f"Ваш баланс: {context.user_data[BALANCE]}", reply_markup=keyboard)
    return MAIN_MENU


def admin_menu(update, context):
    message = update.message if update.message is not None else update.callback_query.message
    buttons = [
        [
            InlineKeyboardButton(
                text=f'Добавить промокод', callback_data=str(INPUT_BONUS)),
            InlineKeyboardButton(
                text=f'Назад', callback_data=str(BACK_TO_MENU)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    message.reply_text(
        text=f"Вы ёбаный админ", reply_markup=keyboard)
    return ADMIN_DLG


def perform_add_bonus(update, context):
    message = update.message if update.message is not None else update.callback_query.message
    message.reply_text(text="Введите данные для добавления через запятую\n"
                       "<промокод>, <сумма промокода>, <число или любое слово>")
    return SAVE_BONUS


def save_bonus(update, context):
    message = update.message if update.message is not None else update.callback_query.message
    bonus = message.text.split(',')
    try:
        row = db.create_promo(context.user_data[ENGINE], bonus[0], {
            'bonus_id': bonus[0], 'bonus': bonus[1], 'data': bonus[2]})
        if row:
            message.reply_text(text="Уже существует такой промокод")
            return admin_menu(update, context)
    except:
        message.reply_text(text="Неверные данные")
        return admin_menu(update, context)

    db.create_log(context.user_data[ENGINE], context.user_data[USER_ID],
                  'Add promo {promo.bonus}', f'{context.user_data[AMOUNT]}')
    message.reply_text(
        text=f"Промокод добавле\n'bonus_id': {bonus[0]}, 'bonus': {bonus[1]}, 'data': {bonus[2]}")
    return admin_menu(update, context)


def show_support(update, context):
    message = update.message if update.message is not None else update.callback_query.message
    message.reply_text(
        text=f"Для обращения в поддержку перейдите по ссылкам, укажите id '{context.user_data[USER_ID]}' и опишите вашу проблему\n https://t.me/TexBomber ")
    return main_menu_dlg(update, context)


def return_to_menu(update, context):
    main_menu_dlg(update, context)
    return UP


def return_to_menu_from_admin(update, context):
    return main_menu_dlg(update, context)


def balannce_dlg(update, context):
    message = update.message if update.message is not None else update.callback_query.message
    buttons = [
        [
            InlineKeyboardButton(
                text=f'Пополнить баланс {emoji_money}', callback_data=str(GET_PRICE_MENU)),
            InlineKeyboardButton(
                text=f'Ввести промокод {emoji_promo}', callback_data=str(GET_PROMO)),

        ],
        [
            InlineKeyboardButton(
                text='Вернуться в меню', callback_data=str(BACK_TO_MENU)),

        ]

    ]
    keyboard = InlineKeyboardMarkup(buttons)
    message.reply_text(
        text=f"Ваш баланс:  {context.user_data[BALANCE]}", reply_markup=keyboard)
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
    message.reply_text(text=f"Введите промокод {emoji_promo}")
    return SAVE_PROMO


def get_promo(update, context):
    message = update.message if update.message is not None else update.callback_query.message
    promo = db.get_row(context.user_data[ENGINE], db.Promo, {
                       'bonus_id': message.text})
    if promo:
        data = promo.data
        try:
            data = int(data)
            if data > 0:
                data -= 1
                db.update_promo(
                    context.user_data[ENGINE], message.text, str(data))
                context.user_data[BALANCE] += promo.bonus
                db.update_balance(
                    context.user_data[ENGINE], context.user_data[USER_ID], context.user_data[BALANCE])
                message.reply_text(
                    text=f"Ваш баланс пополнен на {promo.bonus} рублей")
                db.create_log(context.user_data[ENGINE], context.user_data[USER_ID],
                              'Use promo {promo.bonus}', f'{context.user_data[AMOUNT]}')
                main_menu_dlg(update, context)
                return UP
            else:
                message.reply_text(text=f"Этот промокод уже не действителен")
                return balannce_dlg(update, context)

        except ValueError:
            data_list = data.split(',')
            if str(context.user_data[USER_ID]) not in data_list:
                data += f',{context.user_data[USER_ID]}'
                db.update_promo(context.user_data[ENGINE], message.text, data)
                context.user_data[BALANCE] += promo.bonus
                db.update_balance(
                    context.user_data[ENGINE], context.user_data[USER_ID], context.user_data[BALANCE])
                message.reply_text(
                    text=f"Ваш баланс пополнен на {promo.bonus} рублей")
                db.create_log(context.user_data[ENGINE], context.user_data[USER_ID],
                              'Use promo {promo.bonus}', f'{context.user_data[AMOUNT]}')
                main_menu_dlg(update, context)
                return UP
            else:
                message.reply_text(text=f"Вы уже использовали этот промокод")
                return balannce_dlg(update, context)
        except Exception as e:
            a = 1
    message.reply_text(text=f"Неверный промокод")
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

    text = f"Данные для пранка {emoji_clown} :\n"\
        f"-Ваш баланс: {ud[BALANCE]} {emoji_moneyb} рублей\n"\
        f"-Номер: {ud[PHONE]} {emoji_phone}\n"\
        f"-Тип: {ud[TYPE]}\n"\
        f"-Время: {ud[TIME]} {emoji_time}"
    if ud[PRICE]:
        text += f"\n-Цена: {ud[PRICE]} рублей {emoji_moneyb}"
    message.reply_text(text=text , reply_markup=keyboard)
    return SPAM_MENU


def get_type_dlg(update, context):
    message = update.message if update.message is not None else update.callback_query.message
    buttons = [
        [
            InlineKeyboardButton(
                text='СМС', callback_data='TYPE_Смс')
            # InlineKeyboardButton(
            #     text='Звонки', callback_data='TYPE_Звонок'),
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
    minutes = [[1,5], [5,15], [10,20], [30,50], [40,80], [60,100]]
    minutes_button = []
    for minute in minutes:
        minutes_button.append(
            InlineKeyboardButton(text=f'{minute[0]} минут/ {minute[1]} рублей',
                                 callback_data=f'ATTEMP_{minute[0],minute[1]}'))

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
    data = get_obj_from_callback(update.callback_query.data)
    data = data.replace('(','').replace(')','').split(',')
    context.user_data[TIME] =int(data[0])
    context.user_data[PRICE] = int(data[1])
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
