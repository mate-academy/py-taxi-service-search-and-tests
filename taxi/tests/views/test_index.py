from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

INDEX_URL = reverse("taxi:index")


class PublicIndexViewTest(TestCase):
    def test_login_required(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateIndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        bmw = Manufacturer.objects.create(name="BMW", country="Germany")
        audi = Manufacturer.objects.create(name="AUDI", country="Germany")
        Car.objects.create(model="e34", manufacturer=bmw)
        Car.objects.create(model="RS6", manufacturer=audi)

    def setUp(self):
        user = get_user_model().objects.create_user(
            username="bob",
            password="1234test"
        )

        self.client.force_login(user)

    def test_valid_response(self):
        res = self.client.get(INDEX_URL)
        self.assertEqual(res.status_code, 200)
        expected_num_drivers = Driver.objects.count()
        expected_num_cars = Car.objects.count()
        expected_num_manufacturers = Manufacturer.objects.count()
        self.assertEqual(res.context["num_drivers"], expected_num_drivers)
        self.assertEqual(res.context["num_cars"], expected_num_cars)
        self.assertEqual(
            res.context["num_manufacturers"],
            expected_num_manufacturers
        )

        self.assertEqual(res.context["num_visits"], 1)
        self.assertTemplateUsed(res, "taxi/index.html")
