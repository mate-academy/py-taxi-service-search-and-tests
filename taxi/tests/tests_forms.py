from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Driver


class FormsTests(TestCase):
    def test_driver_from(self):
        form_data = {
            "username": "username",
            "password1": "Password123",
            "password2": "Password123",
            "first_name": "firstname",
            "last_name": "lastname",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class PrivateAuthorTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_create_author(self):
        form_data = {
            "username": "testuser",
            "password1": "<PASSWORD>",
            "password2": "<PASSWORD>",
            "first_name": "test",
            "last_name": "test",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)

        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.first_name, "test")
        self.assertEqual(self.user.last_name, "test")
