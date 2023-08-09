from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Driver, Car


DRIVER_FORMATS_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicDriverFormatTests(TestCase):
    def test_login_requirement_list_driver(self):
        res_list = self.client.get(DRIVER_FORMATS_URL)

        self.assertNotEquals(res_list.status_code, 200)

    def test_login__driver_requirement_create(self):
        res_create = self.client.get(DRIVER_CREATE_URL)

        self.assertNotEquals(res_create.status_code, 200)

    def test_update_delete_driver_without_login(self):

        username = "admin.user"
        password = "qwe12345"
        driver = Driver.objects.create_user(
            username=username,
            password=password,
        )

        url_1 = reverse('taxi:manufacturer-update', kwargs={'pk': driver.pk})
        url_2 = reverse('taxi:manufacturer-delete', kwargs={'pk': driver.pk})
        res_1 = self.client.get(url_1)
        res_2 = self.client.get(url_2)
        self.assertNotEquals(res_1.status_code, 200)
        self.assertNotEquals(res_2.status_code, 200)


class PrivateDriverFormatTests(TestCase):

    def setUp(self) -> None:
        number_of_drivers = 7
        username = "user"
        password = "qwe12345"
        license_number = "qwe1234"

        self.user = get_user_model().objects.create_user(
            username="admin.user_test",
            password="vbn12345"
        )
        self.client.force_login(self.user)

        for car_id in range(number_of_drivers):
                Driver.objects.create_user(
                username=f"{username}{car_id}",
                password=password,
                license_number=f"{license_number}{car_id}"
            )

    def test_retrieve_driver(self):

        response = self.client.get(DRIVER_FORMATS_URL +"?page=1")
        response_2 = self.client.get(DRIVER_FORMATS_URL + "?page=2")
        driver = Driver.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            (list(response.context["driver_list"])
             + list(response_2.context["driver_list"])
             )
            ,list(driver)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_update_delete_driver_with_login(self):

        driver = Driver.objects.first()
        url_1 = reverse('taxi:driver-update', kwargs={'pk': driver.pk})
        url_2 = reverse('taxi:driver-delete', kwargs={'pk': driver.pk})
        res_1 = self.client.get(url_1)
        res_2 = self.client.get(url_2)
        self.assertEquals(res_1.status_code, 200)
        self.assertEquals(res_2.status_code, 200)


    def test_if_search_name_is_admin_user(self):
        response = self.client.get(DRIVER_FORMATS_URL +"?username=admin.user1")
        driver = Driver.objects.filter(
            username__icontains="admin.user1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEquals(
            list(response.context["driver_list"]),list(driver)
        )
        self.assertTrue("search_form" in response.context)
        self.assertEqual(response.context["search_form"].initial["username"], "admin.user1")

    def test_view_url_exists_at_desired_location_driver(self):
        response = self.client.get("/drivers/")
        self.assertEquals(response.status_code, 200)


    def test_pagination_in_driver_is_five(self):
        response = self.client.get(DRIVER_FORMATS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertEqual(len(response.context['driver_list']), 5)

    def test_pagination_is_second__driver_page_five(self):
        response = self.client.get(DRIVER_FORMATS_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertEqual(len(response.context['driver_list']), 3)

    def test_create_driver_success_url_is_with_redict_to_list(self):
        data = { "username" : "Test",
                "password" : "test12345",
                "license_number" : "ccc12345"}
        response = self.client.post(DRIVER_CREATE_URL, data)
        self.assertEquals(response.status_code, 200)

    def test_update_driver_success_url_is_with_redict_to_list(self):
        response = reverse('taxi:driver-update', kwargs={'pk': 1})
        data = {
            "first_name" :"Test",
            "last_name": "Test2"
        }
        self.client.post(response, data)
        driver = Driver.objects.get(id=1)
        self.assertEquals(str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})")
