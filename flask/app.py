import asyncio

from flask import Flask, make_response, jsonify, request
from pymongo import MongoClient
import mongo as mg
import telebot
import img

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

db_name = "pet_detection"
col_pics_name = "pics"
col_pets_name = "pets"


@app.route("/mongo/test")
def mongo_test():
    return make_response("Success", 200)


@app.route("/mongo/db", methods=["POST"])
def mongo_db():
    package = mg.mongo_establish_connection_write()

    if package["code"] == 0:
        return package["response"]

    client = package["response"]

    # Datenbank erstellen
    db = client[db_name]
    print(client.list_database_names())

    # Collections erstellen
    pics = db["pics"]
    pets = db["pets"]

    document = {"picture": img.image, "id": 1, "date": "2023-05-29", "time": "11:03:46"}
    pics.insert_one(document)

    document2 = {"id": 1, "type": "dog", "accuracy": 0.9, "bid": "1", "foreignKey": 1}
    pets.insert_one(document2)

    response = make_response("Datenbank erfolgreich initialisiert", 201)

    return response


@app.route("/mongo/input", methods=["POST"])
def mongo_camera_post():
    data = request.get_json()
    package = mg.mongo_establish_connection_write()

    if package["code"] == 0:
        return package["response"]

    """
    if code != 0, dann bedeutet das, dass die Verbindung herrgestellt werden konnte
    'response' ist dann kein make_response-Objekt, sondern der client
    """
    client = package["response"]

    # Überprüfung, ob die DB und die Collections existieren
    mongo_check = mg.mongo_check_all(client, db_name, col_pics_name, col_pets_name)
    if not mongo_check["status"]:
        return mongo_check["response"]

    # Falls alles in Ordnung ist, dann wird auf die DB und die Collections zugegriffen
    db = client[db_name]
    collection_pics = db[col_pics_name]
    collection_pets = db[col_pets_name]

    unique_id = 1
    result = collection_pics.find_one({}, sort=[("id", -1)])
    if result is not None:
        unique_id = result["id"] + 1
    else:
        return make_response("keine bilder vorhanden", 503)

    pic = {
        "id": unique_id,    
        "picture": data['picture'],
        "date": data['date'],
        "time": data['time']
    }

    # Pet bauen und abspeichern
    for item in data['detections']:
        unique_pet_id = 0
        pet_result = collection_pets.find_one({}, sort=[("id", -1)])
        if pet_result is not None:
            highest_pet_id = pet_result["id"]
            unique_pet_id = highest_pet_id + 1
        else:
            return make_response("keine pets initialisiert", 503)

        pet = {
            "id": unique_pet_id,
            "type": item['type'],
            "accuracy": item['accuracy'],
            "bid": item['bid'],
            "foreignKey": unique_id
        }

        try:
            collection_pets.insert_one(pet)
        except Exception as error:
            return make_response("pet konnte nicht gespeichert werden", 503)

    # Abspeichern des Bildes
    try:
        collection_pics.insert_one(pic)
    except:
        return make_response("pic konnte nicht gespeichert werden", 503)

    try:
        asyncio.run(telebot.send_telegram_notification(data))
    except:
        return make_response("db insert: success, telebot: failed", 201)
    
    return make_response("Erfolg", 201)


