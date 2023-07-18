from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver


DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def test_list_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertNotEquals(response.status_code, 200)


class PrivateDriverrTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer_count = 3

        for i in range(manufacturer_count):
            Driver.objects.create(
                username=f"user{i}",
                password=f"password{i}",
                license_number=f"NDS1234{i}"
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_LIST_URL)
        drivers = Driver.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_driver_list_search_by_username(self):
        search_value = "2"
        response = self.client.get(
            DRIVER_LIST_URL,
            {"user_name": search_value}
        )
        drivers = Driver.objects.filter(username__icontains=search_value)

        self.assertQuerysetEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
