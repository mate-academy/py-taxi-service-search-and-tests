from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class BaseTest(TestCase):
    def create_test_user(self):
        return get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )

    def create_manufacturer(self, name="BWD", country="Germany"):
        return Manufacturer.objects.create(name=name, country=country)

    def create_car(self, model="Panzerhaubitze 2000", manufacturer=None):
        if manufacturer is None:
            manufacturer = self.create_manufacturer()
        return Car.objects.create(model=model, manufacturer=manufacturer)

    def assertresponse(
            self,
            response,
            status_code=200,
            template_name=None,
            context_key=None,
            expected_value=None
    ):
        self.assertEqual(response.status_code, status_code)
        if template_name:
            self.assertTemplateUsed(response, template_name)
        if context_key and expected_value:
            self.assertEqual(
                list(response.context[context_key]), list(expected_value)
            )


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(BaseTest):
    def setUp(self):
        self.user = self.create_test_user()
        self.client.force_login(self.user)
        self.manufacturer_bwd = self.create_manufacturer(
            name="BWD", country="Germany"
        )
        self.manufacturer_uaz = self.create_manufacturer(
            name="UAZ Factory", country="Muchosransk"
        )

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertresponse(
            response,
            template_name="taxi/manufacturer_list.html",
            context_key="manufacturer_list",
            expected_value=manufacturers
        )

    def test_search_manufacturer(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "BWD"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BWD")
        self.assertNotContains(response, "UAZ Factory")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(BaseTest):
    def setUp(self):
        self.user = self.create_test_user()
        self.client.force_login(self.user)
        self.manufacturer_bwd = self.create_manufacturer(
            name="BWD", country="Germany"
        )
        self.car_panzer = self.create_car(
            model="Panzerhaubitze 2000", manufacturer=self.manufacturer_bwd
        )
        self.car_uaz = self.create_car(
            model="UAZ", manufacturer=self.manufacturer_bwd
        )

    def test_retrieve_cars(self):
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.select_related("manufacturer").all()
        self.assertresponse(
            response,
            template_name="taxi/car_list.html",
            context_key="car_list",
            expected_value=cars
        )


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(BaseTest):
    def setUp(self):
        self.user = self.create_test_user()
        self.client.force_login(self.user)
        Driver.objects.create(username="driver1", license_number="ABC12345")
        Driver.objects.create(username="driver2", license_number="DEF67890")

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_LIST_URL)
        drivers = Driver.objects.all()
        self.assertresponse(
            response,
            template_name="taxi/driver_list.html",
            context_key="driver_list",
            expected_value=drivers
        )

    def test_search_driver(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "driver1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver1")
        self.assertNotContains(response, "driver2")


class PrivateIndexViewTest(BaseTest):
    def setUp(self):
        self.user = self.create_test_user()
        self.client.force_login(self.user)

    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertresponse(response, template_name="taxi/index.html")
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
