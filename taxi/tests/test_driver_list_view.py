from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver


class TestManufacturerListView(TestCase):
    def setUp(self):
        self.driver_1 = get_user_model().objects.create_user(
            username="Bob", password="pass67890", license_number="1234"
        )
        self.driver_2 = get_user_model().objects.create_user(
            username="Alice", password="pass67890", license_number="4567"
        )
        self.driver_3 = get_user_model().objects.create_user(
            username="Marline", password="pass67890", license_number="7890"
        )

        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )

    def test_search_field(self):
        self.client.force_login(self.user)
        get_value = "Mar"
        url = reverse("taxi:driver-list") + f"?username={get_value}"
        response = self.client.get(url)
        driver_query = Driver.objects.filter(username__icontains=get_value)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]),
                         list(driver_query))

    def test_login_required(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)

        self.assertNotEquals(response.status_code, 200)