@app.route("/mongo/get_image")
def mongo_frontend_get():
    data = request.get_json()
    package = mg.mongo_establish_connection_write()

    if package["code"] == 0:
        return package["response"]

    client = package["response"]

    #Überprüfung, ob die DB und die Collections existieren
    mongo_check = mg.mongo_check_all(client, db_name, col_pics_name, col_pets_name)
    if not mongo_check["status"]:
        return mongo_check["response"]

    # Falls alles in Ordnung ist, dann wird auf die DB und die Collections zugegriffen
    db = client[db_name]
    collection_pics = db[col_pics_name]
    collection_pets = db[col_pets_name]

    id_filter = None
    if data["id"]:
        id_filter = {
            "id": {
                "$lte": data["id"]
            }
        }

    date_filter = {
        "date": {
            "$lte": data["date"]
        }
    }

    type_filter = None
    if data["type"] != "all":
        type_filter = {
            "type": data["type"]
        }

    accuracy_filter = {
        "accuracy": {
            "$gte": data["accuracy"]
        }
    }

    # Kombinieren der Filter
    pic_filters = None
    print(data["id"])
    if data["id"]:
        pic_filters = {
            "$and": [date_filter, id_filter]
        }
    else:
        pic_filters = date_filter
    print(pic_filters)

    pet_filters = None
    if data["type"] != "all":
        pet_filters = {
            "$and": [type_filter, accuracy_filter]
        }
    else:
        pet_filters = {
            "$and": [accuracy_filter]
        }

    # Abfrage der Dokumente
    pic_result = collection_pics.find(pic_filters).sort([("id", -1)]).limit(1)
    pet_result = collection_pets.find(pet_filters).sort([("id", -1)])

    # Überprüfung des Ergebnisses
    pets = []
    if len(list(pet_result.clone())) > 0:
        for document in pet_result:
            pet = {
                "id": document["id"],
                "type": document["type"],
                "accuracy": document["accuracy"],
                "bid": document["bid"],
                "foreignKey": document["foreignKey"]
            }
            pets.append(pet)
            print(f"pet document:{document}")
            print(pet)
    else:
        return make_response("Keine Pets unter diesen Bedingungen gefunden", 404)

    pic = list()
    print(f"länge: {len(list(pic_result.clone()))}")
    if len(list(pic_result.clone())) > 0:
        for document in list(pic_result):
            pic2 = {
                "id": document["id"],
                "picture": document["picture"],
                "date": document["date"],
                "time": document["time"],
                "detections": pets
            }
            pic.append(pic2)
            print(f"document: {document}")
            print(f"pic: {pic}")
    else:
        return make_response("kein pic unter diesen Bedingungen gefunden", 404)
    import json
    print(f"pic: {pic}")
    print(json.dumps(pic[0], indent=1))
    return make_response(jsonify(pic[0]), 200)


@app.route("/mongo/col_drop")
def mongo_drop():
    package = mg.mongo_establish_connection_write()

    if package["code"] == 0:
        return package["response"]

    client = package["response"]

    #Überprüfung, ob die DB und die Collections existieren
    mongo_check = mg.mongo_check_all(client, db_name, col_pics_name, col_pets_name)
    if not mongo_check["status"]:
        return mongo_check["response"]

    # Falls alles in Ordnung ist, dann wird auf die DB und die Collections zugegriffen
    db = client[db_name]
    collection_pics = db[col_pics_name]
    collection_pets = db[col_pets_name]

    collection_pics.drop()
    collection_pets.drop()

    return make_response("alle collections gelöscht", 200)


@app.route("/mongo/all")
def mongo_show_all():
    package = mg.mongo_establish_connection_write()

    if package["code"] == 0:
        return package["response"]

    client = package["response"]

    #Überprüfung, ob die DB und die Collections existieren
    mongo_check = mg.mongo_check_all(client, db_name, col_pics_name, col_pets_name)
    if not mongo_check["status"]:
        return mongo_check["response"]

    # Falls alles in Ordnung ist, dann wird auf die DB und die Collections zugegriffen
    db = client[db_name]
    collection_pics = db[col_pics_name]
    collection_pets = db[col_pets_name]

    cursor = collection_pics.find()
    cursor2 = collection_pets.find()

    for document in cursor:
        print(document)
    for document in cursor2:
        print(document)

    return make_response("ok", 200)


@app.route("/mongo/telegram", methods=["POST"])
def mongo_telegram():
    data = request.get_json()
    asyncio.run(telebot.send_telegram_notification(data))
    return make_response(data)


if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)