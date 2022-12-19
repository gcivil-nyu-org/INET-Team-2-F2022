from django.test import TestCase
from django.urls import reverse
from .models import ScoreTable, ForumPost, Profile
from .serializers import ScoreTableSerializer
from django.contrib.auth.models import User
from .views import find,get_others,search,get_info
from unittest.mock import patch
import json
import requests
from django.http import HttpRequest

from django.test.client import RequestFactory
from django.core.handlers.wsgi import WSGIRequest
from http import HTTPStatus
import unittest.mock as mock
import numpy as np


from django.test import Client


class AppViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            "john", "lennon@thebeatles.com", "johnpassword"
        )
        self.profile = Profile.objects.create(user=self.user)
    
    def test_profile_model(self):
        user = User.objects.create_user(
            username='testuser', password='testpass'
         )
        profile = Profile.objects.create(
            user=user, bio='Test bio'
        )
        self.assertEqual(Profile.objects.count(), 2)
        self.assertEqual(str(Profile.objects.first()), "john")
        self.assertEqual(str(profile), 'testuser')
        with mock.patch.object(Profile, 'save') as mock_save:
            profile.save()
            mock_save.assert_called_once()

    def test_home_endpoint_returns_welcome_page(self):
        response = self.client.get(path="/")
        assert response.status_code == 200
        self.assertTemplateUsed(response, "app/index.html")

    def test_about_page(self):
        response = self.client.get(path="/about/")
        assert response.status_code == 200
        self.assertTemplateUsed(response, "app/about.html")

    def test_register_page(self):
        response = self.client.get(path="/register")
        assert response.status_code == 200
        self.assertTemplateUsed(response, "app/register.html")

    def test_login_page(self):
        response = self.client.get(path="/login")
        assert response.status_code == 200
        self.assertTemplateUsed(response, "app/login.html")

    def test_index_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/index.html")

    @patch("requests.post")
    def test_get_info(self,re1):
        req=HttpRequest()
        response = get_info(req)
        self.assertEqual(response.status_code, 200)


    def test_forum_index(self):
        response = self.client.get(path="/forumPosts/")
        assert response.status_code == 200
        self.assertTemplateUsed(response, "app/forum_home.html")

    def test_forum_zipcode(self):
        response = self.client.get(path="forumPosts/11216")
        self.assertEqual(response.status_code, 404)

    def test_add_forum_post(self):
        response = self.client.get(path="/addInForumPost/")
        assert response.status_code == 302

    def test_add_forum_post_login(self):
        self.client.login(username="john", password="johnpassword")
        response = self.client.get(path="/addInForumPost/")
        assert response.status_code == 200

    def test_add_forum_comment(self):
        response = self.client.get(path="/addInComment/")
        assert response.status_code == 302

    def test_add_forum_post_login(self):
        self.client.login(username="john", password="johnpassword")
        response = self.client.get(path="/addInComment/")
        assert response.status_code == 200

    def test_profile_view(self):
        self.client.login(username="john", password="johnpassword")
        response = self.client.get(path="/users/profile/")
        self.assertTemplateUsed(response, "app/users/profile.html")
        assert response.status_code == 200


class TestSearch(TestCase):
    def setUp(self):

        ScoreTable.objects.create(
            id=1,
            zipcode=11220,
            residentialNoise=1,
            dirtyConditions=2,
            sanitationCondition=3,
            wasteDisposal=4,
            unsanitaryCondition=5,
            constructionImpact=1.0,
            userAvg=1,
            treeCensus=1,
            parkCount=1,
        )

    def testZipResults(self):
        testZip = ScoreTable.objects.get(zipcode=11220)
        self.assertEqual(testZip.residentialNoise, 1)
        self.assertEqual(testZip.zipcode, 11220)
        self.assertEqual(testZip.dirtyConditions, 2)


