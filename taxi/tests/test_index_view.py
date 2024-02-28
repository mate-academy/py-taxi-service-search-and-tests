from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

INDEX_URL = reverse("taxi:index")


class PublicIndexViewTests(TestCase):
    def test_index_view_login_required(self):
        response = self.client.get(INDEX_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateIndexViewTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Bumga Gamga",
            country="Poltava"
        )
        self.user = get_user_model().objects.create_user(
            username="fastDominik",
            password="Pa$$wor9",
            license_number="WIN12213"
        )
        self.car = Car.objects.create(
            manufacturer=self.manufacturer,
            model="Boeing"
        )
        self.client.force_login(self.user)

    def test_index_response_logged_in(self):
        response = self.client.get(INDEX_URL)
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_correct_index_stats(self):
        response = self.client.get(INDEX_URL)
        all_manufacturers = Manufacturer.objects.all()
        all_drivers = get_user_model().objects.all()
        all_cars = Car.objects.all()

        self.assertEqual(
            response.context["num_manufacturers"],
            all_manufacturers.count()
        )
        self.assertEqual(
            response.context["num_drivers"],
            all_drivers.count()
        )
        self.assertEqual(
            response.context["num_cars"],
            all_cars.count()
        )
