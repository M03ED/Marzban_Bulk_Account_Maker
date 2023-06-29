import requests
import datetime
import logging


API_URL = 'https://Domain.com:port/api'  # Replace with the actual API URL
BASE_NAME = 'user'  # Base name for the new users
START_NUMBER = 1  # Start number for the new users
NUM_USERS = 5  # Number of new users to create
DATA_LIMIT_GB = 15  # Data limit per GB
Days = 12 # Expire Date per Day
Username = "user"
Password = "pass"

def generate_username(base_name, number):
    return f"{base_name}{number}"

def get_access_token(username, password):
    url = f"{API_URL}/admin/token"
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

def create_new_user(access_token, username, proxies, inbounds, expire, data_limit, data_limit_reset_strategy):
    url = f"{API_URL}/user"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {access_token}"
    }
    payload = {
        'username': username,
        'proxies': proxies,
        'inbounds': inbounds,
        'expire': expire,
        'data_limit': data_limit,
        'data_limit_reset_strategy': data_limit_reset_strategy
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while creating user {username}: {e}")
        return None

logging.basicConfig(filename='script_log.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_users(base_name, start_number, num_users, data_limit):
    data_limit_bytes = data_limit * 1024**3  # Convert data limit from GB to bytes

    access_token = get_access_token(Username, Password)  # Replace with your actual username and password

    if access_token:
        for i in range(start_number, start_number + num_users):
            username = generate_username(base_name, i)
            proxies = {
                'vmess': {},
                'vless': {
                    'flow': 'xtls-rprx-vision'
                    }
            }
            inbounds = {
                'vmess': ['VMESS_TCP_INBOUND'],
                'vless': ['VLESS_TCP_Reality_INBOUND', 'VLESS_TCP_INBOUND']
            }
            expire = int(datetime.datetime.now().timestamp()) + (24 * 3600 * (Days+1))  # Expiring in 7 days

            user = create_new_user(access_token, username, proxies, inbounds, expire, data_limit_bytes, 'no_reset')
            if user:
                print(f"User {username} created successfully.")
    else:
        print("Failed to obtain the access token.")

# Generate new users
generate_users(BASE_NAME, START_NUMBER, NUM_USERS, DATA_LIMIT_GB)
