from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_FILTER_URL = "{url}?{filter}={value}".format(
    url=MANUFACTURER_URL, filter="name", value="t3"
)
DRIVER_URL = reverse("taxi:driver-list")
DRIVER_FILTER_URL = "{url}?{filter}={value}".format(
    url=DRIVER_URL, filter="username", value="t3"
)
CAR_URL = reverse("taxi:car-list")
CAR_FILTER_URL = "{url}?{filter}={value}".format(
    url=CAR_URL, filter="model", value="t3"
)


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        """Test that authorization is mandatory"""
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_superuser(
            username="test", password="test12345"
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="test1")
        Manufacturer.objects.create(name="test2")
        Manufacturer.objects.create(name="test3", country="test")

    def test_retrieve_manufacturers(self):
        """Test that all manufacturers records are displayed"""
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_manufacturers_by_filter(self):
        """Test that manufacturers filter is worked"""
        response = self.client.get(MANUFACTURER_FILTER_URL)
        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.filter(name__icontains="t3")
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_superuser(
            username="test", password="test12345"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        """Test that driver is created correctly via the form"""
        form_data = {
            "username": "user",
            "password1": "user12345",
            "password2": "user12345",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "AAA12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_retrieve_drivers_by_filter(self):
        """Test that drivers filter is worked"""
        get_user_model().objects.create_user(
            username="test1", password="test12345", license_number="AAA12345"
        )
        get_user_model().objects.create_user(
            username="test2", password="test12345", license_number="AAB12345"
        )
        get_user_model().objects.create_user(
            username="test3", password="test12345", license_number="AAC12345"
        )

        response = self.client.get(DRIVER_FILTER_URL)
        self.assertEqual(response.status_code, 200)

        drivers = get_user_model().objects.filter(username__icontains="t3")
        self.assertEqual(list(response.context["driver_list"]), list(drivers))

        self.assertTemplateUsed(response, "taxi/driver_list.html")


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_superuser(
            username="test", password="test12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars_by_filter(self):
        """Test that drivers filter is worked"""
        manufacturer = Manufacturer.objects.create(name="test1")
        Car.objects.create(model="test1", manufacturer=manufacturer)
        Car.objects.create(model="test2", manufacturer=manufacturer)
        Car.objects.create(model="test3", manufacturer=manufacturer)

        response = self.client.get(CAR_FILTER_URL)
        self.assertEqual(response.status_code, 200)

        cars = Car.objects.filter(model__icontains="t3")
        self.assertEqual(list(response.context["car_list"]), list(cars))

        self.assertTemplateUsed(response, "taxi/car_list.html")
