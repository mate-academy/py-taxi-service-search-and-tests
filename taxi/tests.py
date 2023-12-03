from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Driver
from .forms import SearchForm


class DriverListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

        self.driver1 = Driver.objects.create(
            username="testuser1",
            first_name="John",
            last_name="Doe",
            license_number="12345",
        )
        self.driver2 = Driver.objects.create(
            username="testuser2",
            first_name="Jane",
            last_name="Doe",
            license_number="67890",
        )

    def test_search_view_with_results(self):
        search_query = "testuser1"
        response = self.client.get(
            reverse("taxi:driver-list"), {"search": search_query}
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn("search_form", response.context)

        self.assertIsInstance(response.context["search_form"], SearchForm)

        self.assertIn(self.driver1, response.context["driver_list"])

        self.assertContains(response, self.driver1.username)
        self.assertContains(response, self.driver1.first_name)
        self.assertContains(response, self.driver1.last_name)

    def test_search_view_with_no_results(self):
        search_query = "nonexistentuser"
        response = self.client.get(
            reverse("taxi:driver-list"), {"search": search_query}
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn("search_form", response.context)

        self.assertIsInstance(response.context["search_form"], SearchForm)

        self.assertQuerysetEqual(response.context["driver_list"], [])

        self.assertContains(response, "There are no drivers in the service.")

    def test_search_view_with_empty_query(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 200)

        self.assertIn("search_form", response.context)

        self.assertIsInstance(response.context["search_form"], SearchForm)

        self.assertIn(self.driver1, response.context["driver_list"])
        self.assertIn(self.driver2, response.context["driver_list"])

        self.assertContains(response, self.driver1.username)
        self.assertContains(response, self.driver2.username)

        def test_license_display(self):
            response = self.client.get(reverse("taxi:driver-list"))

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, self.driver1.license_number)
            self.assertContains(response, self.driver2.license_number)

    def test_no_license_display(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "InvalidLicense123")

    def test_authenticated_user_access(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.driver1, response.context["driver_list"])
        self.assertIn(self.driver2, response.context["driver_list"])
        self.assertContains(response, self.driver1.username)
        self.assertContains(response, self.driver2.username)

    def test_non_authenticated_user_access(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f'/accounts/login/?next={reverse("taxi:driver-list")}'
        )
