from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class CarAccessTestUnlogged(TestCase):

    def test_access_car_list_without_login(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))


class InvalidLoginTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="correctpassword"
        )

    def test_invalid_password(self):
        url = reverse("login")
        response = self.client.post(
            url, {"username": "testuser", "password": "wrongpassword"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Please enter a correct username and password."
        )

    class InvalidLoginTest(TestCase):

        def setUp(self):
            self.user = get_user_model().objects.create_user(
                username="testuser", password="1234"
            )

        def test_invalid_password(self):
            url = reverse("login")
            response = self.client.post(
                url, {"username": "testuser", "password": "password"}
            )

            self.assertEqual(response.status_code, 200)
            self.assertContains(
                response, "Please enter a correct username and password."
            )
