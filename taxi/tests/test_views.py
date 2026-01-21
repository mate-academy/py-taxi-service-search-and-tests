from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
INDEX_URL = reverse("taxi:index")


class PublicListView(TestCase):
    def test_index_login_required(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEquals(res.status_code, 200)

    def test_car_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEquals(res.status_code, 200)

    def test_manufacturer_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEquals(res.status_code, 200)

    def test_driver_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateListView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        Manufacturer.objects.create(
            name="Renault",
            country="France"
        )
        res = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        Car.objects.create(
            model="test_model",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="test_model_2",
            manufacturer=manufacturer
        )
        cars = Car.objects.all()
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_drivers(self) -> None:
        get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
            license_number="AAA12345",
        )
        get_user_model().objects.create_user(
            username="test_username_2",
            password="test_password_2",
            license_number="BBB12345",
        )
        drivers = Driver.objects.all()
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")
