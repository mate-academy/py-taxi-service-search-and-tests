from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car

DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
INDEX_URL = reverse("taxi:index")
TOGGLE_ASSIGN_URL = "taxi:toggle-car-assign"


class PublicDriverListViewTest(TestCase):
    """ Checking if a page is visible to unauthorized users"""

    def test_login_required(self):
        self.assertNotEqual(
            self.client.get(DRIVER_URL).status_code,
            200
        )
        self.assertNotEqual(
            self.client.get(CAR_URL).status_code,
            200
        )
        self.assertNotEqual(
            self.client.get(MANUFACTURER_URL).status_code,
            200
        )


class PrivateDriverListViewTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="TestUserName",
            password="Test123",
        )
        self.client.force_login(self.user)
        self.driver = Driver.objects.create(
            username="Driver",
            password="Test123",
            license_number="ABC12345"
        )
        self.manufacturer = Manufacturer.objects.create(name="Manufacturer")
        self.car = Car.objects.create(
            model="CarModel",
            manufacturer=self.manufacturer
        )

    """ Checking if a page is visible to authorized users """

    def test_authorized_users(self) -> None:
        self.assertEqual(
            self.client.get(DRIVER_URL).status_code, 200)
        self.assertEqual(
            self.client.get(CAR_URL).status_code, 200)
        self.assertEqual(
            self.client.get(MANUFACTURER_URL).status_code, 200)

    """ Checking the correct operation of the search form """

    def test_search(self) -> None:
        self.assertContains(self.client.get(
            DRIVER_URL, {"search_query": "Driver"}), "Driver")
        self.assertContains(self.client.get(
            CAR_URL, {"search_query": "Car"}), "Car")
        self.assertContains(self.client.get(
            MANUFACTURER_URL, {"search_query": "Manufacturer"}),
            "Manufacturer")

        self.assertNotContains(self.client.get(
            DRIVER_URL, {"search_query": "Driver"}), "Driver1")
        self.assertNotContains(self.client.get(
            CAR_URL, {"search_query": "Car"}), "Car1")
        self.assertNotContains(self.client.get(
            MANUFACTURER_URL, {"search_query": "Manufacturer"}),
            "Manufacturer1")

    """ Checking the correct operation of sessions on the main page """

    def test_home_page(self) -> None:
        session = self.client.session
        session["num_visits"] = 0
        session.save()

        response = self.client.get(INDEX_URL)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Taxi Service Home")
        self.assertContains(response, "You have visited this page")
        self.assertContains(response, str(response.context["num_visits"]))

        self.assertIn("num_visits", response.context)
        self.assertEqual(response.context["num_visits"], 1)
