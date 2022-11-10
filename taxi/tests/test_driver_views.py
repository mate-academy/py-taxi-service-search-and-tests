from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

DRIVERS_URL = reverse("taxi:driver-list")


class PublicCarsTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVERS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCarsTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="testuser", password="test123user"
        )

        self.client.force_login(self.driver)

    def test_retrieve_cars(self):
        drivers = get_user_model().objects.all()

        response = self.client.get(DRIVERS_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_car_listed(self):
        self.driver.license_number = "AAA12345"
        self.driver.first_name = "Bobik"
        self.driver.last_name = "Sdoh"
        self.driver.save()

        response = self.client.get(DRIVERS_URL)

        for value in [
            self.driver.id,
            self.driver.username,
            self.driver.first_name,
            self.driver.last_name,
            self.driver.license_number,
        ]:
            self.assertContains(response, value)
