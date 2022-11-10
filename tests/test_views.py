from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicDriverTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(DRIVER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "test123645",
        )

        self.client.force_login(self.user)

    def test_retrieve_drivers_list(self):
        get_user_model().objects.create(
            username="test_name",
            first_name="test_first",
            last_name="test_last",
            license_number="SAF12536",
        )

        response = self.client.get(DRIVER_URL)
        drivers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_create_driver(self):
        initial_data = {
            "username": "test_username",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "SAF12536",
            "password1": "test12568",
            "password2": "test12568",
        }

        self.client.post(reverse("taxi:driver-create"), data=initial_data)
        new_user = get_user_model().objects.get(
            username=initial_data["username"]
        )

        self.assertEqual(new_user.first_name, "test_first")
        self.assertEqual(new_user.last_name, "test_last")
        self.assertEqual(new_user.license_number, "SAF12536")

    def test_car_search_form(self):
        response = self.client.get(CAR_URL + "?model=Yar")
        car = Car.objects.filter(model__icontains="Yar")

        self.assertEqual(
            list(response.context["car_list"]),
            list(car)
        )

    def test_driver_search_form(self):
        response = self.client.get(DRIVER_URL + "?username=opp")
        driver = get_user_model().objects.filter(username__icontains="opp")

        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver)
        )

    def test_manufacturer_search_form(self):
        response = self.client.get(MANUFACTURER_URL + "?name=Toy")
        manufacturer = Manufacturer.objects.filter(name__icontains="Toy")

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
