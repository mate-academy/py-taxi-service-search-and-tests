from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import CarSearchForm, DriverSearchForm, ManufacturerSearchForm
from taxi.models import Car, Driver, Manufacturer


class SearchFormsTests(TestCase):
    def setUp(self):
        self.manufacturer1 = Manufacturer.objects.create(
            name="test1", country="test country1"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="test2", country="test country2"
        )

        self.driver1 = get_user_model().objects.create_user(
            username="test user1",
            password="password123",
            license_number="ABC12345"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="test user2",
            password="password123",
            license_number="XYZ67890"
        )

        self.car1 = Car.objects.create(
            model="test model1", manufacturer=self.manufacturer2
        )
        self.car2 = Car.objects.create(
            model="test model2", manufacturer=self.manufacturer1
        )

    def test_car_search_form_valid_with_data(self):
        form = CarSearchForm(data={"model": "test model1"})
        self.assertTrue(form.is_valid())

    def test_car_search_filter_results(self):
        search_query = "model2"
        form = CarSearchForm(data={"model": search_query})
        self.assertTrue(form.is_valid())

        cars = Car.objects.filter(model__icontains=form.cleaned_data["model"])
        self.assertIn(self.car2, cars)
        self.assertNotIn(self.car1, cars)

    def test_car_search_empty_returns_all(self):
        form = CarSearchForm(data={"model": ""})
        self.assertTrue(form.is_valid())

        cars = Car.objects.filter(model__icontains=form.cleaned_data["model"])
        self.assertEqual(cars.count(), 2)

    def test_car_search_no_matches(self):
        form = CarSearchForm(data={"model": "NonExistentModel"})
        self.assertTrue(form.is_valid())

        cars = Car.objects.filter(model__icontains=form.cleaned_data["model"])
        self.assertEqual(cars.count(), 0)

    def test_driver_search_form_valid_with_data(self):
        form = DriverSearchForm(data={"username": "test user1"})
        self.assertTrue(form.is_valid())

    def test_driver_search_filter_results(self):
        search_query = "user1"
        form = DriverSearchForm(data={"username": search_query})
        self.assertTrue(form.is_valid())

        drivers = Driver.objects.filter(
            username__icontains=form.cleaned_data["username"]
        )
        self.assertIn(self.driver1, drivers)
        self.assertNotIn(self.driver2, drivers)

    def test_driver_search_empty_returns_all(self):
        form = DriverSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())

        drivers = Driver.objects.filter(
            username__icontains=form.cleaned_data["username"]
        )
        self.assertEqual(drivers.count(), 2)

    def test_manufacturer_search_form_valid_with_data(self):
        form = ManufacturerSearchForm(data={"name": "test1"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_filter_results(self):
        search_query = "test1"
        form = ManufacturerSearchForm(data={"name": search_query})
        self.assertTrue(form.is_valid())

        manufacturers = Manufacturer.objects.filter(
            name__icontains=form.cleaned_data["name"]
        )
        self.assertIn(self.manufacturer1, manufacturers)
        self.assertNotIn(self.manufacturer2, manufacturers)

    def test_manufacturer_search_empty_returns_all(self):
        form = ManufacturerSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())

        manufacturers = Manufacturer.objects.filter(
            name__icontains=form.cleaned_data["name"]
        )
        self.assertEqual(manufacturers.count(), 2)
