from django.test import TestCase

from taxi.forms import (DriverCreationForm,
                        DriverSearchForm,
                        CarSearchForm,
                        ManufacturerSearchForm)
from taxi.models import Driver, Car, Manufacturer


class DriverFormsTest(TestCase):
    def setUp(self):
        Driver.objects.create(username="testuser1",
                              license_number="AAA12345")
        Driver.objects.create(username="testuser2",
                              license_number="BBB12345")
        Driver.objects.create(username="anotheruser",
                              license_number="CCC12345")

    def test_creation_form_with_license_first_last_name_is_valid(self):
        form_data = {
            "username": "nameuser",
            "password1": "testpass123",
            "password2": "testpass123",
            "license_number": "LLL12345",
            "first_name": "First",
            "last_name": "Last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_search_form(self):
        form = DriverSearchForm()
        self.assertIn("username", form.fields)

    def test_search_form_is_valid_with_empty_data(self):
        form = DriverSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_search_form_is_valid_with_valid_data(self):
        form = DriverSearchForm(data={"username": "name"})
        self.assertTrue(form.is_valid())

    def test_search_form_filter(self):
        form_data = {"username": "test"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        filtered_drivers = Driver.objects.filter(
            username__icontains=form.cleaned_data["username"]
        )
        self.assertEqual(filtered_drivers.count(), 2)
        self.assertIn(
            "testuser1",
            [driver.username for driver in filtered_drivers])
        self.assertIn(
            "testuser2",
            [driver.username for driver in filtered_drivers])


class CarFormsTest(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(
            name="testname",
            country="testcountry")
        Car.objects.create(model="testmodel1", manufacturer=manufacturer)
        Car.objects.create(model="testmodel2", manufacturer=manufacturer)
        Car.objects.create(model="anothermodel", manufacturer=manufacturer)

    def test_search_form(self):
        form = CarSearchForm()
        self.assertIn("model", form.fields)

    def test_search_form_is_valid_with_empty_data(self):
        form = CarSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_search_form_is_valid_with_valid_data(self):
        form = CarSearchForm(data={"model": "model"})
        self.assertTrue(form.is_valid())

    def test_search_form_filter(self):
        form_data = {"model": "test"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        filtered_cars = Car.objects.filter(
            model__icontains=form.cleaned_data["model"])
        self.assertEqual(filtered_cars.count(), 2)
        self.assertIn("testmodel1", [car.model for car in filtered_cars])
        self.assertIn("testmodel2", [car.model for car in filtered_cars])


class ManufacturerFormsTest(TestCase):
    def setUp(self):
        Manufacturer.objects.create(name="testname1", country="testcountry")
        Manufacturer.objects.create(name="testname2", country="testcountry")
        Manufacturer.objects.create(name="anothername", country="testcountry")

    def test_search_form(self):
        form = ManufacturerSearchForm()
        self.assertIn("name", form.fields)

    def test_search_form_is_valid_with_empty_data(self):
        form = ManufacturerSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_search_form_is_valid_with_valid_data(self):
        form = ManufacturerSearchForm(data={"name": "name"})
        self.assertTrue(form.is_valid())

    def test_search_form_filter(self):
        form_data = {"name": "test"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        filtered_manufacturers = Manufacturer.objects.filter(
            name__icontains=form.cleaned_data["name"])
        self.assertEqual(filtered_manufacturers.count(), 2)
        self.assertIn(
            "testname1",
            [manufacturer.name for manufacturer in filtered_manufacturers])
        self.assertIn(
            "testname2",
            [manufacturer.name for manufacturer in filtered_manufacturers])
