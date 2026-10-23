from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class AdminSiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test12345",
            license_number="ADM12345",
        )
        cls.driver = get_user_model().objects.create_user(
            username="driver",
            password="test12345",
            license_number="DRV12345",
        )

    def setUp(self):
        self.client.force_login(self.admin_user)

    def test_driver_license_number_is_listed(self):
        response = self.client.get(reverse("admin:taxi_driver_changelist"))
        self.assertContains(response, self.driver.license_number)

    def test_driver_change_page_has_license_number(self):
        response = self.client.get(
            reverse("admin:taxi_driver_change", args=[self.driver.pk])
        )
        self.assertContains(response, 'name="license_number"')
        self.assertContains(response, self.driver.license_number)

    def test_driver_add_page_has_additional_info_fields(self):
        response = self.client.get(reverse("admin:taxi_driver_add"))
        for field_name in ("first_name", "last_name", "license_number"):
            with self.subTest(field=field_name):
                self.assertContains(response, f'name="{field_name}"')

    def test_car_admin_searches_by_model(self):
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        Car.objects.create(model="Focus", manufacturer=manufacturer)
        Car.objects.create(model="Mustang", manufacturer=manufacturer)
        response = self.client.get(
            reverse("admin:taxi_car_changelist"), {"q": "focus"}
        )
        models = [car.model for car in response.context["cl"].result_list]
        self.assertEqual(models, ["Focus"])

    def test_car_admin_filters_by_manufacturer(self):
        # Django shows a related-field filter only with 2+ choices.
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="BMW", country="Germany")
        response = self.client.get(reverse("admin:taxi_car_changelist"))
        self.assertContains(response, "By manufacturer")
