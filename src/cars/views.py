from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import *
from .serializers import *
from .permissions import IsOwnerOrReadOnly

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsOwnerOrReadOnly]

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        car_id = self.kwargs.get('id')
        try:
            Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            raise NotFound(detail="No Car matches the given query.")
        return Comment.objects.filter(car=car_id)
    
    def perform_create(self, serializer):
        car_id = self.kwargs.get('id')
        try:
            Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            raise NotFound(detail="No Car matches the given query.")
        serializer.save(car=car_id)


def cars(request):
    cars = Car.objects.all().order_by('created_at')
    count = len(cars)
    return render(request, 'cars/cars.html', {'cars': cars, 'count': count})

def car(request, id):
    car = get_object_or_404(Car, id=id)
    comments = Comment.objects.filter(car=id).order_by('created_at')
    return render(request, 'cars/car.html', {'car': car, 'comments': comments})