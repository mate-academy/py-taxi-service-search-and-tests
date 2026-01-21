from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Car, Manufacturer


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="<PASSWORD>",
        )

        self.client.force_login(self.user)

    def test_search(self) -> None:
        test_manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )

        Car.objects.bulk_create([
            Car(model="AAA Test1", manufacturer=test_manufacturer),
            Car(model="AAA Test2", manufacturer=test_manufacturer),
            Car(model="BBB Test1", manufacturer=test_manufacturer),
            Car(model="BBB Test2", manufacturer=test_manufacturer),
        ])

        res = self.client.get(
            reverse("taxi:car-list"),
            {"title": "AAA"}
        )

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "AAA Test1")
        self.assertContains(res, "AAA Test2")
        self.assertNotContains(res, "BBB Test1")
        self.assertNotContains(res, "BBB Test2")
