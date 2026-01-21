from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import site
from taxi.models import Manufacturer, Car

Driver = get_user_model()


class AdminRegistrationTests(TestCase):
    def test_models_registered_in_admin(self):
        for model in (Manufacturer, Car, Driver):
            with self.subTest(model=model.__name__):
                self.assertIn(model, site._registry)


class AdminPermissionsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = Driver.objects.create_superuser(
            username="admin",
            password="adminpass",
            license_number="ADMIN001"
        )
        cls.user = Driver.objects.create_user(
            username="user",
            password="userpass",
            license_number="USER0001"
        )
        cls.m = Manufacturer.objects.create(name="Audi", country="Germany")
        cls.c = Car.objects.create(model="A6", manufacturer=cls.m)

    def test_admin_requires_staff(self):
        self.client.login(username="user", password="userpass")
        resp = self.client.get(reverse("admin:taxi_car_changelist"))
        self.assertIn(resp.status_code, (302, 403))

    def test_admin_changelist_access_for_superuser(self):
        self.client.login(username="admin", password="adminpass")
        for url_name in [
            "admin:taxi_manufacturer_changelist",
            "admin:taxi_car_changelist",
            "admin:taxi_driver_changelist"
        ]:
            with self.subTest(url=url_name):
                resp = self.client.get(reverse(url_name))
                self.assertEqual(resp.status_code, 200)

    def test_admin_add_and_change_pages(self):
        self.client.login(username="admin", password="adminpass")
        urls = [
            reverse("admin:taxi_manufacturer_add"),
            reverse("admin:taxi_car_add"),
            reverse("admin:taxi_driver_add"),
            reverse("admin:taxi_manufacturer_change", args=[self.m.id]),
            reverse("admin:taxi_car_change", args=[self.c.id]),
            reverse("admin:taxi_driver_change", args=[self.user.id]),
        ]
        for ukr in urls:
            with self.subTest(ukr=ukr):
                self.assertEqual(self.client.get(ukr).status_code, 200)

    def test_admin_driver_changelist_shows_license_number(self):
        self.client.login(username="admin", password="adminpass")
        resp = self.client.get(reverse("admin:taxi_driver_changelist"))
        self.assertContains(resp, self.user.license_number)
