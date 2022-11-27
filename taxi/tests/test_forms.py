from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Manufacturer, Car


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_first_last_name_is_valid(self):
        form_data = {
            "username": "test",
            "password1": "test1234test",
            "password2": "test1234test",
            "license_number": "AAA00000",
            "first_name": "Test",
            "last_name": "Testson"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class SearchFormsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_driver",
            password="driver1234",
            license_number="AAA00000"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Manufacturer_Test",
            country="Country_1"
        )
        self.car = Car.objects.create(
            model="Test1",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.user)

    def test_manufacturer_search_form_by_name(self):
        search_data = {"name": "Manufacturer_Test"}
        res = self.client.get(
            path=reverse("taxi:manufacturer-list"),
            data=search_data
        )

        self.assertContains(res, search_data["name"])

    def test_car_search_form_by_model(self):
        search_data = {"model": "Test1"}
        res = self.client.get(
            path=reverse("taxi:car-list"),
            data=search_data
        )

        self.assertContains(res, search_data["model"])

    def test_driver_search_form_by_username(self):
        search_data = {"username": "test_driver"}
        res = self.client.get(
            path=reverse("taxi:driver-list"),
            data=search_data
        )

        self.assertContains(res, search_data["username"])
