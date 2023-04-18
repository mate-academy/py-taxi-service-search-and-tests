from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
CARS_URL = reverse("taxi:car-list")
DRIVERS_URL = reverse("taxi:driver-list")


class PublicManufacturerListViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertRedirects(response, "/accounts/login/?next=/manufacturers/")


class PrivateManufacturerListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 manufacturers for pagination tests
        number_of_manufacturers = 13

        for manufacturer_id in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name=f"TestName {manufacturer_id}",
                country=f"TestCountry {manufacturer_id}",
            )

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "test1234"
        )

        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/manufacturers/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_pagination_is_5(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_lists_all_manufacturers(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(MANUFACTURERS_URL + "?page=3")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 3)

    def test_search_form(self):
        response = self.client.get(MANUFACTURERS_URL + "?name=1")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 4)


class PublicCarListViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CARS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(CARS_URL)
        self.assertRedirects(response, "/accounts/login/?next=/cars/")


class PrivateCarListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 cars for pagination tests
        number_of_cars = 13

        Driver.objects.create(
            username="test_1",
            password="test12345_1",
            license_number="AAA11111",
            first_name="TestFirstName1",
            last_name="TestLastName1"
        )

        Driver.objects.create(
            username="test_2",
            password="test12345_2",
            license_number="AAA22222",
            first_name="TestFirstName2",
            last_name="TestLastName2"
        )

        drivers_for_car = Driver.objects.all()

        for car_id in range(number_of_cars):
            manufacturer = Manufacturer.objects.create(
                name=f"TestName {car_id}",
                country=f"TestCountry {car_id}")

            test_car = Car.objects.create(
                model=f"TestModel {car_id}",
                manufacturer=manufacturer)

            test_car.drivers.set(drivers_for_car)
            test_car.save()

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "test1234"
        )

        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/cars/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(CARS_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(CARS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_pagination_is_5(self):
        response = self.client.get(CARS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_lists_all_cars(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(CARS_URL + "?page=3")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 3)

    def test_search_form(self):
        response = self.client.get(CARS_URL + "?model=1")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 4)


class PublicDriverListViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVERS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(DRIVERS_URL)
        self.assertRedirects(response, "/accounts/login/?next=/drivers/")


class PrivateDriverListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 8 drivers for pagination tests
        number_of_drivers = 8

        for driver_id in range(number_of_drivers):
            Driver.objects.create(
                username=f"test_{driver_id}",
                password=f"test12345_{driver_id}",
                license_number=f"AAA1111{driver_id}",
                first_name=f"TestFirstName{driver_id}",
                last_name=f"TestLastName{driver_id}"
            )

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "test12345"
        )

        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/drivers/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(DRIVERS_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(DRIVERS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_pagination_is_5(self):
        response = self.client.get(DRIVERS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_lists_all_drivers(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(DRIVERS_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 4)

    def test_search_form(self):
        response = self.client.get(DRIVERS_URL + "?username_=1")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 1)
