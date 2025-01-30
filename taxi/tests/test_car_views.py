from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car


class CarTest(TestCase):
    def setUp(self) -> None:
        self.driver1 = get_user_model().objects.create_user(
            username="skywalker",
            password="force123!@#",
            first_name="Zephyr",
            last_name="Blake",
            license_number="XYZ92476"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="stormrider",
            password="thunder&lightning88",
            first_name="Atlas",
            last_name="Knight",
            license_number="RDR45678"
        )
        self.driver3 = get_user_model().objects.create_user(
            username="moonwatcher",
            password="starlight$99",
            first_name="Phoenix",
            last_name="Storm",
            license_number="MW13579"
        )
        self.client.force_login(self.driver1)

        self.man1 = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.man2 = Manufacturer.objects.create(
            name="Tesla", country="USA")
        self.man3 = Manufacturer.objects.create(
            name="Tata Motors", country="India")

        self.car1 = Car.objects.create(model="Novus", manufacturer=self.man3)
        self.car2 = Car.objects.create(model="Model Y", manufacturer=self.man2)
        self.car1.drivers.add(self.driver1)
        self.car2.drivers.add(self.driver2, self.driver3)

    def test_car_without_searching(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertNotIn("Yaris", content)
        self.assertIn("Novus", content)
        self.assertIn("Model Y", content)

    def test_search(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "O"})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("Tesla", content)
        self.assertIn("Model Y", content)

    def test_car_detail_page(self):
        response = self.client.get(
            reverse("taxi:car-detail", args=[self.car2.id]))
        self.assertEqual(response.status_code, 200)
