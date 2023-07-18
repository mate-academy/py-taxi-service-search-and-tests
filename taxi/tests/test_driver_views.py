from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase


DRIVERS_LIST_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):
    def test_login_required_for_list(self) -> None:
        response = self.client.get(DRIVERS_LIST_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver_list(self) -> None:
        get_user_model().objects.create_user(
            username="Test1", password="Test12345", license_number="TRE12345"
        )
        get_user_model().objects.create_user(
            username="Test2", password="Test12345", license_number="TRE12346"
        )
        response = self.client.get(DRIVERS_LIST_URL)
        drivers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_create_driver(self) -> None:
        form_data = {
            "username": "Test1",
            "password1": "Password1234@",
            "password2": "Password1234@",
            "first_name": "FirstName",
            "last_name": "LastName",
            "license_number": "TRE12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_update_driver_license_number(self) -> None:
        driver = get_user_model().objects.get(id=1)
        url = reverse("taxi:driver-update", kwargs={"pk": driver.pk})
        response = self.client.post(
            url, data={"license_number": "TRE12347"}, follow=True
        )

        self.assertEqual(response.status_code, 200)
        driver.refresh_from_db()
        self.assertEqual(driver.license_number, "TRE12347")
        self.assertContains(response, "TRE12347")


class PrivateDriverListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        number_of_drivers = 7

        for driver_id in range(number_of_drivers):
            get_user_model().objects.create_user(
                username=f"Dominique {driver_id}",
                last_name=f"Surname {driver_id}",
                license_number=f"License {driver_id}",
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password1234@"
        )
        self.client.force_login(self.user)

    def test_pagination_is_five(self) -> None:
        response = self.client.get(DRIVERS_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_lists_all_drivers(self) -> None:
        response = self.client.get(DRIVERS_LIST_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["driver_list"]), 3)

    def test_list_with_search_parameter(self) -> None:
        response = self.client.get(DRIVERS_LIST_URL, {"username": "5"})
        drivers = get_user_model().objects.filter(username__contains="5")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
