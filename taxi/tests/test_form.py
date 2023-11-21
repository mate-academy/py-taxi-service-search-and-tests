from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car, Driver


class FormsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="test1", password="test1pass"
        )
        self.client.force_login(self.user)

    def test_driver_search(self):
        Driver.objects.create(
            username="driver1test",
            password="driver1pass",
            license_number="ABC12346"
        )
        Driver.objects.create(
            username="driver2",
            password="driver2pass",
            license_number="ABC12345"
        )
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "test"})
        drivers = Driver.objects.filter(username__icontains="test")
        self.assertEqual(list(response.context["driver_list"]), list(drivers))

    def test_manufacturer_search(self):
        Manufacturer.objects.create(name="test1cool", country="test1country")
        Manufacturer.objects.create(name="test2", country="test2country")
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "cool"})
        manufacturers = Manufacturer.objects.filter(name__icontains="cool")
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )

    def test_car_search(self):
        manufacturer = Manufacturer.objects.create(name="test1man")
        Car.objects.create(model="test1carsuper", manufacturer=manufacturer)
        Car.objects.create(model="test2car", manufacturer=manufacturer)
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "super"})
        cars = Car.objects.filter(model__icontains="super")
        self.assertEqual(list(response.context["car_list"]), list(cars))

    def test_driver_correct_license(self):
        form_data = {
            "username": "test1user",
            "password1": "testpass1",
            "password2": "testpass1",
            "license_number": "ABC12345",
            "first_name": "first1",
            "last_name": "last1",
        }
        form1 = DriverCreationForm(data=form_data)
        form2 = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form1.is_valid())
        self.assertEqual(form1.cleaned_data, form_data)
        self.assertTrue(form2.is_valid())

    def test_driver_noletters_license(self):
        form_data = {
            "username": "test1user",
            "password1": "test1pass",
            "password2": "test1pass",
            "license_number": "12345678",
            "first_name": "first1",
            "last_name": "last1",
        }
        form1 = DriverCreationForm(data=form_data)
        self.assertFalse(form1.is_valid())
        form2 = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form2.is_valid())

    def test_driver_wrong_len_license(self):
        form_data = {
            "username": "test1user",
            "password1": "test1pass",
            "password2": "test1pass",
            "license_number": "ABC12345678",
            "first_name": "first1",
            "last_name": "last1",
        }
        form1 = DriverCreationForm(data=form_data)
        self.assertFalse(form1.is_valid())
        form2 = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form2.is_valid())

    def test_driver_nodijits_license(self):
        form_data = {
            "username": "test1user",
            "password1": "test1pass",
            "password2": "test1pass",
            "license_number": "ABCABCAB",
            "first_name": "first1",
            "last_name": "last1",
        }
        form1 = DriverCreationForm(data=form_data)
        self.assertFalse(form1.is_valid())
        self.assertNotEqual(form1.cleaned_data, form_data)
        form2 = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form2.is_valid())
