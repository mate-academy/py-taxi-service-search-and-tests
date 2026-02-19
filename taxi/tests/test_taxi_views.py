from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class PublicViewsTests(TestCase):
    def test_home_page(self) -> None:
        url = reverse("taxi:index")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_driver_list_page(self) -> None:
        url = reverse("taxi:driver-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_car_list_page(self) -> None:
        url = reverse("taxi:car-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_list_page(self) -> None:
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateViewsTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin.test",
            email="admin@admin.com",
            password="testpassword",
        )
        self.client.force_login(self.admin_user)

    def test_home_page(self) -> None:
        url = reverse("taxi:index")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_driver_list_page(self) -> None:
        url = reverse("taxi:driver-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_car_list_page(self) -> None:
        url = reverse("taxi:car-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_list_page(self) -> None:
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
