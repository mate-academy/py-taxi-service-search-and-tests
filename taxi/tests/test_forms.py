from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car, Driver

CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class FormsTest(TestCase):
    def test_create_driver_with_license_form(self):
        form_data = {
            "username": "test_user",
            "password1": "test0451",
            "password2": "test0451",
            "first_name": "Test",
            "last_name": "Driver",
            "license_number": "AAA00451"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_valid(self):
        user = get_user_model().objects.create(username="test_user")
        form_data = {
            "license_number": "AAA45100",
        }
        form = DriverLicenseUpdateForm(instance=user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid(self):
        user = get_user_model().objects.create(username="test_user")
        form_data = {
            "license_number": "test+test+test+0+4+5+1",
        }
        form = DriverLicenseUpdateForm(instance=user, data=form_data)
        self.assertFalse(form.is_valid())


class FormSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_driver",
            password="test0451"
        )
        self.client.force_login(self.user)

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(name="testa")
        Car.objects.create(
            model="model_test",
            manufacturer=manufacturer
        )
        searched_name = "test"
        response = self.client.get(CAR_URL, {"model": searched_name})
        self.assertEqual(response.status_code, 200)
        context = Car.objects.filter(model__icontains=searched_name)
        self.assertEqual(list(response.context["car_list"]), list(context))

    def test_search_driver_by_username(self):
        Driver.objects.create(
            username="test_driver02",
            password="test0451",
            license_number="AAA00451"
        )

        searched_name = "test"
        response = self.client.get(DRIVER_URL, {"username": searched_name})
        self.assertEqual(response.status_code, 200)
        context = Driver.objects.filter(username__icontains=searched_name)
        self.assertEqual(list(response.context["driver_list"]), list(context))

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(name="testa")
        searched_name = "test"
        response = self.client.get(MANUFACTURER_URL, name=searched_name)
        self.assertEqual(response.status_code, 200)
        context = Manufacturer.objects.filter(name__icontains=searched_name)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(context)
        )
