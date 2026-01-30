from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
TOGGLE_CAR_ASSIGN = "taxi:toggle-car-assign"


class PublicAccessTests(TestCase):
    def test_manufacturer_list_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_driver_list_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_car_list_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class BasePrivateObjectsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            license_number="AXE00001"
        )
        self.user2 = get_user_model().objects.create_user(
            username="JamesBond",
            password="test54321",
            license_number="AXE10000"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="German"
        )
        Manufacturer.objects.create(
            name="Mazda",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="X7",
            manufacturer=self.manufacturer
        )
        Car.objects.create(
            model="M5",
            manufacturer=self.manufacturer
        )


class PrivateManufacturerObjectsTest(BasePrivateObjectsTest):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(MANUFACTURER_URL)

    def test_retrieve_manufacturer(self):
        self.assertEqual(self.response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(self.response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(self.response, "taxi/manufacturer_list.html")

    def test_get_context_data_contains_search_form(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "BMW"})
        self.assertIn("search_form", response.context)
        form = response.context["search_form"]
        self.assertEqual(form.initial["name"], "BMW")

    def test_get_queryset_filters_by_name(self):
        self.assertEqual(
            self.response.context["manufacturer_list"].count(),
            Manufacturer.objects.count()
        )
        response = self.client.get(MANUFACTURER_URL, {"name": "BMW"})
        manufacturers = response.context["manufacturer_list"]
        self.assertEqual(
            manufacturers.count(),
            Manufacturer.objects.filter(name="BMW").count()
        )
        self.assertEqual(manufacturers[0].name, "BMW")


class PrivateDriverObjectsTest(BasePrivateObjectsTest):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(DRIVER_URL)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "AXE54321",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_retrieve_driver(self):
        self.assertEqual(self.response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(self.response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(self.response, "taxi/driver_list.html")

    def test_get_context_data_contains_search_form(self):
        response = self.client.get(DRIVER_URL, {"username": "test"})
        self.assertIn("search_form", response.context)
        form = response.context["search_form"]
        self.assertEqual(form.initial["username"], "test")

    def test_get_queryset_filters_by_username(self):
        self.assertEqual(
            self.response.context["driver_list"].count(),
            get_user_model().objects.count()
        )
        response = self.client.get(DRIVER_URL, {"username": "JamesBond"})
        drivers = response.context["driver_list"]
        self.assertEqual(
            drivers.count(),
            get_user_model().objects.filter(username="JamesBond").count()
        )
        self.assertEqual(drivers[0].username, "JamesBond")


class PrivateCarObjectsTest(BasePrivateObjectsTest):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(CAR_URL)

    def test_retrieve_car(self):
        self.assertEqual(self.response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(self.response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(
            self.response,
            "taxi/car_list.html"
        )

    def test_get_context_data_contains_search_form(self):
        response = self.client.get(CAR_URL, {"model": "M5"})
        self.assertIn("search_form", response.context)
        form = response.context["search_form"]
        self.assertEqual(form.initial["model"], "M5")

    def test_get_queryset_filters_by_model(self):
        self.assertEqual(
            self.response.context["car_list"].count(),
            Car.objects.count()
        )
        response = self.client.get(CAR_URL, {"model": "M5"})
        cars = response.context["car_list"]
        self.assertEqual(
            cars.count(),
            Car.objects.filter(model="M5").count()
        )
        self.assertEqual(cars[0].model, "M5")


class ToggleCarAssignObjectsTest(BasePrivateObjectsTest):
    def test_assign_car_to_driver(self):
        url = reverse(TOGGLE_CAR_ASSIGN, args=[self.car.id])
        response = self.client.get(url)
        self.assertIn(self.car, self.user.cars.all())
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[self.car.id])
        )

    def test_remove_car_from_driver(self):
        self.user.cars.add(self.car)
        url = reverse(TOGGLE_CAR_ASSIGN, args=[self.car.id])
        response = self.client.get(url)
        self.assertNotIn(self.car, self.user.cars.all())
        self.assertRedirects(
            response, reverse("taxi:car-detail", args=[self.car.id])
        )
