from django.test import TestCase
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.models import User
from app.models import ScoreTable
from app.views import search
from unittest.mock import patch
import json
import requests



from django.test import Client


class AppViewTests(TestCase):
    def test_home_endpoint_returns_welcome_page(self):
        response = self.client.get(path="/")
        assert response.status_code == 200
        self.assertTemplateUsed(response, "app/index.html")

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
        )

    def testZipResults(self):
        testZip = ScoreTable.objects.get(zipcode=11220)
        self.assertEqual(testZip.residentialNoise, 1)
        self.assertEqual(testZip.zipcode, 11220)


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
        )

    @patch("requests.post")
    def test_postsearch(self, mock_post):
        req = HttpRequest()
        req.method = "POST"
        req.POST = {"searched": 11220}
        response = search(req)
        assert response.status_code == 200
