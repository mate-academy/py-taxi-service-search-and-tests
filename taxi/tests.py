from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_string_manufacturer(self):
        manufacturer = Manufacturer(name="Manufacturer", country="USA")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}",
        )

    def test_string_driver(self):
        driver = Driver(license_number="ABCD1234")
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )

    def test_string_car(self):
        manufacturer = Manufacturer(
            name="Manufacturer",
            country="USA",
        )
        car = Car(
            model="BMW",
            manufacturer=manufacturer,
        )

        self.assertEqual(str(car), car.model)


class PublicViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required_manufacture_list(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_driver_list(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_car_detail(self):
        url = reverse("taxi:car-detail", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_login_required_car_list(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacture_list(self):
        Manufacturer.objects.create(name="Manufacturer1", country="USA")
        Manufacturer.objects.create(name="Manufacturer2", country="Ukraine")
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            str(response.context["manufacturer_list"]),
            str(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="StrongPass123!",
            license_number="TST12345",
        )
        self.client.force_login(self.user)

    def test_search_manufacturer_by_name(self):
        first_manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "bm"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["manufacturer_list"],
            [first_manufacturer],
        )

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        first_car = Car.objects.create(
            model="X5",
            manufacturer=manufacturer,
        )
        Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer,
        )

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "x5"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["car_list"],
            [first_car],
        )

    def test_search_driver_by_username(self):
        first_driver = get_user_model().objects.create_user(
            username="john_driver",
            password="StrongPass123!",
            license_number="ABC12345",
        )
        get_user_model().objects.create_user(
            username="mike_driver",
            password="StrongPass123!",
            license_number="DEF12345",
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["driver_list"],
            [first_driver],
        )


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "test_driver",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "first_name": "Test",
            "last_name": "Driver",
            "license_number": "ABC12345",
        }

        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(
            form.cleaned_data["username"],
            "test_driver",
        )
        self.assertEqual(
            form.cleaned_data["license_number"],
            "ABC12345",
        )
