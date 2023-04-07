from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver


class PublicTests(TestCase):
    def test_login_required_index(self):
        res = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_list(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "pass1234567"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver_list(self):
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver12345",
            license_number="test_license",
        )

        response = self.client.get(reverse("taxi:driver-list"))

        drivers = Driver.objects.all()
        print(Driver.objects.all())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
