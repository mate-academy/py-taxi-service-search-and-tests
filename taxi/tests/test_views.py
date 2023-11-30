from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TaxiIndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)


class ViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )
        self.client.login(username="testuser", password="12345")

    def test_manufacturer_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_car_list_view(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

    def test_driver_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_access(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertIn(response.status_code, [403, 302])
