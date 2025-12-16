from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class AdminSiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="adm1n_P@ss"
        )
        cls.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="dr1ver_P@ss",
            license_number="TES77587"
        )

        cls.manufacturer = Manufacturer.objects.create(
            name="test_car",
            country="test_country"
        )

        cls.car = Car.objects.create(
            model="test_model",
            manufacturer=cls.manufacturer
        )

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.admin_user)

    def test_driver_license_number_listed(self):
        self.assertContains(
            self.client.get(
                reverse("admin:taxi_driver_changelist")
            ),
            self.driver.license_number
        )

    def test_driver_detail_license_number_listed(self):
        self.assertContains(
            self.client.get(
                reverse(
                    "admin:taxi_driver_change",
                    args=[self.driver.id]
                )
            ),
            self.driver.license_number
        )

    def test_driver_create_license_number_listed(self):
        self.assertContains(
            self.client.get(reverse("admin:taxi_driver_add")),
            "License number"
        )
