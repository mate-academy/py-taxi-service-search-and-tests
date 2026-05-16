from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverUsernameSearchForm
from taxi.models import Driver, Car, Manufacturer


class FormsCreateTest(TestCase):

    def test_forms_driver_create(self):
        form_data = {
            "username": "test_username",
            "password1": "1qazcdE3",
            "password2": "1qazcdE3",
            "license_number": "TES12345",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_validate_license_number(self):
        form_data = {
            "username": "test_username",
            "password1": "1qazcdE3",
            "password2": "1qazcdE3",
            "license_number": "TES12345",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data["license_number"] = "TES1234"
        form_short_len_license_number = DriverCreationForm(data=form_data)
        self.assertFalse(form_short_len_license_number.is_valid())

        form_data["license_number"] = "TES12Y45"
        form_with_letter = DriverCreationForm(data=form_data)
        self.assertFalse(form_with_letter.is_valid())

        form_data["license_number"] = "TEs12345"
        form_with_letter_lower = DriverCreationForm(data=form_data)
        self.assertFalse(form_with_letter_lower.is_valid())

        form_data["license_number"] = "1ES12345"
        form_with_number = DriverCreationForm(data=form_data)
        self.assertFalse(form_with_number.is_valid())


class TestFormsSearch(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD123>",
        )
        self.client.force_login(self.user)

    def test_forms_search_driver(self):
        form_data = {
            "username": "a",
        }
        driver = Driver.objects.filter(username__icontains="a")
        response = self.client.get(reverse("taxi:driver-list"), form_data)
        self.assertEqual(list(response.context_data["driver_list"]) ,
                         list(driver)[:5])

    def test_forms_search_car(self):
        form_data = {
            "model": "ford",
        }
        car = Car.objects.filter(model__icontains="ford")
        response = self.client.get(reverse("taxi:car-list"), form_data)
        self.assertEqual(list(response.context_data["car_list"]) ,
                         list(car)[:5])

    def test_forms_search_manufacturer(self):
        form_data = {
            "name": "ford",
        }
        manufacturer = Manufacturer.objects.filter(name__icontains="ford")
        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   form_data)
        self.assertEqual(list(response.context_data["manufacturer_list"]) ,
                         list(manufacturer)[:5])
