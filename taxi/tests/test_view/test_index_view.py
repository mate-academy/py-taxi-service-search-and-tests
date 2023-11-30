from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

URL_INDEX = reverse("taxi:index")


class PublicIndexView(TestCase):
    def test_index_login(self):
        response = self.client.get(URL_INDEX)
        self.assertNotEqual(response.status_code, 200)


class PrivateIndexView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345",
        )

        self.client.force_login(self.user)

    def test_visit_index(self):
        for count_visit in range(1, 10):
            response = self.client.get(URL_INDEX)
            self.assertEqual(response.context["num_visits"], count_visit)

    def test_context_index(self):
        get_user_model().objects.create_user(
            username="test123",
            password="test123",
            license_number="TES12431"
        )
        manufacturer1 = Manufacturer.objects.create(
            name="test",
            country="test_country",
        )
        Manufacturer.objects.create(
            name="test2",
            country="test_country2"
        )
        Car.objects.create(
            manufacturer=manufacturer1,
            model="test_model",
        )
        response = self.client.get(URL_INDEX)
        self.assertEqual(
            response.context["num_drivers"], get_user_model().objects.count()
        )
        self.assertEqual(
            response.context["num_cars"], Car.objects.count()
        )
        self.assertEqual(
            response.context["num_manufacturers"], Manufacturer.objects.count()
        )
