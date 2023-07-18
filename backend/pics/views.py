from .models import Pic, Pet
from .serializers import PicSerializer, PetSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Max
import json
import zlib
from pymongo import MongoClient
import os


"""
Temporäre Funktionen, die auf die SQLite3 DB zugreifen bis die MongoDB für weitere Zwecke steht.
Die Funktionen für den Zugriff auf die MongoDB sind weiter unten zu finden.
"""


@api_view(['POST'])
def pet_camera_post(request, format=None):

    if request.method == 'POST':
        serializers = []
        pic = {
            "picture": request.data['picture'], #zlib.decompress(request.data['picture']).decode()
            "date": request.data['date'],
            "time": request.data['time']
        }
        picSerializer = PicSerializer(data=pic)
        if picSerializer.is_valid():
            picSerializer.save()
        else:
            return Response(picSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        for item in request.data['detections']:
            pet = {
                "type": item['type'],
                "accuracy": item['accuracy'],
                "bid": item['bid'],
                "foreignKey": Pic.objects.aggregate(max_id=Max('id'))['max_id']
            }
            print(pet)
            petSerializer = PetSerializer(data=pet)
            if petSerializer.is_valid():
                serializers.append(petSerializer)
            else:
                print("Fehler")
                print(petSerializer.errors)
                latest_entry = Pic.objects.latest('id')
                latest_entry.delete
                return Response(petSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        for item in serializers:
            item.save()

        return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
def pet_get_images(request, format=None):
    if request.method == 'GET':
        pics = get_query_images(0)
        if pics == 0:
            return Response(data="no images found", status=status.HTTP_400_BAD_REQUEST)
        else:
            json_string = get_query_pets(pics)
            return Response(data=json_string, status=status.HTTP_200_OK)


@api_view(['GET'])
def pet_check_for_new_images(request, format=None):
    if request.method == 'GET':
        pics = get_query_images(request.data['last_id'])
        if pics == 0:
            return Response(data="no images found", status=status.HTTP_400_BAD_REQUEST)
        else:
            json_string = get_query_pets(pics)
            return Response(data=json_string, status=status.HTTP_200_OK)


def get_query_images(last_element_id):
    if Pic.objects.exists() and last_element_id < Pic.objects.latest('id').id:
        queryset = Pic.objects.filter(id__gt=last_element_id)
        remaining_count = queryset.count()
        if remaining_count < 10:
            images = queryset[:remaining_count]
        else:
            images = queryset[:10]
        return images
    else:
        return 0


def get_query_pets(pics):
    data_entries = []
    for pic in pics:
        pets = Pet.objects.filter(foreignKey=pic.id).values()
        pets_list = list(pets)
        data = {
            'picture': pic.picture,
            'date': pic.date,
            'time': pic.time,
            'detections': pets_list
        }
        data_entries.append(data)
    json_data = {
        'list': data_entries
    }
    json_string = json.dumps(json_data)
    return json_string

"""
Funktionen zum Zugriff auf MongoDB
Eine Erklärung der Funktionsweise der Methoden ist der Dokumentation zu entnehmen.
"""
db_name = "pet_detection"
col_pics_name = "pics"
col_pets_name = "pets"


@api_view(['GET'])
def mongo_test(request, format=None):
    if request.method == 'GET':
        return Response(data="Test erfolgreich!", status=status.HTTP_200_OK)
    else:
        return Response(data="Request Method muss 'GET' sein", status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def mongo_new_db(request, format=None):
    if request.method == 'POST':
        package = mongo_establish_connection_write()

        if package["code"] == 0:
            return package["response"]

        """
        if code != 0, dann bedeutet das, dass die Verbindung herrgestellt werden konnte
        'response' ist dann kein Response-Objekt, sondern der headless-client
        """
        headless_client = package["response"]

        # Datenbank erstellen
        db = headless_client[request.data["name"]]

        # Collections erstellen
        db["pics"]
        db["pets"]

        return Response(data="DB & Coll. erfolgreich erstellt!", status=status.HTTP_201_CREATED)


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
            "response": Response(data=msg, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        }
        return package
    elif response == 1:
        msg = "Verbindung zum Mongo_Headless_Service konnte nicht hergestellt werden."
        package = {
            "code": 0,
            "response": Response(data=msg, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        }
        return package
    else:
        package = {
            "code": 1,
            "response": response    # Rückgabe des Headless_Clients
        }
        return package


@api_view(['POST'])
def mongo_camera_post(request, format=None):
    if request.method == 'POST':
        package = mongo_establish_connection_write()

        if package["code"] == 0:
            return package["response"]

        """
        if code != 0, dann bedeutet das, dass die Verbindung herrgestellt werden konnte
        'response' ist dann kein Response-Objekt, sondern der headless-client
        """
        headless_client = package["response"]

        #Überprüfung, ob die DB und die Collections existieren
        mongo_check = mongo_check_all(headless_client)
        if not mongo_check["status"]:
            return mongo_check["response"]

        # Falls alles in Ordnung ist, dann wird auf die DB und die Collections zugegriffen
        db = headless_client[db_name]
        collection_pics = db[col_pics_name]
        collection_pets = db["pets"]

        # Die höchste bekannte ID aus der collection entnehmen und + 1 rechnen
        unique_id = 1
        unique_id = id + db.collection_pics.find({}, {"_id": 1}).sort({"_id": -1}).limit(1).pretty()

        pic = {
            "_id": unique_id,    # unique identifier
            "picture": request.data['picture'],  # zlib.decompress(request.data['picture']).decode()
            "date": request.data['date'],
            "time": request.data['time']
        }

        # Abspeichern des Bildes
        try:
            collection_pics.insert_one(json.dumps(pic))
        except:
            return Response(data="pic konnte nicht gespeichert werden", status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # Pet bauen und abspeichern
        for item in request.data['detections']:
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
                return Response(data="pet konnte nicht gespeichert werden", status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(data="Erfolg", status=status.HTTP_201_CREATED)


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


def mongo_check_all(headless_client):
    # Überprüfung, ob die DB "pet_detection" existiert
    if not mongo_db_check(headless_client, db_name):
        response = {
            "status": False,
            "response": Response(data="DB 'pet_detection' nicht angelegt.", status=status.HTTP_404_NOT_FOUND)
        }
        return response

    # Zugriff auf DB, wenn sie existiert
    db = headless_client[db_name]

    # Überprüfung, ob die Collections "pics" und "pets" exstieren
    if not mongo_coll_check(db, col_pics_name):
        response = {
            "status": False,
            "response": Response(data="Collection 'pets' nicht angelegt.", status=status.HTTP_404_NOT_FOUND)
        }
        return response

    if not mongo_coll_check(db, col_pets_name):
        response = {
            "status": False,
            "response": Response(data="Collection 'pets' nicht angelegt.", status=status.HTTP_404_NOT_FOUND)
        }
        return response

    response = {
        "status": True
    }
    return response

"""
@api_view(['GET'])
def pets_get_all(request, format=None):

    if request.method == 'GET':
        pets = Pet.objects.all()
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def pics_get_all(request, format=None):

    if request.method == 'GET':
        pics = Pic.objects.all()
        serializer = PicSerializer(pics, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def pics_get_all_until_id(request, format=None):

    if request.method == 'GET':
        pics = Pic.objects.filter(id__lte=request.data['id'])
        serializer = PicSerializer(pics, many=True)
        return Response(serializer.data)

@api_view(['GET'])

@api_view(['GET', 'POST'])
def pic_list(request, format=None):

    if request.method == 'GET':
        pics = Pic.objects.all()
        serializer = PicSerializer(pics, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def pic_detail(request, id, format=None):
    try:
        pic = Pic.objects.get(pk=id)
    except Pic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PicSerializer(pic)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PicSerializer(pic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        pic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)"""
