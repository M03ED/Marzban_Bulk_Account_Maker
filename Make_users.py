import requests
import datetime
import logging

# Constants
USERNAME = "user"
PASSWORD = "pass"
API_URL = 'https://sub.domain.com:port'  # Replace with the panel URL
BASE_NAME = 'user'  # Base name for the new users
START_NUMBER = 22  # Start number for the new users
NUM_USERS = 10  # Number of new users to create
DATA_LIMIT_GB = 15  # Data limit per GB
DAYS = 12  # Expire Date per Day (enter 0 for unlimited)
FLOW = 'xtls-rprx-vision'
STATUS = 'active'  # replace with 'on_hold' for count after first connection
DATA_LIMIT_RESET_STRATEGY = 'no_reset'
proxies = {
    'vmess': {},
    'vless': {
        'flow': flow
        }
}
inbounds = {
    'vmess': ['VMESS_TCP_INBOUND'],
    'vless': ['VLESS_TCP_Reality_INBOUND', 'VLESS_TCP_INBOUND']
} # If you want all inbounds, leave it blank

# Now just run code...
logging.basicConfig(level=logging.INFO, format='%(asctime)s\t|\t%(levelname)-8s\t-> %(message)s' , datefmt='%H:%M:%S')

# Function to obtain access headers
def get_access_headers(username, password):
    url = f"{Api_url}/api/admin/token"
    data = {
        'username': username,
        'password': password
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        access_token = response.json()['access_token']
        access_headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {access_token}"
        }
        logging.info('✅\tAuthorization header was created successfully')
        return access_headers
    except requests.exceptions.RequestException as e:
        logging.error(f'❌\tError occurred while obtaining access headers: {e}')
        return None

# Function to create payload for new users
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
        payload = False
    return payload

# Function to create new user
def create_new_user(access_headers, username, payload):
    url = f"{Api_url}/api/user"
    try:
        response = requests.post(url, json=payload, headers=access_headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f'❌\tError occurred while creating user {username}: {e}')
        return False

# Function to generate users
def generate_users(base_name, start_number, Num_users, data_limit):
    data_limit_bytes = data_limit * 1024 ** 3
    access_headers = get_access_headers(Username, Password)
    if access_headers:
        for i in range(start_number, start_number + Num_users):
            username = f'{base_name}{i}'
            expire = None if Days == 0 else int(datetime.datetime.now().timestamp()) + (24 * 3600 * (Days + 1)) if status == 'active' else (24 * 3600 * Days)
            payload = create_user_payload(username, proxies, inbounds, expire, data_limit_bytes)
            if payload :
                user = create_new_user(access_headers, username, payload)
                if user:
                    logging.info(f"✅\tUser '{username}' is created , user sub_link :\n\t{user.get('subscription_url', '')}")
            else :
                logging.error(f'❌ Wrong status.')

# Generate new users
generate_users(Base_name, Start_number, Num_users, Data_limit_GB)
