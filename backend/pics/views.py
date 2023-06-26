from .models import Pic, Pet
from .serializers import PicSerializer, PetSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Max
import json
import zlib
from pymongo import MongoClient

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
@api_view(['POST'])
def mongo_new_db(request, format=None):
    if request.method == 'POST':
        
        return 0
"""
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
