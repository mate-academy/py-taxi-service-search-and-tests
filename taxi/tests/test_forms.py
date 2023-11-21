from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.forms import DriverCreationForm
from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class FormsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(
            username="john11",
            first_name="John",
            last_name="Doe",
            password="111222John",
            license_number="ADM56984",
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_driver_form_with_valid_license(self):
        form_data = {
            "username": "user",
            "password1": "1122User",
            "password2": "1122User",
            "license_number": "BDM56984",
            "first_name": "User_name",
            "last_name": "User_last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_form_invalid_uppercase_license(self):
        form_data = {
            "username": "user",
            "password1": "1122User",
            "password2": "1122User",
            "license_number": "bdm56984",
            "first_name": "User_name",
            "last_name": "User_last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)

    def test_driver_form_invalid_length_license(self):
        form_data = {
            "username": "user",
            "password1": "1122User",
            "password2": "1122User",
            "license_number": "BDM56",
            "first_name": "User_name",
            "last_name": "User_last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)

    def test_driver_last_5_characters_license(self):
        form_data = {
            "username": "user",
            "password1": "1122User",
            "password2": "1122User",
            "license_number": "BDM125AS",
            "first_name": "User_name",
            "last_name": "User_last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)

    def test_driver_search_by_username(self):
        get_user_model().objects.create(
            username="drover1",
            password="1122drover1",
            license_number="BDM56984"
        )
        get_user_model().objects.create(
            username="driver2",
            password="1122driver2",
            license_number="CDM56984"
        )

        response = self.client.get(DRIVER_URL, {"username": "driver"})
        drivers = get_user_model().objects.filter(username__icontains="driver")
        self.assertEqual(list(response.context["driver_list"]), list(drivers))

    def test_manufacturer_search_by_name(self):
        Manufacturer.objects.create(name="MAN INC")
        Manufacturer.objects.create(name="Toyota INC")

        response = self.client.get(MANUFACTURER_URL, {"name": "MAN"})
        manufacturers = Manufacturer.objects.filter(name__icontains="MAN")
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )

    def test_car_search_by_model(self):
        manufacturer = Manufacturer.objects.create(name="MAN INC")
        Car.objects.create(model="BMW", manufacturer=manufacturer)
        Car.objects.create(model="Mercedes", manufacturer=manufacturer)

        response = self.client.get(CAR_URL, {"model": "BMW"})
        cars = Car.objects.filter(model__icontains="BMW")
        self.assertEqual(list(response.context["car_list"]), list(cars))
