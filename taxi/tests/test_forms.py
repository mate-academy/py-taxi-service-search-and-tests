from django.contrib.auth import get_user_model
from django.forms import CheckboxSelectMultiple
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarForm,
)
from taxi.models import Driver, Car, Manufacturer


class DriverFormsTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "new_user",
            "password1": "test_password12",
            "password2": "test_password12",
            "first_name": "new_first_name",
            "last_name": "new_last_name",
            "license_number": "VDG12345",
        }
        self.update_form_data = {"license_number": "VDG12345"}
        self.incorrect_digits_and_length_update_form_data = {
            "license_number": "VDG1245"
        }
        self.incorrect_upper_first_three_letter_form_data = {
            "license_number": "Vdg12345"
        }
        self.incorrect_length_form_data = {"license_number": "VDH123456"}

    def test_driver_creation_with_cleaned_license_number_form(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_update_driver_license_number_form(self):
        correct_form = DriverLicenseUpdateForm(data=self.update_form_data)

        incorrect_digit_form = DriverLicenseUpdateForm(
            data=self.incorrect_digits_and_length_update_form_data
        )

        incorrect_upper_first_three_letter_form = DriverLicenseUpdateForm(
            data=self.incorrect_upper_first_three_letter_form_data
        )

        self.assertTrue(correct_form.is_valid())
        self.assertFalse(incorrect_digit_form.is_valid())
        self.assertFalse(incorrect_upper_first_three_letter_form.is_valid())


class CarTestsTest(TestCase):

    def test_car_checkbox_form(self):
        form = CarForm()
        self.assertIsInstance(
            form.fields["drivers"].widget, CheckboxSelectMultiple
        )


class SearchFormsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user_login",
            password="123123password",
            license_number="12345"

        )
        self.manufacturer1 = Manufacturer.objects.create(
            name="Manufacturer1",
            country="Germany"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Manufacturer2",
            country="Germany"
        )
        Car.objects.create(
            model="test_model1",
            manufacturer=self.manufacturer1
        )
        Car.objects.create(
            model="test_model2",
            manufacturer=self.manufacturer2
        )

        self.client.force_login(self.user)

    def test_driver_query_set_changed_after_form(self):
        filtered_queryset = Driver.objects.filter(username="user_login")
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "user_login"}
        )
        query_set_after_search = response.context["driver_list"]
        self.assertEqual(list(query_set_after_search), list(filtered_queryset))

    def test_car_query_set_changed_after_form(self):
        filtered_queryset = Car.objects.filter(model="test_model1")
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "test_model1"}
        )
        query_set_after_search = response.context["cars_list"]
        self.assertEqual(list(query_set_after_search), list(filtered_queryset))

    def test_manufacturer_query_set_changed_after_form(self):
        filtered_queryset = Manufacturer.objects.filter(name="Manufacturer1")
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Manufacturer1"}
        )
        query_set_after_search = response.context["manufacturer_list"]
        self.assertEqual(list(query_set_after_search), list(filtered_queryset))
