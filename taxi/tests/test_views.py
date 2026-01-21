from django.contrib.auth import get_user_model
from django.urls import reverse

from django.test import TestCase

from taxi.models import Manufacturer, Car


class PublicManufacturerViewTest(TestCase):

    def test_manufacturer_login_required(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testUser",
            email="email@email.com",
            password="password",
            license_number="AAA55555",
        )
        self.manufacturer_first = Manufacturer.objects.create(
            country="FirstTestCountry",
            name="FirstTestManufacturer",
        )
        self.manufacturer_second = Manufacturer.objects.create(
            country="SecondTestCountry",
            name="SecondTestManufacturer",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):

        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturers(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "FirstTestManufacturer"}
        )
        self.assertContains(response, self.manufacturer_first.name)
        self.assertNotContains(response, self.manufacturer_second.name)


class PublicCarsViewTest(TestCase):

    def test_manufacturer_login_required(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarsViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testUser",
            email="email@email.com",
            password="password",
            license_number="AAA55555",
        )
        manufacturer = Manufacturer.objects.create(
            country="TestCountry",
            name="TestManufacturer",
        )
        self.first_car = Car.objects.create(
            manufacturer=manufacturer,
            model="FirstTestModel",
        )
        self.second_car = Car.objects.create(
            manufacturer=manufacturer,
            model="SecondTestModel",
        )
        self.first_car.drivers.set([self.user])
        self.second_car.drivers.set([self.user])
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_cars(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "FirstTestModel"}
        )
        self.assertContains(response, self.first_car.model)
        self.assertNotContains(response, self.second_car.model)


class PublicDriversViewTest(TestCase):
    def test_driver_login_required(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriversViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testUser",
            email="email@email.com",
            password="password",
            license_number="AAA55555",
        )
        self.manufacturer = Manufacturer.objects.create(
            country="TestCountry",
            name="TestManufacturer",
        )
