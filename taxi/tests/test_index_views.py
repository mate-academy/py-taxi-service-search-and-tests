from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class HomePageTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="Test", password="Testpass123"
        )

    def test_public_home_page_login_required(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(response.status_code, 200)

    def test_private_home_page(self):
        self.client.force_login(self.driver)
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")
