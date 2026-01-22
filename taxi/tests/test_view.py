from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

DRIVER_LIST_URL = reverse("taxi:driver-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")


class PublicViewTests(TestCase):
    def test_login_required(self):
        driver = self.client.get(DRIVER_LIST_URL)
        manufacturer = self.client.get(MANUFACTURER_LIST_URL)
        car = self.client.get(CAR_LIST_URL)
        self.assertNotEquals(driver.status_code, 200)
        self.assertNotEquals(manufacturer.status_code, 200)
        self.assertNotEquals(car.status_code, 200)


class PrivateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_pass"
        )
        self.client.force_login(self.user)

    def test_retrieve_view(self):
        driver = self.client.get(DRIVER_LIST_URL)
        manufacturer = self.client.get(MANUFACTURER_LIST_URL)
        car = self.client.get(CAR_LIST_URL)
        self.assertEqual(driver.status_code, 200)
        self.assertEqual(manufacturer.status_code, 200)
        self.assertEqual(car.status_code, 200)
