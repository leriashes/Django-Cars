from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register(r'cars', CarViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/cars/<int:id>/comments/', CommentListCreateView.as_view())
]