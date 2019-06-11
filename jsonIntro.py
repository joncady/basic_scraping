import json

""" example of loading json file into python"""
with open('schedule.json') as json_file:
    data = json.loads(json_file.read())
    for key in data.keys():
        program = data[key]
        for sections in program:
            print(sections)