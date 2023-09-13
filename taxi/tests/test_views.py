from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PrivateManufacturerTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    @staticmethod
    def create_test_data():
        number_of_manufacturer = 8

        for manufacturer_id in range(number_of_manufacturer):
            Manufacturer.objects.create(
                name=f"name {manufacturer_id}",
                country=f"country {manufacturer_id}"
            )

    def test_view_url_exist_at_needed_location(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertEquals(response.status_code, 200)

    def test_pagination_is_5(self):
        self.create_test_data()
        response = self.client.get(MANUFACTURER_URL)

        self.assertEquals(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEquals(len(response.context["manufacturer_list"]), 5)

    def test_correct_template_used(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_list_all_manufacturer(self):
        self.create_test_data()
        response = self.client.get(MANUFACTURER_URL + "?page=2")

        self.assertEquals(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEquals(len(response.context["manufacturer_list"]), 3)

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(
            name="name",
            country="country"
        )
        search_name = "name"
        response = self.client.get(
            MANUFACTURER_URL, {"name": search_name}
        )

        self.assertEquals(response.status_code, 200)
        manufacturer_in_context = Manufacturer.objects.filter(
            name__icontains=search_name
        )

        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            manufacturer_in_context
        )


class PublicManufacturerListViewTests(TestCase):

    def test_manufacturer_login_required(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEquals(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertRedirects(response, "/accounts/login/?next=/manufacturers/")


class PrivateCarTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_name",
            password="test_password"
        )
        self.client.force_login(self.user)

    @staticmethod
    def crate_test_data():
        manufacturer = Manufacturer.objects.create(
            name="name",
            country="country"
        )

        number_of_car = 8

        for number_id in range(number_of_car):
            Car.objects.create(
                model=f"test{number_id}",
                manufacturer=manufacturer,
            )

    def test_view_url_exist_at_needed_location(self):
        response = self.client.get(CAR_URL)

        self.assertEquals(response.status_code, 200)

    def test_pagination_is_5(self):
        self.crate_test_data()
        response = self.client.get(CAR_URL)

        self.assertEquals(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEquals(len(response.context["car_list"]), 5)

    def test_correct_template_used(self):
        response = self.client.get(CAR_URL)

        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_list_all_manufacturer(self):
        self.crate_test_data()
        response = self.client.get(CAR_URL + "?page=2")

        self.assertEquals(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEquals(len(response.context["car_list"]), 3)

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="name",
            country="country"
        )
        Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        search_model = "test"
        response = self.client.get(
            CAR_URL, {"model": search_model}
        )

        self.assertEquals(response.status_code, 200)
        car_in_contest = Car.objects.filter(
            model__icontains=search_model
        )

        self.assertQuerysetEqual(
            response.context["car_list"],
            car_in_contest
        )


class PublicCarTests(TestCase):

    def test_car_login_required(self):
        response = self.client.get(CAR_URL)

        self.assertEquals(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(CAR_URL)

        self.assertRedirects(response, "/accounts/login/?next=/cars/")


class PrivateDriverTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_name",
            password="password123",
            license_number="HUG12349"

        )
        self.client.force_login(self.user)

    @staticmethod
    def create_test_data():
        number_od_drivers = 8

        for driver_id in range(number_od_drivers):
            get_user_model().objects.create_user(
                username=f"test_name{driver_id}",
                password=f"password123{driver_id}",
                license_number=f"HUG1234{driver_id}"

            )

    def test_view_url_exist_at_needed_location(self):
        response = self.client.get(CAR_URL)

        self.assertEquals(response.status_code, 200)

    def test_pagination_is_5(self):
        self.create_test_data()
        response = self.client.get(DRIVER_URL)

        self.assertEquals(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEquals(len(response.context["driver_list"]), 5)

    def test_correct_template_used(self):
        response = self.client.get(DRIVER_URL)

        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_list_all_manufacturer(self):
        self.create_test_data()
        response = self.client.get(DRIVER_URL + "?page=2")

        self.assertEquals(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEquals(len(response.context["driver_list"]), 4)

    def test_search_driver_by_username(self):
        get_user_model().objects.create_user(
            username="test_name2",
            password="password1223",
            license_number="HUG12249"
        )
        search_username = "test_name2"
        response = self.client.get(
            DRIVER_URL, {"username": search_username}
        )

        self.assertEquals(response.status_code, 200)
        driver_in_context = get_user_model().objects.filter(
            username__icontains=search_username
        )

        self.assertQuerysetEqual(
            response.context["driver_list"],
            driver_in_context
        )


class PublicDriverTests(TestCase):

    def test_driver_login_required(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEquals(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(DRIVER_URL)

        self.assertRedirects(response, "/accounts/login/?next=/drivers/")
