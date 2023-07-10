import os
from pymongo import MongoClient
from flask import make_response


def mongo_connect_read():
    # Retrieve the environment variables
    user_name = os.environ['MONGO_INITDB_ROOT_USERNAME']
    user_pwd = os.environ['MONGO_INITDB_ROOT_PASSWORD']
    mongo_initdb_config = os.environ['MONGO_INITDB_CONFIG']

    # Construct the MongoDB connection string
    mongo_connection_string = f"mongodb://{user_name}:{user_pwd}@{mongo_initdb_config}"

    # Verbindung zur MongoDB herstellen
    try:
        client = MongoClient(mongo_connection_string)
        return client
    except:
        return 0


def mongo_connect_write():
    client = mongo_connect_read()
    if client == 0:
        return 0
    else:
        try:
            host, port = client.primary
            mongo_connection_string_new = f"mongodb://{host}.mongo-headless-svc.default.svc.cluster.local:{port}"
            client.close()
            headless_client = MongoClient(mongo_connection_string_new)
            return headless_client
        except:
            return 1


def mongo_establish_connection_write():
    response = mongo_connect_write()
    if response == 0:
        msg = "Verbindung zum Mongo_Read_Service konnte nicht hergestellt werden."
        package = {
            "code": 0,
            "response": make_response(msg, 503)
        }
        return package
    elif response == 1:
        msg = "Verbindung zum Mongo_Headless_Service konnte nicht hergestellt werden."
        package = {
            "code": 0,
            "response": make_response(msg, 503)
        }
        return package
    else:
        package = {
            "code": 1,
            "response": response    # Rückgabe des Headless_Clients
        }
        return package


def mongo_db_check(client, name):
    dblist = client.list_database_names()
    if name in dblist:
        return True
    else:
        return False


def mongo_coll_check(db, name):
    collist = db.list_collection_names()
    if name in collist:
        return True
    else:
        return False


def mongo_check_all(headless_client, db_name, col_pics_name, col_pets_name):
    # Überprüfung, ob die DB "pet_detection" existiert
    if not mongo_db_check(headless_client, db_name):
        response = {
            "status": False,
            "response": make_response("DB 'pet_detection' nicht angelegt.", 404)
        }
        return response

    # Zugriff auf DB, wenn sie existiert
    db = headless_client[db_name]

    # Überprüfung, ob die Collections "pics" und "pets" exstieren
    if not mongo_coll_check(db, col_pics_name):
        response = {
            "status": False,
            "response": make_response("Collection 'pets' nicht angelegt.", 404)
        }
        return response

    if not mongo_coll_check(db, col_pets_name):
        response = {
            "status": False,
            "response": make_response("Collection 'pets' nicht angelegt.", 404)
        }
        return response

    response = {
        "status": True
    }
    return response
