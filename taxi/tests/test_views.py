from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicPagesTests(TestCase):
    def setUp(self):
        self.client = Client()


class PublicDriversTests(PublicPagesTests):
    def test_driver_list_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 302)


class PublicCarTests(PublicPagesTests):

    def test_car_list_login_required(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 302)


class PublicManufacturerTests(PublicPagesTests):

    def test_manufacturer_list_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 302)


class PrivatePagesTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="testuser", license_number="DAW1845"
        )
        self.client.force_login(self.user)


class PrivateDriversTests(PrivatePagesTests):

    def test_retrieve_drivers(self):
        get_user_model().objects.create(
            username="test_driver", license_number="DAR1845"
        )
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        driver_list = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver_list)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class PrivateCarTests(PrivatePagesTests):

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )
        car.drivers.add(self.user)
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        car_list = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(car_list))
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PrivateManufacturerTests(PrivatePagesTests):

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="test_name", country="test_country")
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturer_list = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer_list)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
