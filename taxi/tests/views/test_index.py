from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer

INDEX_URL = reverse("taxi:index")


class PublicIndexViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(INDEX_URL)
        self.assertTrue(response.status_code, 401)


class PrivateIndexViewTest(TestCase):
    def setUp(self):
        bmw = Manufacturer.objects.create(name="BMW", country="Germany")
        audi = Manufacturer.objects.create(name="AUDI", country="Germany")
        Car.objects.create(model="M5", manufacturer=bmw)
        Car.objects.create(model="A6", manufacturer=audi)

        user = get_user_model().objects.create_user(
            username="test user",
            password="test pass"
        )

        self.client.force_login(user)

    def test_valid_response(self):
        response = self.client.get(INDEX_URL)
        self.assertTrue(response.status_code, 200)

        expected_num_drivers = Driver.objects.count()
        expected_num_cars = Car.objects.count()
        expected_num_manufacturers = Manufacturer.objects.count()

        self.assertEqual(response.context["num_drivers"], expected_num_drivers)
        self.assertEqual(response.context["num_cars"], expected_num_cars)
        self.assertEqual(
            response.context["num_manufacturers"],
            expected_num_manufacturers
        )
        self.assertEqual(response.context["num_visits"], 1)
        self.assertTemplateUsed(response, "taxi/index.html")
