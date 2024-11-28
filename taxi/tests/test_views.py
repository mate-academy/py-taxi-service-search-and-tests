from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

INDEX = reverse("taxi:index")
CAR = reverse("taxi:car-list")
MANUFACTURER = reverse("taxi:manufacturer-list")
DRIVER = reverse("taxi:driver-list")
CAR_DETAIL = reverse("taxi:car-detail", args=[1])


class IndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get(INDEX)
        self.assertEqual(response.status_code, 302)


class CarViewTest(TestCase):
    def test_login_required_for_list_view(self):
        response = self.client.get(CAR)
        self.assertEqual(response.status_code, 302)

    def test_login_required_for_detail_view(self):
        response = self.client.get(CAR_DETAIL)
        self.assertEqual(response.status_code, 302)


class ManufacturerViewTest(TestCase):
    def test_login_required_for_list_view(self):
        response = self.client.get(MANUFACTURER)
        self.assertEqual(response.status_code, 302)


class DriverViewTest(TestCase):
    def test_login_required_for_list_view(self):
        response = self.client.get(DRIVER)
        self.assertEqual(response.status_code, 302)
