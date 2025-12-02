from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class PublicDriverListViewTests(TestCase):
    def test_login_required(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)

        login_url = reverse("login")
        self.assertRedirects(response, f"{login_url}?next={url}")


class PrivateBaseTestCase(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test.user",
            password="testpass123",
            license_number="TES12345",
        )
        self.client.force_login(self.user)

        self.manufacturer_1 = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        self.manufacturer_2 = Manufacturer.objects.create(
            name="Mercedes",
            country="Germany",
        )

        self.car_1 = Car.objects.create(
            model="Model X",
            manufacturer=self.manufacturer_1,
        )
        self.car_2 = Car.objects.create(
            model="Super Model",
            manufacturer=self.manufacturer_2,
        )
        self.car_3 = Car.objects.create(
            model="Corsa",
            manufacturer=self.manufacturer_1,
        )

        self.driver_1 = get_user_model().objects.create_user(
            username="john.smith",
            password="pass12345",
            license_number="DRI12345",
        )
        self.driver_2 = get_user_model().objects.create_user(
            username="johnny",
            password="pass12345",
            license_number="DRI23456",
        )
        self.driver_3 = get_user_model().objects.create_user(
            username="alice",
            password="pass12345",
            license_number="DRI34567",
        )


class IndexViewTests(PrivateBaseTestCase):
    def test_index_context_counts(self):
        url = reverse("taxi:index")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_cars"], 3)
        self.assertEqual(response.context["num_drivers"], 4)
        self.assertEqual(response.context["num_manufacturers"], 2)

    def test_index_visits_counter(self):
        url = reverse("taxi:index")

        response_1 = self.client.get(url)
        self.assertEqual(response_1.context["num_visits"], 1)

        response_2 = self.client.get(url)
        self.assertEqual(response_2.context["num_visits"], 2)


class DriverSearchTests(PrivateBaseTestCase):
    def test_driver_list_without_search_returns_all(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        driver_list = response.context["driver_list"]

        self.assertEqual(driver_list.count(), 4)
        self.assertIn(self.driver_1, driver_list)
        self.assertIn(self.driver_2, driver_list)
        self.assertIn(self.driver_3, driver_list)
        self.assertIn(self.user, driver_list)

    def test_driver_search_by_username(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "john"})

        self.assertEqual(response.status_code, 200)
        driver_list = response.context["driver_list"]

        self.assertIn(self.driver_1, driver_list)
        self.assertIn(self.driver_2, driver_list)
        self.assertNotIn(self.driver_3, driver_list)
        self.assertNotIn(self.user, driver_list)


class CarSearchTests(PrivateBaseTestCase):
    def test_car_list_without_search_returns_all(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        car_list = response.context["car_list"]

        self.assertEqual(car_list.count(), 3)
        self.assertIn(self.car_1, car_list)
        self.assertIn(self.car_2, car_list)
        self.assertIn(self.car_3, car_list)

    def test_car_search_by_model(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "Model"})

        self.assertEqual(response.status_code, 200)
        car_list = response.context["car_list"]

        self.assertIn(self.car_1, car_list)
        self.assertIn(self.car_2, car_list)
        self.assertNotIn(self.car_3, car_list)


class ManufacturerSearchTests(PrivateBaseTestCase):
    def test_manufacturer_list_without_search_returns_all(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        manufacturer_list = response.context["manufacturer_list"]

        self.assertEqual(manufacturer_list.count(), 2)
        self.assertIn(self.manufacturer_1, manufacturer_list)
        self.assertIn(self.manufacturer_2, manufacturer_list)

    def test_manufacturer_search_by_name(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "mer"})

        self.assertEqual(response.status_code, 200)
        manufacturer_list = response.context["manufacturer_list"]

        self.assertIn(self.manufacturer_2, manufacturer_list)
        self.assertNotIn(self.manufacturer_1, manufacturer_list)
