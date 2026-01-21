from django.test import TestCase

from taxi.forms import ManufacturerSearchForm, CarSearchForm, DriverSearchForm
from taxi.models import Driver, Car, Manufacturer


class TestSearchForms(TestCase):

    def setUp(self):

        self.manufacturer1 = Manufacturer.objects.create(
            name="Mercedes-Benz",
            country="Germany"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.driver1 = Driver.objects.create(
            username="petro",
            first_name="Petro",
            last_name="Mostavchuk",
            license_number="XYO14323"
        )
        self.driver2 = Driver.objects.create(
            username="ivan",
            first_name="Ivan",
            last_name="Ivanov",
            license_number="XYO14324"
        )

        self.car1 = Car.objects.create(
            model="Mercedes-Benz A-Class",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="BMW 3 Series",
            manufacturer=self.manufacturer2
        )

    def test_driver_search_form(self):
        form_data = {"name": "petro"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        drivers = Driver.objects.filter(first_name__icontains=form_data["name"])
        self.assertEqual(drivers.count(), 1)
        self.assertEqual(drivers[0], self.driver1)

    def test_car_search_form(self):
        form_data = {"car": "BMW"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        cars = Car.objects.filter(model__icontains=form_data["car"])
        self.assertEqual(cars.count(), 1)
        self.assertEqual(cars[0], self.car2)

    def test_manufacturer_search_form(self):
        form_data = {"manufacturer": "Mercedes"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        manufacturers = Manufacturer.objects.filter(name__icontains=form_data["manufacturer"])
        self.assertEqual(manufacturers.count(), 1)
        self.assertEqual(manufacturers[0], self.manufacturer1)

    def test_driver_search_no_results(self):
        form_data = {"name": "nonexistent"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        drivers = Driver.objects.filter(first_name__icontains=form_data["name"])
        self.assertEqual(drivers.count(), 0)

    def test_car_search_no_results(self):
        form_data = {"car": "Audi"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        cars = Car.objects.filter(model__icontains=form_data["car"])
        self.assertEqual(cars.count(), 0)

    def test_manufacturer_search_no_results(self):
        form_data = {"manufacturer": "Audi"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        manufacturers = Manufacturer.objects.filter(name__icontains=form_data["manufacturer"])
        self.assertEqual(manufacturers.count(), 0)