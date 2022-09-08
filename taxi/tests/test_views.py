from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver
from taxi.views import DriverListView, toggle_assign_to_car


MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class IndexViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123",
        )
        self.client.force_login(self.user)

    def test_index_url_accessible_by_name(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)


class PublicManufacturerViewTest(TestCase):
    def test_manufacturer_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(res.status_code, 200)


class PublicCarViewTest(TestCase):
    def test_manufacturer_login_required(self):
        res = self.client.get(CAR_URL)

        self.assertNotEqual(res.status_code, 200)


class PublicDriverViewTest(TestCase):
    def test_manufacturer_login_required(self):
        res = self.client.get(DRIVER_URL)

        self.assertNotEqual(res.status_code, 200)


class ManufacturerViewTests(TestCase):
    def setUp(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="password123",
        )
        self.client.force_login(driver)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="BMV",
            country="Germany",
        )

        res = self.client.get(MANUFACTURER_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")


class CarListViewTests(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(
            name="BMV",
            country="Germany",
        )
        car = Car.objects.create(
            model="X5",
            manufacturer=manufacturer
        )
        driver = get_user_model().objects.create_user(
            license_number="AAA12345",
            username="user_name_test",
            first_name="First",
            last_name="Last",
            password="password12345"
        )
        car.drivers.add(driver)

        self.client.force_login(driver)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_car(self):
        res = self.client.get(CAR_URL)

        cars = Car.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")


class DriverListViewTests(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        car = Car.objects.create(
            model="X5",
            manufacturer=manufacturer
        )
        driver = get_user_model().objects.create_user(
            license_number="AAA12345",
            username="user_name_test",
            first_name="First",
            last_name="Last",
            password="password12345"
        )
        car.drivers.add(driver)

        self.client.force_login(driver)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_driver(self):
        res = self.client.get(DRIVER_URL)

        drivers = Driver.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")



