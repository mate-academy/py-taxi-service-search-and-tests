from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

INDEX_URL = reverse("taxi:index")


class PublicIndexViewTests(TestCase):
    def test_access_not_logged_in_users(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateIndexViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer
        )

    def test_index_view_displays_stats(self):
        res = self.client.get(INDEX_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["num_drivers"], 1)
        self.assertEqual(res.context["num_cars"], 1)
        self.assertEqual(res.context["num_manufacturers"], 1)
        self.assertTemplateUsed(res, "taxi/index.html")

    def test_index_view_tracks_visits(self):
        res1 = self.client.get(INDEX_URL)
        self.assertEqual(res1.context["num_visits"], 1)

        res2 = self.client.get(INDEX_URL)
        self.assertEqual(res2.context["num_visits"], 2)
