import requests
import sys
import datetime
from datetime import datetime, timedelta
import re
import random
import ast
import json

###
###
### settings

webhook = r""
# webhook = r"https://discordapp.com/api/webhooks/XXXXXXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# Discord

UTC_off = 0
# UTC_off = +4
# UTC_off = -4
# currently UTC

custom_date = False
# custom_date = str("YYYY-MM-DD")
# (2025-04-17----2026-12-31)
# season changes 2026-01-29

###
###
### get missions

today = datetime.now()
today = today.strftime("%Y-%m-%d")

if custom_date:
    url = rf"https://doublexp.net/static/json/bulkmissions/{custom_date}.json"
else:
    url = rf"https://doublexp.net/static/json/bulkmissions/{today}.json"

try:
    response = requests.get(url)
    response.raise_for_status()
except Exception:
    sys.exit(1)

data = response.text

###
###
### UTC +-

def add_two_hours_to_timestamps(text: str) -> str:
    pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"
    def replacer(match):
        ts = match.group(0)
        dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
        dt_plus_2h = dt + timedelta(hours=UTC_off)
        return dt_plus_2h.strftime("%Y-%m-%dT%H:%M:%SZ")
    return re.sub(pattern, replacer, text)

data = add_two_hours_to_timestamps(data)

###
###
### clean up

def remove_fields(obj, keys_to_remove=("Seed", "id", "included_in", "RandomSeed", "CodeName", "timestamp")):
    if isinstance(obj, dict):
        for key in keys_to_remove:
            obj.pop(key, None)
        for value in obj.values():
            remove_fields(value, keys_to_remove)
    elif isinstance(obj, list):
        for item in obj:
            remove_fields(item, keys_to_remove)

data = ast.literal_eval(data)

remove_fields(data)

###
###
### clean up more

now = datetime.now()

rounded_now = now.replace(
    minute=(now.minute // 30) * 30,
    second=0,
    microsecond=0
)

current_key = rounded_now.strftime("%Y-%m-%dT%H:%M:%SZ")

for key in list(data.keys()):
    if key[0].isdigit() and key.endswith("Z"):
        if key < current_key:
            del data[key]

###
###
### cutting

season = data.pop("ver")
#print(f"Season: {season}")


deal = data.pop("dailyDeal")
deal = json.dumps(deal, indent=2)

missions = json.dumps(data, indent=2)

###
###
### prepare and send missions

messeges = [
    "Alright team, I’ve compiled today’s mission assignments. Try not to embarrass the company.",
    "New mission data is in. Read it carefully—Hoxxes won’t forgive mistakes.",
    "These are today’s approved operations. Stick to the plan and bring back something valuable.",
    "Mission briefs uploaded. Remember: survival is optional, results are not.",
    "Fresh mission intel just came in. Management expects results.",
    "Here’s today’s mission lineup. Get to work.",
    "These missions won’t complete themselves. Get moving.",
    "Management dumped another pile of bullshit on my desk. Congratulations, it’s your problem now.",
    "Hoxxes is in a bad mood today. Grab your gear and deal with it."
]

messege = random.choice(messeges)

data = None
content = missions

files = {
    "file": (f"{today}_Missions.txt", content)
}

data = {
    "content": messege
}


try:
    response = requests.post(webhook, data=data, files=files, timeout=5)
    response.raise_for_status()
except Exception:
    sys.exit(1)

###
###
### prepare and send deal

salutes = [
    "Stone.",
    "Rock on!",
    "We rock!",
    "For Karl!",
    "Rock solid!",
    "For Teamwork!",
    "By the Beard!",
    "Rock and roll!",
    "Rock... Solid!",
    "Rock and Stone!",
    "Rock and Stone.",
    "We're the best!",
    "Galaxies finest!",
    "ROCK! AND! STONE!",
    "Rock and... Stone!",
    "For Rock and Stone!",
    "We are unbreakable!",
    "ROCK... AND... STONE!",
    "Let's Rock and Stone!",
    "Rock me like a Stone!",
    "Leave No Dwarf Behind!",
    "Rock and Stone forever!",
    "Rock and roll and stone!",
    "Rock and Stone everyone!",
    "Rock and Stone, Brother!",
    "Yeaahhh! Rock and Stone!",
    "Rockitty Rock and Stone!",
    "None can stand before us!",
    "Like that! Rock and Stone!",
    "Rock and Stone to the Bone!",
    "Yeah, yeah, Rock and Stone.",
    "Gimmie a Rock... and Stone!",
    "We fight for Rock and Stone!",
    "Rock and Stone in the Heart!",
    "Did I hear a Rock and Stone?",
    "Rock and Stone... Yeeaaahhh!",
    "Come on guys! Rock and Stone!",
    "Stone and Rock! ...Oh, wait...",
    "That's it lads! Rock and Stone!",
    "Rock and Stone! It never gets old.",
    "Rock and Stone you beautiful dwarf!",
    "Rock! (burp) And! (burp) Stone! (burp)",
    "Rock and Stone like there's no tomorrow!",
    "If you Rock and Stone, you're never alone!",
    "If I had a credit for every Rock and Stone.",
    "Rock and Stone, the pretty sound of teamwork!",
    "For those about to Rock and Stone, we salute you!",
    "If you don't Rock and Stone, you ain't comin' home!",
    "Last one to Rock and Stone pays for the first round!",
    "Gimmie an R! Gimmie an S! Gimmie a Rock. And. Stone!"
    ]

salute = random.choice(salutes)

data = None
content = deal

files = {
    "file": (f"{today}_Deal.txt", content)
}

data = {
    "content": salute
}


try:
    response = requests.post(webhook, data=data, files=files, timeout=5)
    response.raise_for_status()
except Exception:
    sys.exit(1)

sys.exit(0)