from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer
from taxi.views import toggle_assign_to_car

DRIVERS_LIST_URL = [
    reverse("taxi:driver-list"),
    reverse("taxi:car-list"),
    reverse("taxi:manufacturer-list"),
    reverse("taxi:driver-detail", kwargs={"pk": 1}),
    reverse("taxi:car-detail", kwargs={"pk": 1}),
]


class PublicViewsTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        for url in DRIVERS_LIST_URL:
            response = self.client.get(url)

            self.assertNotEqual(response.status_code, 200)


class DriverLoggedInViewsTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )

        self.car = Car.objects.create(
            model="Test Car", manufacturer=self.manufacturer
        )

        self.driver = Driver.objects.create(
            username="testdriver",
            first_name="Test",
            last_name="Driver",
        )

        self.client.force_login(self.driver)

    def test_retrieve_all_pages(self):
        for url in DRIVERS_LIST_URL:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_toggle_assign_to_car_adds_car(self):
        self.assertNotIn(self.car, self.driver.cars.all())

        request = self.factory.get(
            reverse(
                "taxi:toggle-car-assign",
                kwargs={"pk": self.car.id}
            )
        )

        request.user = self.driver
        response = toggle_assign_to_car(request, self.car.id)
        self.assertEqual(response.status_code, 302)

        self.assertIn(self.car, self.driver.cars.all())

    def test_toggle_assign_to_car_removes_car(self):
        self.car.drivers.add(self.driver)

        self.assertIn(self.car, self.driver.cars.all())

        request = self.factory.get(
            reverse(
                "taxi:toggle-car-assign", kwargs={"pk": self.car.id}
            )
        )
        request.user = self.driver

        response = toggle_assign_to_car(request, self.car.id)
        self.assertEqual(response.status_code, 302)

        self.assertNotIn(self.car, self.driver.cars.all())
