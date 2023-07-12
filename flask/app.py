import asyncio

from flask import Flask, render_template, make_response, jsonify, request
from pymongo import MongoClient
import mongo as mg
import zlib
import json
import telebot

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

"""
Funktionen zum Zugriff auf MongoDB
Eine Erklärung der Funktionsweise der Methoden ist der Dokumentation zu entnehmen.
"""
db_name = "pet_detection"
col_pics_name = "pics"
col_pets_name = "pets"


@app.route("/mongo/test")
def mongo_test():
    return make_response("Success", 200)


@app.route("/mongo/new_db", methods=["POST"])
def mongo_new_db():
    try:
        data = request.get_json()
        """
        package = mg.mongo_establish_connection_write()

        if package["code"] == 0 or package["code"] == 1:
            return package["response"]

        """
        """
        if code != 0 or 1, dann bedeutet das, dass die Verbindung herrgestellt werden konnte
        'response' ist dann kein make_response-Objekt, sondern der headless-client
        """
        """
        headless_client = package["response"]

        # Datenbank erstellen
        db = headless_client[data["name"]]

        # Collections erstellen
        db["pics"]
        db["pets"]
        """
        return make_response("DB & Coll. erfolgreich erstellt!", 201)
    except Exception as error:
        return make_response(str(error), 503)

@app.route("/mongo/db", methods=["POST"])
def mongo_db():
    data = request.get_json()

    package = mg.mongo_establish_connection_write()

    if package["code"] == 0:
        return package["response"]

    client = package["response"]

    """
    # Datenbank erstellen
    db = headless_client[data["name"]]

    # Collections erstellen
    db["pics"]
    db["pets"]
    """
    host = "jo"
    host, port = client.primary
    #address = host.address
    print(host)
    #print(str(host))
    response = make_response(str(host), 201)

    return response

@app.route("/mongo/input", methods=["POST"])
def mongo_camera_post():
    data = zlib.decompress(request.get_json()).decode()
    package = mg.mongo_establish_connection_write()

    if package["code"] == 0 or package["code"] == 1:
        return package["response"]

    """
    if code != 0 or 1, dann bedeutet das, dass die Verbindung herrgestellt werden konnte
    'response' ist dann kein make_response-Objekt, sondern der headless-client
    """
    headless_client = package["response"]

    #Überprüfung, ob die DB und die Collections existieren
    mongo_check = mg.mongo_check_all(headless_client)
    if not mongo_check["status"]:
        return mongo_check["response"]

    # Falls alles in Ordnung ist, dann wird auf die DB und die Collections zugegriffen
    db = headless_client[db_name]
    collection_pics = db[col_pics_name]
    collection_pets = db[col_pets_name]

    # Die höchste bekannte ID aus der collection entnehmen und + 1 rechnen
    unique_id = 1 + db.collection_pics.find({}, {"_id": 1}).sort({"_id": -1}).limit(1).pretty()

    pic = {
        "_id": unique_id,    # unique identifier
        "picture": data['picture'],  # zlib.decompress(request.data['picture']).decode()
        "date": data['date'],
        "time": data['time']
    }

    # Abspeichern des Bildes
    try:
        collection_pics.insert_one(json.dumps(pic))
    except:
        return make_response("pic konnte nicht gespeichert werden", 503)

    # Pet bauen und abspeichern
    for item in data['detections']:
        unique_pet_id = 1
        unique_pet_id = unique_pet_id + db.collection_pets.find({}, {"_id": 1}).sort({"_id": -1}).limit(1).pretty()

        pet = {
            "_id": unique_pet_id,
            "type": item['type'],
            "accuracy": item['accuracy'],
            "bid": item['bid'],
            "foreignKey": unique_id
        }

        try:
            collection_pets.insert_one(json.dumps(pet))
        except:
            return make_response("pet konnte nicht gespeichert werden", 503)

    asyncio.run(telebot.send_telegram_notification(data))
    return make_response("Erfolg", 201)


if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)