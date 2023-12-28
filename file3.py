import requests

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

if __name__ == "__main__":
    access_token = get_access_token(Username, Password)

    if access_token:
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
        print("Failed to obtain the access token.")