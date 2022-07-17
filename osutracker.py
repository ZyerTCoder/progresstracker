import requests
import json
import sys
from time import strftime, localtime, time
import ctypes
import os

os.chdir(r"C:\Users\AZM\Documents\Python\progresstracker")
version = "1.1"
def logger(s):
    timestamp = strftime("%Y/%m/%d %H:%M:%S ", localtime()) 
    _s = f"Osu tracker v{version}: " + s
    with open("trackerlog.txt", mode='a') as l:
        l.write(timestamp + _s + "\n")
    print(_s)

logger("Started")


with open("osuapitoken", mode="r") as r:
    API_KEY = r.read()

link = "https://osu.ppy.sh/api/get_user"
player = "zyertplayer"

if (len(sys.argv)>1):
    player = sys.argv[1]

def request_data():
    params = {
        'k': API_KEY,
        'u': player
    }

    try:
        logger(f"Requesting {player}'s data from {link}")
        response = requests.get(link, params=params)
    except Exception as e:
        ctypes.windll.user32.MessageBoxW(None, u"Error occured when requesting data:\n{}".format(e), u"Osu Progress Tracker", 0)
        logger("Error occured when requesting data: {}".format(e))
        logger("Exited")
        exit()
    try:
        r = response.json()[0]
    except Exception as e:
        ctypes.windll.user32.MessageBoxW(None, u"Error occured when parsing data, mostly likely due to invalid user input:\n{}".format(e), u"Osu Progress Tracker", 0)
        logger("Error occured when parsing data, mostly likely due to invalid user input: {}".format(e))
        logger("Exited")
        exit()
    # remove data we dont care about
    r.pop("join_date")
    r.pop("country")
    r.pop("events")

    return r

now = time()
user_data = request_data()

id =  int(user_data["user_id"])
_300s = int(user_data["count300"])
_100s = int(user_data["count100"])
_50s = int(user_data["count50"])
plays = int(user_data["playcount"])
time = int(user_data["total_seconds_played"])

totalhits = _300s + _100s + _50s
hitsperplay = totalhits/plays
hitspersecond = totalhits/time
averageplaylength = time/plays

data = ", ".join([str(v) for v in user_data.values()])
write = f"{now}, {totalhits}, {hitsperplay}, {hitspersecond}, {averageplaylength}, {data}\n"

path = f"{os.getcwd()}\\{id}.csv"

try:
    with open(path, mode='a') as f:
        f.write(write)
        logger(f"Wrote data to {path}")
except Exception as e:
    ctypes.windll.user32.MessageBoxW(None, u"Error occured when writing data to {}, maybe file is open on another app:\n{}".format(path, e), u"Osu Progress Tracker", 0)
    logger(f"Error occured when writing data to {path}, maybe file is open on another app: {e}")
logger("Exited")