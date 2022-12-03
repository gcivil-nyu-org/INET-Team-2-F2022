from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScoreTableViewSet
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import logout

# from django.conf.urls import patterns,url
from . import views

# api router
api_router = DefaultRouter()
api_router.register("table", ScoreTableViewSet)

urlpatterns = [
    path("", views.index, name="home"),
    path("api/", include(api_router.urls)),
    path("search", views.search, name="search"),
    path("find", views.find, name="find"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logoutUser, name="logout"),
    path("rate/", views.submit_rating, name="rate"),
    path("thanks/", views.get_rating, name="thanks"),
    path("forumPosts/", views.forum_home, name="forum_home"),
    path("forumPosts/<borough>/", views.forum_borough, name="forum_borough"),  # burough
    path(
        "forumPosts/zipcode/<pk>/", views.forum_zipcode, name="forum_zipcode"
    ),  # zipcode
    path("forumPosts/zipcode/<pk>/<id>/", views.forum_post, name="forum_post"),  # post
    path("addInForumPost/", views.addInForumPost, name="addInForumPost"),
    path("addInComment/", views.addInComment, name="addInComment"),
    path("about/", views.get_info, name="about"),
    path("users/profile/", views.profile, name="profile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "app.views.page_not_found_view"
handler500 = "app.views.internal_error_view"
