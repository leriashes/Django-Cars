from django.shortcuts import render
from rest_framework import generics, viewsets

from .models import *
from .serializers import *

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
