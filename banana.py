import os
import sys
import random
import time
import traceback
import requests
from colorama import *
from datetime import datetime
import json
import brotli

import cloudscraper

scraper = cloudscraper.create_scraper()

red = Fore.LIGHTRED_EX
yellow = Fore.LIGHTYELLOW_EX
green = Fore.LIGHTGREEN_EX
black = Fore.LIGHTBLACK_EX
blue = Fore.LIGHTBLUE_EX
white = Fore.LIGHTWHITE_EX
reset = Style.RESET_ALL

script_dir = os.path.dirname(os.path.realpath(__file__))

data_file = os.path.join(script_dir, "data.txt")
config_file = os.path.join(script_dir, "config.json")
banana_file = os.path.join(script_dir, "banana.txt")

class Banana:
    def __init__(self):
        self.line = white + "~" * 50
        self.unique_entries = set()
        self.load_existing_entries()

        self.auto_equip_banana = (
            json.load(open(config_file, "r")).get("auto-equip-banana", "false").lower()
            == "true"
        )

        self.auto_do_task = (
            json.load(open(config_file, "r")).get("auto-do-task", "false").lower()
            == "true"
        )

        self.auto_claim_invite = (
            json.load(open(config_file, "r")).get("auto-claim-invite", "false").lower()
            == "true"
        )

        self.auto_claim_and_harvest = (
            json.load(open(config_file, "r"))
            .get("auto-claim-and-harvest", "false")
            .lower()
            == "true"
        )

        self.auto_click = (
            json.load(open(config_file, "r")).get("auto-click", "false").lower()
            == "true"
        )

    def load_existing_entries(self):
        try:
            with open(banana_file, "r", encoding="utf-8") as f:
                for line in f:
                    self.unique_entries.add(line.strip())
        except FileNotFoundError:
            pass

    def write_unique_entry(self, entry):
        if entry not in self.unique_entries:
            try:
                with open(banana_file, "a", encoding="utf-8") as f:
                    f.write(entry + "\n")
                self.unique_entries.add(entry)
                return True
            except Exception as write_error:
                self.log(f"{red}Error writing to banana.txt: {str(write_error)}")
        return False

    def headers(self, token):
        return {
            "Accept": "application/json, text/plain, */*",
            "Authorization": f"Bearer {token}",
            "Origin": "https://banana.carv.io",
            "Referer": "https://banana.carv.io/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }

    def get_token(self, data):
        url = f"https://interface.carv.io/banana/login"

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://banana.carv.io",
            "Referer": "https://banana.carv.io/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }

        data = {"tgInfo": f"{data}"}

        response = scraper.post(url=url, headers=headers, data=data)

        return response

    def user_info(self, token):
        url = f"https://interface.carv.io/banana/get_user_info"

        headers = self.headers(token=token)

        response = scraper.get(url=url, headers=headers)

        return response

    def banana_list(self, token):
        url = f"https://interface.carv.io/banana/get_banana_list"

        headers = self.headers(token=token)

        response = scraper.get(url=url, headers=headers)

        return response

    def equip_banana(self, token, banana_id):
        url = f"https://interface.carv.io/banana/do_equip"

        headers = self.headers(token=token)

        data = {"bananaId": banana_id}

        response = scraper.post(url=url, headers=headers, data=data)

        return response

    def quest_list(self, token):
        url = f"https://interface.carv.io/banana/get_quest_list"

        headers = self.headers(token=token)

        response = scraper.get(url=url, headers=headers)

        return response

    def achieve_quest(self, token, quest_id):
        url = f"https://interface.carv.io/banana/achieve_quest"

        headers = self.headers(token=token)

        data = {"quest_id": quest_id}

        response = scraper.post(url=url, headers=headers, data=data)

        return response

    def claim_quest(self, token, quest_id):
        url = f"https://interface.carv.io/banana/claim_quest"

        headers = self.headers(token=token)

        data = {"quest_id": quest_id}

        response = scraper.post(url=url, headers=headers, data=data)

        return response

    def claim_quest_lottery(self, token):
        url = f"https://interface.carv.io/banana/claim_quest_lottery"

        headers = self.headers(token=token)

        headers["Content-Type"] = "application/json"

        data = {}

        response = scraper.post(url=url, headers=headers, data=data)

        return response

    def invite_list(self, token):
        url = f"https://interface.carv.io/banana/get_invite_list"

        headers = self.headers(token=token)

        response = scraper.get(url=url, headers=headers)

        return response

    def claim_invite(self, token):
        url = f"https://interface.carv.io/banana/claim_lottery"

        headers = self.headers(token=token)

        data = {"claimLotteryType": 2}

        response = scraper.post(url=url, headers=headers, data=data)

        return response

    def lottery_info(self, token):
        url = f"https://interface.carv.io/banana/get_lottery_info"

        headers = self.headers(token=token)

        response = scraper.get(url=url, headers=headers)

        return response

    def claim_lottery(self, token):
        url = f"https://interface.carv.io/banana/claim_lottery"

        headers = self.headers(token=token)

        data = {"claimLotteryType": 1}

        response = scraper.post(url=url, headers=headers, data=data)

        return response

    def do_lottery(self, token):
        url = f"https://interface.carv.io/banana/do_lottery"

        headers = self.headers(token=token)

        headers["Content-Type"] = "application/json"

        data = {}

        response = scraper.post(url=url, headers=headers, data=data)

        return response

    def claim_ads_income(self, token, ad_type):
        url = "https://interface.carv.io/banana/claim_ads_income"
        headers = self.headers(token=token)
        data = {"type": ad_type}
        response = scraper.post(url=url, headers=headers, data=data)
        return response

    def do_share(self, token, banana_id):
        url = "https://interface.carv.io/banana/do_share"
        headers = self.headers(token=token)
        data = {"banana_id": banana_id}
        response = scraper.post(url=url, headers=headers, data=data)
        return response

    def do_click(self, token, click_count):
        url = f"https://interface.carv.io/banana/do_click"

        headers = self.headers(token=token)

        data = {"clickCount": click_count}

        response = scraper.post(url=url, headers=headers, data=data)

        return response

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}]{reset} {msg}{reset}")

    def do_speedup(self, token):
        url = "https://interface.carv.io/banana/do_speedup"
        headers = self.headers(token=token)
        data = {}
        response = scraper.post(url=url, headers=headers, json=data)
        return response

    def calculate_remaining_time(self, lottery_data):
        last_countdown_start_time = lottery_data.get('last_countdown_start_time', 0)
        countdown_interval = lottery_data.get('countdown_interval', 0)
        countdown_end = lottery_data.get('countdown_end', False)

        if not countdown_end:
            current_time = datetime.now()
            last_countdown_start = datetime.fromtimestamp(last_countdown_start_time / 1000)
            elapsed_time = (current_time - last_countdown_start).total_seconds() / 60
            remaining_time_minutes = max(countdown_interval - elapsed_time, 0)
            return remaining_time_minutes
        return 0

    def user_ads_info(self, token):
        url = "https://interface.carv.io/banana/user_ads_info"
        headers = self.headers(token=token)
        response = scraper.get(url=url, headers=headers)
        return response

    def claim_ads_income(self, token, ad_type):
        url = "https://interface.carv.io/banana/claim_ads_income"
        headers = self.headers(token=token)
        data = {"type": ad_type}
        response = scraper.post(url=url, headers=headers, data=data)
        return response

    def call_adsgram_api(self, tg_id):
        url = f"https://api.adsgram.ai/adv?blockId=2748&tg_id={tg_id}&tg_platform=tdesktop&platform=Win32&language=en&is_premium=true&chat_type=sender&chat_instance=-6089476818413932417"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Referer": "https://banana.carv.io/",
            "Origin": "https://banana.carv.io/",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "*/*",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Ch-Ua": '\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\", \"Microsoft Edge WebView2\";v=\"128\"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '\"Windows\"'
        }
        response = scraper.get(url=url, headers=headers)
        return response

    def handle_ads(self, token, tg_id=None):
        self.log(f"{yellow}Check and view advertisements: {green}In progress")
        try:
            ads_info = self.user_ads_info(token=token).json()
            if ads_info["code"] == 0 and ads_info["msg"] == "Success":
                data = ads_info["data"]
                if data["show_for_speedup"] or data["show_for_peels"]:
                    if tg_id:
                        self.log(f"{yellow}Calling adsgram API...")
                        adsgram_response = self.call_adsgram_api(tg_id)
                        
                        if adsgram_response.status_code == 200:
                            self.log(f"{green}Successfully called adsgram API")
                        else:
                            self.log(f"{red}Failed to call adsgram API: {adsgram_response.status_code}")
                            self.log(f"{red}Response content: {adsgram_response.text[:500]}...")
                    else:
                        self.log(f"{yellow}No tg_id, skipping adsgram API call")
                    
                    wait_time = 15 + random.uniform(0.1, 0.5)
                    self.log(f"{yellow}Waiting {wait_time:.2f} seconds before claiming advertisement...")
                    time.sleep(wait_time)
                    
                    ad_type = 1 if data["show_for_speedup"] else 2
                    
                    claim_response = self.claim_ads_income(token=token, ad_type=ad_type).json()
                    if claim_response["code"] == 0 and claim_response["msg"] == "Success":
                        income = claim_response["data"]["income"]
                        peels = claim_response["data"]["peels"]
                        speedup = claim_response["data"]["speedup"]
                        ad_type_str = "Speedup" if ad_type == 1 else "Peels"
                        self.log(f"{green}Successfully viewed advertisement {ad_type_str}: received {white}{income} USDT - {peels} Peels - {speedup} Speedup")
                    else:
                        self.log(f"{red}Failed to view advertisement: {claim_response['msg']}")
                else:
                    self.log(f"{yellow}No available advertisements at this time")
            else:
                self.log(f"{red}Unable to retrieve advertisement information: {ads_info['msg']}")
                self.log(f"{red}Full response: {json.dumps(ads_info, indent=2)}")
        except Exception as e:
            self.log(f"{red}Error processing advertisement:")
            self.log(f"{red}{str(e)}")
            self.log(f"{red}Traceback:")
            self.log(f"{red}{traceback.format_exc()}")

    def main(self):
        while True:
            data = open(data_file, "r").read().splitlines()
            num_acc = len(data)
            self.log(self.line)
            self.log(f"{green}Total accounts: {white}{num_acc}")
            for no, data in enumerate(data):
                self.log(self.line)
                self.log(f"{green}Account: {white}{no+1}/{num_acc}")

                # Get token
                try:
                    get_token = self.get_token(data=data).json()
                    token = get_token["data"]["token"]

                    # Get user info
                    get_user_info = self.user_info(token=token).json()
                    banana = get_user_info["data"]["banana_count"]
                    peel = get_user_info["data"]["peel"]
                    usdt = get_user_info["data"]["usdt"]
                    speedup = get_user_info["data"]["speedup_count"]
                    tg_id = get_user_info["data"]["user_id"] 
                    equip_banana_name = get_user_info["data"]["equip_banana"]["name"]
                    equip_banana_peel_limit = get_user_info["data"]["equip_banana"]["daily_peel_limit"]
                    equip_banana_peel_price = get_user_info["data"]["equip_banana"]["sell_exchange_peel"]
                    equip_banana_usdt_price = get_user_info["data"]["equip_banana"]["sell_exchange_usdt"]
                    self.log(
                        f"{green}Banana: {white}{banana} - {green}Peels: {white}{peel} - {green}USDT: {white}{usdt} - {green}SPEEDUP: {white}{speedup}"
                    )
                    self.log(
                        f"{green}Currently using: {white}{equip_banana_name} - {green}Daily Peel Limit: {white}{equip_banana_peel_limit} - {green}Peel Price: {white}{equip_banana_peel_price} - {green}USDT Price: {white}{equip_banana_usdt_price}"
                    )

                    if float(equip_banana_usdt_price) >= 1:
                        entry = f"Account {no+1} - {equip_banana_name} - USDT Price: {equip_banana_usdt_price}"
                        if self.write_unique_entry(entry):
                            self.log(f"{green}Information for banana worth more than 1 written to banana.txt")
                        else:
                            self.log(f"{yellow}Information for banana worth more than 1 written to banana.txt")
                            
                    # View ads
                    self.handle_ads(token, tg_id)

                    # Auto Click
                    if self.auto_click:
                        self.log(f"{yellow}Auto Tap: {green}ON")
                        get_user_info = self.user_info(token=token).json()
                        max_click_count = get_user_info["data"]["max_click_count"]
                        today_click_count = get_user_info["data"]["today_click_count"]
                        click_left = max_click_count - today_click_count

                        if click_left > 0:
                            sessions = 10
                            clicks_per_session = [0] * sessions
                            
                            for _ in range(click_left):
                                session = random.randint(0, sessions - 1)
                                clicks_per_session[session] += 1
                            
                            for session, clicks in enumerate(clicks_per_session, 1):
                                if clicks > 0:
                                    do_click = self.do_click(token=token, click_count=clicks).json()
                                    status = do_click["msg"]
                                    if status == "Success":
                                        peel_added = do_click["data"]["peel"]
                                        speedup = do_click["data"]["speedup"]
                                        self.log(
                                            f"{white}Tap successful: received {green}{peel_added} peels {white}and {green}{speedup} speedup"
                                        )
                                    else:
                                        self.log(f"{red}Tap failed in session {session}")
                                    
                                    time.sleep(random.uniform(1, 5))
                        else:
                            self.log(f"{red}Reached today's tap limit")
                    else:
                        self.log(f"{yellow}Auto Tap: {red}OFF")

                    # Do task
                    if self.auto_do_task:
                        self.log(f"{yellow}Automatically performing tasks: {green}ON")
                        get_quest_list = self.quest_list(token=token).json()
                        quest_list = get_quest_list["data"]["quest_list"]
                        for quest in quest_list:
                            quest_id = quest["quest_id"]
                            quest_name = quest["quest_name"]
                            achieve_status = quest["is_achieved"]
                            claim_status = quest["is_claimed"]
                            if not achieve_status and not claim_status:
                                achieve_quest = self.achieve_quest(
                                    token=token, quest_id=quest_id
                                ).json()
                                claim_quest = self.claim_quest(
                                    token=token, quest_id=quest_id
                                ).json()
                                quest_status = claim_quest["msg"]
                                if quest_status == "Success":
                                    self.log(f"{white}Completed task {yellow}{quest_name}: {green}Success")
                                else:
                                    self.log(
                                        f"{white}Completed task {yellow}{quest_name
