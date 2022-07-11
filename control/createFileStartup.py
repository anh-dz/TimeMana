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
