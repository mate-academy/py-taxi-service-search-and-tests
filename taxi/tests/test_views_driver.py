from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def test_driver_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEquals(res, 200)


class DriverListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        numbers_of_drivers = 6
        for driver_id in range(numbers_of_drivers):
            get_user_model().objects.create_user(
                username=f"test{driver_id}",
                password=f"test{driver_id}",
                license_number=driver_id
            )

    def test_driver_view_url_exists_at_desired_location(self):
        response = self.client.get("/drivers/")
        self.assertEqual(response.status_code, 200)

    def test_driver_view_url_accessible_by_name(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)

    def test_driver_uses_correct_template_name(self):
        res = self.client.get(DRIVER_URL)
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_driver_pagination_is_five(self):
        res = self.client.get(DRIVER_URL)
        self.assertTrue("is_paginated" in res.context)
        self.assertTrue(res.context["is_paginated"])
        self.assertEqual(len(res.context["driver_list"]), 5)
        self.assertEqual(
            list(res.context["driver_list"]),
            list(get_user_model().objects.filter(pk__lte=5))
        )

    def test_lists_all_driver(self):
        res = self.client.get(DRIVER_URL + "?page=2")
        self.assertEqual(res.status_code, 200)
        self.assertTrue("is_paginated" in res.context)
        self.assertTrue(res.context["is_paginated"])
        self.assertEqual(len(res.context["driver_list"]), 2)


class DriverCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.driver_create_url = reverse("taxi:driver-create")

    def test_driver_create_view_url_exists_at_desired_location(self):
        res = self.client.get("/drivers/create/")
        self.assertEqual(res.status_code, 200)

    def test_driver_create_view_url_accessible_by_name(self):
        res = self.client.get(self.driver_create_url)
        self.assertEqual(res.status_code, 200)

    def test_driver_create_uses_correct_template_name(self):
        res = self.client.get(self.driver_create_url)
        self.assertTemplateUsed(res, "taxi/driver_form.html")


class DriverUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="QWE12346"
        )
        self.client.force_login(self.user)
        self.driver_update_url = reverse(
            "taxi:driver-update",

            args=[self.user.id]
        )

    def test_driver_update_view_url_exists_at_desired_location(self):
        res = self.client.get(f"/drivers/{self.user.id}/update/")
        self.assertEqual(res.status_code, 200)

    def test_driver_update_view_url_accessible_by_name(self):
        res = self.client.get(self.driver_update_url)
        self.assertEqual(res.status_code, 200)

    def test_driver_update_uses_correct_template_name(self):
        res = self.client.get(self.driver_update_url)
        self.assertTemplateUsed(res, "taxi/driver_form.html")

    def test_driver_update(self):
        res = self.client.post(
            self.driver_update_url, {
                "license_number": "QWE12345"
            }
        )
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "/drivers/")
        self.assertEqual(self.user.license_number, "QWE12346")
        self.user.refresh_from_db()
        self.assertEqual(self.user.license_number, "QWE12345")

    def test_driver_update_with_no_valid_license_number(self):
        res = self.client.post(
            self.driver_update_url, {
                "license_number": "QWE12345666666"
            }
        )
        self.assertEqual(res.status_code, 200)


class DriverDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.driver = get_user_model().objects.create_user(
            username="test1",
            password="test1231",
            license_number="QWE12345",
        )
        self.driver_delete_url = reverse(
            "taxi:driver-delete",
            args=[self.driver.id]
        )

    def test_driver_delete_view_url_exists_at_desired_location(self):
        res = self.client.get(f"/drivers/{self.driver.id}/delete/")
        self.assertEqual(res.status_code, 200)

    def test_driver_delete_view_url_accessible_by_name(self):
        res = self.client.get(self.driver_delete_url)
        self.assertEqual(res.status_code, 200)

    def test_driver_delete_uses_correct_template_name(self):
        res = self.client.get(self.driver_delete_url)
        self.assertTemplateUsed(res, "taxi/driver_confirm_delete.html")

    def test_driver_delete(self):
        res = self.client.post(self.driver_delete_url)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "/drivers/")
        self.assertFalse(get_user_model().objects.filter(id=self.driver.id))


class DriverDetailViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.driver_detail_url = reverse(

            "taxi:driver-detail",
            args=[self.user.id]
        )

    def test_driver_detail_view_url_exists_at_desired_location(self):
        res = self.client.get(f"/drivers/{self.user.id}/")
        self.assertEqual(res.status_code, 200)

    def test_driver_detail_view_url_accessible_by_name(self):
        res = self.client.get(self.driver_detail_url)
        self.assertEqual(res.status_code, 200)

    def test_driver_detail_uses_correct_template_name(self):
        res = self.client.get(self.driver_detail_url)
        self.assertTemplateUsed(res, "taxi/driver_detail.html")
