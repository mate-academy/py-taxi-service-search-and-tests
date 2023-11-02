from django.test import TestCase
from taxi.forms import validate_license_number, ManufacturerSearchByName
from django.core.exceptions import ValidationError
from parameterized import parameterized
from taxi.models import Driver, Manufacturer, Car
from django.urls import reverse


class FormTest(TestCase):
    def test_license_is_valid(self):
        license_number = "ABC12345"
        req = validate_license_number(license_number)
        self.assertEqual(req, license_number)

    @parameterized.expand([
        ("Test length of license number", "ABC1234"),
        ("Test first 3 letters is upper", "abc12345"),
        ("Test first 3 characters is letter", "AB123456"),
        ("Test last 5 characters is digits", "ABCD1234")
    ])
    def test_license_is_invalid(self, test_name: str, number: str):
        license_number = number
        with self.assertRaises(ValidationError, msg=test_name):
            validate_license_number(license_number)


class ViewTest(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create_user(
            username="test_user",
            password="test_pass",
            license_number="ABC12345"
        )
        self.driver2 = Driver.objects.create(
            username="Alex",
            password="test_pass",
            license_number="ABC23456"
        )
        self.factory1 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.factory2 = Manufacturer.objects.create(
            name="Mercedes",
            country="Germany"
        )
        self.factory3 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car1 = Car.objects.create(
            model="Prius",
            manufacturer=self.factory3,
        )
        self.car2 = Car.objects.create(
            model="M3",
            manufacturer=self.factory2,
        )

    list_and_create_urls = [
        "taxi:index",
        "taxi:manufacturer-list",
        "taxi:manufacturer-create",
        "taxi:car-list",
        "taxi:car-create",
        "taxi:driver-list",
        "taxi:driver-create",
    ]
    update_and_delete_urls = [
        ("taxi:manufacturer-update", 1),
        ("taxi:manufacturer-delete", 1),
        ("taxi:car-update", 1),
        ("taxi:car-delete", 1),
        ("taxi:driver-update", 1),
        ("taxi:driver-delete", 1)
    ]

    @parameterized.expand(list_and_create_urls)
    def test_authenticated_user(self, view_name):
        self.client.login(
            username="test_user",
            password="test_pass"
        )
        response = self.client.get(reverse(view_name))
        self.assertEqual(response.status_code, 200)

    @parameterized.expand(list_and_create_urls)
    def test_unauthenticated_user_list_create(self, view_name):
        response = self.client.get(reverse(view_name))
        self.assertEqual(response.status_code, 302)

    @parameterized.expand(update_and_delete_urls)
    def test_unauthenticated_user_update_delete(self, view_name, pk):
        response = self.client.get(reverse(view_name, args=[pk]))
        self.assertEqual(response.status_code, 302)

    def test_search_manufacturer(self):
        self.client.login(
            username="test_user",
            password="test_pass"
        )
        search_query = "BMW"
        response = self.client.get(reverse(
            "taxi:manufacturer-list"),
            kwargs={"name": search_query}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.factory1.name)
