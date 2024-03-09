from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class ManufacturerPublicTest(TestCase):
    def test_login_required(self):
        response = self.client.get("MANUFACTURER_LIST_URL")
        self.assertNotEqual(response.status_code, 200)


class ManufacturerPrivateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin_test",
            password="12345test"
        )
        self.client.force_login(self.user)

    def test_receive_manufacturers(self):
        Manufacturer.objects.create(name="Subaru test")
        all_manufacturers = Manufacturer.objects.all()

        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(all_manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class CarPublicTest(TestCase):
    def test_login_required(self):
        response = self.client.get("CAR_LIST_URL")
        self.assertNotEqual(response.status_code, 200)


class CarPrivateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin_test",
            password="12345test"
        )
        self.client.force_login(self.user)

    def test_receive_cars(self):
        manufacturer = Manufacturer.objects.create(name="Subaru test")
        Car.objects.create(
            model="Boxer",
            manufacturer=manufacturer
        )
        all_cars = Car.objects.all()

        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(all_cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class DriverPublicTest(TestCase):
    def test_login_required(self):
        response = self.client.get("DRIVER_LIST_URL")
        self.assertNotEqual(response.status_code, 200)


class DriverPrivateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin_test",
            password="12345test"
        )
        self.client.force_login(self.user)

    def test_receive_drivers(self):
        Driver.objects.create(
            username="driver_test_name",
            password="password111",
            license_number="KAA33333"
        )
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.all())
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin_test",
            password="12345test"
        )
        self.client.force_login(self.user)
        Manufacturer.objects.bulk_create([
            Manufacturer(name=f"Manufacturer {i}") for i in range(10)
        ])

    def test_pagination(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("manufacturer_list" in response.context)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin_test",
            password="12345test"
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(name="Subaru test")
        Car.objects.bulk_create([
            Car(
                model=f"Model {i}",
                manufacturer=manufacturer
            ) for i in range(10)
        ])

    def test_pagination(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("car_list" in response.context)
        self.assertEqual(len(response.context["car_list"]), 5)
