from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from taxi.models import Car, Manufacturer


class CarViewTest(TestCase):
    def setUp(self):
        self.url = reverse_lazy("taxi:index")
        self.user = get_user_model().objects.create_user(
            username="usertest",
            password="testpassword456",
        )

    def test_login_required_views(self):
        response = self.client.get(self.url)
        expected_url = f"/accounts/login/?next={self.url}"

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, expected_url)

    def test_index_context(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(
            response.context["num_drivers"], get_user_model().objects.count()
        )
        self.assertEqual(response.context["num_cars"], Car.objects.count())
        self.assertEqual(
            response.context["num_manufacturers"], Manufacturer.objects.count()
        )
        self.assertEqual(response.context["num_visits"], 1)
