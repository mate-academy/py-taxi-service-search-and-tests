from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Driver


DRIVERS_URL = reverse("taxi:driver-list")


def driver_detail_url(pk: int) -> str:
    return reverse("taxi:driver-detail", args=[pk])


class PrivateDriverTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_drivers = 22

        for driver_id in range(number_of_drivers):
            Driver.objects.create(
                username=f"User {driver_id}",
                password="safety123",
                license_number=f"ABC1234{driver_id}",
            )

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVERS_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 5)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)[:5],
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_drivers_second_page(self):
        response = self.client.get(DRIVERS_URL + "?page=5")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 3)

    def test_retrieve_drivers_search(self):
        response = self.client.get(DRIVERS_URL + "?username=2")
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.filter(username__icontains=2)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))

        response = self.client.get(DRIVERS_URL + "?page=2&username=1")
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.filter(username__icontains=1)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)[5:10],
        )

    def test_retrieve_driver_detail(self):
        response = self.client.get(driver_detail_url(1))
        self.assertEqual(response.status_code, 200)
        driver = Driver.objects.get(pk=1)
        self.assertEqual(response.context["driver"], driver)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "license_number": "ABC54321",
            "first_name": "Test",
            "last_name": "User",
            "password1": "user123test",
            "password2": "user123test",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = Driver.objects.get(username=form_data["username"])

        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"],
        )
        self.assertNotEqual(new_driver.password, form_data["password1"])

    def test_update_license_driver(self):
        form_data = {
            "license_number": "BCP43225",
        }
        self.client.post(
            reverse("taxi:driver-update", args=[1]),
            data=form_data,
        )
        driver = Driver.objects.get(pk=1)

        self.assertEqual(driver.license_number, form_data["license_number"])

    def test_delete_driver_get_request(self):
        response = self.client.get(
            reverse("taxi:driver-delete", args=[10]), follow=True
        )
        self.assertContains(response, "Delete driver?")

    def test_delete_driver_post_request(self):
        response = self.client.post(
            reverse("taxi:driver-delete", args=[10]), follow=True
        )
        self.assertRedirects(response, reverse("taxi:index"), status_code=302)
