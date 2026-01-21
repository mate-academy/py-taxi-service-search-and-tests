from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car, Driver
from taxi.forms import (
    ManufacturerNameSearchForm,
    CarModelSearchForm,
    DriverUsernameSearchForm,
)


class ManufacturerNameSearchFormTests(TestCase):

    def setUp(self):
        self.user = Driver.objects.create_superuser(
            username="admin", password="password", license_number="UNIQUE123"
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Tesla", country="USA")
        Manufacturer.objects.create(name="BMW", country="Germany")

    def test_search_by_name(self):
        form_data = {"name": "Tesla"}
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        manufacturers = Manufacturer.objects.filter(name__icontains="Tesla")
        self.assertEqual(manufacturers.count(), 1)
        self.assertEqual(manufacturers.first().name, "Tesla")


class CarModelSearchFormTests(TestCase):

    def setUp(self):
        self.user = Driver.objects.create_superuser(
            username="admin", password="password", license_number="UNIQUE456"
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(name="Tesla", country="USA")
        Car.objects.create(model="Model S", manufacturer=manufacturer)
        Car.objects.create(model="Model 3", manufacturer=manufacturer)

    def test_search_by_model(self):
        form_data = {"model": "Model S"}
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        cars = Car.objects.filter(model__icontains="Model S")
        self.assertEqual(cars.count(), 1)
        self.assertEqual(cars.first().model, "Model S")


class DriverUsernameSearchFormTests(TestCase):

    def setUp(self):
        self.user = Driver.objects.create_superuser(
            username="admin", password="password", license_number="UNIQUE789"
        )
        self.client.force_login(self.user)
        Driver.objects.create_user(
            username="driver1", password="password", license_number="UNIQUE111"
        )
        Driver.objects.create_user(
            username="driver2", password="password", license_number="UNIQUE222"
        )

    def test_search_by_username(self):
        form_data = {"username": "driver1"}
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        drivers = get_user_model().objects.filter(
            username__icontains="driver1"
        )
        self.assertEqual(drivers.count(), 1)
        self.assertEqual(drivers.first().username, "driver1")
