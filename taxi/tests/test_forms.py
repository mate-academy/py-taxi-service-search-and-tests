from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Driver, Manufacturer, Car


class DriverCreationFormTest(TestCase):
    def test_driver_create_form_license_number_label(self):
        form = DriverCreationForm()
        self.assertTrue(
            (form.fields["license_number"].label is None
             or form.fields["license_number"].label == "License number")
        )

    def test_driver_create_form_license_number_length_is_not_8(self):
        data = {
            "username": "test_user",
            "license_number": "ABC123456",
            "password1": "test12345test",
            "password2": "test12345test",
            "first_name": "Test",
            "last_name": "Test"
        }

        form = DriverCreationForm(data)
        self.assertFalse(form.is_valid())

    def test_driver_create_form_license_number_first_3_is_not_upper(self):
        data = {
            "username": "test_user",
            "license_number": "abc12345",
            "password1": "test12345test",
            "password2": "test12345test",
            "first_name": "Test",
            "last_name": "Test"
        }

        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_driver_create_form_license_number_last_5_is_not_digits(self):
        data = {
            "username": "test_user",
            "license_number": "abcd1234",
            "password1": "test12345test",
            "password2": "test12345test",
            "first_name": "Test",
            "last_name": "Test"
        }

        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_driver_create_form_license_number_is_valid(self):
        data = {
            "username": "test_user",
            "license_number": "ABC12345",
            "password1": "test12345test",
            "password2": "test12345test",
            "first_name": "Test",
            "last_name": "Test"
        }

        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_update_form_license_number_label(self):
        form = DriverLicenseUpdateForm()
        self.assertTrue(
            (form.fields["license_number"].label is None
             or form.fields["license_number"].label == "License number")
        )

    def test_driver_update_form_license_number_length_is_not_8(self):
        data = {
            "license_number": "ABC123456",
        }

        form = DriverLicenseUpdateForm(data)
        self.assertFalse(form.is_valid())

    def test_driver_update_form_license_number_first_3_is_not_upper(self):
        data = {
            "license_number": "abc12345",
        }

        form = DriverLicenseUpdateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_driver_update_form_license_number_last_5_is_not_digits(self):
        data = {
            "license_number": "abcd1234",
        }

        form = DriverLicenseUpdateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_driver_update_form_license_number_is_valid(self):
        data = {
            "license_number": "ABC12345",
        }

        form = DriverLicenseUpdateForm(data=data)
        self.assertTrue(form.is_valid())


class UpdateFormsHaveInitialValuesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="test_1",
            password="test12345_1",
            license_number="AAA11111",
            first_name="TestFirstName_1",
            last_name="TestLastName_1"
        )

        get_user_model().objects.create_user(
            username="test_2",
            password="test12345_2",
            license_number="AAA22222",
            first_name="TestFirstName_2",
            last_name="TestLastName_2"
        )

        manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry",
        )

        drivers_for_car = Driver.objects.all()
        test_car = Car.objects.create(
            model="TestModel",
            manufacturer=manufacturer)

        test_car.drivers.set(drivers_for_car)
        test_car.save()

    def setUp(self):
        user = get_object_or_404(Driver, username="test_1")
        self.client.force_login(user)

    def test_driver_update_form_has_initial_value(self):
        response = self.client.get(reverse(
            "taxi:driver-update",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["form"].initial["license_number"],
            "AAA11111"
        )

    def test_manufacturer_update_form_has_initial_value(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["form"].initial["name"],
            "TestName"
        )
        self.assertEqual(
            response.context["form"].initial["country"],
            "TestCountry"
        )

    def test_car_update_form_has_initial_value(self):
        drivers_for_car = Driver.objects.all()
        response = self.client.get(reverse(
            "taxi:car-update",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["form"].initial["model"],
            "TestModel"
        )
        self.assertEqual(
            response.context["form"].initial["manufacturer"],
            1
        )
        self.assertEqual(
            response.context["form"].initial["drivers"],
            list(drivers_for_car)
        )
