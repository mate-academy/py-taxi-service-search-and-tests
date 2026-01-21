from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestHomePage(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="TestUser1", password="TestPassword1"
        )

    def test_home_page_login_required(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(response.status_code, 200)

    def test_home_page(self):
        self.client.force_login(self.driver)
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")


class TestDriverViewsLoginRequired(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="TestDriver4", password="TestPassword4"
        )

    def test_driver_list_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_driver_detail_login_required(self):
        response = self.client.get(
            reverse("taxi:driver-detail", args=[self.driver.id])
        )
        self.assertNotEqual(response.status_code, 200)

    def test_driver_create_login_required(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertNotEqual(response.status_code, 200)

    def test_driver_update_login_required(self):
        response = self.client.get(
            reverse("taxi:driver-update", args=[self.driver.id])
        )
        self.assertNotEqual(response.status_code, 200)

    def test_driver_delete_login_required(self):
        response = self.client.get(
            reverse("taxi:driver-delete", args=[self.driver.id])
        )
        self.assertNotEqual(response.status_code, 200)


class BaseDriverTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="TestDriver5", password="TestPassword5"
        )
        self.client.force_login(self.driver)


class TestDriverList(BaseDriverTest):
    driver_list_url = reverse("taxi:driver-list")
    paginated_by = 5

    def setUp(self):
        super().setUp()
        for i in range(1, 10):
            get_user_model().objects.create_user(
                username=f"UniqueTestDriver{i}",
                password=f"UniqueTestPassword{i}",
                license_number=f"ABC0000{i}",
            )

    def test_driver_list_template(self):
        response = self.client.get(self.driver_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_list_pagination(self):
        response = self.client.get(self.driver_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(response.context["is_paginated"], True)
        self.assertEqual(
            len(response.context["driver_list"]), self.paginated_by
        )

    def test_driver_list_search(self):
        response = self.client.get(self.driver_list_url + "?username=7")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertContains(response, "UniqueTestDriver7")
        self.assertNotContains(response, "UniqueTestDriver8")


class TestDriverDetail(BaseDriverTest):
    def test_driver_detail_template(self):
        response = self.client.get(
            reverse("taxi:driver-detail", args=[self.driver.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")


class TestDriverCreate(BaseDriverTest):
    def test_driver_create_template(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_driver_create(self):
        data = {
            "username": "NewTestDriver1",
            "password1": "NewTestPassword1",
            "password2": "NewTestPassword1",
            "first_name": "NewTestFirstName1",
            "last_name": "NewTestLastName1",
            "license_number": "OOO00000",
        }
        self.client.post(
            reverse("taxi:driver-create"),
            data=data,
        )
        new_driver = get_user_model().objects.get(username=data["username"])
        self.assertEqual(new_driver.username, data["username"])
        self.assertTrue(new_driver.check_password(data["password1"]))


class TestDriverLicenseUpdate(BaseDriverTest):
    def test_driver_license_update_template(self):
        response = self.client.get(
            reverse("taxi:driver-update", args=[self.driver.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_driver_license_update(self):
        data = {
            "license_number": "UPD00000",
        }
        self.client.post(
            reverse("taxi:driver-update", args=[self.driver.id]),
            data=data,
        )
        updated_driver = get_user_model().objects.get(id=self.driver.id)
        self.assertEqual(
            updated_driver.license_number, data["license_number"]
        )


class TestDriverDelete(BaseDriverTest):
    def test_driver_delete_template(self):
        response = self.client.get(
            reverse("taxi:driver-delete", args=[self.driver.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_confirm_delete.html")

    def test_driver_delete(self):
        self.client.post(reverse("taxi:driver-delete", args=[self.driver.id]))
        drivers = get_user_model().objects.filter(id=self.driver.id)
        self.assertEqual(drivers.count(), 0)
