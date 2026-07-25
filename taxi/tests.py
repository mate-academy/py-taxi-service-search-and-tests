from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    SearchForm,
)
from taxi.models import Car, Driver, Manufacturer


class BaseTaxiTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="test_driver",
            password="test_password",
            license_number="ABC12345",
        )
        cls.other_driver = Driver.objects.create_user(
            username="alex",
            password="test_password",
            license_number="XYZ98765",
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        cls.other_manufacturer = Manufacturer.objects.create(
            name="Volkswagen",
            country="Germany",
        )
        cls.car = Car.objects.create(
            model="Corolla",
            manufacturer=cls.manufacturer,
        )
        cls.other_car = Car.objects.create(
            model="Golf",
            manufacturer=cls.other_manufacturer,
        )


class ModelTests(BaseTaxiTestCase):
    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            "Toyota Japan",
        )

    def test_driver_str(self):
        self.user.first_name = "John"
        self.user.last_name = "Smith"
        self.assertEqual(
            str(self.user),
            "test_driver (John Smith)",
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), "Corolla")

    def test_driver_absolute_url(self):
        self.assertEqual(
            self.user.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": self.user.pk}),
        )


class FormTests(TestCase):
    def test_search_form_allows_empty_query(self):
        form = SearchForm(data={"query": ""})
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_accepts_valid_license(self):
        form = DriverCreationForm(
            data={
                "username": "new_driver",
                "password1": "StrongPassword123",
                "password2": "StrongPassword123",
                "license_number": "AAA12345",
            }
        )
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_rejects_invalid_license(self):
        form = DriverCreationForm(
            data={
                "username": "new_driver",
                "password1": "StrongPassword123",
                "password2": "StrongPassword123",
                "license_number": "aa123",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_update_form_rejects_lowercase_prefix(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "abc12345"}
        )
        self.assertFalse(form.is_valid())

    def test_license_update_form_rejects_non_digit_suffix(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC12X45"}
        )
        self.assertFalse(form.is_valid())


class LoginRequiredTests(BaseTaxiTestCase):
    def test_list_pages_require_login(self):
        urls = [
            reverse("taxi:manufacturer-list"),
            reverse("taxi:car-list"),
            reverse("taxi:driver-list"),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertIn("/accounts/login/", response.url)


class SearchViewTests(BaseTaxiTestCase):
    def setUp(self):
        self.client.force_login(self.user)

    def test_driver_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"query": "alex"},
        )

        drivers = response.context["driver_list"]

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.other_driver, drivers)
        self.assertNotIn(self.user, drivers)

    def test_driver_search_is_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"query": "ALEX"},
        )

        self.assertContains(response, "alex")

    def test_car_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"query": "Cor"},
        )

        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Golf")

    def test_manufacturer_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"query": "Toy"},
        )

        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Volkswagen")

    def test_empty_search_returns_all_objects(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"query": ""},
        )

        self.assertContains(response, "Corolla")
        self.assertContains(response, "Golf")

    def test_search_form_is_in_context(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertIn("search_form", response.context)


class IndexViewTests(BaseTaxiTestCase):
    def setUp(self):
        self.client.force_login(self.user)

    def test_index_contains_object_counts(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.context["num_drivers"], 2)
        self.assertEqual(response.context["num_cars"], 2)
        self.assertEqual(response.context["num_manufacturers"], 2)

    def test_visit_counter_increases(self):
        first_response = self.client.get(reverse("taxi:index"))
        second_response = self.client.get(reverse("taxi:index"))

        self.assertEqual(first_response.context["num_visits"], 1)
        self.assertEqual(second_response.context["num_visits"], 2)


class ToggleAssignmentTests(BaseTaxiTestCase):
    def setUp(self):
        self.client.force_login(self.user)

    def test_driver_can_assign_and_remove_self_from_car(self):
        url = reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": self.car.pk},
        )

        self.client.post(url)
        self.assertTrue(self.car.drivers.filter(pk=self.user.pk).exists())

        self.client.post(url)
        self.assertFalse(self.car.drivers.filter(pk=self.user.pk).exists())
