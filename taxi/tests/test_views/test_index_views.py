from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

INDEX_URL = reverse("taxi:index")


class PublicIndexViewTest(TestCase):
    def test_index_view_login_required(self):
        response = self.client.get(INDEX_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_unauthenticated_redirect_to_login(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, INDEX_URL + "//accounts/login/?next=/"
        )


class PrivateIndexViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            license_number="test_license",
            password="test1234",
        )

        self.client.force_login(self.user)

    def test_index_view_returns_correct_template(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_index_view_context_data(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("num_drivers" in response.context)
        self.assertTrue("num_cars" in response.context)
        self.assertTrue("num_manufacturers" in response.context)
        self.assertTrue("num_visits" in response.context)

    def test_index_view_session_counter(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["num_visits"], 1)

        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["num_visits"], 2)
