from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class PublicIndexViewsTest(TestCase):
    def test_index_login_required(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateIndexViewsTest(TestCase):
    def setUp(self):
        driver = get_user_model().objects.create_user(
            first_name="First",
            last_name="Last",
            username="Username",
            license_number="AAA12345",
            password="1qaz3edc",
        )
        self.client.force_login(driver)

    def test_visits_counter(self):
        url = reverse("taxi:index")

        # First visit
        response = self.client.get(url)
        self.assertEqual(response.context["num_visits"], 1)

        # Second visit
        response = self.client.get(url)
        self.assertEqual(response.context["num_visits"], 2)
