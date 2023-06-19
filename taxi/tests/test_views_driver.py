from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def test_driver_list(self) -> None:
        result = self.client.get(DRIVER_LIST_URL)

        self.assertNotEquals(result.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_driver_list(self) -> None:
        Driver.objects.create(
            username="test1",
            license_number="TES12345"
        )
        Driver.objects.create(
            username="test2",
            license_number="TES12343"
        )

        result = self.client.get(DRIVER_LIST_URL)

        self.assertEquals(result.status_code, 200)
        self.assertEquals(
            list(result.context["driver_list"]),
            list(Driver.objects.all())
        )
