
from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import ScoreTableViewSet
from . import views

router = DefaultRouter()
router.register('api', ScoreTableViewSet)

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', include(router.urls)),
    path('index/search', views.search,name='search')
]