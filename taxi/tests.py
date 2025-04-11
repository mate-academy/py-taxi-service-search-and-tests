from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car, Driver


class ModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )

        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="test12345",
            first_name="Test",
            last_name="Driver",
            license_number="ABC12345"
        )

        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_driver_str(self):
        expected = (
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )
        self.assertEqual(str(self.driver), expected)

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)

    def test_driver_car_relation(self):
        self.assertIn(self.car, self.driver.cars.all())
        self.assertIn(self.driver, self.car.drivers.all())


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="test12345",
            first_name="Test",
            last_name="Driver",
            license_number="ABC12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer
        )

        self.client.force_login(self.driver)

    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<strong>Cars:</strong> 1")
        self.assertContains(response, "<strong>Drivers:</strong> 1")
        self.assertContains(response, "<strong>Manufacturers:</strong> 1")

    def test_manufacturer_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer.name)
        self.assertContains(response, self.manufacturer.country)

    def test_car_list_view(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.model)
        self.assertContains(response, self.manufacturer.name)

    def test_driver_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver.username)
        self.assertContains(response, self.driver.license_number)


class SearchTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.driver1 = get_user_model().objects.create_user(
            username="johndoe",
            password="test12345",
            license_number="ABC12345"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="janedoe",
            password="test12345",
            license_number="XYZ67890"
        )

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Focus",
            manufacturer=self.manufacturer2
        )

        self.client.force_login(self.driver1)

    def test_driver_search(self):
        url = reverse("taxi:driver-list") + "?username=john"
        response = self.client.get(url)
        self.assertContains(response, "johndoe")
        self.assertNotContains(response, "janedoe")

        url = reverse("taxi:driver-list") + "?username=nonexistent"
        response = self.client.get(url)
        self.assertNotContains(response, "ABC12345")
        self.assertNotContains(response, "XYZ67890")
        self.assertContains(response, "There are no drivers in the service")

        url = reverse("taxi:driver-list") + "?username="
        response = self.client.get(url)
        self.assertContains(response, "johndoe")
        self.assertContains(response, "janedoe")

    def test_car_search(self):
        url = reverse("taxi:car-list") + "?model=Cor"
        response = self.client.get(url)
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Focus")

        url = reverse("taxi:car-list") + "?model=nonexistent"
        response = self.client.get(url)
        self.assertNotContains(response, "Corolla")
        self.assertNotContains(response, "Focus")

        url = reverse("taxi:car-list") + "?model="
        response = self.client.get(url)
        self.assertContains(response, "Corolla")
        self.assertContains(response, "Focus")

    def test_manufacturer_search(self):
        url = reverse("taxi:manufacturer-list") + "?name=Toy"
        response = self.client.get(url)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

        url = reverse("taxi:manufacturer-list") + "?name=nonexistent"
        response = self.client.get(url)
        self.assertNotContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

        url = reverse("taxi:manufacturer-list") + "?name="
        response = self.client.get(url)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Ford")
