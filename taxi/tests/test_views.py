from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

URL_DRIVER_URL = reverse("taxi:driver-list")
URL_MANUFACTURER_URL = reverse("taxi:manufacturer-list")
URL_CAR_URL = reverse("taxi:car-list")


class PublicTaxiTest(TestCase):

    def test_login_required(self):
        res = self.client.get(URL_DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTaxiTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            first_name="test",
            last_name="test",
            username="test",
            email="test@test.tes",
            password="Test123",
            license_number="TES12345",
        )
        self.client.force_login(self.user)
        self.man1 = Manufacturer.objects.create(
            name="Honda",
            country="Japan")
        self.man2 = Manufacturer.objects.create(
            name="Audi",
            country="Germany")

    def test_driver_list(self):
        response = self.client.get(URL_DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_manufacturer_load(self):
        res = URL_MANUFACTURER_URL
        response = self.client.get(res, {"name": "toy"})
        self.assertEqual(response.status_code, 200)

    def test_search_manufacturer(self):
        man1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan")
        man2 = Manufacturer.objects.create(name="BMW", country="Germany")
        response = self.client.get(URL_MANUFACTURER_URL, {"name": "toy"})
        self.assertIn(man1, response.context["manufacturer_list"])
        self.assertNotIn(man2, response.context["manufacturer_list"])

    def test_search_car(self):
        car1 = Car.objects.create(
            model="Prius",
            manufacturer=self.man1)
        car2 = Car.objects.create(
            model="X5M60I",
            manufacturer=self.man2)
        response = self.client.get(URL_CAR_URL, {"model": "p"})
        self.assertIn(car1, response.context["car_list"])
        self.assertNotIn(car2, response.context["car_list"])

    def test_search_driver(self):
        driver1 = get_user_model().objects.create_user(
            username="Joe_541",
            password="345261Ii@",
            license_number="ARI87431",
        )
        driver2 = get_user_model().objects.create_user(
            username="Mark_781",
            password="786950Pp@",
            license_number="ARI87434"
        )
        response = self.client.get(URL_DRIVER_URL, {"username": "Jo"})
        self.assertIn(driver1, response.context["driver_list"])
        self.assertNotIn(driver2, response.context["driver_list"])
