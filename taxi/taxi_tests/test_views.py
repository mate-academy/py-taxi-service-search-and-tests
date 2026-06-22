from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testUser",
            password="test123",
        )

    def test_index_page_counter_increments(self):
        self.client.force_login(self.user)
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertEqual(response.context["num_visits"], 1)
        response = self.client.get(url)
        self.assertEqual(response.context["num_visits"], 2)


class SearchViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="driver123",
            license_number="AAA11111"
        )
        self.client.force_login(self.user)

        self.m1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.m2 = Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )

        self.car1 = Car.objects.create(
            model="Model S",
            manufacturer=self.m2,
        )
        self.car2 = Car.objects.create(
            model="Camry",
            manufacturer=self.m1,
        )

    def test_manufacturer_search(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "Toy"})
        self.assertContains(response, self.m1.name)
        self.assertNotContains(response, self.m2.name)

    def test_car_search(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "Model"})
        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)

    def test_driver_search(self):
        url = reverse("taxi:driver-list")
        get_user_model().objects.create_user(
            username="john",
            password="password123",
            license_number="BBB22222",  # ІНША ліцензія!
        )
        response = self.client.get(url, {"username": "driver"})
        self.assertContains(response, self.user.username)
        self.assertNotContains(response, "john")


class ToggleAssignmentTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testUser",
            password="test123",
            license_number="AAA11111"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Manufacturer1",
            country="Anonym1",
        )
        self.car = Car.objects.create(
            model="copyM1",
            manufacturer=self.manufacturer,
        )

        self.url = reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": self.car.pk}
        )

    def test_toggle_assign_adds_and_removes_driver(self):
        self.assertNotIn(self.user, self.car.drivers.all())

        self.client.get(self.url)
        self.car.refresh_from_db()
        self.assertIn(self.user, self.car.drivers.all())

        self.client.get(self.url)
        self.car.refresh_from_db()
        self.assertNotIn(self.user, self.car.drivers.all())


class SecurityTests(TestCase):
    def test_anonymous_user_redirected_to_login(self):
        url = reverse("taxi:car-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)
