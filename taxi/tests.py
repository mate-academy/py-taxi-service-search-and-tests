from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import (
    ManufacturerSearchForm,
    CarSearchForm,
    DriverUsernameSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
)
from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test", country="test country"
        )
        self.driver = get_user_model().objects.create_user(
            username="Test",
            password="test12345",
            first_name="test first",
            last_name="test last",
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})",
        )

    def test_driver_get_absolute_url(self):
        self.assertEquals(self.driver.get_absolute_url(), "/drivers/1/")

    def test_car_str(self):
        car = Car.objects.create(
            model="test car",
            manufacturer=self.manufacturer,
        )
        self.assertEqual(str(car), car.model)


class AdminTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user_admin = get_user_model().objects.create_superuser(
            username="admin", password="admin753"
        )
        self.client.force_login(self.user_admin)
        self.driver = get_user_model().objects.create_user(
            username="test", password="test15975", license_number="testnum14"
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)


class ViewsTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="user.admin", password="testpassword12589"
        )
        self.client.force_login(self.admin_user)

        number_of_users = 6

        for users in range(number_of_users):
            get_user_model().objects.create(
                username="TestUser %s" % users,
                password="tests126 %s" % users,
                license_number="tes14856%s" % users,
            )

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get("/drivers/")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, "taxi/driver_list.html")

    def test_pagination_is_five(self):
        resp = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"] is True)
        self.assertTrue(len(resp.context["driver_list"]) == 5)

    def test_lists_all_drivers(self):
        resp = self.client.get(reverse("taxi:driver-list") + "?page=2")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"] is True)
        self.assertTrue(len(resp.context["driver_list"]) == 2)


class FormTest(TestCase):
    def test_license_update_form_with_non_valid_data(self):
        form_data = {"license_number": "TS1234"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_creation_form_with_licensenumber_first_last_name_is_valid(
        self,
    ):
        form_data = {
            "username": "username",
            "password1": "passtes45",
            "password2": "passtes45",
            "first_name": "test first",
            "last_name": "test last",
            "license_number": "GHJ47896",
        }

        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_username_search_form(self):
        form_data = {"username": "testuser"}
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form(self):
        form_data = {"model": "Toyota"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form(self):
        form_data = {"name": "Ford"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
