from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car, Driver

User = get_user_model()


class SearchFeatureTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            password="secret"
        )
        self.client = Client()
        self.client.login(username="testuser", password="secret")

        self.manufacturer1 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="Fiat",
            country="Italy"
        )

        self.car1 = Car.objects.create(
            model="Mustang",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer2
        )
        self.car3 = Car.objects.create(
            model="Punto",
            manufacturer=self.manufacturer3
        )

        self.driver1 = Driver.objects.create_user(
            username="alice",
            password="secret",
            license_number="ABC12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="bob",
            password="secret",
            license_number="DEF67890"
        )
        self.driver3 = Driver.objects.create_user(
            username="charlie",
            password="secret",
            license_number="GHI13579"
        )

    def test_manufacturer_search(self) -> None:
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"q": "toy"})
        self.assertEqual(response.status_code, 200)
        manufacturer_list = response.context["manufacturer_list"]
        self.assertEqual(len(manufacturer_list), 1)
        self.assertEqual(manufacturer_list[0].name, "Toyota")

    def test_car_search(self) -> None:
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"q": "must"})
        self.assertEqual(response.status_code, 200)
        car_list = response.context["object_list"]
        self.assertEqual(len(car_list), 1)
        self.assertEqual(car_list[0].model, "Mustang")

    def test_driver_search(self) -> None:
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"q": "ali"})
        self.assertEqual(response.status_code, 200)
        driver_list = response.context["object_list"]
        self.assertEqual(len(driver_list), 1)
        self.assertEqual(driver_list[0].username, "alice")

    def test_empty_search_returns_all(self) -> None:
        m_url = reverse("taxi:manufacturer-list")
        c_url = reverse("taxi:car-list")
        d_url = reverse("taxi:driver-list")

        response_m = self.client.get(m_url)
        response_c = self.client.get(c_url)
        response_d = self.client.get(d_url)

        self.assertEqual(len(response_m.context["manufacturer_list"]), 3)
        self.assertEqual(len(response_c.context["object_list"]), 3)
        self.assertEqual(len(response_d.context["object_list"]), 4)
