from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class SearchTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="Aa1234554321",
            license_number="ABC01234",
        )
        self.client.force_login(self.admin_user)
        self.driver_one = Driver.objects.create(
            username="driver_one",
            password="Aa1234554321",
            license_number="ABC11111",
        )
        self.driver_one_one = Driver.objects.create(
            username="driver_one_one",
            password="Aa1234554321",
            license_number="ABC22222",
        )
        self.manufacturer_one = Manufacturer.objects.create(
            name="Manufacturer_one",
            country="Ukraine",
        )
        self.manufacturer_two = Manufacturer.objects.create(
            name="Manufacturer_two",
            country="Ukraine",
        )
        self.manufacturer_one_one = Manufacturer.objects.create(
            name="Manufacturer_one_one",
            country="Ukraine",
        )
        self.car_one = Car.objects.create(
            manufacturer=self.manufacturer_one,
            model="Car_one"
        )
        self.car_one.drivers.add(self.admin_user)
        self.car_two = Car.objects.create(
            manufacturer=self.manufacturer_one,
            model="Car_two"
        )
        self.car_two.drivers.add(self.driver_one)
        self.car_two_one = Car.objects.create(
            manufacturer=self.manufacturer_one,
            model="Car_two_one"
        )
        self.car_two_one.drivers.add(self.driver_one)

    def test_search_car(self):
        url = reverse("taxi:car-list")
        key_search_word = "two"
        response = self.client.get(url, {"title": key_search_word})
        search = Car.objects.filter(model__icontains=key_search_word)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(search))

    def test_search_driver(self):
        url = reverse("taxi:driver-list")
        key_search_word = "one"
        response = self.client.get(url, {"title": key_search_word})
        search = Driver.objects.filter(username__icontains=key_search_word)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(search)
        )

    def test_search_manufacturer(self):
        url = reverse("taxi:manufacturer-list")
        key_search_word = "one"
        response = self.client.get(url, {"title": key_search_word})
        search = Manufacturer.objects.filter(name__icontains=key_search_word)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(search)
        )
