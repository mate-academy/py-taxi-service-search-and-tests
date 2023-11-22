from django.contrib.auth import get_user_model
from django.test import TestCase


from taxi.forms import (
    DriverCreationForm,
    CarSearchForm,
    DriverSearchForm,
    ManufacturerSearchForm
)
from taxi.models import Manufacturer, Car, Driver


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_first_last_name_is_valid(self):
        form_data = {
            "username": "User12345",
            "password1": "usertest0987",
            "password2": "usertest0987",
            "license_number": "ADC10293",
            "first_name": "User",
            "last_name": "Test"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_form_with_license_is_not_valid(self):
        form_data = {
            "username": "User12345",
            "password1": "usertest0987",
            "password2": "usertest0987",
            "license_number": "ADC1093",
        }

        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)

    def test_car_search_form(self):
        manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )
        Car.objects.create(
            model="CarTest",
            manufacturer=manufacturer
        )

        self.user = get_user_model().objects.create_user(
            username="UserTest",
            password="testpass"
        )
        self.client.force_login(self.user)

        response = self.client.get("/cars/?model=ca")
        cars = Car.objects.filter(model__icontains="ca")

        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_manufacturer_search_form(self):
        self.manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )

        self.user = get_user_model().objects.create_user(
            username="UserTest",
            password="testpass"
        )
        self.client.force_login(self.user)

        response = self.client.get("/manufacturers/?name=na")
        manufacturers = Manufacturer.objects.filter(name__icontains="na")

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_driver_search_form(self):
        self.user = get_user_model().objects.create_user(
            username="UserTest",
            password="testpass"
        )
        self.client.force_login(self.user)

        response = self.client.get("/drivers/?username=use")
        drivers = Driver.objects.filter(username__icontains="use")

        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
