from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class DriverTest(TestCase):
    def setUp(self) -> None:
        self.driver1 = get_user_model().objects.create_user(
            username="panjaby",
            password="lkj456_&^%",
            first_name="Radj",
            last_name="Mallah",
            license_number="OIU78543"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="speedster",
            password="fast&furious99",
            first_name="Vin",
            last_name="Diesel",
            license_number="SPD12345"
        )

        self.driver3 = get_user_model().objects.create_user(
            username="driftking",
            password="tokyoDrift!",
            first_name="Takashi",
            last_name="Fujimoto",
            license_number="DK67890"
        )

        self.driver4 = get_user_model().objects.create_user(
            username="taximaster",
            password="uber4life$",
            first_name="John",
            last_name="Wheeler",
            license_number="TXI56789"
        )

        self.driver5 = get_user_model().objects.create_user(
            username="nightdriver",
            password="midnightRacer*",
            first_name="Eleanor",
            last_name="Shelby",
            license_number="NDR24680"
        )
        self.client.force_login(self.driver1)
        self.client.force_login(self.driver2)
        self.client.force_login(self.driver3)
        self.client.force_login(self.driver4)
        self.client.force_login(self.driver5)

    def test_drivers_list_without_searching(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Eleanor")
        self.assertContains(response, "Fujimoto")
        self.assertContains(response, "SPD12345")
        self.assertContains(response, "panjaby")

        self.assertNotContains(response, "uber4life$")

    def test_search(self):
        self.assertContains(
            self.client.get(
                reverse("taxi:driver-list"),
                {"username": "king"},
            ), "driftking"
        )

    def test_driver_page(self):
        res = self.client.get(
            reverse(
                "taxi:driver-detail",
                args=[self.driver5.id]
            )
        )
        self.assertEqual(res.status_code, 200)
