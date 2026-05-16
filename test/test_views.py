from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver


class PublicFormatTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        response_index = self.client.get(reverse("taxi:index"))
        response_car_list = self.client.get(reverse("taxi:car-list"))
        response_driver = self.client.get(reverse("taxi:driver-list"))
        response_manufacturer = self.client.get(
            reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response_index.status_code, 200)
        self.assertNotEqual(response_car_list.status_code, 200)
        self.assertNotEqual(response_driver.status_code, 200)
        self.assertNotEqual(response_manufacturer.status_code, 200)


class PrivateFormatTests(TestCase):
    fixtures = ["taxi_service_db_data.json"]
    PAGINATION = 5

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD123>",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country",
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )

    def test_private_format(self):
        response_index = self.client.get(reverse("taxi:index"))
        response_car_list = self.client.get(reverse("taxi:car-detail",
                                                    args=[self.car.id]))
        response_driver = self.client.get(reverse("taxi:driver-detail",
                                                  args=[self.user.id]))
        self.assertEqual(response_index.status_code, 200)
        self.assertEqual(response_car_list.status_code, 200)
        self.assertEqual(response_driver.status_code, 200)

    def test_context_car(self, pag=PAGINATION):
        car = Car.objects.all()
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(list(response.context["car_list"]),
                         list(car)[:pag])

    def test_context_driver(self, pag=PAGINATION):
        driver = Driver.objects.all()
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(list(response.context["driver_list"]),
                         list(driver)[:pag])

    def test_context_manufacturer(self, pag=PAGINATION):
        manufacturer = Manufacturer.objects.all()
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturer)[:pag])
