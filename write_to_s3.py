import boto3
import json


def write_to_s3_func(s3_geofences, s3_events):
    s3 = boto3.resource('s3')
    s3.Object('shay-geofence-sync', 'geofences.json').put(Body=(bytes(json.dumps(s3_geofences).encode('UTF-8'))))
    s3.Object('shay-geofence-sync', 'events.json').put(Body=(bytes(json.dumps(s3_events).encode('UTF-8'))))

    known_locations = open('known_locations.json')
    s3.Object('shay-geofence-sync', 'knownlocations.json').put(
        Body=(bytes(json.dumps(json.load(known_locations)).encode('UTF-8'))))
