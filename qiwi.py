from pyqiwip2p import QiwiP2P

p2p = QiwiP2P(auth_key="eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6ImM1bHJpNy0wMCIsInVzZXJfaWQiOiI3OTc3OTIzMTg1NSIsInNlY3JldCI6ImQwZDFlNjU3NGY2NjY5YTMyYTM0ZGE5NjU5NzM3MTQ0Mjg4MmNmYjQwMGZhZjYyYjRiZTQyNTY5MjdmNjAwOGUifX0=")


def create_pay(amount=100, lifetime=10):
    comment = 'Пополнение баланса'
    bill = p2p.bill(amount=amount, lifetime=lifetime, comment=comment)
    return bill


def check_pay(bill_id):
    status = p2p.check(bill_id)
    if status.status == 'PAID': 
        return True                                         
    else:                                  
        return False                       
