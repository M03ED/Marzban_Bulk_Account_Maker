# Marzban_Bulk_Account_Maker

Change Variables Depend On Your Usage

```python
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
```
Change proxies and inbounds depend on your marzban setting , you can add trojan if you want
```python
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
```
After you start script it will start making users with usernames like these
- user1 , user2 , user3 , user4 , user5
- `START_NUMBER` is which number you wanna start and `NUM_USERS` its number of users you wanna create
- if you need to make on hold users replace status with 'on_hold'
- if you need to make users with unlimited expire replace days with 0
- if you have questions: https://t.me/gozargah_marzban
# فارسی
متغیرها را بر اساس استفاده خود تغییر دهید.
```python
USERNAME = "user" # نام کاربری ادمین پنل
PASSWORD = "pass" # رمز ورود ادمین پنل
API_URL = 'https://sub.domain.com:port'  # با آدرس پنل طبق الگو جایگزین کنید
BASE_NAME = 'user'  # پسوند برای نام کاربران
START_NUMBER = 22  # شماره گذاری برای استارت
NUM_USERS = 10  # تعداد کاربران مورد نیاز 
DATA_LIMIT_GB = 15  # محدودیت حجم به واحد گیگابایت
DAYS = 12  # محدودیت حجم به واحد روز (اگر نامحدود میخوایید 0 بزارید)
FLOW = 'xtls-rprx-vision'
STATUS = 'active'  # اگر میخواهید با اولین اتصال آمار کاربر محاسبه شود 'on_hold' بزنید
DATA_LIMIT_RESET_STRATEGY = 'no_reset'
```
پروکسی‌ها و ورودی‌ها را بر اساس تنظیمات مرزبان خود تغییر دهید. در صورت تمایل می‌توانید trojan را اضافه کنید. ضمنا اگر میخواهید همه‌ی اینباندهارو شامل شود، میتوانید اینباندهارو خالی بگذارید. مثل `inbounds = {}`
```python
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
```
- پس از شروع اسکریپت، شروع به ایجاد کاربران با نام‌هایی مانند این خواهد شد : user1، user2، user3، user4، user5
- شماره_شروع که عددی است که می‌خواهید شروع کنید و تعداد_کاربران تعداد کاربرانی است که می‌خواهید ایجاد کنید.
- اگر نیاز دارید کاربران را در حالت "متوقف" ایجاد کنید، وضعیت را با 'متوقف' جایگزین کنید.
- اگر نیاز دارید کاربرانی با تاریخ انقضای نامحدود ایجاد کنید، روزها را با 0 جایگزین کنید.
- اگر سوالی دارید : https://t.me/gozargah_marzban