class ForumSearch(TestCase):
    def setUp(self):

        ScoreTable.objects.create(
            id=1,
            zipcode=11220,
            residentialNoise=1,
            dirtyConditions=2,
            sanitationCondition=3,
            wasteDisposal=4,
            unsanitaryCondition=5,
            constructionImpact=1.0,
            treeCensus=1,
            parkCount=1,
        )

    def testZipResults(self):
        object = ScoreTable.objects.get(zipcode=11220)
        testPost = ForumPost.objects.create(
            id=1,
            zipcode=object,
            name="test",
            email="testemail@gmail.com",
            topic="test topic",
            description="test description",
            date_created="null",
        )
        self.assertEqual(testPost.id, 1)
        self.assertEqual(testPost.zipcode.zipcode, 11220)


class TestLogin(TestCase):
    def test_login(self):
        user = User.objects.create(username="testuser")
        user.set_password("12345")
        user.save()
        c = Client()
        logged_in = c.login(username="testuser", password="12345")
        assert logged_in == True


class SignUpPageTests(TestCase):
    def setUp(self) -> None:
        self.username = "testuser"
        self.email = "testuser@email.com"
        self.password = "password"

    def test_signup_page_url(self):
        response = self.client.get("/register")
        self.assertEqual(response.status_code, 200)

    def test_signup_form(self):
        response = self.client.post(
            reverse("register"),
            data={
                "username": self.username,
                "email": self.email,
                "password1": self.password,
                "password2": self.password,
            },
        )

        self.assertEqual(response.status_code, 200)


class TestIndexView(TestCase):
    @patch("requests.post")
    def test_post(self, mock_post):
        info = {"searched": 11220}
        requests.post(
            "/", data=json.dumps(info), headers={"Content-Type": "application/json"}
        )
        mock_post.assert_called_with(
            "/",
            data=json.dumps(info),
            headers={"Content-Type": "application/json"},
        )


class testSearchView(TestCase):
    def setUp(self) -> None:
        ScoreTable.objects.create(
            id=1,
            zipcode=11220,
            residentialNoise=1,
            dirtyConditions=2,
            sanitationCondition=3,
            wasteDisposal=4,
            unsanitaryCondition=5,
            borough="Brooklyn",
            constructionImpact=1.0,
            treeCensus=1,
            parkCount=1,
        )

    @patch("requests.post")
    def test_postsearch(self, mock_post):
        req = HttpRequest()
        req.method = "POST"
        req.POST = {"searched": 11220}
        response = search(req, True)
        assert response.status_code == 200

    @patch("requests.post")
    def test_postfind(self, mock_post):
        req = HttpRequest()
        req.method = "POST"
        req.POST = {"find": 11220}
        response = find(req)
        assert response.status_code == 302


class TestForumZip(TestCase):
    def setUp(self) -> None:
        ScoreTable.objects.create(
            id=1,
            zipcode=11220,
            residentialNoise=1,
            dirtyConditions=2,
            sanitationCondition=3,
            wasteDisposal=4,
            unsanitaryCondition=5,
            constructionImpact=1.0,
            treeCensus=1,
            parkCount=1,
        )

        object = ScoreTable.objects.get(zipcode=11220)

        ForumPost.objects.create(
            id=1,
            zipcode=object,
            name="test",
            email="testemail@gmail.com",
            topic="test topic",
            description="test description",
            date_created="null",
        )

    @patch("requests.post")
    def test_forumzip(self, mock_post):
        from .views import forum_home

        req = HttpRequest()
        req.method = "POST"
        req.POST = {"searched": 11220}
        response = forum_home(req)
        assert response.status_code == 200

    @patch("requests.post")
    def test_zip_posts(self, mock_post):
        from .views import forum_zipcode

        req = HttpRequest()
        req.method = "POST"
        req.POST = {"searched": 11220}
        response = forum_zipcode(req, "11220")
        self.assertEqual(response.status_code, 200)


