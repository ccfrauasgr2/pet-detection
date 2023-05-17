from django.http import JsonResponse
from .models import Pic, Pet
from .serializers import PicSerializer, PetSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def pet_camera_post(request, format=None):

    if request.method == 'POST':
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def pet_get_all(request, format=None):

    if request.method == 'GET':
        pets = Pet.objects.all()
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)


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
        return Response(status=status.HTTP_204_NO_CONTENT)