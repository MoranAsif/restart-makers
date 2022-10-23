import json


def load_known_locations():
    print('load_known_locations from knownlocations.json')
    f = open('known_locations.json')
    data = json.load(f)
    f.close()
    return data


def get_known_location(known_locations, event):
    for item in known_locations:
        if item['location'] == event:
            return item

    return None