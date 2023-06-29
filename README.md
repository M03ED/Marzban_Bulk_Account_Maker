# Marzban_Bulk_Account_Maker

Change Variables Depend On Your Usage

```python
API_URL = 'https://Domain.com:port/api'  # Replace with the actual API URL
BASE_NAME = 'user'  # Base name for the new users
START_NUMBER = 1  # Start number for the new users
NUM_USERS = 5  # Number of new users to create
DATA_LIMIT_GB = 15  # Data limit per GB
Days = 12 # Expire Date per Day
Username = "user"
Password = "pass"
```
Change proxies and inbounds depend on your marzban setting , you can add trojan if you want
```python
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
```
After you start script it will start making users with usernames like these
- user1 , user2 , user3 , user4 , user5
- `START_NUMBER` is which number you wanna start and `NUM_USERS` its number of users you wanna create
