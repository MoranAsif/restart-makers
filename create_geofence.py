import uuid
from geographiclib.geodesic import Geodesic
import boto3

location_client = boto3.client('location')


def create_new_geofence(place, event_id):
    if place == "":
        return

    # get long and lat
    response = location_client.search_place_index_for_text(
        IndexName="explore.place", Text=place
    )
    position = response["Results"][0]["Place"]["Geometry"]["Point"]
    long = position[0]
    lat = position[1]
    polygon = get_polygon(long, lat)
    geofence_id = str(uuid.uuid4())

    geofence = {
        "location": place,
        "is_known": False,
        "radius": 100,
        "id": geofence_id,
        "polygon": polygon,
        "centerLatitude": lat,
        "centerLongitude": long,
        "calender_events": [event_id],
    }

    return geofence


def get_polygon(longitude, latitude):
    result = []
    radius = 100  # meters
    number_of_vertices = 18
    for i in range(number_of_vertices):
        degree = 360.0 / number_of_vertices * i
        geo = Geodesic.WGS84.Direct(latitude, longitude, degree, radius)
        result.append([geo["lon2"], geo["lat2"]])

    result.append(result[0])  # close the circle
    result.reverse()
    print(f"Result: {result}")
    print('\n\n')

    return result


