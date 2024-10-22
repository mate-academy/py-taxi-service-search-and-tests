from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    CarModelSearchForm,
    ManufacturerNameSearchForm,
    DriverLicenseUpdateForm,
    DriverUsernameSearchForm,
    DriverCreationForm
)
from taxi.models import Manufacturer, Driver


class TestCarForms(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="new_driver1",
            password="root1234",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Manufacture Test", country="China"
        )

    def test_car_search_form_with_arg(self):
        form_data = {
            "model": "X3",
        }
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form_without_arg(self):
        form_data = {
            "model": "",
        }
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestManufacturerForms(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="new_driver1",
            password="root1234",
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Manufacture Test", country="China"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Another Manufacturer", country="USA"
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="Test Company", country="Germany"
        )

    def test_manufacturer_search_form_with_arg(self):
        url = reverse("taxi:manufacturer-list")

        response = self.client.get(url, {"name": "Test"})

        self.assertEquals(response.status_code, 200)

        self.assertNotContains(response, "Another Manufacturer")

        self.assertContains(response, "Manufacture Test")
        self.assertContains(response, "Test Company")

    def test_manufacturer_search_form_without_arg(self):
        url = reverse("taxi:manufacturer-list")

        response = self.client.get(url, {"name": ""})

        self.assertEquals(response.status_code, 200)

        self.assertContains(response, "Manufacture Test")
        self.assertContains(response, "Another Manufacturer")
        self.assertContains(response, "Test Company")


class TestDriverForms(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="new_driver1",
            password="root1234",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Manufacture Test", country="China"
        )

        self.driver = Driver.objects.create(
            username="existing_driver",
            license_number="ABC12345",
            password="password123"
        )

    def test_driver_form(self):
        form_data = {
            "username": "another_driver",
            "license_number": "HRN84739",
            "password1": "Root1234",
            "password2": "Root1234"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        driver = form.save()
        self.assertEqual(driver.username, "another_driver")

    def test_driver_search_form_with_arg(self):
        form_data = {
            "username": "existing_driver",
        }
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_update_license_form_incorrect_num(self):
        form_data = {"license_number": "HrN8473"}
        form = DriverLicenseUpdateForm(data=form_data, instance=self.driver)
        self.assertFalse(form.is_valid())

    def test_driver_search_form_without_arg(self):
        form_data = {
            "username": "",
        }
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_update_license_form_correct_num(self):
        form_data = {"license_number": "HRN84739"}
        form = DriverLicenseUpdateForm(data=form_data, instance=self.driver)
        self.assertTrue(form.is_valid())
        form.save()
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.license_number, "HRN84739")
