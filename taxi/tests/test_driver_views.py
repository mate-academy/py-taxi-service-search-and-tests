from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverViewsTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="driver",
            email="<EMAIL>",
            password="<PASSWORD>",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)

        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers),
        )
        self.assertTemplateUsed(
            response,
            "taxi/driver_list.html"
        )

    def test_driver_search(self):
        Driver.objects.create(
            username="shell.don",
            password="<PASSWORD>",
            first_name="Sheldon",
            last_name="Cooper",
            license_number="ABC02345",

        )
        Driver.objects.create(
            username="leon.hof",
            password="<PASSWORD>",
            first_name="Leonard",
            last_name="Hofstadter",
            license_number="HJK90658",

        )
        driver = Driver.objects.filter(username="shell.don")
        response = self.client.get(f"{DRIVER_URL}?username=shell.don")
        self.assertEqual(list(response.context["driver_list"]), list(driver))
