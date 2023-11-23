from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car, Driver
from taxi.tests.test_view import MANUFACTURER_URL, CAR_URL, DRIVER_URL


class FormsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="test1",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_driver_form_with_valid_license(self):
        form_data = {
            "username": "testuser",
            "password1": "dhg543h567",
            "password2": "dhg543h567",
            "license_number": "ABC12345",
            "first_name": "First",
            "last_name": "Last"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_form_with_invalid_uppercase_license(self):
        form_data = {
            "username": "testuser",
            "password1": "dhg543h567",
            "password2": "dhg543h567",
            "license_number": "ABc12345",
            "first_name": "First",
            "last_name": "Last"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_form_with_invalid_letters_license(self):
        form_data = {
            "username": "testuser",
            "password1": "dhg543h567",
            "password2": "dhg543h567",
            "license_number": "AB312345",
            "first_name": "First",
            "last_name": "Last"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_form_with_invalid_len_license(self):
        form_data = {
            "username": "testuser",
            "password1": "dhg543h567",
            "password2": "dhg543h567",
            "license_number": "ABC1h2345",
            "first_name": "First",
            "last_name": "Last"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_form_with_invalid_dijits_license(self):
        form_data = {
            "username": "testuser",
            "password1": "dhg543h567",
            "password2": "dhg543h567",
            "license_number": "ABC1h234",
            "first_name": "First",
            "last_name": "Last"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_search_by_username(self):
        Driver.objects.create(
            username="driver1",
            password="driver123",
            license_number="XAX12345"
        )
        Driver.objects.create(
            username="driver2",
            password="driver123",
            license_number="XAX12346"
        )
        response = self.client.get(DRIVER_URL, {"username": "2"})
        drivers = Driver.objects.filter(username__icontains="2")
        self.assertEqual(list(response.context["driver_list"]), list(drivers))

    def test_manufacturer_search_by_name(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")
        response = self.client.get(MANUFACTURER_URL, {"name": "audi"})
        manufacturers = Manufacturer.objects.filter(name__icontains="audi")

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertEqual(list(response.context["manufacturer_list"]), list(manufacturers))

    def test_car_search_by_model(self):
        manufacturer = Manufacturer.objects.create(name="Toyota")
        Car.objects.create(
            model="Toyota Land Cruiser",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="Toyota FJ Crusier",
            manufacturer=manufacturer
        )
        response = self.client.get(CAR_URL, {"model": "fj"})
        cars = Car.objects.filter(model__icontains="fj")
        self.assertEqual(list(response.context["car_list"]), list(cars))
