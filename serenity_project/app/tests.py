from django.test import TestCase
from django.urls import reverse
from .models import ScoreTable
from django.contrib.auth.models import User


from django.test import Client


class AppViewTests(TestCase):
    def test_home_endpoint_returns_welcome_page(self):
        response = self.client.get(path="/")
        assert response.status_code == 200

    def test_register_page(self):
        response = self.client.get(path="/register")
        assert response.status_code == 200

    def test_login_page(self):
        response = self.client.get(path="/login")
        assert response.status_code == 200


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
