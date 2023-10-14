from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


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


class ToggleAssignToCarViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username="testuser", password="testpass")

        self.manufacturer = Manufacturer.objects.create(name="TestManufacturer", country="TestCountry")
        self.car = Car.objects.create(model="TestCar", manufacturer=self.manufacturer)
        self.client.login(username="testuser", password="testpass")

    def test_add_car_to_driver(self):
        self.client.get(reverse("taxi:toggle-car-assign", args=[self.car.id]))
        self.user.refresh_from_db()
        self.assertIn(self.car, self.user.cars.all())

    def test_remove_car_from_driver(self):
        self.user.cars.add(self.car)
        self.client.get(reverse("taxi:toggle-car-assign", args=[self.car.id]))
        self.user.refresh_from_db()
        self.assertNotIn(self.car, self.user.cars.all())

    def test_redirect_after_toggle(self):
        response = self.client.get(reverse("taxi:toggle-car-assign", args=[self.car.id]))
        self.assertRedirects(response, reverse("taxi:car-detail", args=[self.car.id]))