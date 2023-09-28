from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver


class TaxiViewsTest(TestCase):
    def setUp(self) -> None:
        self.driver = Driver.objects.create(
            username="riceman",
            password="ChinaIsTheBest",
            first_name="BimBim",
            last_name="BamBam",
            license_number="ABC12345"
        )

    def test_login_user_access(self) -> None:
        self.client.force_login(self.driver)
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_not_login_user_denied(self) -> None:
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 302)
