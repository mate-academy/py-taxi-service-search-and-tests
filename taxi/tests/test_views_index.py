from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_index_view(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to Best Taxi Ever!")

    def test_index_view_with_session(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have visited this page")
        self.assertContains(response, "1 time.")

    def test_index_view_with_logged_out_user(self):
        self.client.logout()
        url = reverse("taxi:index")
        response = self.client.get(url)
        login_url = reverse("login")
        self.assertRedirects(response, login_url + "?next=" + url)
