from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer, Car


class FromTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="superuser",
            password="password",
            license_number="QWE12323"
        )
        self.client.force_login(user=user)

    def test_manufacturer_search_form(self):
        form_data = {
            "name": "Manufacturer",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_create_form(self):
        form_data = {
            "name": "Manufacturer",
            "country": "USA",
        }
        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)
        self.assertEqual(len(Manufacturer.objects.all()), 1)
        manufacturer = Manufacturer.objects.get(name="Manufacturer")
        self.assertEqual(manufacturer.name, form_data["name"])
        self.assertEqual(manufacturer.country, form_data["country"])

    def test_search_by_manufacturer_form(self):
        url = reverse("taxi:manufacturer-list")
        Manufacturer.objects.create(name="1", country="USA")
        Manufacturer.objects.create(name="2", country="USA")
        Manufacturer.objects.create(name="31", country="USA")
        res = self.client.get(url, data={"name": "1"})
        self.assertEqual(len(res.context["manufacturer_list"]), 2)

    def test_search_by_car_form(self):
        url = reverse("taxi:car-list")
        test_manufacturer = Manufacturer.objects.create(name="test", country="USA")
        Car.objects.create(manufacturer=test_manufacturer, model="test")
        Car.objects.create(manufacturer=test_manufacturer, model="tset")
        res = self.client.get(url, data={"model": "test"})
        self.assertEqual(len(res.context["car_list"]), 1)

    def test_search_by_driver_form(self):
        url = reverse("taxi:driver-list")
        get_user_model().objects.create_user(
            username="user",
            password="password",
        )
        res = self.client.get(url, data={"username": "superuser"})
        self.assertEqual(len(res.context["driver_list"]), 1)
