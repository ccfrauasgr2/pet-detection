from rest_framework import serializers
from .models import Pic, Pet

class PicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pic
        fields = ['id', 'type', 'accuracy', 'date', 'time']

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'image', 'date', 'time', 'type', 'accuracy', 'bid']