from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, validate_license_number
from taxi.models import Driver, Manufacturer, Car


class FormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="test_user",
            password="1357Test_password"
        )
        self.client.force_login(self.user)

    def test_driver_search(self):
        Driver.objects.create(
            username="test_driver1",
            password="1357Test_password",
            license_number="QWE45678"
        )
        Driver.objects.create(
            username="test_driver2",
            password="1357Test_password",
            license_number="ASD45678"
        )
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "driver"})
        drivers = Driver.objects.filter(username__icontains="driver")
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_manufacturer_search(self):
        Manufacturer.objects.create(name="jeep", country="USA")
        Manufacturer.objects.create(name="bmw", country="Germany")
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "m"})
        manufacturers = Manufacturer.objects.filter(name__icontains="m")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_car_search(self):
        manufacturer = Manufacturer.objects.create(
            name="bmw",
            country="Germany"
        )
        Car.objects.create(model="x-5", manufacturer=manufacturer)
        Car.objects.create(model="x-7", manufacturer=manufacturer)
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "x"})
        cars = Car.objects.filter(model__icontains="x")
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_driver_creation_form_with_license_number_first_last_name_is_valid(
            self
    ):
        form_data = {
            "username": "test_user1",
            "password1": "1357Test_password",
            "password2": "1357Test_password",
            "license_number": "ASD45678",
            "first_name": "First",
            "last_name": "Last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_validate_license_number_with_invalid_data(self):
        with self.assertRaisesMessage(
                ValidationError,
                "License number should consist of 8 characters"
        ):
            validate_license_number("000")

        with self.assertRaisesMessage(
                ValidationError,
                "First 3 characters should be uppercase letters"
        ):
            validate_license_number("asd45678")

        with self.assertRaisesMessage(
                ValidationError,
                "Last 5 characters should be digits"
        ):
            validate_license_number("ASD4567a")
