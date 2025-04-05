from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Car, Comment
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carsproject.settings')

class CarAPITestCase(TestCase):
    def setUp(self):
        """Создаём тестовые объекты"""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client = APIClient()
        self.car = Car.objects.create(model="BMW", owner=self.user)
        self.comment = Comment.objects.create(car=self.car, author=self.user, content="Отличная машина!")

    def test_get_car_list(self):
        """Проверяем, что можно получить список машин"""
        response = self.client.get('/api/cars/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_car_authenticated(self):
        """Только аутентифицированный пользователь может создать машину"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.post('/api/cars/', {'name': 'Audi', 'owner': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_car_unauthenticated(self):
        """Неаутентифицированный пользователь не может создать машину"""
        response = self.client.post('/api/cars/', {'name': 'Audi'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_car_detail(self):
        """Можно получить конкретную машину"""
        response = self.client.get(f'/api/cars/{self.car.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_comment_authenticated(self):
        """Аутентифицированный пользователь может оставить комментарий"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(f'/api/cars/{self.car.id}/comments/', {'text': 'Неплохая тачка!'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_comment_unauthenticated(self):
        """Неаутентифицированный пользователь не может оставить комментарий"""
        response = self.client.post(f'/api/cars/{self.car.id}/comments/', {'text': 'Крутая машина!'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
