import subprocess


options = {
    '1': "ساخت اشتراک معمولی",
    '2': "محاسبه از اولین اتصال",
    '3': "دریافت لینک  گروهی"
}

max_length = max(len(value) for value in options.values())  

for key, value in options.items():
    print(f"({key}) {value.rjust(max_length)}")

choice = input(" Choose an option and press Enter ")

if choice in options:
    subprocess.run(['python', f'file{choice}.py'])
else:
    print("انتخاب نامعتبر. لطفا عددی از ۱ تا ۳ وارد کنید.")