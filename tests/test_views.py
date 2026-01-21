from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car, Driver
from taxi.forms import ManufacturerSearchForm, CarSearchForm, DriverSearchForm

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Honda", country="Japan")

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "Toyota"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Honda")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        Car.objects.create(model="Corolla", manufacturer=self.manufacturer)
        Car.objects.create(model="Civic", manufacturer=self.manufacturer)

    def test_retrieve_cars(self):

        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.select_related("manufacturer").all()
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_car(self):

        response = self.client.get(CAR_LIST_URL, {"model": "Corolla"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Civic")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.force_login(self.user)
        Driver.objects.create(username="driver1", license_number="ABC12345")
        Driver.objects.create(username="driver2", license_number="DEF67890")

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_driver(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "driver1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver1")
        self.assertNotContains(response, "driver2")


class PrivateIndexViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.force_login(self.user)

    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")
        self.assertIn("num_drivers", response.context)
        self.assertIn("num_cars", response.context)
        self.assertIn("num_manufacturers", response.context)
        self.assertIn("num_visits", response.context)

    def test_index_view_increment_visits(self):
        session = self.client.session
        session["num_visits"] = 5
        session.save()
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_visits"], 6)
