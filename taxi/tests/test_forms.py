from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    CarSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    ManufacturerSearchForm
)
from taxi.models import Car, Manufacturer


class DriverTests(TestCase):
    def test_driver_creation_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "test123user",
            "password2": "test123user",
            "first_name": "New",
            "last_name": "User",
            "license_number": "MPS23412"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_license_number_equal_8(self):
        license_numbers = ["MPS234120000", "MPS239"]

        for license_number in license_numbers:
            form_data = {"license_number": license_number}
            form = DriverLicenseUpdateForm(data=form_data)

            self.assertFalse(form.is_valid())
            self.assertEqual(
                form.errors["license_number"][0],
                "License number should consist of 8 characters"
            )

    def test_license_number_first_3_characters_uppercase(self):
        form_data = {"license_number": "Mps23934"}
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"][0],
            "First 3 characters should be uppercase letters"
        )

    def test_license_number_last_5_characters_digits(self):
        form_data = {"license_number": "MPSSD934"}
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"][0],
            "Last 5 characters should be digits"
        )


class CarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="john_smith",
            license_number="ADM12345",
            first_name="John",
            last_name="Smith",
            password="Johns12345",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Fiat",
            country="Italy",
        )

    def test_create_car(self):
        response = self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "Panda",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Car.objects.get(id=self.user.cars.first().id).model, "Panda"
        )

    def test_update_car(self):
        car = Car.objects.create(
            model="Panda",
            manufacturer=self.manufacturer,
        )
        response = self.client.post(
            reverse("taxi:car-update", kwargs={"pk": car.id}),
            {
                "pk": car.id,
                "model": "Not Panda",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            },
        )
        Car.objects.get(id=car.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Car.objects.get(id=car.id).model, "Not Panda")

    def test_delete_car(self):
        car = Car.objects.create(
            model="Panda",
            manufacturer=self.manufacturer,
        )
        response = self.client.post(
            reverse("taxi:car-delete", kwargs={"pk": car.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(id=car.id).exists())


class SearchFormTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="search_test",
            license_number="ABC12345",
            first_name="Search",
            last_name="Test",
            password="searchtest123",
        )
        self.client.force_login(self.user)

    def test_car_search_form(self):
        manufacturer = Manufacturer.objects.create(
            name="Fiat",
            country="Italy",
        )
        Car.objects.create(
            model="Panda",
            manufacturer=manufacturer,
        )
        form_data = {"model": "Pan"}
        form = CarSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

        expected_result = Car.objects.filter(model="Panda")

        response = self.client.get(
            reverse("taxi:car-list") + "?model=" + form_data["model"]
        )
        self.assertEqual(
            list(response.context["car_list"]), list(expected_result)
        )

    def test_manufacturer_search_form(self):
        Manufacturer.objects.create(
            name="Citroen",
            country="France"
        )
        form_data = {"name": "Citroen"}
        form = ManufacturerSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

        expected_result = Manufacturer.objects.filter(name="Citroen")

        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=" + form_data["name"]
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(expected_result)
        )

    def test_search_form_driver(self) -> None:
        get_user_model().objects.create_user(
            username="adam_smith",
            password="smith12345",
            license_number="BCD15443",
        )

        form_data = {"username": "Adam"}
        form = DriverSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

        expected_result = get_user_model().objects.filter(
            username="adam_smith"
        )

        response = self.client.get(
            reverse("taxi:driver-list") + "?username=" + form_data["username"]
        )
        self.assertEqual(
            list(response.context["driver_list"]), list(expected_result)
        )
