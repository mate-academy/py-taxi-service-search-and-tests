from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car, Driver


MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", kwargs={"pk": 1})
CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", kwargs={"pk": 1})


class PublicManufacturerTest(TestCase):
    def test_login_list_required(self):
        response = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrive_manufacturers(self):
        Manufacturer.objects.create(name="Toyota")
        Manufacturer.objects.create(name="BMW")

        response = self.client.get(MANUFACTURERS_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicDriverTest(TestCase):
    def test_login_list_required(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_detail_required(self):
        response = self.client.get(DRIVER_DETAIL_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrive_driver(self):
        Driver.objects.create_user(
            username="test12",
            password="test12345",
            license_number="TES12345",
            first_name="Test first1",
            last_name="Test last1"
        )
        Driver.objects.create_user(
            username="test123",
            password="test12345",
            license_number="QWE12345",
            first_name="Test first",
            last_name="Test last"
        )

        response = self.client.get(DRIVER_LIST_URL)

        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "us123test",
            "password2": "us123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ASD12345"
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class PublicCarTest(TestCase):
    def test_login_list_required(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_detail_required(self):
        response = self.client.get(CAR_DETAIL_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrive_car(self):
        corola_manufacturers = Manufacturer.objects.create(name="Toyota")
        dart_manufacturers = Manufacturer.objects.create(name="Dodge")

        Car.objects.create(model="Corola", manufacturer=corola_manufacturers)
        Car.objects.create(model="Dart", manufacturer=dart_manufacturers)

        response = self.client.get(CAR_LIST_URL)

        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

        self.assertTemplateUsed(response, "taxi/car_list.html")
