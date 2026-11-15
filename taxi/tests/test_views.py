from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URl = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(MANUFACTURER_URl)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self) -> None:
        Manufacturer.objects.create(name="Test123", country="TestCountry")
        Manufacturer.objects.create(name="Test", country="TestCountry")
        response = self.client.get(MANUFACTURER_URl)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturers)
                         )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicCarTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self) -> None:
        manufacturer = Manufacturer.objects.create(name="Test123",
                                                   country="TestCountry"
                                                   )
        manufacturer2 = Manufacturer.objects.create(name="Test",
                                                    country="TestCountry"
                                                    )
        Car.objects.create(model="testmodel1", manufacturer=manufacturer)
        Car.objects.create(model="testmodel2", manufacturer=manufacturer2)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicDriverTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_retrieve_driver(self):
        driver1 = get_user_model().objects.create_user(
            username="testusername1",
            password="testpassword1",
            license_number="ABC12345"
        )
        get_user_model().objects.create_user(
            username="testusername2",
            password="testpassword2",
            license_number="DEF12345"
        )

        self.client.force_login(driver1)

        response = self.client.get(DRIVER_URL)

        drivers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
