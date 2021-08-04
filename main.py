import json

import requests
import datetime

URLPATH = ' https://cloud.ucams.ru'
PATHCONTEXT = 'https://cloud.ucams.ru/api/v0/context'
PATHAUTH = 'https://cloud.ucams.ru/api/v0/auth'
PARHCAMERA_ALL = 'https://cloud.ucams.ru/api/v0/cameras/my/'
PARHCAMERA = 'https://cloud.ucams.ru/api/v0/cameras/this'

auth_dict = {"username": "telnet",
             "password": "LnbqJC8gWDRL"
             }


def get_token():
    auth_dict = {"username": "telnet",
                 "password": "LnbqJC8gWDRL"
                 }
    res = requests.post(PATHAUTH, data=auth_dict)
    return res.json()['token']


def get_header(token):
    header = {
        'Accepts': 'text/html,'
                   'application/xhtml+xml,'
                   'application/xml;q=0.9,'
                   'image/avif,image/webp,'
                   'image/apng,*/*;'
                   'q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Authorization': f'Bearer {token}'
    }
    return header


def get_server(header, number):
    body = {
        "fields": ['address',
                   'title',
                   'is_embed',
                   'server',
                   'streams_count',
                   'permission',
                   'token_l',
                   # 'token_r',
                   ],
        "token_l_ttl": 3600 ,
        "numbers": [number]
    }
    res = requests.post(PARHCAMERA, allow_redirects=True, headers=header, data=json.dumps(body))
    real_camera = res.json()
    print(real_camera)
    real_result = real_camera['results'][0]
    return real_result['token_l'] ,real_result['server']


def main():
    """
    1 получаем токен для ручке auth
    2 доступ к камере
    """
    print('begin')

    my_token = get_token()

    api_header = get_header(my_token)
    print(api_header)

    res = requests.post(PATHCONTEXT, headers=api_header)
    print(res.status_code)

    token_1,real_server = get_server(api_header, '1627277293VCG202')
    print(token_1)
    print(real_server['domain'])
    print(real_server['screenshot_domain'])
    header_l ={'Accepts': 'text/html,'
                   'application/xhtml+xml,'
                   'application/xml;q=0.9,'
                   'image/avif,image/webp,'
                   'image/apng,*/*;'
                   'q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                        }
    url = f'https://{real_server["domain"]}/1627277293VCG202/tracks-v1/mono.m3u8'
    payload = {'token': token_1}
    print(url)

    res = requests.get(url,params=payload)
    print('token from camera', res.status_code)
    print(res.url)
    # res_1 = requests.get(f'https://{real_server["domain"]}/1627277293VCG202/tracks-v1/mono.m3u8?token={token_1}')
    # res_s = requests.post(f'https://{real_server["screenshot_domain"]}/screenshots/', headers=real_header)


if __name__ == '__main__':
    main()
