import aws_geofences_collection_handler
import known_locations_handler
import get_calendar_events
import write_to_s3
import uuid
import time
import create_geofence

s3_events = []  # list of final events
s3_geofences = []  # loist of final geofences


def lambda_handler(event, context):
    print("Starting lambda ha:")

    aws_geofences_collection_handler.delete_geofences()  # delete all geofences except for home
    s3_known_geofences = known_locations_handler.load_known_locations()  # get known locations from s3
    events = get_calendar_events.get_calender_events_list()  # fetch calender events

    add_home(s3_known_geofences)  # first add home to geofence list

    if events == None:
        print('error: no events found')
        return

    print(f'---------Found {len(events["items"])} events-----------')

    for event in events["items"]:  # loop through events

        print("Starting to loop on events:")
        print(f"s3_events: {s3_events}")
        print(f"s3_geofences: {s3_geofences}")

        if event.get('location') is None:  # if event does not have location
            no_location_found(event)  # add event to s3_events with empty location - is it necessary?
            continue

        known_location = known_locations_handler.get_known_location(s3_known_geofences, event['location'])
        if known_location is not None:  # check if geofence is known
            print("-------------is known_location")
            add_known_location(event, known_location)  # if so add known geofence
            continue
        else:
            print("-------------not known_location")
            new_event_id = str(uuid.uuid4())
            geofence_id = geofence_already_exits(event, new_event_id)  # check if geofence already exists
            if geofence_id is None:  # geofence not exist
                geofence = create_geofence.create_new_geofence(event['location'],
                                                               new_event_id)  # else create a new geofence
                s3_geofences.append(geofence)
                geofence_id = geofence["id"]

            new_event = create_new_event(new_event_id, event, geofence_id)
            s3_events.append(new_event)

    print('geofences created = ', len(s3_geofences))
    print('events created = ', len(s3_events))

    aws_geofences_collection_handler.add_new_geofences(s3_geofences)  # add all geofences at the end

    write_to_s3.write_to_s3_func(s3_geofences, s3_events)  # write results to events and geofence buckets


def add_home(known_geofences):
    for geofence in known_geofences:
        if geofence["is_home"] == True:
            print("adding home geofence")
            s3_geofences.append(geofence)


def add_known_location(event, geofence):
    # create new event and add to events
    event_id = str(uuid.uuid4())
    new_event = create_new_event(event_id, event, geofence['id'])
    s3_events.append(new_event)

    # check if we need to add geofence to events
    for fence in s3_geofences:
        if fence['id'] == geofence['id']:  # already exists in geofence
            fence['calender_events'].append(event_id)
            return

    # if does not already exists
    geofence['calender_events'].append(event_id)
    s3_geofences.append(geofence)  # add to master geofence list


def geofence_already_exits(event, new_event_id):
    for geofence in s3_geofences:
        if geofence['location'] == event['location']:
            geofence['calender_events'].append(new_event_id)
            return geofence['id']

    return None


def no_location_found(event):
    event_id = str(uuid.uuid4())
    new_event = create_new_event(event_id, event, "")
    s3_events.append(new_event)


def create_new_event(event_id, event, geofence_id):
    location = ""
    if event.get("location") is not None:
        location = event["location"]

    return {
        "id": event_id,
        "timestamp": int(time.time()),
        "summary": event["summary"],
        "start": event["start"]["dateTime"],
        "end": event["end"]["dateTime"],
        "location": location,
        "geofence": geofence_id,
    }