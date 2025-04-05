from django.test import TestCase
from django.urls import reverse


class TestView(TestCase):
    def test_driver_list_login_required(self) -> None:
        url = reverse("taxi:driver-list")
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)

    def test_cars_list_login_required(self) -> None:
        url = reverse("taxi:car-list")
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)

    def test_manufacturers_list_login_required(self) -> None:
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)
