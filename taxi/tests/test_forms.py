from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "test_user",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TST12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="john",
            first_name="John",
            last_name="Doe",
            license_number="ABC12334"
        )
        get_user_model().objects.create_user(
            username="jane",
            first_name="Jane",
            last_name="Smith",
            license_number="XYZ78922"
        )
        get_user_model().objects.create_user(
            username="bob",
            first_name="Bob",
            last_name="Johnson",
            license_number="DEF45612"
        )
        self.client.force_login(user=self.user)

    def test_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john")
        self.assertNotContains(response, "Jane Smith")
        self.assertNotContains(response, "Bob Johnson")
