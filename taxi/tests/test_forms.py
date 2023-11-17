from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, LicenseForm
from taxi.models import Driver, Manufacturer, Car


class FormsTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
        )
        self.client.force_login(self.admin_user)

    def test_driver_license_number_first_last_name_is_valid(self):
        form_data = {
            "username": "test_check",
            "password1": "Test12345",
            "password2": "Test12345",
            "first_name": "first",
            "last_name": "second",
            "license_number": "DWD12341",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_search_form_by_username(self):
        Driver.objects.create_user(
            username="test1",
            password="Test12345",
            license_number="RER12345",
        )
        Driver.objects.create_user(
            username="test2",
            password="Test12342",
            license_number="RER12342",
        )
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "test1"}
        )
        drivers = Driver.objects.filter(username__icontains="test1")
        print("response", response)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))

    def test_manufacturer_search_form_by_name(self):
        Manufacturer.objects.create(name="SAIC Motor", country="China")
        Manufacturer.objects.create(name="FAW Group", country="China")
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "FAW Group"}
        )
        manufacturers = Manufacturer.objects.filter(
            name__icontains="FAW Group"
        )
        print("RESPONSE: ", response)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_car_search_form_by_model(self):
        man1 = Manufacturer.objects.create(name="SAIC Motor", country="China")
        man2 = Manufacturer.objects.create(name="FAW Group", country="China")
        Car.objects.create(model="XC32", manufacturer=man1)
        Car.objects.create(model="CHARD", manufacturer=man2)
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "CHARD"}
        )
        cars = Car.objects.filter(model__icontains="CHARD")
        self.assertEqual(list(response.context["car_list"]), list(cars))

    def test_validate_license_number(self):
        form_data = {
            "license_number": "DWS12341",
        }
        form = LicenseForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
