from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.html import escape

from taxi.models import Manufacturer, Car


class AdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="<TEST_ADMIN>"
        )
        self.client.force_login(self.admin_user)
        self.manufacturer_one = Manufacturer.objects.create(
            name="test_manufacturer_one",
            country="test_country"
        )
        self.manufacturer_two = Manufacturer.objects.create(
            name="test_manufacturer_two",
            country="test_country"
        )
        self.car_one = Car.objects.create(
            model="test_car_one",
            manufacturer=self.manufacturer_one
        )
        self.car_two = Car.objects.create(
            model="test_car_two",
            manufacturer=self.manufacturer_one
        )
        self.car_three = Car.objects.create(
            model="test_car_three",
            manufacturer=self.manufacturer_two
        )
        self.driver = get_user_model().objects.create(
            username="test_driver",
            password="<TEST_DRIVER>",
            license_number="ABC12345"
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.driver.license_number)

    def test_driver_fieldsets(self):
        url = reverse(
            "admin:taxi_driver_change",
            args=[self.driver.pk]
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Additional info")
        self.assertContains(res, escape("license_number"))

    def test_driver_add_fieldsets(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Additional info")
        self.assertContains(res, escape("first_name"))
        self.assertContains(res, escape("last_name"))
        self.assertContains(res, escape("license_number"))

    def test_car_search_fields(self):
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url + "?q=test_car_one")

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.car_one.model)
        self.assertNotContains(res, self.car_two.model)
        self.assertNotContains(res, self.car_three.model)

    def test_car_search_fields_nonexistent(self):
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url + "?q=nonexistent_car")

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "0 results")

    def test_car_list_filter(self):
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(
            url + "?manufacturer_id__exact=%d" % self.manufacturer_one.id
        )

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.car_one.model)
        self.assertContains(res, self.car_two.model)
        self.assertNotContains(res, self.car_three.model)
