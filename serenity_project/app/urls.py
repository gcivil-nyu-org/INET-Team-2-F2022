from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScoreTableViewSet
from . import views

## api router
api_router = DefaultRouter()
api_router.register("table", ScoreTableViewSet)

urlpatterns = [
    path("", views.index),
    path("api/", include(api_router.urls)),
    path("search", views.search, name="search"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
]