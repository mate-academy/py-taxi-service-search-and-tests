from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm


class TestForms(TestCase):
    def test_driver_creation_form_has_valid_data(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "first_name": "firstname",
            "last_name": "lastname",
            "license_number": "ASD12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
            first_name="firstname",
            last_name="lastname",
            license_number="ASD12345",
        )
        self.client.force_login(self.user)

    def test_driver_create_new_user(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword1234",
            "password2": "testpassword1234",
            "first_name": "firstname",
            "last_name": "lastname",
            "license_number": "ASD12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_driver_license_number_displayed_on_update_page(self):
        response = self.client.get(
            reverse("taxi:driver-update", args=[self.user.id])
        )
        self.assertContains(response, self.user.license_number)
