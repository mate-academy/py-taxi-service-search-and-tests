from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer
from taxi.forms import ManufacturerSearchForm, DriverSearchForm, CarSearchForm


class SearchFormTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_driver",
            password="<PASSWORD>",
            license_number="TES1234"
        )
        self.client.force_login(self.user)


class DriverSearchFormTest(SearchFormTests):

    def test_driver_search_form(self):
        form_data = {
            "username": "test_driver",
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class CarSearchFormTest(SearchFormTests):

    def test_car_search_form(self):

        manufacturer = Manufacturer.objects.create(
            name="manufacturer_test",
            country="test_country",
        )

        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )

        car.drivers.add(self.user)

        form_data = {
            "model": "test_model",
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class ManufacturerSearchFormTest(SearchFormTests):

    def test_manufacturer_search_form(self):
        Manufacturer.objects.create(
            name="manufacturer_test",
            country="test_country",
        )

        form_data = {
            "name": "test_manufacturer",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
