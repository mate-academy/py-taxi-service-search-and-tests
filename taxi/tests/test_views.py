from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm, DriverSearchForm, CarSearchForm
from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class ManufacturersListTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="pass1234"
        )
        self.audi = Manufacturer.objects.create(
            name="Audi",
            country="Germany",
        )
        self.toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        response_custom = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response_custom.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response_custom.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(
            response_custom,
            "taxi/manufacturer_list.html"
        )

    def test_manufacturer_context_messages(self):
        query = "Audi"
        custom_response = self.client.get(MANUFACTURER_URL, {"name": query})
        search_form_context = custom_response.context["search_form"]
        self.assertIsInstance(search_form_context, ManufacturerSearchForm)
        self.assertEqual(search_form_context.initial.get("name"), query)

    def test_manufacturer_search_by_name(self):
        custom_response = self.client.get(MANUFACTURER_URL, {"name": "A"})
        object_list = custom_response.context["object_list"]
        self.assertIn(self.audi, object_list)
        self.assertNotIn(self.bmw, object_list)
        self.assertIn(self.toyota, object_list)


class DriversListTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="pass1234"
        )
        self.client.force_login(self.user)

        self.driver1 = get_user_model().objects.create(
            username="test1",
            password="test1234",
            license_number="ABC12345"
        )

        self.driver2 = get_user_model().objects.create(
            username="test2",
            password="test1234",
            license_number="DFE12345"
        )

        self.driver3 = get_user_model().objects.create(
            username="name",
            password="test1234",
            license_number="DCE12345"
        )

    def test_retrieve_driver(self):
        response_custom = self.client.get(DRIVER_URL)
        self.assertEqual(response_custom.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response_custom.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response_custom, "taxi/driver_list.html")

    def test_driver_context_message(self):
        query = "test1"
        custom_response = self.client.get(DRIVER_URL, {"username": query})
        search_form_context = custom_response.context["search_form"]
        self.assertIsInstance(search_form_context, DriverSearchForm)
        self.assertEqual(search_form_context.initial.get("username"), query)

    def test_driver_search_by_username(self):
        custom_response = self.client.get(DRIVER_URL, {"username": "t"})
        object_list = custom_response.context["object_list"]
        self.assertIn(self.driver1, object_list)
        self.assertNotIn(self.driver3, object_list)
        self.assertIn(self.driver2, object_list)


class CarListTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="pass1234"
        )
        self.client.force_login(self.user)

        self.driver1 = get_user_model().objects.create(
            username="test1",
            password="test1234",
            license_number="ABC12345"
        )
        self.driver2 = get_user_model().objects.create(
            username="test2",
            password="test1234",
            license_number="DFE12345"
        )
        self.mercedes = Manufacturer.objects.create(
            name="Mercedes",
            country="Germany",
        )
        self.toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.car1 = Car.objects.create(
            model="W124",
            manufacturer=self.mercedes

        )
        self.car1.drivers.set([self.driver1, self.driver2])
        self.car2 = Car.objects.create(
            model="Corolla",
            manufacturer=self.toyota
        )
        self.car2.drivers.set([self.driver1, self.driver2])

    def test_retrieve_cars(self):
        response_custom = self.client.get(CAR_URL)
        self.assertEqual(response_custom.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(response_custom.context["car_list"]), list(cars))
        self.assertTemplateUsed(response_custom, "taxi/car_list.html")

    def test_cars_context_message(self):
        query = "Q8"
        custom_response = self.client.get(CAR_URL, {"model": query})
        search_form_context = custom_response.context["search_form"]
        self.assertIsInstance(search_form_context, CarSearchForm)
        self.assertEqual(search_form_context.initial.get("model"), query)

    def test_car_search_by_username(self):
        custom_response = self.client.get(CAR_URL, {"model": "c"})
        object_list = custom_response.context["object_list"]
        self.assertIn(self.car2, object_list)
        self.assertNotIn(self.car1, object_list)
