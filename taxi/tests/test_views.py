from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

DRIVERS_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
DRIVERS_DETAIL_URL = reverse("taxi:driver-detail",
                             kwargs={"pk": 1})
CARS_DETAIL_URL = reverse("taxi:car-detail",
                          kwargs={"pk": 1})


class PublicViewTests(TestCase):
    def test_list_login_required_list(self):
        tests = [DRIVERS_URL, CARS_URL, MANUFACTURERS_URL]
        for test in tests:
            res = self.client.get(test)
            self.assertNotEqual(res.status_code, 200)

    def test_detail_login_required_list(self):
        tests = [
            DRIVERS_DETAIL_URL,
            CARS_DETAIL_URL
        ]
        for test in tests:
            res = self.client.get(test)
            self.assertNotEqual(res.status_code, 200)


class PrivateViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password"
        )
        self.client.force_login(self.user)

    def test_logged_in_page_view(self):
        manufacturer = Manufacturer.objects.create(
            name="Ford"
        )
        Car.objects.create(
            model="Mustang",
            manufacturer=manufacturer
        )
        tests = [
            self.client.get(MANUFACTURERS_URL),
            self.client.get(CARS_URL)
        ]

        for test in tests:
            self.assertEqual(test.status_code, 200)
