from django.urls import path

from .views import *

urlpatterns = [
    path('api/cars/', CarListCreateAPIView.as_view()),
    path('api/cars/<int:pk>/', CarRetrieveUpdateDestroyAPIView.as_view()),
]