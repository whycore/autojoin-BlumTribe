import requests
import time
from colorama import init, Fore, Style

init(autoreset=True)

def print_watermark():
    watermark = """
    ██╗    ██╗ █████╗  ██████╗ ██╗   ██╗██╗   ██╗    ███╗   ███╗ ██████╗ ██████╗ ███████╗
    ██║    ██║██╔══██╗██╔════╝ ╚██╗ ██╔╝██║   ██║    ████╗ ████║██╔═══██╗██╔══██╗██╔════╝
    ██║ █╗ ██║███████║██║  ███╗ ╚████╔╝ ██║   ██║    ██╔████╔██║██║   ██║██║  ██║█████╗  
    ██║███╗██║██╔══██║██║   ██║  ╚██╔╝  ██║   ██║    ██║╚██╔╝██║██║   ██║██║  ██║██╔══╝  
    ╚███╔███╔╝██║  ██║╚██████╔╝   ██║   ╚██████╔╝    ██║ ╚═╝ ██║╚██████╔╝██████╔╝███████╗
     ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝     ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝
    """
    print(f"{Fore.RED}{watermark}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Blum Tribe Manager - WAGYU MODE{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Created by: Whycore{Style.RESET_ALL}")
    print("\n")

def debug_print(message):
    print(f"{Fore.CYAN+Style.BRIGHT}[DEBUG] {message}")

def get_new_token(query_id):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://telegram.blum.codes",
        "referer": "https://telegram.blum.codes/"
    }
    data = {"query": query_id}
    url = "https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"
    for attempt in range(3):
        print(f"\r{Fore.YELLOW+Style.BRIGHT}Getting token...", end="", flush=True)
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            debug_print(f"Token obtained successfully")
            return response.json()['token']['refresh']
        else:
            print(f"\r{Fore.RED+Style.BRIGHT}Failed to get token, attempt {attempt + 1}", flush=True)
    
    print(f"\r{Fore.RED+Style.BRIGHT}Failed to get token after 3 attempts.", flush=True)
    return None

def check_tribe(token):
    url = 'https://game-domain.blum.codes/api/v1/tribe/my'
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }
    response = requests.get(url, headers=headers)
    debug_print(f"Check tribe status code: {response.status_code}")
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return {"message": "NOT_FOUND"}
    else:
        print(f"{Fore.RED+Style.BRIGHT}Failed to get tribe information")
        return None

def join_tribe(token, tribe_id):
    url = f'https://game-domain.blum.codes/api/v1/tribe/{tribe_id}/join'
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'content-length': '0'
    }
    response = requests.post(url, headers=headers)
    debug_print(f"Join tribe status code: {response.status_code}")
    if response.status_code == 200:
        print(f"{Fore.GREEN+Style.BRIGHT}[ Tribe ] Joined TRIBE")
        return True
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Tribe ] Failed to join TRIBE")
        return False

def leave_tribe(token):
    url = 'https://game-domain.blum.codes/api/v1/tribe/leave'
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'content-type': 'application/json'
    }
    data = {}  # data kosong sebagai body request
    
    time.sleep(5)
    
    debug_print(f"Attempting to leave tribe with URL: {url}")
    debug_print(f"Headers: {headers}")
    debug_print(f"Data: {data}")
    
    response = requests.post(url, headers=headers, json=data)
    debug_print(f"Leave tribe status code: {response.status_code}")
    debug_print(f"Leave tribe response: {response.text}")
    
    if response.status_code == 200:
        print(f"{Fore.GREEN+Style.BRIGHT}[ Tribe ] Left TRIBE")
        return True
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Tribe ] Failed to leave TRIBE")
        print(f"{Fore.RED+Style.BRIGHT}Response: {response.text}")
        return False

def process_account(token, tribe_id, index):
    print(f"{Fore.BLUE+Style.BRIGHT}\n====[{Fore.WHITE+Style.BRIGHT}Account {index}{Fore.BLUE+Style.BRIGHT}]====")
    
    print(f"{Fore.GREEN+Style.BRIGHT}[ Tribe ]: Checking tribe...", end="", flush=True)
    tribe_info = check_tribe(token)
    time.sleep(1)
    
    if tribe_info and tribe_info.get("id"):
        print(f"\r{Fore.YELLOW+Style.BRIGHT}[ Tribe ]: Already in tribe: {tribe_info['title']}", flush=True)
        print(f"{Fore.YELLOW+Style.BRIGHT}[ Tribe ]: Leaving tribe...", flush=True)
        
        for attempt in range(3):
            if leave_tribe(token):
                break
            else:
                print(f"{Fore.YELLOW+Style.BRIGHT}[ Tribe ]: Retry leaving tribe (attempt {attempt+1}/3)...")
                time.sleep(5)
    
    print(f"{Fore.YELLOW+Style.BRIGHT}[ Tribe ]: Joining specified tribe...", flush=True)
    join_success = join_tribe(token, tribe_id)
    
    if join_success:
        print(f"{Fore.GREEN+Style.BRIGHT}[ Tribe ]: Successfully joined specified tribe", flush=True)
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Tribe ]: Failed to join specified tribe", flush=True)
    
    # Final check
    tribe_info = check_tribe(token)
    time.sleep(1)
    if tribe_info and tribe_info.get("id"):
        print(f"\r{Fore.YELLOW+Style.BRIGHT}[ Tribe ]: Current tribe: {tribe_info['title']}", flush=True)
    else:
        print(f"\r{Fore.RED+Style.BRIGHT}[ Tribe ]: Not in any tribe (join may have failed)", flush=True)

def main():
    print_watermark()
    tribe_id = "YOUR_TRIBEID"  # Your TRIBE_ID
    
    while True:
        with open('tgwebapp.txt', 'r') as file:
            query_ids = file.read().splitlines()
        
        if not query_ids:
            print(f"{Fore.RED+Style.BRIGHT}No more query IDs in tgwebapp.txt. Exiting...")
            break
        
        for index, query_id in enumerate(query_ids, start=1):
            token = get_new_token(query_id)
            if token is None:
                continue
            
            process_account(token, tribe_id, index)
            
            # Remove the processed query_id from the file
            with open('tgwebapp.txt', 'r') as file:
                lines = file.readlines()
            with open('tgwebapp.txt', 'w') as file:
                file.writelines(lines[1:])
            
            # Add 3-second delay between processing accounts
            if index < len(query_ids):
                print(f"{Fore.YELLOW+Style.BRIGHT}Waiting 3 seconds before processing next account...")
                time.sleep(3)
        
        print(f"\n{Fore.GREEN+Style.BRIGHT}========={Fore.WHITE+Style.BRIGHT}All accounts in this batch processed{Fore.GREEN+Style.BRIGHT}=========")
        print(f"{Fore.YELLOW+Style.BRIGHT}Waiting for 5 minutes before processing the next batch...")
        time.sleep(300)  # Wait for 5 minutes

if __name__ == "__main__":
    main()