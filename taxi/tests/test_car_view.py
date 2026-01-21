from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarViewTest(TestCase):
    def test_login_required_car(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Ukraine"
        )
        Car.objects.create(model="Test_car", manufacturer=manufacturer)
        Car.objects.create(model="Test_car2", manufacturer=manufacturer)
        res = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["car_list"]), list(cars))
