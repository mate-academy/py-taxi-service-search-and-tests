from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicListViewTests(TestCase):
    def test_login_required_for_view_driver_list(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_for_view_manufacturer_list(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_for_view_car_list(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateListViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password"
        )
        self.client.force_login(self.user)

    def test_login_required_for_view_driver_list(self):
        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 200)

    def test_login_required_for_view_manufacturer_list(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(res.status_code, 200)

    def test_login_required_for_view_car_list(self):
        res = self.client.get(CAR_URL)
        self.assertEqual(res.status_code, 200)


class ContextRetrieveSearchTests(TestCase):
    def setUp(self) -> None:
        names = ["one", "two", "three", "four", "five"]
        for name in names:
            manufacturer_instance = Manufacturer.objects.create(
                name="manufacturer_" + name,
                country="Some_country",
            )
            Car.objects.create(
                model="car_" + name,
                manufacturer=manufacturer_instance,
            )
            Driver.objects.create_user(
                username="driver_username_" + name,
                password="Some_password",
                license_number=name,
            )
        self.user = Driver.objects.first()
        self.client.force_login(self.user)

    def test_index_view_rule_count_all(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["num_manufacturers"],
            Manufacturer.objects.count()
        )
        self.assertEqual(response.context["num_cars"], Car.objects.count())
        self.assertEqual(
            response.context["num_drivers"],
            Driver.objects.count()
        )

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_retrieve_cars(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_manufacturer_search(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "o"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "one")
        self.assertContains(response, "two")
        self.assertContains(response, "four")
        self.assertNotContains(response, "three")
        self.assertNotContains(response, "five")

    def test_car_search(self):
        response = self.client.get(CAR_URL, {"model": "o"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "one")
        self.assertContains(response, "two")
        self.assertContains(response, "four")
        self.assertNotContains(response, "three")
        self.assertNotContains(response, "five")

    def test_driver_search(self):
        response = self.client.get(DRIVER_URL, {"username": "o"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "one")
        self.assertContains(response, "two")
        self.assertContains(response, "four")
        self.assertNotContains(response, "three")
        self.assertNotContains(response, "five")
