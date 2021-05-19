# -*- coding: utf-8 -*-

# надо следить за тем, чтобы диапазоны в разных файлах states не пересекались
# иначе данные одного диалога будут пересекаться с данными другого диалога
ORIGIN = 1000

# STATES
(
    MAIN_MENU,
    SUPPORT,
    SPAM,
    STOPPING,
    BALANCE_MENU,
    FILL_BALANCE,  
    GET_PROMO,  
    BACK_TO_MENU,
    SAVE_PHONE,
    SAVE_ATTEMPS,  
    SPAM_MENU, 
    START_SPAM,
    UP,
    SAVE_PROMO,
    CHECK_BALANCE,
    PAY_MENU,
    BACK_TO_BALANCE_MENU,
    GET_PRICE_MENU,
    GET_PRICE,
    SAVE_TYPE,
    TYPE_MENU,
    ATTEMP_MENU,
) = range(ORIGIN, ORIGIN + 22)
# DATA
(
    USER_ID, BILL_OBJ, BALANCE, AMOUNT, ENGINE, PHONE, TYPE, TIME, PRICE
)=range(ORIGIN * 2, ORIGIN*2 + 9)