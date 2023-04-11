from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarModelSearchForm
)
from taxi.models import Car, Manufacturer


class DriverTest(TestCase):

    def test_driver_creation_with_license_first_last(self):
        form_data = {
            "username": "test_user",
            "password1": "test12345",
            "password2": "test12345",
            "license_number": "TES12345",
            "first_name": "Test",
            "last_name": "Case",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverLicenseTest(TestCase):

    def test_driver_license_update(self):
        form = DriverLicenseUpdateForm()
        expected_fields = ["license_number"]
        self.assertSequenceEqual(list(form.fields), expected_fields)

    def test_wrong_count_of_letters_license(self):
        form = DriverLicenseUpdateForm(data={"license_number": "TEST1234"})
        self.assertFalse(form.is_valid())

    def test_right_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "TES12345"})
        self.assertTrue(form.is_valid())

    def test_wrong_len_license(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "TVTS12342"}
        )
        self.assertFalse(form.is_valid())

    def test_wrong_case_license(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "dfa12344"}
        )
        self.assertFalse(form.is_valid())

    def test_numbers_in_letters_license(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "34212344"}
        )
        self.assertFalse(form.is_valid())

    def test_letters_in_numbers_license(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "testsads"}
        )
        self.assertFalse(form.is_valid())


class DriverSearchFormTest(TestCase):
    def setUp(self):
        self.form_data = {"username": "john.wik"}

    def test_valid_search(self):
        form = DriverSearchForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_empty_search(self):
        form = DriverSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())

    def test_case_insensitive_search(self):
        form = DriverSearchForm(data={"username": "JoHN.wik"})
        self.assertTrue(form.is_valid())


class CarModelSearchFormTest(TestCase):
    def setUp(self):
        self.form_data = {"model": "fusion"}

    def test_valid_search(self):
        form = CarModelSearchForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_empty_search(self):
        form = CarModelSearchForm(data={"model": ""})
        self.assertTrue(form.is_valid())

    def test_case_insensitive_search(self):
        form = CarModelSearchForm(data={"model": "fuSiOn"})
        self.assertTrue(form.is_valid())


class ManufacturerSearchFormTest(TestCase):
    def setUp(self):
        self.form_data = {"name": "Audi"}

    def test_valid_search(self):
        form = CarModelSearchForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_empty_search(self):
        form = CarModelSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())

    def test_case_insensitive_search(self):
        form = CarModelSearchForm(data={"name": "AuDI"})
        self.assertTrue(form.is_valid())


class FormSearchTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user_test",
            password="t1e2s3t4",
            first_name="name",
            last_name="second",
        )
        self.client.force_login(self.user)
        self.manufacturer1 = Manufacturer.objects.create(
            name="Jeep", country="USA"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Honda", country="Japan"
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="Hyundai", country="Korea"
        )
        self.car1 = Car.objects.create(
            model="Wrangler_i", manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Civic", manufacturer=self.manufacturer2
        )
        self.car3 = Car.objects.create(
            model="Ioniq", manufacturer=self.manufacturer3
        )
        self.driver1 = get_user_model().objects.create_user(
            username="Mate", password="t1e2s3t4", license_number="LEN65214"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="George", password="t1e2s3t4", license_number="LEN65212"
        )
        self.driver3 = get_user_model().objects.create_user(
            username="Oleg", password="t1e2s3t4", license_number="LEN64214"
        )

    def test_manufacturer_search_by_name(self):
        response = self.help_in_tests_response(
            "manufacturers", "name", "Jeep"
        )

        self.assertContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)
        self.assertNotContains(response, self.manufacturer3.name)

        response = self.help_in_tests_response(
            "manufacturers", "name", "Bugatti"
        )

        self.assertNotContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)
        self.assertNotContains(response, self.manufacturer3.name)

        response = self.help_in_tests_response(
            "manufacturers", "name", ""
        )

        self.assertContains(response, self.manufacturer1.name)
        self.assertContains(response, self.manufacturer2.name)
        self.assertContains(response, self.manufacturer3.name)

    def test_car_search_by_model(self):
        response = self.help_in_tests_response(
            "cars", "model", "wrang"
        )

        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)
        self.assertNotContains(response, self.car3.model)

        response = self.help_in_tests_response(
            "cars", "model", "i"
        )

        self.assertContains(response, self.car1.model)
        self.assertContains(response, self.car2.model)
        self.assertContains(response, self.car3.model)

        response = self.help_in_tests_response(
            "cars", "model", ""
        )

        self.assertContains(response, self.car1.model)
        self.assertContains(response, self.car2.model)
        self.assertContains(response, self.car3.model)

    def test_driver_search_by_username(self):
        response = self.help_in_tests_response(
            "drivers", "username", "Geo"
        )

        self.assertNotContains(response, self.driver1.username)
        self.assertContains(response, self.driver2.username)
        self.assertNotContains(response, self.driver3.username)

        response = self.help_in_tests_response(
            "drivers", "username", "Julia"
        )

        self.assertNotContains(response, self.driver1.username)
        self.assertNotContains(response, self.driver2.username)
        self.assertNotContains(response, self.driver3.username)

        response = self.help_in_tests_response(
            "drivers", "username", ""
        )

        self.assertContains(response, self.driver1.username)
        self.assertContains(response, self.driver2.username)
        self.assertContains(response, self.driver3.username)

    def help_in_tests_response(self, model, field, value):
        return self.client.get(
            f"http://127.0.0.1:8001/{model}/?{field}={value}"
        )
