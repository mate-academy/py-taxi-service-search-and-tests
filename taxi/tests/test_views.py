from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        result = self.client.get(MANUFACTURER_URL)

        self.assertNotEquals(result.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="ZAZ",
            country="Ukraine"
        )
        result = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEquals(result.status_code, 200)
        self.assertEquals(
            list(result.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(result, "taxi/manufacturer_list.html")


class PrivetDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            license_number="ABC12345",
            first_name="fime",
            last_name="lame",
        )
        self.user777 = get_user_model().objects.create_user(
            username="James777",
            license_number="ABC54321",
            first_name="James777",
            last_name="Bond",
        )
        self.client.force_login(self.user777)
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "testuser",
            "license_number": "ABC12345",
            "first_name": "fime",
            "last_name": "lame",
            "password1": "test12345",
            "password2": "test12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEquals(new_user.first_name, form_data["first_name"])
        self.assertEquals(new_user.last_name, form_data["last_name"])
        self.assertEquals(new_user.license_number, form_data["license_number"])

    def test_driver_list(self):
        result = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()
        self.assertEquals(
            list(result.context["driver_list"]),
            list(drivers)
        )

    def test_toggle_driver_to_car(self):
        manufacturer = Manufacturer.objects.create(
            name="mitsubishi",
            country="Japan"
        )
        car = Car.objects.create(model="lancer", manufacturer=manufacturer)
        self.client.post(reverse(
            "taxi:toggle-car-assign",
            args=[car.pk]
        ))
        self.assertIn(car, self.user.cars.all())
        self.client.post(reverse(
            "taxi:toggle-car-assign",
            args=[car.pk]
        ))
        self.assertNotIn(car, self.user.cars.all())


class PublicDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            license_number="ABC12345",
            first_name="fime",
            last_name="lame",
        )
        self.client.force_login(self.user)
        self.client = Client()

    def test_login_required(self):
        result = self.client.get(DRIVER_URL)

        self.assertNotEquals(result.status_code, 200)
