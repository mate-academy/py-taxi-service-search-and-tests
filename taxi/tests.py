from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Manufacturer, Car, Driver

User = get_user_model()


class SearchAndAssignTests(TestCase):
    def setUp(self):
        self.m_toyota = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.m_ford = Manufacturer.objects.create(
            name="Ford", country="USA"
        )

        self.car_corolla = Car.objects.create(
            model="Corolla", manufacturer=self.m_toyota
        )
        self.car_focus = Car.objects.create(
            model="Focus", manufacturer=self.m_ford
        )
        self.car_camry = Car.objects.create(
            model="Camry", manufacturer=self.m_toyota
        )

        self.driver_alice = Driver.objects.create_user(
            username="alice",
            first_name="Alice",
            last_name="Wonder",
            password="pass",
            license_number="ABC123",
        )
        self.driver_bob = Driver.objects.create_user(
            username="bob",
            first_name="Bob",
            last_name="Builder",
            password="pass",
            license_number="XYZ789",
        )

        self.car_focus.drivers.add(self.driver_bob)

    def test_driver_search_by_username(self):
        url = reverse("taxi:driver-list")
        resp = self.client.get(url, {"q": "ali"})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "alice")
        self.assertNotContains(resp, "bob")

    def test_driver_search_by_first_or_last_name(self):
        url = reverse("taxi:driver-list")
        resp = self.client.get(url, {"q": "Wonder"})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "alice")
        self.assertNotContains(resp, "bob")

    def test_car_search_by_model(self):
        url = reverse("taxi:car-list")
        resp = self.client.get(url, {"q": "Cor"})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Corolla")
        self.assertNotContains(resp, "Focus")

    def test_car_search_by_manufacturer_name(self):
        url = reverse("taxi:car-list")
        resp = self.client.get(url, {"q": "Toyota"})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Corolla")
        self.assertContains(resp, "Camry")
        self.assertNotContains(resp, "Focus")

    def test_manufacturer_search_by_name(self):
        url = reverse("taxi:manufacturer-list")
        resp = self.client.get(url, {"q": "For"})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Ford")
        self.assertNotContains(resp, "Toyota")

    def test_search_no_query_returns_all(self):
        url = reverse("taxi:driver-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "alice")
        self.assertContains(resp, "bob")

        url = reverse("taxi:car-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Corolla")
        self.assertContains(resp, "Focus")
        self.assertContains(resp, "Camry")

    def test_search_no_results_shows_empty(self):
        url = reverse("taxi:car-list")
        resp = self.client.get(url, {"q": "ZZZZ"})
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, "Corolla")
        self.assertNotContains(resp, "Focus")
        self.assertNotContains(resp, "Camry")

    def test_toggle_assign_to_car_requires_auth(self):
        url = reverse("taxi:toggle-car-assign", kwargs={"pk": self.car_corolla.pk})
        resp = self.client.post(url)
        self.assertIn(resp.status_code, (302, 403))

    def test_toggle_assign_to_car_assigns_and_unassigns(self):
        self.client.login(username="alice", password="pass")
        url = reverse("taxi:toggle-car-assign", kwargs={"pk": self.car_corolla.pk})

        resp = self.client.post(url, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.car_corolla.refresh_from_db()
        self.assertIn(self.driver_alice, self.car_corolla.drivers.all())

        resp = self.client.post(url, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.car_corolla.refresh_from_db()
        self.assertNotIn(self.driver_alice, self.car_corolla.drivers.all())

    def test_existing_assignment_remains_for_other_driver(self):
        self.assertIn(self.driver_bob, self.car_focus.drivers.all())

        self.client.login(username="alice", password="pass")
        url = reverse("taxi:toggle-car-assign", kwargs={"pk": self.car_focus.pk})
        resp = self.client.post(url, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.driver_bob, self.car_focus.drivers.all())
        self.assertIn(self.driver_alice, self.car_focus.drivers.all())
