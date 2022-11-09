from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
DRIVER_URL = reverse("taxi:driver-create")
DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-create")
CAR_LIST_URL = reverse("taxi:car-list")


class PublicTests(TestCase):
    def test_login_required(self):
        res_manufacturers = self.client.get(MANUFACTURER_LIST_URL)
        res_cars = self.client.get(CAR_LIST_URL)
        res_drivers = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(res_manufacturers.status_code, 200)
        self.assertNotEqual(res_cars.status_code, 200)
        self.assertNotEqual(res_drivers.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("test", "password123")
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="BAIC", country="Japan")

        res = self.client.get(MANUFACTURER_LIST_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        name = "BMW"
        country = "Germany"

        form_data = {"name": name, "country": country}

        self.client.post(MANUFACTURER_CREATE_URL, data=form_data)
        manufacturer = Manufacturer.objects.get(name=name)

        self.assertEqual(manufacturer.name, name)
        self.assertEqual(manufacturer.country, country)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("test", "password123")
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "license_number": "ABC12345",
        }
        self.client.post(DRIVER_URL, data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.username, form_data["username"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_retrieve_drivers(self):

        get_user_model().objects.create_user(
            username="driver1", password="test12345", license_number="ABC12345"
        )
        get_user_model().objects.create_user(
            username="test1", password="test12345", license_number="ABD12345"
        )

        res = self.client.get(DRIVER_LIST_URL)

        drivers = get_user_model().objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["driver_list"]), list(drivers))

        self.assertTemplateUsed(res, "taxi/driver_list.html")


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("test", "password123")
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="ZAZ", country="Germany"
        )

        Car.objects.create(model="car1", manufacturer=manufacturer)

        res = self.client.get(CAR_LIST_URL)

        cars = Car.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["car_list"]), list(cars))
        self.assertTemplateUsed(res, "taxi/car_list.html")
