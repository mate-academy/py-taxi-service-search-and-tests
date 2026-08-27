from django.urls import reverse
from taxi.models import Driver
from django.contrib.auth import get_user_model
from django.test import TestCase, Client


class PublicDriverTest(TestCase):
    DRIVER_URL = reverse("taxi:driver-list")

    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(self.DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    DRIVER_URL = reverse("taxi:driver-list")

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="bogdanchik",
            password="bbb1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        get_user_model().objects.create(
            username="driver",
            password="bog1234",
            first_name="Bohdan",
            last_name="Bielyi",
            license_number="BBB11111",
        )
        get_user_model().objects.create(
            username="roman",
            password="dri1234",
            first_name="Roman",
            last_name="Bielyi",
            license_number="AAA11111",
        )
        response = self.client.get(self.DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            response.context["driver_list"],
            list(drivers)
        )
        self.assertTemplateUsed(
            response,
            "taxi/driver_list.html"
        )

    def test_search_driver(self):
        get_user_model().objects.create(
            username="driver",
            password="bog1234",
            first_name="Bohdan",
            last_name="Bielyi",
            license_number="BBB11111",
        )
        get_user_model().objects.create(
            username="roman",
            password="dri1234",
            first_name="Roman",
            last_name="Bielyi",
            license_number="AAA11111",
        )
        response = self.client.get(self.DRIVER_URL, {"username": "driver"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver")
        self.assertNotContains(response, "roman")
