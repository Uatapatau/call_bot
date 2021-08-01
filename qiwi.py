from pyqiwip2p import QiwiP2P
from pyqiwip2p.types import QiwiCustomer, QiwiDatetime

p2p = QiwiP2P(auth_key="eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6ImM1bHJpNy0wMCIsInVzZXJfaWQiOiI3OTc3OTIzMTg1NSIsInNlY3JldCI6ImQwZDFlNjU3NGY2NjY5YTMyYTM0ZGE5NjU5NzM3MTQ0Mjg4MmNmYjQwMGZhZjYyYjRiZTQyNTY5MjdmNjAwOGUifX0=")










def test():
    amount = 1 # Сумма 1 рубль
    lifetime = 15 # Форма будет жить 15 минут
    comment = 'Купить арбуз' # Комментарий
    bill = p2p.bill(amount=amount, lifetime=lifetime, comment=comment) # Выставление счета
    return bill.pay_url #await message.answer(f'Сумма: {amount}\nСсылка живет: {lifetime} минут\nСсылка:\n{bill.pay_url}') # Отправляем ссылку человеку







def check(bill_id):
    status = p2p.check_status(bill_id) # bill_id - номер платежа
    if status == 'PAID': # Если статус счета оплачен (PAID)
        return True                                           #      await message.answer('Оплата прошла успешно!')# return true 
    else:                                    # В другом случае
        return False                       #   await message.answer('Вы не оплатили счет!')#return false