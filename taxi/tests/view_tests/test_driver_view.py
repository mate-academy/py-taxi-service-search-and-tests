from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


DRIVERS_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVERS_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_access(self):
        response = self.client.get(DRIVERS_URL)
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(DRIVERS_URL)
        self.assertTemplateUsed(
            response,
            "taxi/driver_list.html"
        )

    def test_filter(self):
        response = self.client.get(f"{DRIVERS_URL}?username=Yura")
        self.assertQuerysetEqual(
            response.context["driver_list"],
            get_user_model().objects.filter(
                username__icontains="Yura"
            )
        )
