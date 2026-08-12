from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer


class BaseTaxiTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = "test.driver"
        self.password = "password123"
        self.user = Driver.objects.create_user(
            username=self.username, password=self.password
        )
        self.client.force_login(self.user)


class DriverSearchTest(BaseTaxiTestCase):

    def setUp(self):
        super().setUp()

        self.test_driver_1 = "Alice"
        self.test_driver_2 = "Bob"
        self.license_1 = "ABC12345"
        self.license_2 = "XYZ98765"
        self.search_query = "Ali"
        self.url = reverse("taxi:driver-list")

        Driver.objects.create_user(
            username=self.test_driver_1,
            password=self.password,
            license_number=self.license_1,
        )
        Driver.objects.create_user(
            username=self.test_driver_2,
            password=self.password,
            license_number=self.license_2,
        )

    def test_driver_search_by_username(self):
        response = self.client.get(self.url, {"username": self.search_query})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.test_driver_1)
        self.assertNotContains(response, self.test_driver_2)


class CarSearchTest(BaseTaxiTestCase):

    def setUp(self):
        super().setUp()

        self.test_manufacturer_1 = "Toyota"
        self.test_car_1 = "Corolla"
        self.test_car_2 = "Camry"
        self.search_query = "Coro"
        self.url = reverse("taxi:car-list")

        manufacturer = Manufacturer.objects.create(
            name=self.test_manufacturer_1,
            country="Japan",
        )

        Car.objects.create(
            model=self.test_car_1,
            manufacturer=manufacturer
        )
        Car.objects.create(
            model=self.test_car_2,
            manufacturer=manufacturer
        )

    def test_car_search_by_model(self):
        response = self.client.get(
            self.url,
            {"model": self.search_query}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.test_car_1)
        self.assertNotContains(response, self.test_car_2)


class ManufacturerSearchTest(BaseTaxiTestCase):

    def setUp(self):
        super().setUp()

        self.test_manufacturer_1 = "Toyota"
        self.test_manufacturer_2 = "BIAC"

        self.manufacturer_country = "Japan"

        self.search_query = "Toyo"
        self.url = reverse("taxi:manufacturer-list")

        Manufacturer.objects.create(
            name=self.test_manufacturer_1,
            country=self.manufacturer_country
        )
        Manufacturer.objects.create(
            name=self.test_manufacturer_2,
            country=self.manufacturer_country
        )

    def test_manufacturer_search_by_name(self):
        response = self.client.get(
            self.url,
            {"name": self.search_query}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.test_manufacturer_1)
        self.assertNotContains(response, self.test_manufacturer_2)
