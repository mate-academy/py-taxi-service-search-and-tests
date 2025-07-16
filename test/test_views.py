from django.contrib.auth import get_user_model
from django.test import (
    TestCase,
    Client
)
from django.urls import reverse


class ViewsUnauthorizedTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_car_list(self) -> None:
        url = reverse("taxi:car-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_car_create(self) -> None:
        url = reverse("taxi:car-create")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_driver_list(self) -> None:
        url = reverse("taxi:driver-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_list(self) -> None:
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_create(self) -> None:
        url = reverse("taxi:manufacturer-create")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class ViewsAuthorizedTest(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create(
            username="admin",
            password="<PASSWORD>",
            email="<EMAIL>",
            first_name="Admin",
            last_name="Admin",
        )
        self.client.force_login(self.admin)

    def test_car_list(self) -> None:
        url = reverse("taxi:car-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_car_create(self) -> None:
        url = reverse("taxi:car-create")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_driver_list(self) -> None:
        url = reverse("taxi:driver-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_list(self) -> None:
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_create(self) -> None:
        url = reverse("taxi:manufacturer-create")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
