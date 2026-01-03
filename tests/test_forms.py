from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverLicenseUpdateForm, DriverCreationForm
from taxi.models import Manufacturer, Car


class TestValidLicenseNumber(TestCase):

    @staticmethod
    def create_license_update_form(test_license_number):
        return DriverLicenseUpdateForm(
            data={"license_number": test_license_number}
        )

    @staticmethod
    def create_user_create_form(test_license_number):
        return DriverCreationForm(
            data={
                "username": "unikum_test",
                "password1": "1un2testing",
                "password2": "1un2testing",
                "license_number": test_license_number,
                "first_name": "Tom",
                "last_name": "Bydgosh"
            }
        )

    def test_valid_license_number(self):
        self.assertTrue(
            self.create_license_update_form("ASW23141").is_valid()
        )
        self.assertTrue(
            self.create_user_create_form("ASW23141").is_valid()
        )

    def test_invalid_license_number_more_than_8(self):
        self.assertFalse(
            self.create_license_update_form("ASW231412").is_valid()
        )
        self.assertFalse(
            self.create_user_create_form("ASW231412").is_valid()
        )

    def test_invalid_license_number_first_lowercase(self):
        self.assertFalse(
            self.create_license_update_form("qAS23141").is_valid()
        )
        self.assertFalse(
            self.create_user_create_form("qAS23141").is_valid()
        )

    def test_invalid_license_number_last_not_numbers(self):
        self.assertFalse(
            self.create_license_update_form("ASW23as1").is_valid()
        )
        self.assertFalse(
            self.create_user_create_form("ASW23as1").is_valid()
        )


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.driver = get_user_model().objects.create(
            username="test_username",
            first_name="Adam",
            last_name="Hefner",
            password="1aadjango1",
            license_number="QWE23435"
        )
        self.client.force_login(self.driver)
        Manufacturer.objects.create(
            name="Toyota",
            country="Italy"
        )
        Manufacturer.objects.create(
            name="Tesla",
            country="Italy"
        )
        Manufacturer.objects.create(
            name="Ford",
            country="Italy"
        )

    def test_search_returns_results(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Tesla"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tesla")
        self.assertNotContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_search_no_results(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=BMW"
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Toyota")
        self.assertNotContains(response, "Tesla")
        self.assertNotContains(response, "Ford")
        self.assertQuerysetEqual(response.context["manufacturer_list"], [])

    def test_search_without_parameter(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Tesla")
        self.assertContains(response, "Ford")


class CarSearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.manufacturer1 = Manufacturer.objects.create(
            name="Test_name",
            country="Test_Country"
        )
        self.driver = get_user_model().objects.create(
            username="test_username",
            first_name="Adam",
            last_name="Hefner",
            password="1aadjango1",
            license_number="QWE23435"
        )
        self.client.force_login(self.driver)
        self.car1 = Car.objects.create(
            model="Toyota",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Tesla",
            manufacturer=self.manufacturer1
        )
        self.car3 = Car.objects.create(
            model="Ford",
            manufacturer=self.manufacturer1
        )
        self.car1.drivers.add(self.driver)
        self.car2.drivers.add(self.driver)
        self.car3.drivers.add(self.driver)

    def test_search_returns_results(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?model=Tesla"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tesla")
        self.assertNotContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_search_no_results(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?model=BMW"
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Toyota")
        self.assertNotContains(response, "Tesla")
        self.assertNotContains(response, "Ford")
        self.assertQuerysetEqual(response.context["car_list"], [])

    def test_search_without_parameter(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Tesla")
        self.assertContains(response, "Ford")


class DriverSearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.driver = get_user_model().objects.create(
            username="test_username",
            first_name="Adam",
            last_name="Hefner",
            password="1aadjango1",
            license_number="QWE23435"
        )
        get_user_model().objects.create(
            username="bob",
            first_name="Adam",
            last_name="Hefner",
            password="1aadjango1",
            license_number="QWE23431"
        )
        get_user_model().objects.create(
            username="cic",
            first_name="Adam",
            last_name="Hefner",
            password="1aadjango1",
            license_number="QWE23434"
        )
        self.client.force_login(self.driver)

    def test_search_returns_results(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=cic"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cic")
        self.assertNotContains(response, "bob")

    def test_search_no_results(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=..."
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "cic")
        self.assertNotContains(response, "bob")
        self.assertQuerysetEqual(response.context["driver_list"], [])

    def test_search_without_parameter(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cic")
        self.assertContains(response, "bob")
        self.assertContains(response, "test_username")
