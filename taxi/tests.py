from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Car, Manufacturer, Driver


class DriverLicenseUpdateFormTest(TestCase):

    def _form(self, license_number):
        return DriverLicenseUpdateForm(data={"license_number": license_number})

    def test_valid_license_number(self):
        self.assertTrue(self._form("ABC12345").is_valid())

    def test_too_short(self):
        self.assertFalse(self._form("ABC1234").is_valid())

    def test_too_long(self):
        self.assertFalse(self._form("ABC123456").is_valid())

    def test_first_three_not_uppercase(self):
        self.assertFalse(self._form("abc12345").is_valid())

    def test_first_three_not_alpha(self):
        self.assertFalse(self._form("AB312345").is_valid())

    def test_last_five_not_digits(self):
        self.assertFalse(self._form("ABCde345").is_valid())


class DriverCreationFormTest(TestCase):

    def _data(self, **overrides):
        base = {
            "username": "testdriver",
            "password1": "complexpass123",
            "password2": "complexpass123",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        return {**base, **overrides}

    def test_valid_form(self):
        self.assertTrue(DriverCreationForm(data=self._data()).is_valid())

    def test_invalid_license_number_rejected(self):
        self.assertFalse(
            DriverCreationForm(
                data=self._data(license_number="bad")
            ).is_valid()
        )


def create_driver(**kwargs):
    defaults = {
        "username": "driver",
        "password": "pass",
        "license_number": "ABC12345",
    }
    return Driver.objects.create_user(**{**defaults, **kwargs})


def create_manufacturer(name="Toyota", country="Japan"):
    return Manufacturer.objects.create(name=name, country=country)


def create_car(model="Camry", manufacturer=None, **kwargs):
    if manufacturer is None:
        manufacturer = create_manufacturer()
    return Car.objects.create(model=model, manufacturer=manufacturer, **kwargs)


class LoginRequiredTest(TestCase):

    PROTECTED_URLS = [
        "/",
        "/manufacturers/",
        "/cars/",
        "/drivers/",
    ]

    def test_redirects_to_login_when_anonymous(self):
        client = Client()
        for url in self.PROTECTED_URLS:
            with self.subTest(url=url):
                response = client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertIn("/accounts/login/", response["Location"])


class ManufacturerSearchTest(TestCase):

    def setUp(self):
        self.client.force_login(
            create_driver(username="u", license_number="ABC12345")
        )
        create_manufacturer(name="Toyota", country="Japan")
        create_manufacturer(name="Ford", country="USA")
        create_manufacturer(name="Mitsubishi", country="Japan")

    def test_no_query_returns_all(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(len(response.context["manufacturer_list"]), 3)

    def test_filter_by_name_exact_match(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Toyota"}
        )
        self.assertEqual(len(response.context["manufacturer_list"]), 1)

    def test_filter_by_name_partial_match(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "ot"}
        )
        # Toyota contains "ot"
        self.assertEqual(len(response.context["manufacturer_list"]), 1)

    def test_filter_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "toyota"}
        )
        self.assertEqual(len(response.context["manufacturer_list"]), 1)

    def test_no_match_returns_empty(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "BMW"}
        )
        self.assertEqual(len(response.context["manufacturer_list"]), 0)

    def test_search_query_preserved_in_context(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Toyota"}
        )
        self.assertEqual(response.context["search_query"], "Toyota")


class CarSearchTest(TestCase):

    def setUp(self):
        self.client.force_login(
            create_driver(
                username="u",
                license_number="ABC12345"
            )
        )
        mnfc = create_manufacturer()
        create_car(model="Camry", manufacturer=mnfc)
        create_car(model="Corolla", manufacturer=mnfc)
        create_car(model="Civic", manufacturer=mnfc)

    def test_no_query_returns_all(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(len(response.context["object_list"]), 3)

    def test_filter_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Camry"}
        )
        self.assertEqual(len(response.context["object_list"]), 1)

    def test_filter_partial(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "c"})
        # Camry, Corolla, Civic all contain "c"
        self.assertEqual(len(response.context["object_list"]), 3)

    def test_filter_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "camry"}
        )
        self.assertEqual(len(response.context["object_list"]), 1)

    def test_no_match_returns_empty(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Tesla"}
        )
        self.assertEqual(len(response.context["object_list"]), 0)

    def test_search_query_preserved_in_context(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Camry"}
        )
        self.assertEqual(response.context["search_query"], "Camry")


class DriverSearchTest(TestCase):

    def setUp(self):
        self.client.force_login(
            create_driver(
                username="admin",
                license_number="AAA11111"
            )
        )
        create_driver(username="john_doe", license_number="ABC12345")
        create_driver(username="jane_doe", license_number="ABC12346")
        create_driver(username="alice", license_number="ABC12347")

    def test_no_query_returns_all(self):
        response = self.client.get(reverse("taxi:driver-list"))
        # 3 created + 1 logged-in admin
        self.assertEqual(response.context["object_list"].count(), 4)

    def test_filter_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "john_doe"}
        )
        self.assertEqual(response.context["object_list"].count(), 1)

    def test_filter_partial(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "doe"}
        )
        self.assertEqual(response.context["object_list"].count(), 2)

    def test_filter_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "ALICE"}
        )
        self.assertEqual(response.context["object_list"].count(), 1)

    def test_no_match_returns_empty(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "nobody"}
        )
        self.assertEqual(response.context["object_list"].count(), 0)


class ToggleAssignToCarTest(TestCase):

    def setUp(self):
        self.driver = create_driver(
            username="driver1", license_number="ABC12345"
        )
        self.client.force_login(self.driver)
        self.car = create_car()

    def test_assign_car(self):
        self.client.get(reverse("taxi:toggle-car-assign", args=[self.car.pk]))
        self.assertIn(self.car, self.driver.cars.all())

    def test_unassign_car(self):
        self.driver.cars.add(self.car)
        self.client.get(reverse("taxi:toggle-car-assign", args=[self.car.pk]))
        self.assertNotIn(self.car, self.driver.cars.all())

    def test_toggle_redirects_to_car_detail(self):
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.pk])
        )
        self.assertRedirects(
            response, reverse("taxi:car-detail", args=[self.car.pk])
        )
