# Made with ❤ by @adearman
# Update at github.com/adearman/hamsterkombat
# Free for use

import requests
import json
import time
from datetime import datetime
from itertools import cycle
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def load_tokens(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def get_headers(token):
    return {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'Origin': 'https://hamsterkombat.io',
        'Referer': 'https://hamsterkombat.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Content-Type': 'application/json'
   
    }

def get_token(init_data_raw):
    url = 'https://api.hamsterkombat.io/auth/auth-by-telegram-webapp'
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://hamsterkombat.io',
        'Referer': 'https://hamsterkombat.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36',
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    data = json.dumps({"initDataRaw": init_data_raw})
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()['authToken']
    else:
        error_data = response.json()
        if "invalid" in error_data.get("error_code", "").lower():
            print(Fore.RED + Style.BRIGHT + "\rFailed Get Token. Invalid init data", flush=True)
        else:
            print(Fore.RED + Style.BRIGHT + f"\rFailed Get Token. {error_data}", flush=True)
        return None

def authenticate(token):
    url = 'https://api.hamsterkombat.io/auth/me-telegram'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

def sync_clicker(token):
    url = 'https://api.hamsterkombat.io/clicker/sync'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

def claim_daily(token):
    url = 'https://api.hamsterkombat.io/clicker/check-task'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"taskId": "streak_days"})
    response = requests.post(url, headers=headers, data=data)
    return response
def upgrade(token, upgrade_type):
    url = 'https://api.hamsterkombat.io/clicker/buy-boost'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"boostId": upgrade_type, "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    return response


def tap(token, max_taps, available_taps):
    url = 'https://api.hamsterkombat.io/clicker/tap'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"count": max_taps, "availableTaps": available_taps, "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    return response

def list_tasks(token):
    url = 'https://api.hamsterkombat.io/clicker/list-tasks'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

def exchange(token):
    url = 'https://api.hamsterkombat.io/clicker/select-exchange'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"exchangeId": 'okx'})
    response = requests.post(url, headers=headers, data=data)
    return response

def check_task(token, task_id):
    url = 'https://api.hamsterkombat.io/clicker/check-task'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"taskId": task_id})
    response = requests.post(url, headers=headers, data=data)
    return response

def use_booster(token):
    url = 'https://api.hamsterkombat.io/clicker/check-task'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"boostId": "BoostFullAvailableTaps", "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    return response



def get_available_upgrades(token):
    url = 'https://api.hamsterkombat.io/clicker/upgrades-for-buy'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade Minning ] : Berhasil mendapatkan list upgrade.", flush=True)
        return response.json()['upgradesForBuy']
    else:

        print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade Minning ] : Gagal mendapatkan daftar upgrade: {response.status_code}", flush=True)
        return []


def buy_upgrade(token, upgrade_id, upgrade_name):
    url = 'https://api.hamsterkombat.io/clicker/buy-upgrade'
    headers = get_headers(token)
    data = json.dumps({"upgradeId": upgrade_id, "timestamp": int(time.time())})
    # print(data)
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade Minning ] : Upgrade {upgrade_name} berhasil dibeli.", flush=True)
    else:
        error_response = response.json()
        if error_response.get('error_code') == 'INSUFFICIENT_FUNDS':
            print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade Minning ] : Coin tidak cukup wkwkw :V", flush=True)
            return 'insufficient_funds'
        else:
            print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade Minning ] : Failed upgrade {upgrade_name}: {response.json()}", flush=True)




def auto_upgrade_passive_earn(token):
    upgrades = get_available_upgrades(token)
    if not upgrades:  # Cek jika daftar upgrade kosong
        print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade Minning ] : Tidak ada upgrade yang tersedia atau gagal mendapatkan daftar upgrade.", flush=True)
        return  # Keluar dari fungsi jika tidak ada upgrade yang bisa diproses
    for upgrade in upgrades:
        if upgrade['isAvailable'] and not upgrade['isExpired']:
            print(Fore.YELLOW + Style.BRIGHT + f"[ Upgrade Minning ] : {upgrade['name']} | Harga: {upgrade['price']} | Profit: {upgrade['profitPerHour']} / Jam ")
            print(Fore.CYAN + Style.BRIGHT + f"\r[ Upgrade Minning ] : Upgrading {upgrade['name']}", end="", flush=True)
            result = buy_upgrade(token, upgrade['id'], upgrade['name'])
            if result == 'insufficient_funds':
                print(Fore.RED + Style.BRIGHT + f"\rBeralih ke akun selanjutnya\n\n", flush=True)
                return 


 






