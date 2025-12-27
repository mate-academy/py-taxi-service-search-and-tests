from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    CarModelSearchForm,
    ManufacturerNameSearchForm,
    DriverLicenseUpdateForm,
    DriverUsernameSearchForm,
    DriverCreationForm
)
from taxi.models import Manufacturer, Car


class TestCarForms(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="new_driver",
            password="root1234",
        )
        self.client.force_login(self.user)

        # Create some sample car models
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacture",
            country="USA"
        )
        self.car1 = Car.objects.create(
            model="M5",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Civic",
            manufacturer=self.manufacturer
        )
        self.car3 = Car.objects.create(
            model="M3",
            manufacturer=self.manufacturer
        )

    def test_car_search_form_with_arg(self):
        form_data = {
            "model": "M5",
        }
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        results = Car.objects.filter(
            model__icontains=form.cleaned_data["model"]
        )
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first().model, "M5")

    def test_car_search_form_without_arg(self):
        form_data = {
            "model": "",
        }
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        results = Car.objects.all()
        self.assertEqual(results.count(), 3)
        self.assertIn(self.car1, results)
        self.assertIn(self.car2, results)
        self.assertIn(self.car3, results)


class TestManufacturerForms(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="new_driver",
            password="root1234",
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Test Manufacture",
            country="USA"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Sample Manufacture",
            country="Canada"
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="Example Manufacture",
            country="UK"
        )

    def test_manufacturer_search_form_with_arg(self):
        form_data = {
            "name": "Test Manufacture",
        }
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        results = Manufacturer.objects.filter(
            name__icontains=form.cleaned_data["name"]
        )
        self.assertEqual(results.count(), 1)
        self.assertEqual(
            results.first().name,
            "Test Manufacture"
        )

    def test_manufacturer_search_form_without_arg(self):
        form_data = {
            "name": "",
        }
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        results = Manufacturer.objects.all()
        self.assertEqual(results.count(), 3)
        self.assertIn(self.manufacturer1, results)
        self.assertIn(self.manufacturer2, results)
        self.assertIn(self.manufacturer3, results)


class TestDriverForms(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="new_driver",
            license_number="HRN84739",
            password="root1234",
        )
        self.user2 = get_user_model().objects.create_user(
            username="another_driver",
            license_number="HRN12345",
            password="root1234",
        )
        self.user3 = get_user_model().objects.create_user(
            username="some_other_driver",
            license_number="HRN67890",
            password="root1234",
        )
        self.client.force_login(self.user1)

        self.manufacturer = Manufacturer.objects.create(
            name="Test manufacture", country="USA"
        )

    def test_driver_form(self):
        form_data = {
            "username": "fourth_driver",
            "license_number": "HRN84735",
            "password1": "Root1234",
            "password2": "Root1234"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        new_driver = form.save()
        self.assertIsNotNone(new_driver)
        created_user = get_user_model().objects.get(
            username="fourth_driver"
        )
        self.assertEqual(
            created_user.username,
            "fourth_driver"
        )
        self.assertEqual(
            created_user.license_number,
            "HRN84735"
        )
        self.assertTrue(
            created_user.check_password("Root1234")
        )

    def test_driver_search_form_with_arg(self):
        form_data = {
            "username": "new_driver",
        }
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form_without_arg(self):
        form_data = {
            "username": "",
        }
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        search_username = form.cleaned_data.get("username")
        results = get_user_model().objects.filter(
            username__icontains=search_username
        )
        self.assertEqual(results.count(), 3)
        self.assertEqual(results.first().username, "new_driver")

    def test_update_license_form_correct_num(self):
        self.user1.license_number = "OLD12345"
        self.user1.save()
        form_data = {"license_number": "HRN84739"}
        form = DriverLicenseUpdateForm(form_data, instance=self.user1)
        self.assertTrue(form.is_valid())
        form.save()
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.license_number, "HRN84739")

    def test_update_license_form_incorrect_num(self):
        form_data = {"license_number": "HrN8473"}
        form = DriverLicenseUpdateForm(form_data)
        self.assertEqual(form.is_valid(), False)
