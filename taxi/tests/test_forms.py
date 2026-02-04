from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from taxi.forms import ManufacturerSearchForm, DriverSearchForm, CarSearchForm
from taxi.models import Car, Manufacturer


class TestData(TestCase):
    @classmethod
    def setUpTestData(cls):
        driver1 = get_user_model().objects.create_user(
            username="DRiver_1",
            password="password1",
            license_number="JAM12345"
        )
        driver2 = get_user_model().objects.create_user(
            username="driver_2",
            password="password2",
            license_number="JAM32145"
        )
        get_user_model().objects.create_user(
            username="someone_else",
            password="password3",
            license_number="JAM54321"
        )

        germany = Manufacturer.objects.create(name="Germany")
        mexico = Manufacturer.objects.create(name="Mexico")

        bmw = Car.objects.create(
            model="Series 5",
            manufacturer=germany
        )
        bmw.drivers.set([driver1, driver2])
        touareg = Car.objects.create(
            model="Touareg",
            manufacturer=germany,
        )
        touareg.drivers.set([driver2])
        tiguan = Car.objects.create(
            model="Tiguan",
            manufacturer=mexico,
        )
        tiguan.drivers.set([driver1])


class ManufacturerSearchFormTest(TestData):
    def setUp(self):
        self.drivers = get_user_model().objects.all()
        self.driver = get_user_model().objects.create(
            username="driver-1",
            password="django1234",
        )
        self.client.force_login(self.driver)

    def test_driver_search(self):
        key, query = "username", "dr"
        search_params = {
            key: query
        }
        form = DriverSearchForm(search_params)
        self.assertTrue(form.is_valid())
        founded_drivers = self.drivers.filter(
            username__icontains=form.cleaned_data[key]
        )
        self.assertEqual(founded_drivers.count(), 3)

    def test_car_search(self):
        cars = Car.objects.all()
        key, query = "model", "t"
        search_params = {
            key: query
        }
        form = CarSearchForm(search_params)
        self.assertTrue(form.is_valid())
        cars = cars.filter(model__icontains=form.cleaned_data[key])
        self.assertEqual(cars.count(), 2)

    def test_manufacturer_search(self):
        manufacturer = Manufacturer.objects.all()
        key, query = "name", "ger"
        search_params = {key: query}
        form = ManufacturerSearchForm(search_params)
        self.assertTrue(form.is_valid())
        cars = manufacturer.filter(name__icontains=form.cleaned_data[key])
        self.assertEqual(cars.count(), 1)

    def test_manufacturer_form_label(self):
        form = ManufacturerSearchForm()
        self.assertTrue(
            form.fields["name"].label is None
            or form.fields["name"].label == ""
        )

    def test_manufacturer_form_placeholder(self):
        form = ManufacturerSearchForm()
        placeholder = "Search Manufacturer by Name"
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"], placeholder
        )
