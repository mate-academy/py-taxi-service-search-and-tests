from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm


class FormTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_driver_creation_form_with_license_number_first_last_name(self):
        form_data = {
            "username": "new_user",
            "password1": "admin1234admin",
            "password2": "admin1234admin",
            "license_number": "ADD12345",
            "first_name": "test first",
            "last_name": "test last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_update_driver_license_number_with_valid_data(self):
        license_number = "ADS12345"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": license_number}
        )
        print(response.status_code)
        self.assertEqual(response.status_code, 302)

    def test_update_driver_license_number_with_non_valid_data(self):
        license_number = "ADS312345"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": license_number}
        )

        self.assertEqual(response.status_code, 200)
