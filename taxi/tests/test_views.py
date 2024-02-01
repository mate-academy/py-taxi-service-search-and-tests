from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer

DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")

class PublicDriverTest(TestCase):

    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='123',
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        Driver.objects.create(
            username='test_driver',
            first_name='Test',
            last_name='Test',
            license_number='ASD12345'
        )
        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(list(res.context["driver_list"]), list(drivers))


class PublicCarTest(TestCase):

    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='123',
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        Manufacturer = Manufacturer.objects.create(
            name='Test',
            country='Test'
        )
        Car.objects.create(
            model
        )
        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(list(res.context["driver_list"]), list(drivers))