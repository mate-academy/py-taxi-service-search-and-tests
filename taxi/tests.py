from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import validate_license_number
from taxi.models import Manufacturer, Car, Driver

url_test_cases = {
    reverse("taxi:manufacturer-list"),
    reverse("taxi:car-list"),
    reverse("taxi:driver-list"),
    reverse("taxi:manufacturer-create"),
    reverse("taxi:car-create"),
    reverse("taxi:driver-create"),
}
url_kwarg_test_cases = {
    reverse("taxi:driver-detail", kwargs={"pk": 1}),
    reverse("taxi:car-detail", kwargs={"pk": 1}),
    reverse("taxi:manufacturer-update", kwargs={"pk": 1}),
    reverse("taxi:car-update", kwargs={"pk": 1}),
    reverse("taxi:driver-update", kwargs={"pk": 1}),
    reverse("taxi:driver-delete", kwargs={"pk": 1}),
    reverse("taxi:car-delete", kwargs={"pk": 1}),
    reverse("taxi:manufacturer-delete", kwargs={"pk": 1}),
}


class ManufacturerStrReprTest(TestCase):
    def test_model(self):
        obj = Manufacturer.objects.create(name="Bombastic", country="US")
        self.assertEqual(obj.name, "Bombastic")
        self.assertEqual(str(obj), "Bombastic US")


class LoginRequiredTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_pages_login_requirement(self):
        for test_reverse_url in url_test_cases:
            response = self.client.get(test_reverse_url)
            self.assertNotEqual(response.status_code, 200)


class PagesTests(TestCase):
    def setUp(self):
        Manufacturer.objects.create(name="Bombastic", country="US")
        Car.objects.create(
            model="fantastic",
            manufacturer=Manufacturer.objects.get(name="Bombastic"),
        )
        Driver.objects.create(
            username="driver",
            license_number="DRV33123",
        )
        self.user = get_user_model().objects.create(
            username="user",
            password="qwer3214",
        )
        self.client.force_login(self.user)

    def test_pages_logged_in(self):
        for test_case in url_kwarg_test_cases:
            response = self.client.get(test_case)
            self.assertEqual(response.status_code, 200)


class TestLicenseNumberValidator(TestCase):
    def test_license_validation(self):
        with self.assertRaises(ValidationError):
            validate_license_number("")
            validate_license_number("123abcde")
            validate_license_number("___12345")
            validate_license_number("abc.....")
            validate_license_number("ilovecar")


class TestSearchForm(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="user",
            password="testpass123",
        )
        self.client.force_login(self.user)

        get_user_model().objects.create(
            username="driver",
            license_number="DRV33123"
        )
        get_user_model().objects.create(
            username="rider",
            license_number="RDR69852"
        )

        self.manufacturer1 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Bombastic",
            country="YOUESAY"
        )

        self.car1 = Car.objects.create(
            model="Mustang",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Focus",
            manufacturer=self.manufacturer1
        )
        self.car3 = Car.objects.create(
            model="Fiesta",
            manufacturer=self.manufacturer1
        )
        self.car3 = Car.objects.create(
            model="Falafel",
            manufacturer=self.manufacturer1
        )
        self.car3 = Car.objects.create(
            model="Frikadelen",
            manufacturer=self.manufacturer1
        )
        self.car3 = Car.objects.create(
            model="Form",
            manufacturer=self.manufacturer1
        )
        self.car3 = Car.objects.create(
            model="Fork",
            manufacturer=self.manufacturer1
        )

    def test_search_returns_matching_car(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "must"}  # partial, case-insensitive match
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mustang")
        self.assertNotContains(response, "Focus")
        self.assertNotContains(response, "Fiesta")

    def test_search_returns_matching_manufacturer(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "bomB"}  # partial, case-insensitive match
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bombastic")
        self.assertNotContains(response, "Ford")

    def test_search_returns_matching_drivers(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "RIDER"}  # partial, case-insensitive match
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "rider")
        self.assertNotContains(
            response,
            '<a href="/drivers/2/">driver',
            html=True
        )

    def test_search_pagination_works_with_query_transformer(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "f", "page": 2}
        )
        self.assertEqual(response.status_code, 200)

        next_page_url = '<span class="page-link">2 of 2</span>'

        self.assertContains(response, next_page_url)
        self.assertContains(response, "Fork")
        self.assertNotContains(response, "Mustang")
        self.assertEqual(
            response.request["QUERY_STRING"],
            "model=f&page=2"
        )
