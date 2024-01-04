import requests
import datetime
import logging


Username = "user"
Password = "pass"
Api_url = 'https://domain.com:1234/api'  # Replace with the actual API URL
Base_name = 'user'  # Base name for the new users
Start_number = 22  # Start number for the new users
Num_users = 10  # Number of new users to create
Data_limit_GB = 15  # Data limit per GB
Days = 12 # Expire Date per Day (enter 0 for unlimite)
flow = 'xtls-rprx-vision'
status = 'active' # replace with on_hold for count after first connection
data_limit_reset_strategy = 'no_reset'

proxies = {
    'vmess': {},
    'vless': {
        'flow': flow
        }
}
inbounds = {
    'vmess': ['VMESS_TCP_INBOUND'],
    'vless': ['VLESS_TCP_Reality_INBOUND', 'VLESS_TCP_INBOUND']
}

def generate_username(base_name, number):
    return f"{base_name}{number}"

def get_access_token(username, password):
    url = f"{Api_url}/admin/token"
    data = {
        'username': username,
        'password': password
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        access_token = response.json()['access_token']
        return access_token
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while obtaining access token: {e}')
        return None

def create_user_payload(username, proxies, inbounds, expire, data_limit):
    if status == 'active':
        payload = {
            'username': username,
            'proxies': proxies,
            'inbounds': inbounds,
            'expire': expire,
            'status' : status,
            'data_limit': data_limit,
            'data_limit_reset_strategy': data_limit_reset_strategy
        }
    elif status == 'on_hold':
        payload = {
            'username': username,
            'proxies': proxies,
            'inbounds': inbounds,
            'on_hold_expire_duration': expire,
            'status' : status,
            'data_limit': data_limit,
            'data_limit_reset_strategy': data_limit_reset_strategy
        }
    else:
        print("wrong status.")

    return payload

def create_new_user(access_token, username, payload):
    url = f"{Api_url}/user"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {access_token}"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while creating user {username}: {e}")
        return None

logging.basicConfig(filename='script_log.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def generate_users(base_name, start_number, Num_users, data_limit):
    data_limit_bytes = data_limit * 1024 ** 3

    access_token = get_access_token(Username, Password)

    if access_token:

        for i in range(start_number, start_number + Num_users):
            username = generate_username(base_name, i)
            
            if status == 'active':
                if Days == 0:
                    expire = None
                else:
                    expire = int(datetime.datetime.now().timestamp()) + \
                        (24 * 3600 * (Days + 1))
            else:
                expire = (24 * 3600 * Days)
            
            payload = create_user_payload(username, proxies, inbounds, expire, data_limit_bytes)
            if payload :
                user = create_new_user(access_token, username, payload)
            if user:
                subscription_url = user.get('subscription_url', '')
                if subscription_url:
                    print(f"{username} sub link: {subscription_url}")
    else:
        print("Failed to obtain the access token.")

# Generate new users
generate_users(Base_name, Start_number, Num_users, Data_limit_GB)
