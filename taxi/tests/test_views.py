from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Driver
from taxi.forms import DriverCreationForm, DriverSearchForm

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test1", country="test123")
        Manufacturer.objects.create(name="test2", country="test321")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "test",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "",
            "last_name": "",
            "license_number": ""
        }
        response = self.client.post(reverse("taxi:driver-create"),
                                    data=form_data
                                    )
        self.assertEqual(response.status_code, 200)

        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertIsNotNone(new_user)

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class SearchFeatureTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testname",
            password="user12test"
        )
        self.client = Client()
        self.client.force_login(self.user)

        Manufacturer.objects.create(
            name="Test Manufacturer 1",
            country="Test Country 1"
        )
        Manufacturer.objects.create(
            name="Test Manufacturer 2",
            country="Test Country 2"
        )
        Manufacturer.objects.create(
            name="Another Manufacturer",
            country="Another Country"
        )

    def test_search_results(self):
        search_term = "Test Manufacturer"
        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"name": search_term})
        self.assertEqual(response.status_code, 200)
        manufacturers = response.context["manufacturer_list"]
        self.assertEqual(len(manufacturers), 2)

        invalid_search_term = "Invalid Manufacturer"
        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"name": invalid_search_term})
        self.assertEqual(response.status_code, 200)
        manufacturers = response.context["manufacturer_list"]
        self.assertEqual(len(manufacturers), 0)


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="name123", password="password123"
        )
        self.client = Client()
        self.client.force_login(self.user)

    def test_search_driver_by_username(self):
        Driver.objects.create(username="newuser1", license_number="WAR12345")
        Driver.objects.create(username="newuser2", license_number="WAR54321")

        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "newuser2"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context["search_form"], DriverSearchForm
        )
        self.assertQuerysetEqual(
            response.context["object_list"],
            Driver.objects.filter(username__icontains="newuser2"),
        )
