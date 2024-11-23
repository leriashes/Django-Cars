from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.exceptions import NotFound

from .models import *
from .serializers import *

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        car_id = self.kwargs.get('id')
        try:
            Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            raise NotFound(detail="No Car matches the given query.")
        return Comment.objects.filter(car=car_id)