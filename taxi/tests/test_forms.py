from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    DriverUsernameSearchForm,
    ManufacturerNameSearchForm,
    CarModelSearchForm
)
from taxi.models import Driver, Manufacturer, Car


class DriverListSearchTest(TestCase):
    def setUp(self):
        self.driver1 = get_user_model().objects.create(
            username="test_driver1",
            password="1234",
            license_number="LLL12345"
        )
        self.driver2 = get_user_model().objects.create(
            username="test_driver2",
            password="1234",
            license_number="LLL12346"
        )
        self.admin_driver = get_user_model().objects.create(
            username="admin",
            password="1234",
            license_number="LLL12347"
        )

    def test_search_driver_by_username_form(self):
        form_data = {"username": "test"}
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        queryset = Driver.objects.filter(
            username__icontains=form.cleaned_data["username"]
        )

        self.assertEqual(queryset.count(), 2)
        self.assertIn(self.driver1, queryset)
        self.assertIn(self.driver2, queryset)
        self.assertNotIn(self.admin_driver, queryset)


class ManufacturerListSearchTest(TestCase):
    def setUp(self):
        self.manufacturer1 = Manufacturer.objects.create(
            name="test_manufacturer1",
            country="Ukraine"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="TEST_manufacturer2",
            country="Ukraine"
        )
        self.manufacturer_3 = Manufacturer.objects.create(
            name="manufacturer3",
            country="Ukraine"
        )

    def test_search_manufacturer_by_name_form(self):
        form_data = {"name": "Test"}
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        queryset = Manufacturer.objects.filter(
            name__icontains=form.cleaned_data["name"]
        )

        self.assertEqual(queryset.count(), 2)
        self.assertIn(self.manufacturer1, queryset)
        self.assertIn(self.manufacturer2, queryset)
        self.assertNotIn(self.manufacturer_3, queryset)


class CarListSearchTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="Ukraine"
        )
        self.car1 = Car.objects.create(
            model="car1_test",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="CAR1000_test",
            manufacturer=self.manufacturer
        )
        self.car3 = Car.objects.create(
            model="car0_test",
            manufacturer=self.manufacturer
        )
        self.car4 = Car.objects.create(
            model="admin_car",
            manufacturer=self.manufacturer
        )

    def test_search_car_by_name_form(self):
        form_data = {"model": "Car1"}
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        queryset = Car.objects.filter(
            model__icontains=form.cleaned_data["model"]
        )

        self.assertEqual(queryset.count(), 2)
        self.assertIn(self.car1, queryset)
        self.assertIn(self.car2, queryset)
        self.assertNotIn(self.car3, queryset)
        self.assertNotIn(self.car4, queryset)
