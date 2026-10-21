from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class AuthenticatedTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test1234",
            license_number="ABC12345"
        )
        self.client.force_login(user=self.user)



class PublicCarTest(TestCase):
    def test_login_required(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(AuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="Country",
        )
        self.car_1 = Car.objects.create(
            model="Model",
            manufacturer=self.manufacturer,
        )

    def test_retrieve_car_list(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_car_list(self):
        car_2 = Car.objects.create(
            model="BMW",
            manufacturer=self.manufacturer,
        )
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "b"}
        )
        expected_cars = Car.objects.filter(model__icontains="b")
        self.assertEqual(
            list(response.context["car_list"]),
            list(expected_cars)
        )

        self.assertIn("search_form", response.context)

        self.assertEqual(
            response.context["search_form"].initial["model"],
            "b"
        )


class PrivateManufacturerTest(AuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

    def test_retrieve_manufacturer_list(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_search_manufacturer_list(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "yo"}
        )
        expected_manufacturers = Manufacturer.objects.filter(
            name__icontains="yo"
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(expected_manufacturers)
        )

        self.assertIn("search_form", response.context)

        self.assertEqual(
            response.context["search_form"].initial["name"],
            "yo"
        )


class PrivateDriverTest(AuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        get_user_model().objects.create_user(
            username="second_one",
            password="strongpass",
            license_number="DFG54321"
        )

    def test_retrieve_driver_list(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)

        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_search_driver_list(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "_"}
        )
        expected_drivers = get_user_model().objects.filter(
            username__icontains="_"
        )
        self.assertEqual(
            list(response.context["driver_list"]),
            list(expected_drivers)
        )

        self.assertIn("search_form", response.context)

        self.assertEqual(
            response.context["search_form"].initial["username"],
            "_"
        )
