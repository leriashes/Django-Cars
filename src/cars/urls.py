from django.urls import path, include
from rest_framework import routers
from cars import views

router = routers.SimpleRouter()
router.register(r'cars', views.CarViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/cars/<int:id>/comments/', views.CommentListCreateView.as_view()),

    path('logout', views.LogoutUser, name="logout"),

    path('', views.index, name="index"),
    path('cars/', views.cars, name='cars_all'),
    path('cars/<int:id>/', views.car, name='car_detail'),
]