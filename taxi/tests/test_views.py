from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from taxi.models import Manufacturer, Car


class ViewSearchTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123",
            license_number="ZZZ99999"
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )

        self.car1 = Car.objects.create(
            model="X5", manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="A4", manufacturer=self.manufacturer2
        )

        self.driver2 = get_user_model().objects.create_user(
            username="johndoe",
            password="password123",
            license_number="YYY88888"
        )

    def test_manufacturer_search(self) -> None:
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "BM"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            self.manufacturer1,
            response.context["manufacturer_list"]
        )
        self.assertNotIn(
            self.manufacturer2,
            response.context["manufacturer_list"]
        )

    def test_car_search(self) -> None:
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "X5"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.car1, response.context["car_list"])
        self.assertNotIn(self.car2, response.context["car_list"])

    def test_driver_search(self) -> None:
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "john"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.driver2, response.context["driver_list"])
        self.assertNotIn(self.user, response.context["driver_list"])


class ToggleAssignToCarTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="password123",
            license_number="AAA11111"
        )
        self.client.force_login(self.driver)
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        self.car = Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer
        )

    def test_toggle_assign_adds_car(self) -> None:
        url = reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": self.car.pk}
        )

        self.assertEqual(self.driver.cars.count(), 0)

        response = self.client.post(url)

        self.assertRedirects(response, reverse(
            "taxi:car-detail",
            kwargs={"pk": self.car.pk}
        ))
        self.assertEqual(self.driver.cars.count(), 1)
        self.assertIn(self.car, self.driver.cars.all())

    def test_toggle_assign_removes_car(self) -> None:
        self.driver.cars.add(self.car)
        self.assertEqual(self.driver.cars.count(), 1)

        url = reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": self.car.pk}
        )

        self.client.post(url)

        self.assertEqual(self.driver.cars.count(), 0)
        self.assertNotIn(self.car, self.driver.cars.all())
