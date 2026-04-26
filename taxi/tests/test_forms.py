from django.test import TestCase
from django.urls import reverse

from django.contrib.auth import get_user_model
from taxi.forms import (
    CarSearchForm,
    DriverSearchForm,
    ManufacturerSearchForm
)

User = get_user_model()


class FormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="test12345"
        )

    def test_login(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "test",
                "password": "test12345"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        self.client.login(username="test", password="test12345")
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/")
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_car_search_form(self):
        form = CarSearchForm(data={"model": "Tesla"})
        self.assertTrue(form.is_valid())

    def test_driver_search_form(self):
        form = DriverSearchForm(data={"username": "john"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"name": "BMW"})
        self.assertTrue(form.is_valid())
