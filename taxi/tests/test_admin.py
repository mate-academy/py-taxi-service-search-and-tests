from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Car, Manufacturer


class DriverAdminTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="admin123", license_number="ADF12345"
        )
        self.client.force_login(self.admin_user)

    def test_driver_license_number_in_list_display(self) -> None:
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.admin_user.license_number)

    def test_driver_license_number_in_fieldsets(self) -> None:
        url = reverse("admin:taxi_driver_change", args=(self.admin_user.id,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.admin_user.license_number)

    def test_driver_add_fieldsets_contains_all_fields(self) -> None:
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'name="license_number"')
        self.assertContains(res, 'name="license_number"')
        self.assertContains(res, 'name="first_name"')

    def test_create_driver_with_additional_info(self) -> None:
        url = reverse("admin:taxi_driver_add")
        data = {
            "username": "new_driver",
            "password1": "pass_user123",
            "password2": "pass_user123",
            "license_number": "GHJ67890",
            "first_name": "New",
            "last_name": "Driver",
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 302)
        driver = get_user_model().objects.get(username="new_driver")
        self.assertEqual(driver.license_number, "GHJ67890")
        self.assertEqual(driver.first_name, "New")
        self.assertEqual(driver.last_name, "Driver")


class CarAdminTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="admin123", license_number="ADF12345"
        )
        self.client.force_login(self.admin_user)
        manufact = Manufacturer.objects.create(name="ZAZ", country="Ukraine")
        another_manufact = Manufacturer.objects.create(
            name="Mercedes-Benz", country="Germany"
        )
        self.car = Car.objects.create(
            model="ZAZ-1000",
            manufacturer=manufact,
        )
        self.another_car = Car.objects.create(
            model="Focus", manufacturer=another_manufact
        )

    def test_search_fields_contains_all_fields_and_all_models(self) -> None:
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "model")
        self.assertContains(res, self.car.model)
        self.assertContains(res, self.another_car.model)

    def test_search_fields_finds_model_needed_only(self) -> None:
        url = reverse("admin:taxi_car_changelist") + "?q=1000"
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.car.model)
        self.assertNotContains(res, self.another_car.model)

    def test_list_filter_contains_all_fields_and_all_manufacturers(
        self,
    ) -> None:
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "manufacturer")
        self.assertContains(res, self.car.manufacturer.name)
        self.assertContains(res, self.another_car.manufacturer.name)

    def test_list_filter_correctly_filters(self) -> None:
        url = (
            reverse("admin:taxi_car_changelist")
            + f"?manufacturer__id__exact={self.car.manufacturer.id}"
        )
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.car.model)
        self.assertNotContains(res, self.another_car.model)