# MAIN CODE
cek_task_dict = {}
def main():
    global cek_task_dict
    print(Fore.GREEN + Style.BRIGHT + "Starting Hamster Kombat....\n\n")
    init_data = load_tokens('initdata.txt')
    token_cycle = cycle(init_data)

    token_dict = {}  # Dictionary to store successful tokens
    while True:
        init_data_raw = next(token_cycle)
        token = token_dict.get(init_data_raw)
        
        if token:
            print(Fore.GREEN + Style.BRIGHT + f"\rMenggunakan token yang sudah ada...", end="", flush=True)
        else:
            print(Fore.GREEN + Style.BRIGHT + f"\rMendapatkan token...", end="", flush=True)

            token = get_token(init_data_raw)
            if token:
                token_dict[init_data_raw] = token
                print(Fore.GREEN + Style.BRIGHT + f"\rBerhasil mendapatkan token    ", flush=True)
            else:
                print(Fore.RED + Style.BRIGHT + f"\rBeralih ke akun selanjutnya\n\n", flush=True)
                continue  # Lanjutkan ke iterasi berikutnya jika gagal mendapatkan token


        response = authenticate(token)
   
        ## TOKEN AMAN
        if response.status_code == 200:

            user_data = response.json()
            username = user_data.get('telegramUser', {}).get('username', 'KONTOL USERNAME AJA GA DISET')
            
            print(Fore.GREEN + Style.BRIGHT + f"\r\n======[{Fore.WHITE + Style.BRIGHT} {username} {Fore.GREEN + Style.BRIGHT}]======")

            # Sync Clicker
            print(Fore.GREEN + f"\rGetting info user...", end="", flush=True)
            response = sync_clicker(token)
            if response.status_code == 200:
                clicker_data = response.json()['clickerUser']
                print(Fore.YELLOW + Style.BRIGHT + f"\r[ Level ] : {clicker_data['level']}          ", flush=True)
                print(Fore.YELLOW + Style.BRIGHT + f"[ Total Earned ] : {int(clicker_data['totalCoins'])}")
                print(Fore.YELLOW + Style.BRIGHT + f"[ Coin ] : {int(clicker_data['balanceCoins'])}")
                print(Fore.YELLOW + Style.BRIGHT + f"[ Energy ] : {clicker_data['availableTaps']}")
                boosts = clicker_data['boosts']
                boost_max_taps_level = boosts.get('BoostMaxTaps', {}).get('level', 0)
                boost_earn_per_tap_level = boosts.get('BoostEarnPerTap', {}).get('level', 0)
                
                print(Fore.CYAN + Style.BRIGHT + f"[ Level Energy ] : {boost_max_taps_level}")
                print(Fore.CYAN + Style.BRIGHT + f"[ Level Tap ] : {boost_earn_per_tap_level}")
                print(Fore.CYAN + Style.BRIGHT + f"[ Exchange ] : {clicker_data['exchangeId']}")
                # print(clicker_data['exchangeId'])
                if clicker_data['exchangeId'] == None:
                    print(Fore.GREEN + '\rSeting exchange to OKX..',end="", flush=True)
                    exchange_set = exchange(token)

                    if exchange_set.status_code == 200:
                        print(Fore.GREEN + Style.BRIGHT +'\rSukses set exchange ke OKX', flush=True)
                    else:
                        print(Fore.RED + Style.BRIGHT +'\rGagal set exchange' + exchange_set.response.json(), flush=True)
                print(Fore.CYAN + Style.BRIGHT + f"[ Passive Earn ] : {clicker_data['earnPassivePerHour']}\n")
                print(Fore.GREEN + f"\r[ Tap Status ] : Tapping ...", end="", flush=True)



                response = tap(token, clicker_data['maxTaps'], clicker_data['availableTaps'])
                if response.status_code == 200:
                    print(Fore.GREEN + Style.BRIGHT + "\r[ Tap Status ] : Tapped            ", flush=True)
                else:
                    print(Fore.RED + Style.BRIGHT + "\r[ Tap Status ] : Gagal Tap           ", flush=True)
                    break 
                print(Fore.GREEN + f"\r[ Checkin Daily ] : Checking...", end="", flush=True)

                time.sleep(1)
                # Check Task
                response = claim_daily(token)
                if response.status_code == 200:
                    daily_response = response.json()['task']
                    if daily_response['isCompleted']:
                        print(Fore.GREEN + Style.BRIGHT + f"\r[ Checkin Daily ] Days {daily_response['days']} | Completed", flush=True)
                    else:
                        print(Fore.RED + Style.BRIGHT + f"\r[ Checkin Daily ] Days {daily_response['days']} | Belum saat nya claim daily", flush=True)
                else:
                    print(Fore.RED + Style.BRIGHT + f"\r[ Checkin Daily ] Gagal cek daily {response.status_code}", flush=True)
                
                # Upgrade 
                if auto_upgrade_energy == 'y':
                    print(Fore.GREEN + f"\r[ Upgrade ] : Upgrading Energy....", end="", flush=True)
                    upgrade_response = upgrade(token, "BoostMaxTaps")
                    if upgrade_response.status_code == 200:
                        level_boostmaxtaps = upgrade_response.json()['clickerUser']['boosts']['BoostMaxTaps']['level']
                        print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade ] : Energy Upgrade to level {level_boostmaxtaps}", flush=True)
                    else:
                        print(Fore.RED + Style.BRIGHT + "\r[ Upgrade ] : Failed to upgrade energy", flush=True)
                if auto_upgrade_multitap == 'y':
                    print(Fore.GREEN + f"\r[ Upgrade ] : Upgrading MultiTap....", end="", flush=True)
                    upgrade_response = upgrade(token, "BoostEarnPerTap")
                    if upgrade_response.status_code == 200:
                        level_boostearnpertap = upgrade_response.json()['clickerUser']['boosts']['BoostEarnPerTap']['level']
                        print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade ] : MultiTap Upgrade to level {level_boostearnpertap}", flush=True)
                    else:
                        print(Fore.RED + Style.BRIGHT + "\r[ Upgrade ] : Failed to upgrade multitap", flush=True)
            
                # List Tasks
                print(Fore.GREEN + f"\r[ List Task ] : Checking...", end="", flush=True)
                if token not in cek_task_dict:  # Pastikan token ada dalam dictionary
                    cek_task_dict[token] = False  # Inisialisasi jika belum ada
                if not cek_task_dict[token]:  # Cek status cek_task untuk token ini
                    response = list_tasks(token)
                    cek_task_dict[token] = True  # Set status cek_task menjadi True setelah dicek
                    if response.status_code == 200:
                        tasks = response.json()['tasks']
                        all_completed = all(task['isCompleted'] or task['id'] == 'invite_friends' for task in tasks)
                        if all_completed:
                            print(Fore.GREEN + Style.BRIGHT + "\r[ List Task ] : Semua task sudah diclaim\n", flush=True)
                        else:
                            for task in tasks:
                                if not task['isCompleted']:
                                    print(Fore.YELLOW + Style.BRIGHT + f"\r[ List Task ] : Claiming {task['id']}...", end="", flush=True)
                                    response = check_task(token, task['id'])
                                    if response.status_code == 200 and response.json()['task']['isCompleted']:
                                        print(Fore.GREEN + Style.BRIGHT + f"\r[ List Task ] : Claimed {task['id']}\n", flush=True)
                                    else:
                                        print(Fore.RED + Style.BRIGHT + f"\r[ List Task ] : Gagal Claim {task['id']}\n", flush=True)
                    else:
                        print(Fore.RED + Style.BRIGHT + f"\r[ List Task ] : Gagal mendapatkan list task {response.status_code}\n", flush=True)
                # else:
                    # print(Fore.GREEN + Style.BRIGHT + "\r[ List Task ] : Sudah di cek dan claimed", flush=True)
                    
                # cek upgrade
                
                if auto_upgrade_passive == 'y':
                    print(Fore.GREEN + f"\r[ Upgrade Minning ] : Checking...", end="", flush=True)
                    auto_upgrade_passive_earn(token)
            else:


                print(Fore.RED + Style.BRIGHT + f"\r Gagal mendapatkan info user {response.status_code}", flush=True)



        ## TOKEN MATI        
        elif response.status_code == 401:
            error_data = response.json()
            if error_data.get("error_code") == "NotFound_Session":
                print(Fore.RED + Style.BRIGHT + f"=== [ Token Invalid {token} ] ===")
                token_dict.pop(init_data_raw, None)  # Remove invalid token
                token = None  # Set token ke None untuk mendapatkan token baru di iterasi berikutnya
            else:
                print(Fore.RED + Style.BRIGHT + "Authentication failed with unknown error")
        else:
            print(Fore.RED + Style.BRIGHT + f"Error with status code: {response.status_code}")
            token = None  # Set token ke None jika terjadi error lain
            
        time.sleep(1)

while True:
    auto_upgrade_energy = input("Upgrade Energy (default n) ? (y/n): ").strip().lower()
    if auto_upgrade_energy in ['y', 'n', '']:
        auto_upgrade_energy = auto_upgrade_energy or 'n'
        break
    else:
        print("Masukkan 'y' atau 'n'.")

while True:
    auto_upgrade_multitap = input("Upgrade Multitap (default n) ? (y/n): ").strip().lower()
    if auto_upgrade_multitap in ['y', 'n', '']:
        auto_upgrade_multitap = auto_upgrade_multitap or 'n'
        break
    else:
        print("Masukkan 'y' atau 'n'.")
while True:
    auto_upgrade_passive = input("Auto Upgrade Mining (Passive Earn)? (default n) (y/n): ").strip().lower()
    if auto_upgrade_passive in ['y', 'n', '']:
        auto_upgrade_passive = auto_upgrade_passive or 'n'
        break
    else:
        print("Masukkan 'y' atau 'n'.")

if __name__ == "__main__":
    main()
