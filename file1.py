import requests
import datetime
import logging

with open('credentials.txt', 'r') as file:
    lines = file.readlines()
    API_URL = lines[0].strip()
    Username = lines[1].strip()
    Password = lines[2].strip()

BASE_NAME = input("Enter username: ")
START_NUMBER = int(input("Enter start number: "))
NUM_USERS = int(input("Enter number of users: "))
DATA_LIMIT_GB = int(input("Enter data limit in GB: "))
Days = int(input("Enter Days: "))

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

logging.basicConfig(filename='script_log.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

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

def generate_users(base_name, start_number, num_users, data_limit):
    data_limit_bytes = data_limit * 1024**3

    access_token = get_access_token(Username, Password)

    if access_token:
        proxies = {}
        vmess_input = input(f"Do users have Vmess ۰? (y/n): ")
        if vmess_input.lower() == 'y':
            proxies['vmess'] = {}

        vless_input = input(f"Do users have Vless ? (y/n): ")
        if vless_input.lower() == 'y':
            proxies['vless'] = {'flow': 'xtls-rprx-vision'}

        trojan_input = input(f"Do users have Trojan ? (y/n): ")
        if trojan_input.lower() == 'y':
            proxies['trojan'] = {}

        for i in range(start_number, start_number + num_users):
            username = generate_username(base_name, i)
            inbounds = {}
            expire = int(datetime.datetime.now().timestamp()) + (24 * 3600 * (Days + 1))

            user = create_new_user(access_token, username, proxies, inbounds, expire, data_limit_bytes, 'no_reset')
            if user:
                print(f"User {username} created successfully.")
    else:
        print("Failed to obtain the access token.")

generate_users(BASE_NAME, START_NUMBER, NUM_USERS, DATA_LIMIT_GB)
