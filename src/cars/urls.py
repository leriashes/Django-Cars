from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework import routers
from cars import views

router = routers.SimpleRouter()
router.register(r'cars', views.CarViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/cars/<int:id>/comments/', views.CommentListCreateView.as_view()),

    path('login/', views.LoginUser, name="login"),
    path('logout/', views.LogoutUser, name="logout"),
    path('registration/', views.RegisterUser, name="registration"),

    path('', views.index, name="index"),
    path('cars/', views.cars, name='cars_all'),
    path('cars/<int:id>/', views.car, name='car_detail'),
    path('cars/<int:id>/edit/', views.car_edit, name='car_edit'),
    path('cars/new/', views.car_create, name='car_create'),

    path('<str:username>/', views.user, name='user_page'),
]