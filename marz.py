import requests
import datetime
import logging

with open('credentials.txt', 'r') as file:
    lines = file.readlines()
    API_URL = lines[0].strip()
    Username = lines[1].strip()
    Password = lines[2].strip()

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
        print(f'Error occurred while obtaining access token: {e}')
        return None

def fetch_user_data(username, access_token):
    url = f"{API_URL}/user/{username}"

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {access_token}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching user data: {e}")
        return None

def create_new_user(access_token, username, proxies, inbounds, expire, data_limit, data_limit_reset_strategy, status, note, on_hold_expire_duration):
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
        'data_limit_reset_strategy': data_limit_reset_strategy,
        'status': status,
        'note': note,
        'on_hold_expire_duration': on_hold_expire_duration
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while creating user {username}: {e}")
        return None

if __name__ == "__main__":
    access_token = get_access_token(Username, Password)

    if access_token:
        choice = input("Would you like to create users (c) or fetch sub link (f)? ")

        if choice.lower() == 'c':
            BASE_NAME = input("Enter username: ")
            START_NUMBER = int(input("Enter start number: "))
            NUM_USERS = int(input("Enter number of users: "))
            DATA_LIMIT_GB = int(input("Enter data limit in GB: "))
            Days = int(input("Enter Days: "))
            note = input("Enter note for the users: ")
            data_limit_bytes = DATA_LIMIT_GB * 1024**3

            proxies = {}
            vmess_input = input(f"Do users have Vmess ? (y/n): ")
            if vmess_input.lower() == 'y':
                proxies['vmess'] = {}

            vless_input = input(f"Do users have Vless ? (y/n): ")
            if vless_input.lower() == 'y':
                proxies['vless'] = {'flow': 'xtls-rprx-vision'}

            trojan_input = input(f"Do users have Trojan ? (y/n): ")
            if trojan_input.lower() == 'y':
                proxies['trojan'] = {}

            user_type = input("Enter user type (normal/on hold): ").lower()

            for i in range(START_NUMBER, START_NUMBER + NUM_USERS):
                username = f"{BASE_NAME}{i}"
                inbounds = {}

                if user_type == 'normal':
                    status = None
                    
                    on_hold_expire_duration = None
                    expire = int(datetime.datetime.now().timestamp()) + (24 * 3600 * (Days + 1))
                elif user_type == 'on hold':
                    status = 'on_hold'
                    
                    on_hold_expire_duration = int(datetime.datetime.now().timestamp()) + (24 * 3600 * (Days + 1))
                    expire = None
                else:
                    print("Invalid user type entered.")
                    break

                user = create_new_user(access_token, username, proxies, inbounds, expire, data_limit_bytes, 'no_reset', status, note, on_hold_expire_duration)
                if user:
                    print(f"User {username} created successfully.")
        elif choice.lower() == 'f':
            desired_username = input("Please enter the desired username: ")
            x = int(input("Enter the starting value (x): "))
            y = int(input("Enter the ending value (y): "))
            
            with open('result.txt', 'w') as file:
                for i in range(x, y + 1):
                    user_data = fetch_user_data(f"{desired_username}{i}", access_token)
                    
                    if user_data and 'subscription_url' in user_data:
                        file.write(f"{desired_username}{i}: {user_data['subscription_url']}\n")
                    else:
                        file.write(f"No 'subscription_url' found for {desired_username}{i}.\n")
                        
            print("Results have been saved to 'result.txt'.")
        else:
            print("Invalid choice. Please enter 'c' for creating users or 'f' for fetching user data.")
    else:
        print("Failed to obtain the access token.")
