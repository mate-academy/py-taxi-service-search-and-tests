from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    DriverUsernameSearchForm,
    ManufacturerNameSearchForm,
    CarModelSearchForm
)
from taxi.models import Driver, Manufacturer, Car


HOME_PAGE_URL = reverse("taxi:index")
DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", kwargs={"pk": 1})
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", kwargs={"pk": 1})


class PublicViewsTest(TestCase):
    def test_home_page_login_required(self):
        response = self.client.get(HOME_PAGE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_home_page_redirect_to_login(self):
        response = self.client.get(HOME_PAGE_URL)
        self.assertRedirects(response, "/accounts/login/?next=/")

    def test_driver_list_page_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_list_page_redirect_to_login(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertRedirects(response, "/accounts/login/?next=/drivers/")

    def test_manufacturer_list_page_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_list_page_redirect_to_login(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertRedirects(response, "/accounts/login/?next=/manufacturers/")

    def test_car_list_page_login_required(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_list_page_redirect_to_login(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertRedirects(response, "/accounts/login/?next=/cars/")


class DriverViewsTest(TestCase):
    """
    Users are created here because the Driver model inherits from AbstractUser
    """
    @classmethod
    def setUpTestData(cls):
        for i in range(1, 9):
            Driver.objects.create_user(
                username=f"test_user_{i}",
                password="1qazcde3",
                license_number=f"ABC1234{i}",
            )

    def setUp(self):
        self.user = Driver.objects.get(username="test_user_1")
        self.client.force_login(self.user)

    def test_access_page_when_logged_in(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_list_view_uses_correct_template(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_detail_view_uses_correct_template(self):
        response = self.client.get(DRIVER_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_pagination_is_five(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_pagination_lists_all_drivers(self):
        response = self.client.get(DRIVER_LIST_URL + "?page=2")
        self.assertEqual(len(response.context["driver_list"]), 3)

    def test_search_drivers_by_username(self):
        form_data = {
            "username": self.user.username,
        }
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        response = self.client.get(DRIVER_LIST_URL, data=form.cleaned_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertEqual(len(response.context["driver_list"]), 1)


class ManufacturerViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(1, 9):
            Manufacturer.objects.create(
                name=f"test_manufacturer_{i}",
                country="test_country",
            )

    def setUp(self):
        self.user = Driver.objects.create_user(
            username="user",
            password="1qazcde3",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

    def test_access_page_when_logged_in(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_pagination_is_five(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_pagination_lists_all_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL + "?page=2")
        self.assertEqual(len(response.context["manufacturer_list"]), 3)

    def test_search_manufacturers_by_name(self):
        form_data = {
            "name": "test_manufacturer_1",
        }
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        response = self.client.get(MANUFACTURER_URL, data=form.cleaned_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_manufacturer_1")
        self.assertEqual(len(response.context["manufacturer_list"]), 1)


class CarViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country",
        )
        for i in range(1, 9):
            Car.objects.create(
                model=f"test_model_{i}",
                manufacturer=manufacturer,
            )

    def setUp(self):
        self.user = Driver.objects.create_user(
            username="user",
            password="1qazcde3",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

    def test_access_car_page_when_logged_in(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_car_list_page_uses_correct_template(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_detail_page_uses_correct_template(self):
        response = self.client.get(CAR_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_pagination_is_five(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_pagination_lists_all_cars(self):
        response = self.client.get(CAR_LIST_URL + "?page=2")
        self.assertEqual(len(response.context["car_list"]), 3)

    def test_search_cars_by_model(self):
        form_data = {
            "model": "test_model_1",
        }
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        response = self.client.get(CAR_LIST_URL, data=form.cleaned_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_model_1")
        self.assertEqual(len(response.context["car_list"]), 1)
