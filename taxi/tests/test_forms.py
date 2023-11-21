from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.forms import validate_license_number, DriverCreationForm
from taxi.models import Manufacturer, Car


class LicenseNumberValidationTests(TestCase):
    def test_license_number_validation_success(self):
        license_number = "ABC12345"
        self.assertEquals(
            validate_license_number(license_number),
            license_number
        )

    def test_license_number_validation_failure(self):
        with self.assertRaises(
                ValidationError
        ) as error:
            validate_license_number("abc12345678")
            self.assertEqual(
                error.exception.message,
                "License number should consist of 8 characters"
            )

        with self.assertRaises(
                ValidationError
        ) as error:
            validate_license_number("abc12345")
            self.assertEqual(
                error.exception.message,
                "First 3 characters should be uppercase letters"
            )

        with self.assertRaises(
                ValidationError
        ) as error:
            validate_license_number("ABC12AB5")
            self.assertEqual(
                error.exception.message,
                "Last 5 characters should be digits"
            )


class CarFormTests(TestCase):
    def test_car_search_in_car_list_page_by_model(self):
        user = get_user_model().objects.create_user(
            username="Test",
            password="Test1234!",
            license_number="ABC12345",
        )

        self.client.force_login(user)

        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="USA"
        )
        Car.objects.create(
            model="Car One",
            manufacturer=manufacturer,
        )
        Car.objects.create(
            model="ThisisCARTWO",
            manufacturer=manufacturer,
        )
        Car.objects.create(
            model="Third Auto",
            manufacturer=manufacturer,
        )

        searching_data = {"model": "car"}
        resp = self.client.get(reverse("taxi:car-list"), data=searching_data)

        cars = Car.objects.filter(model__icontains="car")
        print(resp)
        self.assertEqual(
            list(resp.context["car_list"]),
            list(cars),
        )


class DriverFormTests(TestCase):
    def test_driver_creation_with_first_last_name_license_number_valid(self):
        form_data = {
            "username": "test",
            "password1": "Test1234!",
            "password2": "Test1234!",
            "first_name": "TestFirst",
            "last_name": "TestLast",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_search_in_driver_list_page_by_username(self):
        user = get_user_model().objects.create_user(
            username="driver 1",
            password="Test1234!",
            license_number="ABC12345",
        )
        self.client.force_login(user)

        get_user_model().objects.create_user(
            username="SECONDDRIVER",
            password="Test1234!",
            license_number="ABC12346",
        )
        get_user_model().objects.create_user(
            username="Mr Third",
            password="Test1234!",
            license_number="ABC12347",
        )

        searching_data = {"username": "driver"}
        resp = self.client.get(
            reverse("taxi:driver-list"),
            data=searching_data
        )

        drivers = get_user_model().objects.filter(username__icontains="driver")

        self.assertEqual(
            list(resp.context["driver_list"]),
            list(drivers),
        )


class ManufacturerSearchFormTests(TestCase):
    def test_driver_search_in_driver_list_page_by_username(self):
        user = get_user_model().objects.create_user(
            username="driver 1",
            password="Test1234!",
            license_number="ABC12345",
        )

        self.client.force_login(user)

        Manufacturer.objects.create(
            name="First manufacturer",
            country="UK"
        )
        Manufacturer.objects.create(
            name="SECONDMANUFACTURER",
            country="US"
        )
        Manufacturer.objects.create(name="Third", country="Japan")

        searching_data = {"name": "manufacturer"}
        resp = self.client.get(
            reverse("taxi:manufacturer-list"),
            data=searching_data
        )

        manufacturers = Manufacturer.objects.filter(
            name__icontains="manufacturer"
        )

        self.assertEqual(
            list(resp.context["manufacturer_list"]),
            list(manufacturers),
        )
