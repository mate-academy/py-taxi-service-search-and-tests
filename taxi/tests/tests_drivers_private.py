from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Driver


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="<PASSWORD>",
        )

        self.client.force_login(self.user)

    def test_search(self) -> None:
        password = "<PASSWORD>"

        Driver.objects.bulk_create([
            Driver(username="AAA Test1", password=password),
            Driver(username="AAA Test2", password=password),
            Driver(username="BBB Test1", password=password),
            Driver(username="BBB Test2", password=password),
        ])

        res = self.client.get(
            reverse("taxi:driver-list"),
            {"title": "AAA"}
        )

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "AAA Test1")
        self.assertContains(res, "AAA Test2")
        self.assertNotContains(res, "BBB Test1")
        self.assertNotContains(res, "BBB Test2")
