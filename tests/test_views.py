from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

HOME_URL = reverse("taxi:index")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
DRIVERS_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")


class PublicTaxiViewsTest(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get(HOME_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturers_page_status_code(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_drivers_page_status_code(self):
        response = self.client.get(DRIVERS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_cars_page_status_code(self):
        response = self.client.get(CARS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTaxiViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin",
            license_number="QWE12345"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )
        self.car = Car.objects.create(
            model="Test Model", manufacturer=self.manufacturer
        )
        self.user.cars.add(self.car)
        self.client.force_login(self.user)

    def test_driver_list_view(self):
        get_user_model().objects.create_user(
            username="admin2",
            password="admin2",
            license_number="JON26231",
        )
        response = self.client.get(DRIVERS_URL)
        drivers = get_user_model().objects.all()
        self.assertEqual(list(response.context["object_list"]), list(drivers))

    def test_car_detail_view(self):
        response = self.client.get(
            reverse(
                "taxi:car-detail",
                args=[self.car.pk]
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Model")

    def test_driver_detail_view(self):
        response = self.client.get(
            reverse(
                "taxi:driver-detail",
                args=[self.user.pk]
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "admin")
