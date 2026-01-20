from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class ModelTests(TestCase):

    def setUp(self):
        self.manufacturer_bwd = Manufacturer.objects.create(
            name="BWD",
            country="Germany"
        )
        self.manufacturer_uaz = Manufacturer.objects.create(
            name="UAZ Factory",
            country="Muchosransk"
        )

        self.driver_admin = get_user_model().objects.create(
            username="admin",
            first_name="Admin",
            last_name="(Me)",
        )

        self.driver_testdummy = get_user_model().objects.create(
            username="TestDummy",
            first_name="Dummy",
            last_name="Petrenko",
            license_number="SOS322223",
        )

        self.car_panzer = Car.objects.create(
            model="Panzerhaubitze 2000",
            manufacturer=self.manufacturer_bwd,
        )

        self.car_uaz = Car.objects.create(
            model="UAZ",
            manufacturer=self.manufacturer_uaz,
        )

        self.car_boat = Car.objects.create(
            model="Boat with nipples",
            manufacturer=self.manufacturer_bwd,
        )

    def test_manufacturer_str_representation(self):
        self.assertEqual(
            str(self.manufacturer_bwd),
            f"{self.manufacturer_bwd.name} {self.manufacturer_bwd.country}"
        )

    def test_driver_str_representation(self):
        self.assertEqual(
            str(self.driver_testdummy),
            f"{self.driver_testdummy.username} "
            f"({self.driver_testdummy.first_name} "
            f"{self.driver_testdummy.last_name})"
        )

    def test_car_str_representation(self):
        self.assertEqual(str(self.car_panzer), self.car_panzer.model)

    def test_create_driver_with_license_number(self):
        username = "newdriver"
        password = "driver12test"
        license_number = "DEF67890"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
            first_name="First",
            last_name="Last"
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_get_absolute_url(self):
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver_testdummy.pk}
        )
        self.assertEqual(
            self.driver_testdummy.get_absolute_url(),
            expected_url
        )
