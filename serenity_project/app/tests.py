from django.test import TestCase
from django.urls import reverse
from .models import ScoreTable
from django.contrib.auth.models import User
from .views import search
from unittest.mock import patch
import json
import requests
from django.http import HttpRequest

from django.test.client import RequestFactory
from django.core.handlers.wsgi import WSGIRequest
from .views import search


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

class TestForms(TestCase):
    def test_form_save(self):
        from .forms import NewUserForm
        form = NewUserForm()
        form.cleaned_data = {}
        form.cleaned_data['email'] = 'test_email'
        form.cleaned_data['password1'] = 'test_password'

        user = form.save(False)
        email = form.cleaned_data['email']
        assert email == user.email
    
    def test_meta(self):
        from .forms import NewUserForm
        from django.contrib.auth.models import User

        meta = NewUserForm.Meta()
        assert meta.model == User
        assert meta.fields == ("username", "email", "password1", "password2")

class TestViews(TestCase):

    def test_get_city_normalized_noise(self):
        from .views import _get_city_normalized_noise
        
        noise = _get_city_normalized_noise(
                1000, 
                1000, 
                1000, 
                1000, 
                1000)
        assert noise == 5 

    def test_get_city_grade_from_noise(self):
        from .views import _get_city_grade_from_noise
        
        assert _get_city_grade_from_noise(7) == 'G'
        assert _get_city_grade_from_noise(6) == 'F'
        assert _get_city_grade_from_noise(5) == 'E'
        assert _get_city_grade_from_noise(4) == 'D'
        assert _get_city_grade_from_noise(3) == 'C'
        assert _get_city_grade_from_noise(2) == 'B'
        assert _get_city_grade_from_noise(1) == 'A'
        assert _get_city_grade_from_noise(0) == 'A'
