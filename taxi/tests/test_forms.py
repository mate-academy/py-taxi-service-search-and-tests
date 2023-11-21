from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car


class FormsTest(TestCase):
    def test_driver_creation_form_with_walid_data(self):
        form_data = {
            "username": "testuser",
            "password1": "testpass123",
            "password2": "testpass123",
            "first_name": "testfirst",
            "last_name": "lestlast",
            "license_number": "JDI12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form_with_valid_data(self) -> None:
        form_data = {
            "license_number": "JDI12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_validation_form_with_too_long_license_num(self):
        form_data = {
            "username": "testuser",
            "password1": "testpass123",
            "password2": "testpass123",
            "first_name": "testfirst",
            "last_name": "lestlast",
            "license_number": "JDI123456"
        }
        form = DriverCreationForm(data=form_data)
        form2 = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertFalse(form2.is_valid())

    def test_validation_form_with_too_small_license_num(self):
        form_data = {
            "username": "testuser",
            "password1": "testpass123",
            "password2": "testpass123",
            "first_name": "testfirst",
            "last_name": "lestlast",
            "license_number": "JDI1234"
        }
        form = DriverCreationForm(data=form_data)
        form2 = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertFalse(form2.is_valid())

    def test_validation_form_with_number_in_the_begin(self):
        form_data = {
            "username": "testuser",
            "password1": "testpass123",
            "password2": "testpass123",
            "first_name": "testfirst",
            "last_name": "lestlast",
            "license_number": "J2I12345"
        }
        form = DriverCreationForm(data=form_data)
        form2 = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertFalse(form2.is_valid())

    def test_validation_form_with_letter_in_the_end(self):
        form_data = {
            "username": "testuser",
            "password1": "testpass123",
            "password2": "testpass123",
            "first_name": "testfirst",
            "last_name": "lestlast",
            "license_number": "JRI1234D"
        }
        form = DriverCreationForm(data=form_data)
        form2 = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertFalse(form2.is_valid())


class SearchFormTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="maanu1",
            country="a"
        )
        self.car = Car.objects.create(
            model="red",
            manufacturer=self.manufacturer
        )
        self.driver = get_user_model().objects.create(
            username="tester",
            password="Testosteron12",
            license_number="KYD09813"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="manu2",
            country="b"
        )
        self.car2 = Car.objects.create(
            model="blue",
            manufacturer=self.manufacturer2
        )
        self.driver2 = get_user_model().objects.create(
            username="lop",
            password="Testosteron123",
            license_number="KYD09815"
        )
        self.client.force_login(self.driver)

    def test_search_manufacturer(self):
        url = reverse("taxi:manufacturer-list")
        searched_name = "maanu1"
        unsearched_name = "manu2"
        response = self.client.get(url, {"name": searched_name})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, searched_name)
        self.assertNotContains(response, unsearched_name)

    def test_search_car(self):
        url = reverse("taxi:car-list")
        searched_name = "red"
        unsearched_name = "blue"
        response = self.client.get(url, {"model": searched_name})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, searched_name)
        self.assertNotContains(response, unsearched_name)

    def test_search_driver(self):
        url = reverse("taxi:driver-list")
        searched_name = self.driver.username
        unsearched_name = self.driver2.username
        response = self.client.get(url, {"username": searched_name})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, searched_name)
        self.assertNotContains(response, unsearched_name)
