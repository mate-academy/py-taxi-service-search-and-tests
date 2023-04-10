from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from taxi.models import Manufacturer, Car
from taxi.forms import ManufacturerSearchForm, CarSearchForm, DriverSearchForm


class SearchFormsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="test1234"
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA",
        )

    def test_manufacturer_get_context_data_with_search_form(self):
        url = "/manufacturers/"
        data = {"name": "Toyota"}

        response = self.client.get(url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context["search_form"],
            ManufacturerSearchForm
        )
        self.assertEqual(
            response.context["search_form"].initial["name"],
            "Toyota"
        )
    
    def test_car_get_context_data_with_search_form(self):
        self.car1 = Car.objects.create(
            model="Toyota Yaris",
            manufacturer=self.manufacturer1,
        )
        self.car2 = Car.objects.create(
            model="Ford Focus",
            manufacturer=self.manufacturer2,
        )

        url = "/cars/"
        data = {"model": "Toyota"}

        response = self.client.get(url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context["search_form"],
            CarSearchForm
        )
        self.assertEqual(
            response.context["search_form"].initial["model"],
            "Toyota"
        )
        
    def test_driver_get_context_data_with_search_form(self):
        self.driver1 = get_user_model().objects.create_user(
            username="admin101",
            password="admin3476",
            license_number="ADM19087"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="best.driver",
            password="super.driver",
            license_number="ADM19088"
        )

        url = "/drivers/"
        data = {"username": "admin"}

        response = self.client.get(url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context["search_form"],
            DriverSearchForm
        )
        self.assertEqual(
            response.context["search_form"].initial["username"],
            "admin"
        )
