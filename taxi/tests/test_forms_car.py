from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")


class CarSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Car.objects.create(model="X3", manufacturer=manufacturer)
        Car.objects.create(model="M4", manufacturer=manufacturer)
        Car.objects.create(model="Y5", manufacturer=manufacturer)

    def test_search_without_query(self):
        res = self.client.get(CAR_URL)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "X3")
        self.assertContains(res, "M4")
        self.assertContains(res, "Y5")

    def test_search_with_correct_query(self):
        res = self.client.get(CAR_URL, {"model": "X"})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "X3")
        self.assertNotContains(res, "M4")
        self.assertNotContains(res, "Y5")

    def test_search_with_wrong_query(self):
        res = self.client.get(CAR_URL, {"model": "YYY"})
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "X3")
        self.assertNotContains(res, "M4")
        self.assertNotContains(res, "Y5")
