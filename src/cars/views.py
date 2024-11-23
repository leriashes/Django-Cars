from django.shortcuts import render
from rest_framework import generics

from .models import *
from .serializers import *

class CarListCreateAPIView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
