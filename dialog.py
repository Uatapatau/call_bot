from telegram.ext import CommandHandler, ConversationHandler
from telegram.ext import MessageHandler, Filters, CallbackQueryHandler
import conversation
from states import *

def main_conversation(cmd):
    return ConversationHandler(
        entry_points=[
            CommandHandler(cmd, conversation.start),
        ],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(conversation.show_support,
                                     pattern='^' + str(SUPPORT) + '$'),
                spam_conversation('^' + str(SPAM) + '$'),
                balance_conversation('^' + str(BALANCE_MENU) + '$'),
                CallbackQueryHandler(conversation.admin_menu,
                                     pattern='^' + str(ADMIN_DLG) + '$'),
            ],
            ADMIN_DLG:[
                CallbackQueryHandler(conversation.perform_add_bonus,
                                     pattern='^' + str(INPUT_BONUS) + '$'),
                CallbackQueryHandler(conversation.return_to_menu_from_admin,
                                     pattern='^' + str(BACK_TO_MENU) + '$'),
            ],
            SAVE_BONUS: [
                MessageHandler(
                    Filters.text, conversation.save_bonus),
            ],
        },

        fallbacks=[
            MessageHandler(
                Filters.text, conversation.process_arbitrary_message_main),
            CallbackQueryHandler(conversation.process_arbitrary_callback_main)
        ],

        map_to_parent={
            STOPPING: ConversationHandler.END,
            ConversationHandler.END: ConversationHandler.END,
            BALANCE_MENU: ConversationHandler.END,
            SPAM: ConversationHandler.END
        },
    )


def balance_conversation(pattern):
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(conversation.balannce_dlg, pattern=pattern)
        ],
        states={
            BALANCE_MENU: [
                CallbackQueryHandler(conversation.get_price,
                                     pattern='^' + str(GET_PRICE_MENU) + '$'),
                CallbackQueryHandler(conversation.perform_promo_save,
                                     pattern='^' + str(GET_PROMO) + '$'),
                CallbackQueryHandler(conversation.return_to_menu,
                                     pattern='^' + str(BACK_TO_MENU) + '$'),
            ],
            SAVE_PROMO: [
                MessageHandler(
                    Filters.text, conversation.get_promo),
            ],
            PAY_MENU:[
                CallbackQueryHandler(conversation.check_balance,
                                     pattern='^' + str(CHECK_BALANCE) + '$'),
            ],
            GET_PRICE_MENU:[
                CallbackQueryHandler(conversation.perform_pay,
                                     pattern='^PRICE_'),
                CallbackQueryHandler(conversation.return_to_menu,
                                     pattern='^' + str(BACK_TO_BALANCE_MENU) + '$'),
            ]
        },

        fallbacks=[
            CommandHandler('back', conversation.return_to_balance_menu),
            MessageHandler(
                Filters.text, conversation.process_arbitrary_message_sub),
            CallbackQueryHandler(conversation.process_arbitrary_callback_sub)
        ],

        map_to_parent={
            STOPPING: STOPPING,
            ConversationHandler.END: ConversationHandler.END,
            UP: MAIN_MENU
        },
    )


def spam_conversation(pattern):
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(conversation.spam_dlg, pattern=pattern)
        ],
        states={
            SAVE_PHONE: [
                MessageHandler(
                    Filters.text, conversation.save_phone),
            ],
            SAVE_ATTEMPS: [
                MessageHandler(
                    Filters.text, conversation.save_attemp),
            ],
            SPAM_MENU: [
                CallbackQueryHandler(conversation.perform_phone_save,
                                     pattern='^' + str(SAVE_PHONE) + '$'),
                CallbackQueryHandler(conversation.get_attemp_dlg,
                                     pattern='^' + str(ATTEMP_MENU) + '$'),
                CallbackQueryHandler(conversation.get_type_dlg,
                                     pattern='^' + str(TYPE_MENU) + '$'),
                CallbackQueryHandler(conversation.start_spam,
                                     pattern='^' + str(START_SPAM) + '$'),
                CallbackQueryHandler(conversation.return_to_menu,
                                     pattern='^' + str(BACK_TO_MENU) + '$'),
            ],
            TYPE_MENU:[
                CallbackQueryHandler(conversation.save_type,
                                     pattern='^TYPE_'),
            ],
            ATTEMP_MENU:[
                CallbackQueryHandler(conversation.save_attemp,
                                     pattern='^ATTEMP_'),
            ]
        },

        fallbacks=[
            MessageHandler(
                Filters.text, conversation.process_arbitrary_message_sub),
            CallbackQueryHandler(conversation.process_arbitrary_callback_sub)
        ],

        map_to_parent={
            STOPPING: STOPPING,
            ConversationHandler.END: ConversationHandler.END,
            UP: MAIN_MENU
        },
        conversation_timeout=600
    )
