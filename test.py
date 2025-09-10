from django.test import TestCase

from django.urls import reverse
from django.db import IntegrityError

from taxi.forms import DriverCreationForm
from taxi.models import Driver, Manufacturer, Car


class TestManufacturerSearchForm(TestCase):
    def setUp(self):
        Manufacturer.objects.create(name="MonsterCar", country="Lapland")
        Manufacturer.objects.create(name="FairyMachine", country="Fairyland")
        self.driver = Driver.objects.create_user(
            username="testuser", password="testpass", license_number="XYZ12345"
        )
        self.client.force_login(self.driver)

    def test_form_returns_correct_results(self):
        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"name": "mons"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "MonsterCar")
        self.assertNotContains(response, "FairyMachine")


class TestCarSearchForm(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(name="MonsterCar",
                                                   country="Lapland")
        Car.objects.create(model="Cool Car 3", manufacturer=manufacturer)
        Car.objects.create(model="Fancy Machine", manufacturer=manufacturer)
        self.driver = Driver.objects.create_user(
            username="testuser", password="testpass", license_number="XYZ12345"
        )
        self.client.force_login(self.driver)

    def test_form_returns_correct_results(self):
        response = self.client.get(reverse("taxi:car-list"),
                                   {"model": "cool"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cool Car 3")
        self.assertNotContains(response, "Fancy Machine")


class TestDriverSearchForm(TestCase):
    def setUp(self):
        Driver.objects.create(
            username="lololo",
            password="lololo123",
            license_number="ABC12345"
        )
        Driver.objects.create(
            username="kekeke",
            password="kekeke123",
            license_number="DEF67890"
        )
        self.driver = Driver.objects.create_user(
            username="testuser",
            password="testpass",
            license_number="XYZ12345"
        )
        self.client.force_login(self.driver)

    def test_form_returns_correct_results(self):
        response = self.client.get(reverse(
            "taxi:driver-list"), {"username": "lo"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "lololo")
        self.assertNotContains(response, "kekeke")


class TestDriver(TestCase):
    def test_create_driver(self):
        driver = Driver.objects.create(
            username="lalala",
            password="lalala123",
            license_number="ABC23456"
        )
        self.assertEqual(driver, Driver.objects.get(license_number="ABC23456"))

    def test_driver_unique_license_number_constraint(self):
        Driver.objects.create(
            username="lelele",
            password="lelele123",
            license_number="WEL34567"
        )
        with self.assertRaises(IntegrityError):
            Driver.objects.create(
                username="lululu",
                password="lululu123",
                license_number="WEL34567"
            )

    def test_driver_license_wrong_characters(self):
        form = DriverCreationForm(data={
            "username": "kokoko",
            "first_name": "lily",
            "last_name": "lolo",
            "password1": "aboba123",
            "password2": "aboba123",
            "license_number": "ABCDE123"
        })
        self.assertFalse(form.is_valid())

    def test_driver_license_too_long(self):
        form = DriverCreationForm(data={
            "username": "kakaka",
            "first_name": "lily",
            "last_name": "lolo",
            "password1": "aboba123",
            "password2": "aboba123",
            "license_number": "ABCDEF123456"
        })
        self.assertFalse(form.is_valid())

    def test_license_number_valid(self):
        form = DriverCreationForm(data={
            "username": "kokoko",
            "first_name": "lily",
            "last_name": "lolo",
            "password1": "aboba123",
            "password2": "aboba123",
            "license_number": "ABC12345"
        })
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_license_number_too_short(self):
        form = DriverCreationForm(data={
            "username": "fefefe",
            "first_name": "lily",
            "last_name": "lolo",
            "password1": "avova123",
            "password2": "avova123",
            "license_number": "AB12"
        })
        self.assertFalse(form.is_valid())
