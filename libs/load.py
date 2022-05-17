import json
import os

path = os.getcwd()


def settingsLoader():
    with open(f"{path}/settings.json", "r") as f:
        return json.load(f)
