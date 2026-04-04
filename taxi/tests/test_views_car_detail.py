from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class CarDetailViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testuser1",
        )
        self.client.force_login(self.user)
        manufacture = Manufacturer.objects.create(name="Test")
        self.car = Car.objects.create(model="X", manufacturer=manufacture)

    def test_detail_existing_returns_200(self):
        response = self.client.get(
            reverse(
                "taxi:car-detail",
                kwargs={"pk": self.car.pk}
            ))
        self.assertEqual(response.status_code, 200)

    def test_nonexistent_returns_404(self):
        response = self.client.get(
            reverse(
                "taxi:car-detail",
                kwargs={"pk": 999}
            ))
        self.assertEqual(response.status_code, 404)
