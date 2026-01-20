from django.test import TestCase, Client

from taxi.forms import ManufacturerSearchForm, CarSearchForm, DriverSearchForm
from taxi.models import Driver, Car


class FormTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_manufacturer_form_is_valid(self):
        form_data = {
            "name": "Ferrari"
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertEqual(form.is_valid())

    def test_driver_form_is_valid(self):
        form_data = {
            "username": "M1"
        }
        form = DriverSearchForm(data=form_data)
        self.assertEqual(form.is_valid())

    def test_car_form_is_valid(self):
        form_data = {
            "model": "WWW"
        }
        form = CarSearchForm(data=form_data)
        self.assertEqual(form.is_valid())


class AssignToCar(TestCase):
    def setUp(self):
        self.client = Client()
        self.driver = Driver.objects.create_user(license_number="testlicense")
        self.car = Car.objects.create(model="testmodel")
        self.client.force_login(self.driver)

    def test_toggle_assign_to_car(self):
        self.driver.cars.add(self.car)
        self.driver.save()
        self.assertIn(self.car, self.driver.cars.all())

    def test_remove_car(self):
        self.driver.cars.remove(self.car)
        self.driver.save()
        self.assertNotIn(self.car, self.driver.cars.all())
