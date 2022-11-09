from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Driver


class FormsTests(TestCase):
    form_data = {
        "username": "new_user",
        # "password1": "user123test",
        # "password2": "user123test",
        "first_name": "Test first",
        "last_name": "Test last",
        "license_number": "QWE12345"
    }

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password12345"
        )
        self.client.force_login(self.user)

    def test_driver_creation_form_with_license_number_is_valid(self):

        form = DriverCreationForm(data=FormsTests.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, FormsTests.form_data)

    def test_update_license_number(self):

        driver = get_user_model().objects.create_user(**FormsTests.form_data)
        temp = {"license_number": "QNR12457"}
        self.client.post(reverse("taxi:driver-update", args=[driver.id]), temp)
        driver = get_user_model().objects.get(pk=driver.id)
        self.assertEqual(driver.license_number, temp["license_number"])
