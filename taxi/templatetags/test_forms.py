from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm
from taxi.models import Car, Manufacturer


class FormTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "test name",
            "last_name": "test last_name",
            "license_number": "ASD12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class FormSearchTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test1",
            password="test123456",
            first_name="test",
            last_name="test"
        )
        self.client.force_login(self.user)
        self.manufacturer1 = Manufacturer.objects.create(
            name="Audi",
            country="German"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="BMW",
            country="German"
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car1 = Car.objects.create(
            model="test1",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="test2",
            manufacturer=self.manufacturer2
        )
        self.car3 = Car.objects.create(
            model="test3",
            manufacturer=self.manufacturer3
        )
        self.driver1 = get_user_model().objects.create_user(
            username="Bob",
            password="test12345",
            license_number="ASD12345"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="Den",
            password="test12345",
            license_number="TES12345"
        )
        self.driver3 = get_user_model().objects.create_user(
            username="Odin",
            password="test12345",
            license_number="LOL12345"
        )

    def test_car_search_by_model(self):
        response = self.help_for_tests_response("cars", "model", "test1")

        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)
        self.assertNotContains(response, self.car3.model)

        response = self.help_for_tests_response("cars", "model", "")

        self.assertContains(response, self.car1.model)
        self.assertContains(response, self.car2.model)
        self.assertContains(response, self.car3.model)

        response = self.help_for_tests_response("cars", "model", "sdfsf1234")

        self.assertNotContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)
        self.assertNotContains(response, self.car3.model)

    def test_driver_search_by_username(self):
        response = self.help_for_tests_response("drivers", "username", "Bob")

        self.assertContains(response, self.driver1.username)
        self.assertNotContains(response, self.driver2.username)
        self.assertNotContains(response, self.driver3.username)

        response = self.help_for_tests_response("drivers", "username", "")

        self.assertContains(response, self.driver1.username)
        self.assertContains(response, self.driver2.username)
        self.assertContains(response, self.driver3.username)

        response = self.help_for_tests_response(
            "drivers",
            "username",
            "asda13"
        )

        self.assertNotContains(response, self.driver1.username)
        self.assertNotContains(response, self.driver2.username)
        self.assertNotContains(response, self.driver3.username)

    def test_manufacturer_search_by_name(self):
        response = self.help_for_tests_response(
            "manufacturers", "name", "Audi"
        )

        self.assertContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)
        self.assertNotContains(response, self.manufacturer3.name)

        response = self.help_for_tests_response("manufacturers", "name", "")

        self.assertContains(response, self.manufacturer1.name)
        self.assertContains(response, self.manufacturer2.name)
        self.assertContains(response, self.manufacturer3.name)

        response = self.help_for_tests_response(
            "manufacturers",
            "name",
            "2fsdfsf"
        )

        self.assertNotContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)
        self.assertNotContains(response, self.manufacturer3.name)

    def help_for_tests_response(self, model, field, value):
        return self.client.get(
            f"http://127.0.0.1:8001/{model}/?{field}={value}"
        )
