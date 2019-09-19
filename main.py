import json
from datetime import datetime
import firebase_admin
from firebase_admin import firestore

default_app = firebase_admin.initialize_app()
db = firestore.client()

def hello_world(request):
    request_json = request.get_json()
    request_json = str(request_json)
    print(request_json)
    request_json = request_json[1:(len(request_json) - 1)]
    request_json_list = request_json.split(',')

    tags = []
    if 'cam01' in request_json:
        intime = request_json_list[1]
        intime = intime.split(':', 1)
        intime = intime[1]
        intime = intime[2:(len(intime) - 1)]
        hour = int(intime[11:13])

        name = request_json_list[0]
        name = name.split(':')
        name = name[1]
        name = name[2:(len(name) - 1)]

        field = {}
        field["component"] = "Employee_name"
        field["tag"] = "Employee_name"
        field["value"] = name
        field["unit"] = "NA"
        tags.append(field)

        field = {}
        field["component"] = "InTime"
        field["tag"] = "InTime"
        field["value"] = intime
        if hour < 12:
            field["unit"] = "AM"
        else:
            field["unit"] = "PM"
        tags.append(field)

        camera_name = "Cam01"
        field = {}
        field["component"] = "Camera"
        field["tag"] = "Camera"
        field["value"] = camera_name
        field["unit"] = "NA"
        tags.append(field)
    else:
        outtime = request_json_list[1]
        outtime = outtime.split(':', 1)
        outtime = outtime[1]
        outtime = outtime[2:(len(outtime) - 1)]
        hour = int(outtime[11:13])

        name = request_json_list[0]
        name = name.split(':')
        name = name[1]
        name = name[2:(len(name) - 1)]

        field = {}
        field["component"] = "Employee_name"
        field["tag"] = "Employee_name"
        field["value"] = name
        field["unit"] = "NA"
        tags.append(field)

        field = {}
        field["component"] = "OutTime"
        field["tag"] = "OutTime"
        field["value"] = outtime
        if hour < 12:
            field["unit"] = "AM"
        else:
            field["unit"] = "PM"
        tags.append(field)

        camera_name = "Cam02"
        field = {}
        field["component"] = "Camera"
        field["tag"] = "Camera"
        field["value"] = camera_name
        field["unit"] = "NA"
        tags.append(field)

    now = datetime.now()
    epoch = datetime(1970, 1, 1)
    td = now - epoch
    epoch = round((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6) / 1e6)
    present = now.strftime("%d/%m/%Y %H:%M:%S")
    json_body = {}
    json_body["asset"] = "Camera"
    json_body["assetcode"] = camera_name
    json_body["timestamp"] = present
    json_body["messageid"] = epoch
    json_body["description"] = "Attendance"
    json_body["tags"] = tags
    #jsonStr = json.dumps(json_body) -- Dont convert to JSON.
    print("data published to iot_data++++++++++", json_body)
    db.collection(u'<Collection_name>').document().set(json_body) # Provide the collection name of the firestore
    #return json_body  -- Dont return anything!!
