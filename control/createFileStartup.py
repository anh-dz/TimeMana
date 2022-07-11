import json
from os import path, remove, makedirs
from . dataTim import *

def create_folder() -> bool:
    if not path.exists(f"C://Users//{user}//AppData//Roaming//TimeMana"):
        makedirs(f"C://Users//{user}//AppData//Roaming//TimeMana")
        with open(f"C://Users//{user}//AppData//Roaming//TimeMana//settings.json", "w") as f:
            pass

        with open(f"C://Users//{user}//AppData//Roaming//TimeMana//day.json", "w") as f:
            pass

        with open(f"C://Users//{user}//AppData//Roaming//TimeMana//tim.json", "w") as f:
            pass
        return True
    
    return False

def default_data():
    day = {"1": {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0},
           "2": {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0},
           "3": {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0},
           "4": {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0},
           "5": {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}}
    data = {"last time": "00:00:00", "last day": "Thursday"}
    settings_data = {"alarmDur": 30, "startWithSys": False, "openUI": True, "sound": True}
    with open(f"C://Users//{user}//AppData//Roaming//TimeMana//settings.json", "w") as outfile:
        json.dump(settings_data, outfile)
    with open(f"C://Users//{user}//AppData//Roaming//TimeMana//tim.json", "w") as outfile:
        json.dump(data, outfile)
    with open(f"C://Users//{user}//AppData//Roaming//TimeMana//day.json", "w") as outfile:
         json.dump(day, outfile)
