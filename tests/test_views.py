from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="newpass123",
            first_name="Test",
            last_name="Test",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Test", country="Test")
        Manufacturer.objects.create(name="Best", country="Best")
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = list(Manufacturer.objects.all())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            manufacturers,
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_manufacturers_after_searching_by_name(self):
        manufacturers = list(Manufacturer.objects.filter(
            name__icontains="B"
        ))
        response = self.client.get(MANUFACTURER_URL, {"name": "B"})

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            manufacturers,
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicCarTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Zaz-Daewoo",
            country="Ukraine"
        )
        self.user = get_user_model().objects.create_user(
            username="test",
            password="newpass123",
            first_name="Test",
            last_name="Test",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        Car.objects.create(model="Zazix", manufacturer=self.manufacturer)
        Car.objects.create(model="Tavria", manufacturer=self.manufacturer)
        response = self.client.get(CAR_URL)
        cars = list(Car.objects.all())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            cars,
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_cars_after_searching_by_model(self):
        cars = list(Car.objects.filter(
            model__icontains="x"
        ))
        response = self.client.get(CAR_URL, {"model": "x"})

        self.assertEqual(
            list(response.context["car_list"]),
            cars,
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicDriverTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="newpass123",
            first_name="Test",
            last_name="Test",
            license_number="ABC12345"
        )
        get_user_model().objects.create_user(
            username="test2",
            password="newpass456",
            first_name="Test2",
            last_name="Test2",
            license_number="ABC34567"
        )
        get_user_model().objects.create_user(
            username="mario",
            password="@#$S123M",
            first_name="Mario",
            last_name="Super",
            license_number="MSP12345"
        )

        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        drivers = list(get_user_model().objects.all())
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            drivers,
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_drivers_after_searching_by_username(self):
        drivers = list(get_user_model().objects.filter(
            username__icontains="ma"
        ))
        response = self.client.get(DRIVER_URL, {"username": "ma"})

        self.assertEqual(
            list(response.context["driver_list"]),
            drivers,
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
