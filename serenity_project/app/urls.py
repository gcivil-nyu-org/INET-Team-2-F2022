from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScoreTableViewSet
from . import views

router = DefaultRouter()
router.register("api", ScoreTableViewSet)

urlpatterns = [
    path("index/", views.index, name="index"),
    path("", include(router.urls)),
    path("index/search", views.search, name="search"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
]
