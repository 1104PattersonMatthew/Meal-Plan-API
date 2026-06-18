import json
import os


def read_data(filepath):
    if not os.path.exists(filepath):
        return [] #prevents crash if there isn't a json file

    with open(filepath, "r") as file:
        return json.load(file)


def write_data(filepath, data):
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)


#this file just reads from and saves to json.