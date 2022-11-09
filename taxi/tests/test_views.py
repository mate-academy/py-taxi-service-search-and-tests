from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicViewTests(TestCase):
    def test_manufacturer_login_required(self) -> None:
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_car_login_required(self) -> None:
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_driver_login_required(self) -> None:
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Red John", password="9785699S"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self) -> None:
        Manufacturer.objects.create(name="Audi", country="Estonia")
        Manufacturer.objects.create(name="Tesla", country="Zimbabwe")

        response = self.client.get(MANUFACTURER_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_driver(self) -> None:
        get_user_model().objects.create_user(
            username="Patrick Jane",
            password="9785699S",
            first_name="Patrick",
            last_name="Jane",
            license_number="ABC12345",
        )

        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_car(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Tesla", country="Zimbabwe"
        )

        Car.objects.create(model="Mercedes", manufacturer=manufacturer)

        response = self.client.get(CAR_URL)

        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")
