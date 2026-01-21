from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")


class PublicCarViewTest(TestCase):
    def test_login_required(self):
        """
        Test that login is required to access the car page
        """
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        """
        Test that login is required to access the car page
        """
        manufacturer = Manufacturer.objects.create(name="test_manufacturer",
                                                   country="test_country")
        Car.objects.create(model="test_model_1", manufacturer=manufacturer)
        Car.objects.create(model="test_model_2", manufacturer=manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
        )
        self.assertTemplateUsed(
            response, "taxi/car_list.html"
        )
