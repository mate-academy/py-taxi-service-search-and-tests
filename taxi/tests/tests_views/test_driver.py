from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class LoginRequiredDriverViewTest(TestCase):
    def test_login_required_driver_list(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 302)

    def test_login_required_driver_detail(self):
        response = self.client.get(reverse(
            "taxi:driver-detail",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 302)

    def test_login_required_driver_create(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(response.status_code, 302)

    def test_login_required_driver_update(self):
        response = self.client.get(reverse(
            "taxi:driver-update",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 302)

    def test_login_required_driver_delete(self):
        response = self.client.get(reverse(
            "taxi:driver-delete",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 302)


class DriverViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_drivers = 4
        for driver_id in range(number_of_drivers):
            Driver.objects.create(
                username=f"Username {driver_id}",
                password="12345",
                license_number=f"ABC1234{driver_id}"
            )

    def setUp(self):
        self.driver = Driver.objects.get(id=1)
        self.client.force_login(self.driver)

    def test_list_drivers(self):
        response = self.client.get(reverse("taxi:driver-list"))
        drivers = Driver.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))

    def test_filter_list_drivers(self):
        response = self.client.get(f"{reverse("taxi:driver-list")}?username=1")
        self.assertEqual(len(response.context["driver_list"]), 1)

    def test_pagination_list_drivers(self):
        for driver_id in range(9):
            Driver.objects.create(
                username=f"Username 2{driver_id}",
                password="12345",
                license_number=f"AGC1234{driver_id}"
            )
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 5)

        response = self.client.get(
            f"{reverse("taxi:driver-list")}?username=2&page=2"
        )
        self.assertEqual(response.context["paginator"].num_pages, 2)

    def test_driver_detail_correct_data(self):
        response = self.client.get(reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.id}
        ))
        self.assertContains(response, self.driver.username)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_no_cars(self):
        response = self.client.get(reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.id}
        ))
        self.assertContains(response, "No cars!")

    def test_driver_detail_cars(self):
        car = Car.objects.create(
            model="3 Series",
            manufacturer=Manufacturer.objects.create(
                name="BMW",
                country="Germany"
            )
        )
        car.drivers.set((self.driver, ))

        response = self.client.get(reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.id}
        ))
        self.assertContains(response, car.id)
        self.assertContains(response, car.model)
        self.assertContains(response, car.manufacturer.name)

    def test_driver_create_get(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First name")
        self.assertContains(response, "Last name")
        self.assertContains(response, "License number")

    def test_driver_create_post(self):
        data = {
            "username": "Username202",
            "password1": "WhatWasThat2024",
            "password2": "WhatWasThat2024",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "ADC12349"
        }
        self.client.post(reverse("taxi:driver-create"), data=data)
        new_driver = get_user_model().objects.get(username=data["username"])
        self.assertEqual(new_driver.first_name, data["first_name"])
        self.assertEqual(new_driver.last_name, data["last_name"])
        self.assertEqual(new_driver.license_number, data["license_number"])

    def test_driver_update_get(self):
        response = self.client.get(reverse(
            "taxi:driver-update",
            kwargs={"pk": self.driver.id}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver.license_number)

    def test_driver_update_post(self):
        data = {
            "license_number": "ADC00000"
        }
        self.client.post(reverse(
            "taxi:driver-update",
            kwargs={"pk": self.driver.id}
        ), data=data)
        new_driver = get_user_model().objects.get(
            username=self.driver.username
        )
        self.assertEqual(new_driver.license_number, data["license_number"])

    def test_driver_delete_get(self):
        response = self.client.get(reverse(
            "taxi:driver-delete",
            kwargs={"pk": self.driver.id}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete driver?")

    def test_driver_delete_post(self):
        self.client.post(reverse(
            "taxi:driver-delete",
            kwargs={"pk": self.driver.id}
        ))
        ls = get_user_model().objects.filter(username=self.driver.username)
        self.assertEqual(len(ls), 0)