class TestForms(TestCase):
    def test_form_save(self):
        from .forms import NewUserForm

        form = NewUserForm()
        form.cleaned_data = {}
        form.cleaned_data["email"] = "test_email"
        form.cleaned_data["password1"] = "test_password"

        user = form.save(False)

        email = form.cleaned_data["email"]
        assert email == user.email

    def test_meta(self):
        from .forms import NewUserForm
        from django.contrib.auth.models import User

        meta = NewUserForm.Meta()
        assert meta.model == User
        assert meta.fields == ("username", "email", "password1", "password2")

    def test_user_update(self):
        from .forms import UpdateUserForm, NewUserForm

        form2 = UpdateUserForm()

        form2.cleaned_data = {}
        form2.cleaned_data["username"] = "test_user"
        form2.cleaned_data["email"] = "new@email.com"

        email = form2.cleaned_data["email"]
        username = form2.cleaned_data["username"]
        assert email == "new@email.com"
        assert username == "test_user"

    def test_profile_update(self):
        from .forms import UpdateProfileForm

        form = UpdateProfileForm

        form.cleaned_data = {}
        form.cleaned_data["bio"] = "blah"
        form.cleaned_data["avatar"] = "test.jpg"

        bio = form.cleaned_data["bio"]
        avatar = form.cleaned_data["avatar"]
        assert bio == "blah"
        assert avatar == "test.jpg"


class TestViews(TestCase):
    def test_get_grade_from_score(self):
        from .views import _get_grade_from_score

        assert _get_grade_from_score(95) == "F"
        assert _get_grade_from_score(77) == "E"
        assert _get_grade_from_score(69) == "D"
        assert _get_grade_from_score(50) == "C"
        assert _get_grade_from_score(25) == "B"
        assert _get_grade_from_score(9) == "A"

    def test_update_user_rating(self):
        from .views import update_user_rating

        assert update_user_rating(100, "A") == 107.5
        assert update_user_rating(100, "B") == 125
        assert update_user_rating(100, "C") == 150
        assert update_user_rating(100, "D") == 167.5
        assert update_user_rating(100, "E") == 182.5
        assert update_user_rating(100, "F") == 195
        # assert update_user_rating(100, "G") == 100.7


class ForumPostTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            "john", "lennon@thebeatles.com", "johnpassword"
        )
        ScoreTable.objects.create(
            id=2,
            zipcode=11220,
            residentialNoise=1,
            dirtyConditions=2,
            sanitationCondition=3,
            wasteDisposal=4,
            unsanitaryCondition=5,
            constructionImpact=1.0,
            treeCensus=1,
            parkCount=1,
        )

    def testaddForumPost(self):
        self.client.login(username="john", password="johnpassword")
        response = self.client.post(
            "/addInForumPost/",
            data={
                "id": 1,
                "curzip": 11220,
                "topic": "test topic",
                "description": "test description",
                "date_created": "2021-05-05",
            },
        )
        self.assertEqual(response.status_code, 200)

    def testaddForumComment(self):
        self.client.login(username="john", password="johnpassword")
        response = self.client.post(
            "/addInComment/",
            data={"id": 1, "forumPost": 2, "discuss": "test discussion"},
        )
        self.assertEqual(response.status_code, 200)

    @patch("requests.post")
    def test_get_others(self,mock_post):
        self.user = User.objects.create_user(
            "john1", "lennon@thebeatles.com", "johnpassword1"
        )
        Profile.objects.create(
            user=self.user, bio='Test bio'
        )
        username="john1";
        self.client.login( username="john1", password="johnpassword1")
        
        self.client.post(
            "/addInForumPost/",
            data={
                "id": 1,
                "curzip": 11220,
                "topic": "test topic",
                "description": "test description",
                "date_created": "2021-05-05",
            },
        )
        req=HttpRequest()
        response=get_others(req,username)
        self.assertEquals(response.status_code, 200)
        response=get_others(req,"Invalid_User")
        self.assertEquals(response.status_code, 404)


class TestCalculateScore(TestCase):
    def setUp(self) -> None:
        ScoreTable.objects.create(
            id=1,
            zipcode=00000,
            residentialNoise=1,
            dirtyConditions=2,
            sanitationCondition=3,
            wasteDisposal=4,
            unsanitaryCondition=5,
            constructionImpact=1.0,
            userAvg=0.1,
            treeCensus=1,
            parkCount=1,
        )

    def test_calculate(self):
        from .views import calculate_factor

        object = ScoreTable.objects.get(zipcode=00000)
        result = calculate_factor(object.zipcode)
        self.assertEqual(
            result,
            (
                100.04,
                [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
            ),
        )
