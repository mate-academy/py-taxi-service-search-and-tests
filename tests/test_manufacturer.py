from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


URL_CAR_LIST = "taxi:car-list"
URL_DRIVER_LIST = "taxi:driver-list"
URL_MANUFACTURER_LIST = "taxi:manufacturer-list"


class PublicManufacturerViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="1234",
        )

    def test_manufacturer_login_required(self):
        response = self.client.get(reverse(URL_MANUFACTURER_LIST))

        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse(URL_MANUFACTURER_LIST)}"
        )


class PublicCarViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="1234",
        )

    def test_car_login_required(self):
        response = self.client.get(reverse(URL_CAR_LIST))

        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse(URL_CAR_LIST)}"
        )


class PublicDriverViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="1234",
        )

    def test_driver_login_required(self):
        response = self.client.get(reverse(URL_DRIVER_LIST))

        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse(URL_DRIVER_LIST)}"
        )
