import boto3

location_client = boto3.client('location')


def add_new_geofences(s3_geofences):
    print('add_new_geofences')
    for geofence in s3_geofences:
        # put geofence
        response = location_client.put_geofence(
            CollectionName="shay-geofence-collection",
            GeofenceId=geofence['id'],
            Geometry={"Polygon": [geofence['polygon']]},
        )


def delete_geofences():
    print('starting to delete all geofences')
    # get geofences
    geofencesIds = []
    geofences = location_client.list_geofences(CollectionName="shay-geofence-collection")

    for geofence in geofences["Entries"]:
        geofencesIds.append(geofence["GeofenceId"])

    # split into chucks of 10
    batches = split_list(geofencesIds, 10)

    # batch delete each chunk
    for batch in batches:
        res = location_client.batch_delete_geofence(
            CollectionName="shay-geofence-collection", GeofenceIds=batch
        )

    print('number of geofences deleted = ', len(geofencesIds))


def split_list(the_list, chunk_size):
    result_list = []
    while the_list:
        result_list.append(the_list[:chunk_size])
        the_list = the_list[chunk_size:]
    return result_list