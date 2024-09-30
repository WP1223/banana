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
                self.log(f"{red}Error writing to banana.txt file: {str(write_error)}")
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

    def banana_list(self, token, page_num=1, page_size=10):
        url = f"https://interface.carv.io/banana/get_banana_list/v2?page_num={page_num}&page_size={page_size}"
        headers = self.headers(token=token)
        response = scraper.get(url=url, headers=headers)
        return response

    def equip_banana(self, token, banana_id):
        url = f"https://interface.carv.io/banana/do_equip"

        headers = self.headers(token=token)

        data = {"bananaId": banana_id}

        response = scraper.post(url=url, headers=headers, data=data)

        return response

    def quest_list(self, token, page_num=1, page_size=10):
        url = f"https://interface.carv.io/banana/get_quest_list/v2?page_num={page_num}&page_size={page_size}"
        headers = self.headers(token=token)
        try:
            response = scraper.get(url=url, headers=headers)
            response.raise_for_status()
            quest_data = response.json()
            if quest_data["code"] == 0 and quest_data["msg"] == "Success":
                quests = quest_data["data"]["list"]
                return quest_data
            else:
                self.log(f"Error in quest_list: {quest_data['msg']}")
                return None
        except Exception as e:
            return None

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
            "Origin": "https://banana.carv.io",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "*/*",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Ch-Ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128", "Microsoft Edge WebView2";v="128"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"'
        }
        response = scraper.get(url=url, headers=headers)
        return response

    def handle_ads(self, token, tg_id=None):
        self.log(f"{yellow}Checking and watching ads: {green}In progress")
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
                    
                    wait_time = 1 + random.uniform(0.1, 0.5)
                    self.log(f"{yellow}Waiting {wait_time:.2f} seconds before claiming ads...")
                    time.sleep(wait_time)
                    
                    ad_type = 1 if data["show_for_speedup"] else 2
                    
                    claim_response = self.claim_ads_income(token=token, ad_type=ad_type).json()
                    if claim_response["code"] == 0 and claim_response["msg"] == "Success":
                        income = claim_response["data"]["income"]
                        peels = claim_response["data"]["peels"]
                        speedup = claim_response["data"]["speedup"]
                        ad_type_str = "Speedup" if ad_type == 1 else "Peels"
                        self.log(f"{green}Successfully watched {ad_type_str} ad: received {white}{income} USDT - {peels} Peels - {speedup} Speedup")
                    else:
                        self.log(f"{red}Failed to watch ad: {claim_response['msg']}")
                else:
                    self.log(f"{yellow}No ads available at the moment")
            else:
                self.log(f"{red}Failed to retrieve ad info: {ads_info['msg']}")
                self.log(f"{red}Full response: {json.dumps(ads_info, indent=2)}")
        except Exception as e:
            self.log(f"{red}Error handling ads:")
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
                    equip_banana_peel_limit = get_user_info["data"]["equip_banana"][
                        "daily_peel_limit"
                    ]
                    equip_banana_peel_price = get_user_info["data"]["equip_banana"][
                        "sell_exchange_peel"
                    ]
                    equip_banana_usdt_price = get_user_info["data"]["equip_banana"][
                        "sell_exchange_usdt"
                    ]
                    self.log(
                        f"{green}Banana: {white}{banana} - {green}Peels: {white}{peel} - {green}USDT: {white}{usdt} - {green}SPEEDUP: {white}{speedup}"
                    )
                    self.log(
                        f"{green}Using: {white}{equip_banana_name} - {green}Daily Peel Limit: {white}{equip_banana_peel_limit} - {green}Peel Price: {white}{equip_banana_peel_price} - {green}USDT Price: {white}{equip_banana_usdt_price}"
                    )

                    if float(equip_banana_usdt_price) >= 1:
                        entry = f"Account {no+1} - {equip_banana_name} - USDT Price: {equip_banana_usdt_price}"
                        if self.write_unique_entry(entry):
                            self.log(f"{green}Saved valuable banana info (USDT > 1) to banana.txt")
                        else:
                            self.log(f"{yellow}Valuable banana info (USDT > 1) already in banana.txt")
                            
                    # Watch ads
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
                                            f"{white}Tap success: received {green}{peel_added} peels {white}and {green}{speedup} speedup"
                                        )
                                    else:
                                        self.log(f"{red}Tap failed in session {session}")
                                    
                                    time.sleep(random.uniform(1, 5))
                        else:
                            self.log(f"{red}Tap limit reached for today")
                    else:
                        self.log(f"{yellow}Auto Tap: {red}OFF")

                    # Do task
                    if self.auto_do_task:
                        self.log(f"{yellow}Auto Task: {green}ON")
                        get_quest_list = self.quest_list(token=token)
                        if get_quest_list and "data" in get_quest_list and "list" in get_quest_list["data"]:
                            quest_list = get_quest_list["data"]["list"]
                            
                            for quest in quest_list:
                                quest_id = quest.get("quest_id") or quest.get("id")
                                if quest_id is None:
                                    self.log(f"{red}No quest_id found for task: {quest}")
                                    continue
                                
                                quest_name = quest.get("quest_name", "Unknown")
                                achieve_status = quest.get("is_achieved", False)
                                claim_status = quest.get("is_claimed", False)
                                
                                if not achieve_status and not claim_status:
                                    try:
                                        achieve_quest = self.achieve_quest(token=token, quest_id=quest_id).json()
                                        if achieve_quest.get("code") == 0 and achieve_quest.get("msg") == "Success":
                                            self.log(f"{white}Task {yellow}{quest_name} completed: {green}Success")
                                        else:
                                            self.log(f"{white}Task {yellow}{quest_name} completion: {red}Failed - {achieve_quest.get('msg', 'Unknown error')}")
                                        
                                        claim_quest = self.claim_quest(token=token, quest_id=quest_id).json()
                                        if claim_quest.get("code") == 0 and claim_quest.get("msg") == "Success":
                                            self.log(f"{white}Claimed reward for task {yellow}{quest_name}: {green}Success")
                                        else:
                                            self.log(f"{white}Claim reward for task {yellow}{quest_name}: {red}Failed - {claim_quest.get('msg', 'Unknown error')}")
                                    except Exception as e:
                                        self.log(f"{red}Error processing task {quest_name}:")
                                        self.log(f"{red}{str(e)}")
                                        self.log(f"{red}Traceback:")
                                        self.log(f"{red}{traceback.format_exc()}")
                                elif achieve_status and not claim_status:
                                    try:
                                        claim_quest = self.claim_quest(token=token, quest_id=quest_id).json()
                                        if claim_quest.get("code") == 0 and claim_quest.get("msg") == "Success":
                                            self.log(f"{white}Claimed reward for task {yellow}{quest_name}: {green}Success")
                                        else:
                                            self.log(f"{white}Claim reward for task {yellow}{quest_name}: {red}Failed - {claim_quest.get('msg', 'Unknown error')}")
                                    except Exception as e:
                                        self.log(f"{red}Error claiming reward for task {quest_name}:")
                                        self.log(f"{red}{str(e)}")
                                        self.log(f"{red}Traceback:")
                                        self.log(f"{red}{traceback.format_exc()}")
                                else:
                                    self.log(f"{white}Task {yellow}{quest_name}: {green}Already completed and claimed reward")

                            # Handle claim quest lottery
                            while True:
                                try:
                                    claim_quest_lottery = self.claim_quest_lottery(token=token).json()
                                    if claim_quest_lottery.get("code") == 0 and claim_quest_lottery.get("msg") == "Success":
                                        self.log(f"{white}Claim Quest Lottery: {green}Success")
                                    else:
                                        self.log(f"{yellow}No more Quest Lottery to claim")
                                        break
                                except Exception as e:
                                    self.log(f"{red}Error claiming Quest Lottery:")
                                    self.log(f"{red}{str(e)}")
                                    self.log(f"{red}Traceback:")
                                    self.log(f"{red}{traceback.format_exc()}")
                                    break
                        else:
                            self.log(f"{red}Failed to retrieve task list or list is empty")
                    else:
                        self.log(f"{yellow}Auto Task: {red}OFF")

                    # Claim invite
                    if self.auto_claim_invite:
                        self.log(f"{yellow}Auto Claim Invite: {green}ON")
                        get_invite_list = self.invite_list(token=token).json()
                        invite = get_invite_list["data"]
                        if invite is None:
                            self.log(f"{white}Claim Invite: {red}No friends")
                        else:
                            self.log(f"{white}Claim Invite: {green}Friends available")
                            claim_status = invite["claim"]
                            if claim_status:
                                claim_invite = self.claim_invite(token=token)
                                claim_invite_status = claim_invite["msg"]
                                if claim_invite_status == "Success":
                                    self.log(f"{white}Claim Invite: {green}Success")
                                else:
                                    self.log(f"{white}Claim Invite: {red}Failed")
                            else:
                                self.log(
                                    f"{white}Claim Invite: {red}No invite lottery to claim"
                                )
                    else:
                        self.log(f"{yellow}Auto Claim Invite: {red}OFF")

                    # Get lottery info
                    if self.auto_claim_and_harvest:
                        self.log(f"{yellow}Auto harvest bananas: {green}ON")
                        while True:
                            try:
                                get_lottery_info = self.lottery_info(token=token).json()
                                lottery_data = get_lottery_info.get("data", {})
                                lottery_status = lottery_data.get("countdown_end", False)
                                lottery_count = lottery_data.get("remain_lottery_count", 0)
                                
                                remaining_time = self.calculate_remaining_time(lottery_data)
                                remaining_time_str = f"{int(remaining_time)} minutes" if remaining_time > 0 else "0 minutes"
                                
                                self.log(f"{white}Remaining time to harvest: {green}{remaining_time_str}")

                                get_user_info = self.user_info(token=token).json()
                                speedup_count = get_user_info["data"]["speedup_count"]

                                while remaining_time > 60 and speedup_count > 0:
                                    self.log(f"{yellow}Using Speedup. Remaining: {white}{speedup_count}")
                                    do_speedup_response = self.do_speedup(token=token).json()
                                    
                                    if do_speedup_response["code"] == 0 and do_speedup_response["msg"] == "Success":
                                        speedup_count = do_speedup_response["data"]["speedup_count"]
                                        new_lottery_info = do_speedup_response["data"]["lottery_info"]
                                        remaining_time = self.calculate_remaining_time(new_lottery_info)
                                        remaining_time_str = f"{int(remaining_time)} minutes" if remaining_time > 0 else "0 minutes"
                                        self.log(f"{green}Successfully used Speedup. Remaining time: {white}{remaining_time_str}")
                                    else:
                                        self.log(f"{red}Failed to use Speedup: {do_speedup_response['msg']}")
                                        break

                                if speedup_count == 0:
                                    self.log(f"{yellow}No more Speedup available")

                                if lottery_status:
                                    claim_lottery = self.claim_lottery(token=token).json()
                                    claim_status = claim_lottery.get("msg")
                                    if claim_status == "Success":
                                        self.log(f"{white}Claim Banana: {green}Success")
                                    else:
                                        self.log(f"{white}Claim Banana: {red}Failed")
                                        self.log(f"{red}Error details: {claim_lottery}")
                                elif lottery_count > 0:
                                    do_lottery = self.do_lottery(token=token).json()
                                    lottery_status = do_lottery.get("msg")
                                    if lottery_status == "Success":
                                        banana_data = do_lottery.get("data", {})
                                        banana_name = banana_data.get("name", "Unknown")
                                        usdt_value = banana_data.get("sell_exchange_usdt", 0)
                                        peel_value = banana_data.get("sell_exchange_peel", 0)
                                        banana_id = banana_data.get("banana_id")
                                        
                                        self.log(f"{white}Harvest Banana: {green}Success")
                                        self.log(f"{white}Received: {green}{banana_name} - {usdt_value} USDT - {peel_value} Peel")
                                        
                                        ads_response = self.claim_ads_income(token=token, ad_type=2).json()
                                        if ads_response["code"] == 0 and ads_response["msg"] == "Success":
                                            income = ads_response["data"]["income"]
                                            peels = ads_response["data"]["peels"]
                                            speedup = ads_response["data"]["speedup"]
                                            self.log(f"{green}Successfully watched ad: received {white}{income} USDT - {peels} Peels - {speedup} Speedup")
                                        else:
                                            self.log(f"{red}Failed to watch ad: {ads_response['msg']}")
                                        
                                        share_response = self.do_share(token=token, banana_id=banana_id).json()
                                        if share_response["code"] == 0 and share_response["msg"] == "Success":
                                            self.log(f"{green}Successfully shared banana!")
                                        else:
                                            self.log(f"{red}Failed to share banana: {share_response['msg']}")
                                    else:
                                        self.log(f"{white}Harvest Banana: {red}Failed")
                                        self.log(f"{red}Error details: {do_lottery}")
                                else:
                                    self.log(f"{white}Claim and Harvest Banana: {yellow}Not time to harvest yet")
                                    break

                            except Exception as e:
                                self.log(f"{red}Error during harvesting: {str(e)}")
                                break

                    else:
                        self.log(f"{yellow}Auto harvest bananas: {red}OFF")

                    # Equip banana
                    if self.auto_equip_banana:
                        self.log(f"{yellow}Using the best banana: {green}ON")
                        get_banana_list = self.banana_list(token=token).json()
                        if get_banana_list["code"] == 0 and get_banana_list["msg"] == "Success":
                            banana_list = get_banana_list["data"]["list"]
                            available_bananas = [banana for banana in banana_list if banana["count"] > 0]
                            if available_bananas:
                                banana_with_max_peel = max(
                                    available_bananas,
                                    key=lambda b: b["daily_peel_limit"],
                                )
                                banana_id = banana_with_max_peel["banana_id"]
                                banana_name = banana_with_max_peel["name"]
                                banana_peel_limit = banana_with_max_peel["daily_peel_limit"]
                                banana_peel_price = banana_with_max_peel["sell_exchange_peel"]
                                banana_usdt_price = banana_with_max_peel["sell_exchange_usdt"]

                                equip_url = "https://interface.carv.io/banana/do_equip"
                                equip_data = {"bananaId": banana_id}
                                equip_banana = scraper.post(url=equip_url, headers=self.headers(token), json=equip_data).json()
                                equip_status = equip_banana["msg"]
                                if equip_status == "Success":
                                    self.log(
                                        f"{green}You are using the best banana: {white}{banana_name} - "
                                        f"{green}Daily Peel Limit: {white}{banana_peel_limit} - "
                                        f"{green}Peel Price: {white}{banana_peel_price} - "
                                        f"{green}USDT Price: {white}{banana_usdt_price}"
                                    )
                                else:
                                    self.log(f"{white}Banana equip: {red}Failed - {equip_status}")
                            else:
                                self.log(f"{red}No available bananas to equip")
                        else:
                            self.log(f"{red}Failed to retrieve banana list: {get_banana_list['msg']}")
                    else:
                        self.log(f"{yellow}Using the best banana: {red}OFF")

                except Exception as e:
                    self.log(f"{red}Login failed, retrying later!")

            print()
            wait_time = 60 * 60  # Wait for 1 hour before the next loop
            self.log(f"{yellow}Waiting {int(wait_time/60)} minutes to continue!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        banana = Banana()
        banana.main()
    except KeyboardInterrupt:
        sys.exit()
