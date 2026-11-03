from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    validate_license_number,
)
from taxi.models import Car, Manufacturer

from django.core.exceptions import ValidationError

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
INDEX_URL = reverse("taxi:index")


def create_driver(username="driver", license_number="ABC12345", **kwargs):
    return get_user_model().objects.create_user(
        username=username,
        password="test12345",
        license_number=license_number,
        **kwargs,
    )


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.assertEqual(str(manufacturer), "Toyota Japan")

    def test_manufacturer_ordering_by_name(self):
        Manufacturer.objects.create(name="Skoda", country="Czechia")
        Manufacturer.objects.create(name="Audi", country="Germany")
        names = [m.name for m in Manufacturer.objects.all()]
        self.assertEqual(names, ["Audi", "Skoda"])

    def test_driver_str(self):
        driver = create_driver(first_name="John", last_name="Smith")
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )

    def test_driver_get_absolute_url(self):
        driver = create_driver()
        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk}),
        )

    def test_create_driver_with_license_number(self):
        driver = create_driver(license_number="XYZ98765")
        self.assertEqual(driver.license_number, "XYZ98765")
        self.assertTrue(driver.check_password("test12345"))

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        car = Car.objects.create(model="Camry", manufacturer=manufacturer)
        self.assertEqual(str(car), "Camry")


class LicenseNumberValidationTests(TestCase):
    def test_valid_license_number(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_wrong_length(self):
        for value in ("ABC1234", "ABC123456", ""):
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    validate_license_number(value)

    def test_first_three_must_be_uppercase_letters(self):
        for value in ("abc12345", "AbC12345", "123AB345", "AB 12345"):
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    validate_license_number(value)

    def test_last_five_must_be_digits(self):
        for value in ("ABC1234A", "ABCDEFGH", "ABC12 45"):
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    validate_license_number(value)


class FormTests(TestCase):
    def test_driver_creation_form_valid(self):
        data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data, data)

    def test_driver_creation_form_invalid_license(self):
        data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "bad",
        }
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_update_form_valid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "QWE54321"})
        self.assertTrue(form.is_valid())

    def test_license_update_form_invalid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "12345QWE"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class PrivateViewsTests(TestCase):
    def test_login_required(self):
        driver = create_driver()
        manufacturer = Manufacturer.objects.create(name="Audi", country="DE")
        car = Car.objects.create(model="A4", manufacturer=manufacturer)
        urls = [
            INDEX_URL,
            MANUFACTURER_LIST_URL,
            reverse("taxi:manufacturer-create"),
            reverse("taxi:manufacturer-update", args=[manufacturer.pk]),
            reverse("taxi:manufacturer-delete", args=[manufacturer.pk]),
            CAR_LIST_URL,
            reverse("taxi:car-create"),
            reverse("taxi:car-detail", args=[car.pk]),
            reverse("taxi:car-update", args=[car.pk]),
            reverse("taxi:car-delete", args=[car.pk]),
            reverse("taxi:toggle-car-assign", args=[car.pk]),
            DRIVER_LIST_URL,
            reverse("taxi:driver-create"),
            reverse("taxi:driver-detail", args=[driver.pk]),
            reverse("taxi:driver-update", args=[driver.pk]),
            reverse("taxi:driver-delete", args=[driver.pk]),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertNotEqual(response.status_code, 200)
                self.assertEqual(response.status_code, 302)
                self.assertIn("/accounts/login/", response.url)


# ----------------------------------------------------------------- index


class IndexViewTests(TestCase):
    def setUp(self):
        self.user = create_driver()
        self.client.force_login(self.user)

    def test_index_counts_and_template(self):
        manufacturer = Manufacturer.objects.create(name="Audi", country="DE")
        car = Car.objects.create(model="A4", manufacturer=manufacturer)
        car.drivers.add(self.user)

        response = self.client.get(INDEX_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")
        self.assertEqual(response.context["num_drivers"], 1)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.client.force_login(create_driver())
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Audi", country="Germany")
        Manufacturer.objects.create(name="Skoda Auto", country="Czechia")

    def test_search_form_in_context(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertIn("search_form", response.context)

    def test_search_finds_by_name(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "Toyota"})
        names = [m.name for m in response.context["manufacturer_list"]]
        self.assertEqual(names, ["Toyota"])

    def test_search_is_case_insensitive_and_partial(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "AUD"})
        names = [m.name for m in response.context["manufacturer_list"]]
        self.assertEqual(names, ["Audi"])

    def test_search_does_not_use_country(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "Japan"})
        self.assertEqual(len(response.context["manufacturer_list"]), 0)

    def test_search_no_results(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "zzz"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 0)
        self.assertContains(response, "There are no manufacturers")

    def test_empty_search_returns_all(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": ""})
        self.assertEqual(len(response.context["manufacturer_list"]), 3)


class CarSearchTests(TestCase):
    def setUp(self):
        self.client.force_login(create_driver())
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        for model in ("Camry", "Corolla", "Yaris"):
            Car.objects.create(model=model, manufacturer=manufacturer)

    def test_search_form_in_context(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertIn("search_form", response.context)

    def test_search_finds_by_model(self):
        response = self.client.get(CAR_LIST_URL, {"model": "Camry"})
        models = [c.model for c in response.context["car_list"]]
        self.assertEqual(models, ["Camry"])

    def test_search_is_case_insensitive_and_partial(self):
        response = self.client.get(CAR_LIST_URL, {"model": "cOR"})
        models = [c.model for c in response.context["car_list"]]
        self.assertEqual(models, ["Corolla"])

    def test_search_matches_several(self):
        response = self.client.get(CAR_LIST_URL, {"model": "a"})
        models = sorted(c.model for c in response.context["car_list"])
        self.assertEqual(models, ["Camry", "Corolla", "Yaris"])

    def test_search_does_not_use_manufacturer_name(self):
        response = self.client.get(CAR_LIST_URL, {"model": "Toyota"})
        self.assertEqual(len(response.context["car_list"]), 0)

    def test_search_no_results(self):
        response = self.client.get(CAR_LIST_URL, {"model": "zzz"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 0)
        self.assertContains(response, "There are no cars")

    def test_empty_search_returns_all(self):
        response = self.client.get(CAR_LIST_URL, {"model": ""})
        self.assertEqual(len(response.context["car_list"]), 3)


class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = create_driver(username="admin_user")
        self.client.force_login(self.user)
        create_driver(username="john", license_number="AAA11111")
        create_driver(username="johnny", license_number="BBB22222")
        create_driver(username="mary", license_number="CCC33333")

    def test_search_form_in_context(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertIn("search_form", response.context)

    def test_search_finds_by_username(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "mary"})
        usernames = [d.username for d in response.context["driver_list"]]
        self.assertEqual(usernames, ["mary"])

    def test_search_is_partial_and_case_insensitive(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "JOHN"})
        usernames = sorted(d.username for d in response.context["driver_list"])
        self.assertEqual(usernames, ["john", "johnny"])

    def test_search_does_not_use_license_number(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "AAA11111"})
        self.assertEqual(len(response.context["driver_list"]), 0)

    def test_search_no_results(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "zzz"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 0)
        self.assertContains(response, "There are no drivers")

    def test_empty_search_returns_all(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": ""})
        self.assertEqual(len(response.context["driver_list"]), 4)
