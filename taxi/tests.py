from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")


class TaxiTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="auditor",
            license_number="AUD65432",
            first_name="Chris",
            last_name="Wolff",
            password="1qaz2wsx",
        )
        self.driver1 = get_user_model().objects.create_user(
            username="admin_user",
            password="pass1",
            license_number="ABC12345",
            first_name="Admin",
            last_name="User",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="billy",
            password="pass2",
            license_number="DEF67890",
            first_name="Billy",
            last_name="Hargrove",
        )
        self.driver3 = get_user_model().objects.create_user(
            username="bob_newby",
            password="pass3",
            license_number="GHI99999",
            first_name="Bob",
            last_name="Newby",
        )

        self.manufacturer1 = Manufacturer.objects.create(
            name="Audi",
            country="Austria",
        )

        self.manufacturer2 = Manufacturer.objects.create(
            name="BYD",
            country="China",
        )

        self.car1 = Car.objects.create(
            model="A6",
            manufacturer=self.manufacturer1,
        )

        self.car2 = Car.objects.create(
            model="A5",
            manufacturer=self.manufacturer1,
        )

        self.client.force_login(self.user)

    def test_login(self):
        response = self.client.post(reverse("login"),
                                    {"username": "auditor",
                                     "password": "1qaz2wsx"},
                                    follow=True)

        self.assertTrue(response.context["user"].is_active)

    def test_update_driver_license_not_valid_number(self):
        wrong_license_number = "a5"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": wrong_license_number},
        )

        self.assertEqual(response.status_code, 200)

    def test_car_list_correct_template(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_driver_detail_correct_template(self):
        response = self.client.get(reverse("taxi:driver-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_driver_list_search_without_query_returns_all(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 200)
        driver_list = response.context["driver_list"]

        self.assertIn(self.driver1, driver_list)
        self.assertIn(self.driver2, driver_list)
        self.assertIn(self.driver3, driver_list)

    def test_driver_list_search_is_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search_field_name_driver": "BILLY"}
        )

        self.assertEqual(response.status_code, 200)
        driver_list = response.context["driver_list"]

        self.assertIn(self.driver2, driver_list)

    def test_car_list_search_is_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"search_field_car_model": "a6"}
        )

        self.assertEqual(response.status_code, 200)
        car_list = response.context["car_list"]

        self.assertIn(self.car1, car_list)
        self.assertNotIn(self.car2, car_list)

    def test_manufacturer_list_search_is_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"search_field_name_manufacturer": "audi"}
        )

        self.assertEqual(response.status_code, 200)
        manufacturer_list = response.context["manufacturer_list"]

        self.assertIn(self.manufacturer1, manufacturer_list)
        self.assertNotIn(self.manufacturer2, manufacturer_list)
