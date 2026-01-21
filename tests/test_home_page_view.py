from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

HOME_PAGE_URL = reverse("taxi:index")


class PublicHomePageTests(TestCase):
    def test_login_required(self):
        response = self.client.get(HOME_PAGE_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateHomePageTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="AAA12345",
            first_name="Admin",
            last_name="User",
            password="1qwerty2",
        )
        self.client.force_login(self.user)

    def test_index_count_content_correctly(self):
        response = self.client.get(reverse("taxi:index"))
        num_drivers = get_user_model().objects.count()
        num_cars = Car.objects.count()
        num_manufacturers = Manufacturer.objects.count()

        self.assertContains(response, "Taxi Service Home")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")
        self.assertEqual(response.context["num_drivers"], num_drivers)
        self.assertEqual(response.context["num_cars"], num_cars)
        self.assertEqual(
            response.context["num_manufacturers"],
            num_manufacturers
        )
