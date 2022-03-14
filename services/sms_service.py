from typing import List
import requests
import random
from core.config import SMS_PASSWORD, SMS_LOGIN


async def send_sms(phone: str, message: str):
    try:
        response = requests.post(f'https://smsc.kz/sys/send.php?'
                                 f'login={SMS_LOGIN}&'
                                 f'psw={SMS_PASSWORD}&'
                                 f'phones={phone}&'
                                 f'mes={message}')
        print(response.text)
    except Exception as e:
        print(e)


async def generate_code():
    number = random.randint(1000, 9999)
    return number
