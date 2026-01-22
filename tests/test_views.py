from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
CARS_URL = reverse("taxi:car-list")
DRIVERS_URL = reverse("taxi:driver-list")


class PublicManufacturerTests(TestCase):

    def test_login_required(self):
        res = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):

    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="Test",
            password="test1234",
            first_name="Te",
            last_name="St",
            license_number="ABC12345"
        )
        self.client.force_login(self.driver)

        Manufacturer.objects.create(
            name="Test",
            country="Testland"
        )
        Manufacturer.objects.create(
            name="Test2",
            country="Testland2"
        )

    def test_retrieve_manufacturer(self):

        response = self.client.get(MANUFACTURERS_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer(self):
        result = self.client.get(MANUFACTURERS_URL + "?name=Test")

        self.assertContains(result, "Test")
        self.assertNotContains(result, "NoTest")


class PublicCarTests(TestCase):

    def test_login_required(self):
        res = self.client.get(CARS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):

    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="Test",
            password="test1234",
            first_name="Te",
            last_name="St",
            license_number="ABC12345"
        )
        self.client.force_login(self.driver)
        test_manufacturer_1 = Manufacturer.objects.create(
            name="Testa1",
            country="Testland1"
        )
        test_manufacturer_2 = Manufacturer.objects.create(
            name="Testa2",
            country="Testland2"
        )
        Car.objects.create(
            model="Test_tesla_1",
            manufacturer=test_manufacturer_1
        )
        Car.objects.create(
            model="Test_tesla_2",
            manufacturer=test_manufacturer_2
        )

    def test_retrieve_car(self):

        response = self.client.get(CARS_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_car(self):
        search_data = {"model": "tesla"}
        response = self.client.get(CARS_URL, data=search_data)
        car = Car.objects.filter(model__icontains="tesla")

        self.assertEqual(
            list(response.context["car_list"]),
            list(car)
        )


class PublicDriverTests(TestCase):

    def test_login_required(self):
        res = self.client.get(DRIVERS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self):
        Driver.objects.create(
            username="test1",
            first_name="Te1",
            last_name="St2",
            license_number="QWE12345"
        )
        Driver.objects.create(
            username="test2",
            first_name="Te2",
            last_name="St2",
            license_number="КЕН67890",
        )
        self.driver = get_user_model().objects.create_user(
            username="Test",
            password="test1234",
            first_name="Te",
            last_name="St",
            license_number="ABC12345"
        )
        self.client.force_login(self.driver)

    def test_retrieve_driver(self):
        response = self.client.get(DRIVERS_URL)
        driver_list = Driver.objects.all()

        self.assertEqual(
            response.status_code,
            200
        )
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver_list)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_driver_detail(self):
        response = self.client.get(DRIVERS_URL + "1/")

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertTemplateUsed(
            response,
            "taxi/driver_detail.html"
        )

    def test_search_driver_form(self):
        search_data = {"username": "test"}
        response = self.client.get(DRIVERS_URL, data=search_data)
        driver = get_user_model().objects.filter(username__icontains="test")

        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver)
        )
        self.assertNotEqual(
            list(response.context["driver_list"]),
            ["tesla", "tesla1", "tesla2", "tesla3"]
        )
