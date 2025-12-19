from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Manufacturer, Car, Driver


class TaxiServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer1 = Manufacturer.objects.create(name="Toyota")
        cls.manufacturer2 = Manufacturer.objects.create(name="BMW")
        cls.car1 = Car.objects.create(
            model="Camry",
            manufacturer=cls.manufacturer1
        )
        cls.car2 = Car.objects.create(
            model="X5",
            manufacturer=cls.manufacturer2
        )
        cls.driver1 = get_user_model().objects.create_user(
            username="bober1",
            password="pass",
            license_number="ABC12345"
        )
        cls.driver2 = get_user_model().objects.create_user(
            username="bober2",
            password="pass",
            license_number="DEF67890"
        )
        cls.car1.drivers.add(cls.driver1)

    def test_car_list_view(self):
        self.client.login(username="bober1", password="pass")
        response = self.client.get(reverse("taxi:car-list"))
        self.assertContains(response, "Camry")
        self.assertContains(response, "X5")

    def test_car_detail_view(self):
        self.client.login(username="bober1", password="pass")
        response = self.client.get(
            reverse("taxi:car-detail", args=[self.car1.id])
        )
        self.assertContains(response, "Camry")

    def test_driver_list_view(self):
        self.client.login(username="bober1", password="pass")
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertContains(response, "bober1")
        self.assertContains(response, "bober2")

    def test_driver_detail_view(self):
        self.client.login(username="bober1", password="pass")
        response = self.client.get(
            reverse("taxi:driver-detail", args=[self.driver1.id])
        )
        self.assertContains(response, "bober1")

    def test_manufacturer_list_view(self):
        self.client.login(username="bober1", password="pass")
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertContains(response, "Toyota")
        self.assertContains(response, "BMW")

    def test_search_car_exact_match(self):
        self.client.login(username="bober1", password="pass")
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Camry"}
        )
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "X5")

    def test_search_car_no_match(self):
        self.client.login(username="bober1", password="pass")
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Corolla"}
        )
        self.assertNotContains(response, "Camry")
        self.assertNotContains(response, "X5")

    def test_search_driver_partial_match(self):
        self.client.login(username="bober1", password="pass")
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "bober"}
        )
        self.assertContains(response, "bober1")
        self.assertContains(response, "bober2")

    def test_search_driver_no_match(self):
        self.client.login(username="bober1", password="pass")
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "alice"}
        )
        driver_usernames = [
            d.username for d in response.context["object_list"]
        ]
        self.assertNotIn("alice", driver_usernames)

    def test_toggle_assign_to_car_add_remove(self):
        self.client.login(username="bober2", password="pass")
        url = reverse("taxi:toggle-car-assign", args=[self.car2.id])
        self.client.get(url)
        self.assertIn(self.car2, self.driver2.cars.all())
        self.client.get(url)
        self.assertNotIn(self.car2, self.driver2.cars.all())

    def test_search_manufacturer_exact_match(self):
        self.client.login(username="bober1", password="pass")
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Toyota"}
        )
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")

    def test_search_manufacturer_partial_match(self):
        self.client.login(username="bober1", password="pass")
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "To"}
        )
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")

    def test_search_manufacturer_no_match(self):
        self.client.login(username="bober1", password="pass")
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Honda"}
        )
        manufacturer_names = [
            m.name for m in response.context["object_list"]
        ]
        self.assertNotIn("Honda", manufacturer_names)
