from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicTests(TestCase):
    def test_manufacturer_login_required(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_driver_login_required(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_car_login_required(self):
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="BMW", country="German")
        response = self.client.get(MANUFACTURER_URL)
        manufacturer_list = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer_list)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Driver.objects.create(
            username="user1",
            first_name="first1",
            last_name="last1",
            license_number="AAA11111"
        )
        Driver.objects.create(
            username="user2",
            first_name="first2",
            last_name="last2",
            license_number="BBB22222"
        )

        response = self.client.get(DRIVER_URL)
        driver_list = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver_list)
        )
        self.assertTemplateUsed(
            response,
            "taxi/driver_list.html"
        )

    def test_search_form_initial_value(self):
        response = self.client.get(DRIVER_URL)
        form = response.context["search_form"]

        self.assertEqual(form.initial["username"], "")


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):

        driver = Driver.objects.create(
            username="user1",
            first_name="first1",
            last_name="last1",
            license_number="AAA11111"
        )

        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="German"
        )

        car1 = Car.objects.create(
            model="X6",
            manufacturer=manufacturer,
        )
        car1.drivers.set([driver])

        car2 = Car.objects.create(
            model="X8",
            manufacturer=manufacturer,
        )
        car2.drivers.set([driver])

        car3 = Car.objects.create(
            model="X10",
            manufacturer=manufacturer,
        )
        car3.drivers.set([driver])

        response = self.client.get(CAR_URL)
        car_list = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(car_list)
        )
        self.assertTemplateUsed(
            response,
            "taxi/car_list.html"
        )
