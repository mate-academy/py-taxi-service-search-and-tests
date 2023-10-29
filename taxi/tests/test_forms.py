from django.test import TestCase
from taxi.forms import DriverCreationForm
from taxi.models import Manufacturer, Car, Driver


class FormsTest(TestCase):
    def test_check_valid_creation_form(self):
        data1 = {
            "username": "user1",
            "password1": "12376gsda",
            "password2": "12376gsda",
            "first_name": "Testing name",
            "last_name": "Testing last",
            "license_number": "ACD12345",
        }
        form = DriverCreationForm(data=data1)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data1)


class SearchTest(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create(
            username="testdriver1",
            first_name="Asdcs",
            last_name="Fnejkns",
            license_number="RTS12387"
        )
        self.driver2 = Driver.objects.create(
            username="testdriver2",
            first_name="Asdac",
            last_name="Fnejkngn",
            license_number="RTS12388"
        )

        self.manufacturer1 = Manufacturer.objects.create(
            name="Test manufacturer1",
            country="France",
        )

        self.manufacturer2 = Manufacturer.objects.create(
            name="Test manufacturer2",
            country="France",
        )

        self.car1 = Car.objects.create(
            model="Test1",
            manufacturer=self.manufacturer1,
        )
        self.car2 = Car.objects.create(
            model="Test2",
            manufacturer=self.manufacturer2,
        )

    def test_driver_search(self):
        response = self.client.get(
            "/drivers/",
            {"username": "testdriver1"},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testdriver1")
        self.assertNotContains(response, "testdriver2")

    def test_car_search(self):
        response = self.client.get(
            "/cars/",
            {"model": "TestCar1"},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestCar1")
        self.assertNotContains(response, "TestCar2")

    def test_manufacturer_search(self):
        response = self.client.get(
            "/manufacturers/",
            {"name": "TestManufacturer1"},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestManufacturer1")
