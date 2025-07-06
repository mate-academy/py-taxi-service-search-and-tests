from django.test import Client
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import (Manufacturer,
                         Car,
                         Driver)

Manufacturer_Format_URL = reverse("taxi:manufacturer-list")
Driver_Format_URL = reverse("taxi:driver-list")
Car_Format_URL = reverse("taxi:car-list")


class PublicViewsTest(TestCase):
    def test_login_required_for_manufacturer_and_driver(self):
        urls = [
            Manufacturer_Format_URL,
            Driver_Format_URL,
            Car_Format_URL,
        ]
        for url in urls:
            res = self.client.get(url)
            self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Manufacturer 1", country="country1")
        Manufacturer.objects.create(name="Manufacturer 2", country="country2")
        response = self.client.get(Manufacturer_Format_URL)
        self.assertEqual(response.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer_filters_queryset(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")
        response = self.client.get(Manufacturer_Format_URL, {"name": "bm"})
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Audi")


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test First",
            "last_name": "Test Last",
            "license_number": "DFG12345",
        }
        res = self.client.post(reverse("taxi:driver-create"), data=form_data)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(
            username=form_data["username"]).exists())

    def test_search_driver_filters_queryset(self):
        Driver.objects.create_user(
            username="admin", password="Ge12349", license_number="LIC12345"
        )
        Driver.objects.create_user(
            username="asasha", password="test369", license_number="LIC98765"
        )

        response = self.client.get(Driver_Format_URL, {"username": "ad"})
        self.assertContains(response, "admin")
        self.assertNotContains(response, "asasha")


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_search_car_filters_queryset(self):
        manufacturer = Manufacturer.objects.create(name="Toyota",
                                                   country="Japan")
        Car.objects.create(model="Lexus 150", manufacturer=manufacturer)
        Car.objects.create(model="Lexus 120", manufacturer=manufacturer)
        response = self.client.get(Car_Format_URL, {"model": "Lexus 15"})
        self.assertContains(response, "Lexus 150")
        self.assertNotContains(response, "Lexus 120")
