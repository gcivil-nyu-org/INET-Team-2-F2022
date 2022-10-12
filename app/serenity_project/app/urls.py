
from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import ScoreTableViewSet

router = DefaultRouter()
router.register('api', ScoreTableViewSet)

urlpatterns = [
    path('', include(router.urls))
]