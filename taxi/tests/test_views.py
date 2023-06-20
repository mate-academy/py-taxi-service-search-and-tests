from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", kwargs={"pk": 1})
DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", kwargs={"pk": 1})
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_manufacturer_list_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response, reverse("login") + "?next=/manufacturers/"
        )


class PrivateManufacturerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_manufacturers = 12

        for manufacturer_id in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name=f"Test {manufacturer_id}",
                country="Country",
            )

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="dominique",
            password="asdj233w",
            license_number="IWQ21921",
        )
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/manufacturers/")

        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_pagination(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_lists_all_manufacturers(self):
        response = self.client.get(MANUFACTURER_LIST_URL + "?page=3")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["manufacturer_list"]), 2)

    def test_search_form_exists(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertTrue("search_form" in response.context)

    def test_search_form_filters_data(self):
        response = self.client.get(MANUFACTURER_LIST_URL + "?name=Test 5")

        self.assertEqual(len(response.context["manufacturer_list"]), 1)

    def test_search_form_persists_data(self):
        """Tests that search form initial data is persisted"""
        response = self.client.get(MANUFACTURER_LIST_URL + "?name=Test")

        self.assertEqual(
            response.context["search_form"].initial["name"], "Test"
        )


class PublicCarTest(TestCase):
    def test_car_list_login_required(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response, reverse("login") + "?next=/cars/"
        )

    def test_car_detail_login_required(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany",
        )
        Car.objects.create(
            model="A4",
            manufacturer=manufacturer,
        )
        response = self.client.get(CAR_DETAIL_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response, reverse("login") + "?next=/cars/1/"
        )


class PrivateCarTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_cars = 12

        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany",
        )

        for car_id in range(number_of_cars):
            Car.objects.create(
                model=f"Test {car_id}",
                manufacturer=manufacturer,
            )

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="alice",
            password="user12321",
            license_number="QOE93291",
        )
        self.client.force_login(self.user)

    def test_list_url_exists_at_desired_location(self):
        response = self.client.get("/cars/")

        self.assertEqual(response.status_code, 200)

    def test_list_url_accessible_by_name(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertEqual(response.status_code, 200)

    def test_list_uses_correct_template(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_list_pagination(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_list_lists_all_cars(self):
        response = self.client.get(CAR_LIST_URL + "?page=3")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["car_list"]), 2)

    def test_create_car(self):
        manufacturer = Manufacturer.objects.get(name="Audi")
        driver = get_user_model().objects.get(username="alice")
        form_data = {
            "model": "A4",
            "manufacturer": manufacturer.pk,
            "drivers": driver.pk,
        }
        self.client.post(reverse("taxi:car-create"), data=form_data)
        new_car = Car.objects.get(model=form_data["model"])

        self.assertEqual(new_car.manufacturer, manufacturer)
        self.assertTrue(driver in new_car.drivers.all())

    def test_detail_url_exists_at_desired_location(self):
        response = self.client.get("/cars/1/")

        self.assertEqual(response.status_code, 200)

    def test_detail_url_accessible_by_name(self):
        response = self.client.get(CAR_DETAIL_URL)

        self.assertEqual(response.status_code, 200)

    def test_detail_uses_correct_template(self):
        response = self.client.get(CAR_DETAIL_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_search_form_exists(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertTrue("search_form" in response.context)

    def test_search_form_filters_data(self):
        response = self.client.get(CAR_LIST_URL + "?model=Test 5")

        self.assertEqual(len(response.context["car_list"]), 1)

    def test_search_form_persists_data(self):
        """Tests that search form initial data is persisted"""
        response = self.client.get(CAR_LIST_URL + "?model=Test")

        self.assertEqual(
            response.context["search_form"].initial["model"], "Test"
        )


class PublicDriverTest(TestCase):
    def test_driver_list_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response, reverse("login") + "?next=/drivers/"
        )

    def test_driver_detail_login_required(self):
        get_user_model().objects.create_user(
            username="edward",
            password="user12345",
            license_number="IAP49412",
        )
        response = self.client.get(DRIVER_DETAIL_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response, reverse("login") + "?next=/drivers/1/"
        )


class PrivateDriverTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_drivers = 7

        for driver_id in range(number_of_drivers):
            get_user_model().objects.create_user(
                username=f"Test {driver_id}",
                password="user12345",
                license_number=f"ABC1234{driver_id}"
            )

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="bob",
            password="user12321",
            license_number="QOE93291",
        )
        self.client.force_login(self.user)

    def test_list_url_exists_at_desired_location(self):
        response = self.client.get("/drivers/")

        self.assertEqual(response.status_code, 200)

    def test_list_url_accessible_by_name(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(response.status_code, 200)

    def test_list_uses_correct_template(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_list_pagination(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_list_lists_all_drivers(self):
        response = self.client.get(DRIVER_LIST_URL + "?page=2")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["driver_list"]), 3)

    def test_create_driver(self):
        form_data = {
            "username": "charlie",
            "license_number": "DKS32138",
            "password1": "fj2489eq7",
            "password2": "fj2489eq7",
            "first_name": "Charlie",
            "last_name": "Smith"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(
            new_driver.license_number, form_data["license_number"]
        )

    def test_detail_url_exists_at_desired_location(self):
        response = self.client.get("/drivers/1/")

        self.assertEqual(response.status_code, 200)

    def test_detail_url_accessible_by_name(self):
        response = self.client.get(DRIVER_DETAIL_URL)

        self.assertEqual(response.status_code, 200)

    def test_detail_uses_correct_template(self):
        response = self.client.get(DRIVER_DETAIL_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_search_form_exists(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertTrue("search_form" in response.context)

    def test_search_form_filters_data(self):
        response = self.client.get(DRIVER_LIST_URL + "?username=bob")

        self.assertEqual(len(response.context["driver_list"]), 1)

    def test_search_form_persists_data(self):
        """Tests that search form initial data is persisted"""
        response = self.client.get(DRIVER_LIST_URL + "?username=bob")

        self.assertEqual(
            response.context["search_form"].initial["username"], "bob"
        )
