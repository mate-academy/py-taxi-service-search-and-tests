from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer

INDEX_URL = reverse("taxi:index")


class PublicIndexTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(INDEX_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateIndexTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="Test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_index(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)

    def test_index_content(self):
        manufacturer_test = Manufacturer.objects.create(
            name="Test",
            country="Test country",
        )
        car = Car.objects.create(
            model="Test model",
            manufacturer=manufacturer_test,
        )
        car.drivers.set((self.user, ))
        num_drivers = Driver.objects.count()
        num_cars = Car.objects.count()
        num_manufacturers = Manufacturer.objects.count()

        response = self.client.get(INDEX_URL)
        num_visits = response.client.session["num_visits"]

        self.assertEqual(response.context["num_drivers"], num_drivers)
        self.assertEqual(response.context["num_cars"], num_cars)
        self.assertEqual(
            response.context["num_manufacturers"],
            num_manufacturers
        )
        self.assertEqual(response.context["num_visits"], num_visits)

    def test_index_template(self):
        response = self.client.get(INDEX_URL)
        self.assertTemplateUsed(response, "taxi/index.html")
