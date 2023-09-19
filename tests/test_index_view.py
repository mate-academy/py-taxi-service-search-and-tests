from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

INDEX_VIEW = "/"


class PublicCarTest(TestCase):
    def test_index_page_requires_login(self):
        response = self.client.get(INDEX_VIEW)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="Nissan Motor Co.",
            country="Japan"
        )
        Car.objects.create(model="Nissan X-Trail", manufacturer=manufacturer)
        Car.objects.create(model="Nissan JUKE", manufacturer=manufacturer)
        get_user_model().objects.create(
            username="john_doe",
            password="john123doe",
            license_number="JOH12345"
        )
        get_user_model().objects.create(
            username="jack_black",
            password="jack123black",
            license_number="JAC12345"
        )

    def setUp(self) -> None:
        user = get_user_model().objects.create(
            username="test_user",
            password="test123user"
        )
        self.client.force_login(user)

    def test_retrieve_index_page(self):
        response = self.client.get(INDEX_VIEW)
        num_drivers = get_user_model().objects.count()
        num_cars = Car.objects.count()
        num_manufacturers = Manufacturer.objects.count()
        num_visits = 1

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_drivers"], num_drivers)
        self.assertEqual(response.context["num_cars"], num_cars)
        self.assertEqual(
            response.context["num_manufacturers"],
            num_manufacturers
        )
        self.assertEqual(response.context["num_visits"], num_visits)

    def test_retrieve_index_page_by_name(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
