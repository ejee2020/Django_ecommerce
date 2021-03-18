import requests
from django.conf import settings


def get_token():
    access_data = {'imp_key': settings.IAMPORT_KEY,
                   'imp_secret': settings.IAMPORT_SECRET}
    url = "https://api.iamport.kr/users/getToken"
    req = requests.post(url, data=access_data)
    access_res = req.json()

    if access_res['code'] is 0:
        return access_res['response']['access_token']
    else:
        return None


def payments_prepare(order_id, amount, *args, **kwargs):
    access_token = get_token()
    if access_token:
        access_data = {
            'merchant_uid': order_id,
            'amount': amount,
        }
        url = "https://api.iamport.kr/payments/prepare"
        headers = {
            'Authorization': access_token
        }
        req = requests.post(url, data=access_data, headers=headers)
        res = req.json()
        if res['code'] != 0:
            raise ValueError("API Error")
    else:
        raise ValueError("No Token")


def find_transaction(order_id, *args, **kwargs):
    access_token = get_token()
    if access_token:
        url = "https://api.iamport.kr/payments/prepare/find/" + order_id
        headers = {
            'Authorization': access_token
        }
        req = requests.post(url, headers=headers)
        res = req.json()
        response = res['response']
        if res['code'] == 0:
            context = {
                'imp_id': response['imp_uid'],
                'merchant_order_id': response['merchant_uid'],
                'amount': response['amount'],
                'status': response['status'],
                'type': response['pay_method'],
                'receipt_url': response['receipt_url'],
            }
            return context
        else:
            return None
    else:
        raise ValueError("Token Error")
