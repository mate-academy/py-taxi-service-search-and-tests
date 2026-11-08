from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Manufacturer, Car, Driver


class SearchFormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Audi", country="Germany",
        )
        self.car = Car.objects.create(
            model="A6", manufacturer=self.manufacturer
        )
        self.driver = Driver.objects.create_user(
            username="test1",
            password="test12test",
            license_number="ABC12345"
        )

    def test_driver_search(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=test"
        )
        self.assertContains(response, "test")

    def test_car_search(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=A6")
        self.assertContains(response, "A6")

    def test_manufacturer_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Audi"
        )
        self.assertContains(response, "Audi")


class FormsTest(TestCase):
    def test_form_is_valid(self):
        form_data = {
            "username": "test",
            "license_number": "ABC12345",
            "first_name": "test",
            "last_name": "test",
            "password1": "user12test",
            "password2": "user12test",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

        cleaned = form.cleaned_data
        self.assertEqual(cleaned["username"], form_data["username"])
        self.assertEqual(cleaned["license_number"], form_data["license_number"])
        self.assertEqual(cleaned["first_name"], form_data["first_name"])
        self.assertEqual(cleaned["last_name"], form_data["last_name"])
