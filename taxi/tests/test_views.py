from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", kwargs={"pk": 1})
DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", kwargs={"pk": 1})
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicManufacturerViewsTests(TestCase):

    def test_login_required_manufacturer_list(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PublicCarViewsTests(TestCase):

    def test_login_required_car_list(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_car_detail(self):
        response = self.client.get(CAR_DETAIL_URL)
        self.assertNotEqual(response.status_code, 200)


class PublicDriverViewsTests(TestCase):

    def test_login_required_driver_list(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_driver_detail(self):
        response = self.client.get(DRIVER_DETAIL_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivatManufacturerViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test", password="<PASSWORD>"
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(
            name="Test Manufacturer",
            country="United Kingdom",
        )
        Manufacturer.objects.create(name="Test2 Manufacturer", country="USA")
        self.response = self.client.get(MANUFACTURER_LIST_URL)

    def test_login_required_manufacturer_list(self):
        self.assertEqual(self.response.status_code, 200)

    def test_retrieve_manufacturer_list(self):
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(self.response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(self.response, "taxi/manufacturer_list.html")


class PrivatCarViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test", password="<PASSWORD>"
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="USA"
        )
        Car.objects.create(
            model="Toto",
            manufacturer=manufacturer,
        )
        Car.objects.create(
            model="Polo",
            manufacturer=manufacturer,
        )
        self.response = self.client.get(CAR_LIST_URL)

    def test_login_required_car_list(self):
        self.assertEqual(self.response.status_code, 200)

    def test_retrieve_car_list(self):
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_login_required_car_detail(self):
        response = self.client.get(CAR_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")


class PrivatDriverViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test", password="<PASSWORD>"
        )
        self.client.force_login(self.user)

    def test_login_required_driver_list(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_driver_list(self):
        Driver.objects.create(username="Joe", license_number="JJJ12345")
        Driver.objects.create(username="Anna", license_number="AAA12345")
        response = self.client.get(DRIVER_LIST_URL)
        drivers = Driver.objects.all()
        print(list(response.context["driver_list"]))
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_login_required_driver_detail(self):
        response = self.client.get(DRIVER_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
