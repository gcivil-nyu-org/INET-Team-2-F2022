from django.test import TestCase

from .models import ScoreTable


class AppViewTests(TestCase):
    def test_home_endpoint_returns_welcome_page(self):
        response = self.client.get(path="/")
        assert response.status_code == 200
