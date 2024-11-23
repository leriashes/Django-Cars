from rest_framework import serializers
from .models import *

class CarSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Car
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    car = serializers.HiddenField(default=None)

    class Meta:
        model = Comment
        fields = '__all__'
