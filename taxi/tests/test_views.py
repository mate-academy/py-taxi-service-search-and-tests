from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import SearchForm
from taxi.models import Manufacturer

HOME_URL = reverse("taxi:index")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
DRIVERS_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")


class TestViewsStatusCode(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get(HOME_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturers_page_status_code(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_drivers_page_status_code(self):
        response = self.client.get(DRIVERS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_cars_page_status_code(self):
        response = self.client.get(CARS_URL)
        self.assertNotEqual(response.status_code, 200)


class TestDriversListView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin",
        )
        self.client.force_login(self.user)

    def test_driver_list_view(self):
        get_user_model().objects.create_user(
            username="admin2",
            password="admin2",
            license_number="JON26231",
        )
        response = self.client.get(DRIVERS_URL)
        drivers = get_user_model().objects.all()
        self.assertEqual(list(response.context["object_list"]), list(drivers))


class PrivateManufacturerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="Zhiga")
        Manufacturer.objects.create(name="Tesla")
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Mercedes")

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "admin",
            "qwerty"
        )

        self.client.force_login(self.user)

    def test_create_manufacturer(self):
        form_data = {
            "name": "test_name",
            "country": "test_country"
        }

        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(new_manufacturer.name, form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURERS_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturers_search_form_works(self):
        response = self.client.get(MANUFACTURERS_URL, {"search": "m"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertIsInstance(response.context["search_form"], SearchForm)
        self.assertEqual(len(response.context["manufacturer_list"]), 2)

        for manufacturer in response.context["manufacturer_list"]:
            self.assertIn("M", manufacturer.name)
