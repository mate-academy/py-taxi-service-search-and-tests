from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


DRIVER_LIST_VIEW_URL = reverse("taxi:driver-list")
DRIVER_CREATE_VIEW_URL = reverse("taxi:driver-create")


class PublicDriverTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="test123",
            license_number="AMD12345"
        )

    def test_driver_list_view_login_required(self):
        response = self.client.get(DRIVER_LIST_VIEW_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_detail_view_login_required(self):
        url = reverse("taxi:driver-detail", args=[self.driver.id])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_create_view_login_required(self):
        response = self.client.get(DRIVER_CREATE_VIEW_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_update_view_login_required(self):
        url = reverse("taxi:driver-update", args=[self.driver.id])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_delete_view_login_required(self):
        url = reverse("taxi:driver-delete", args=[self.driver.id])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="first_driver",
            password="test1234",
            license_number="AMD56555"
        )
        self.client.force_login(self.driver)
        get_user_model().objects.create_user(
            username="second_driver",
            password="test1234",
            license_number="AMD87123"
        )
        get_user_model().objects.create_user(
            username="third_driver",
            password="test1234",
            license_number="AMD19564"
        )

    def test_driver_list_view_without_search(self):
        drivers = get_user_model().objects.all()
        response = self.client.get(DRIVER_LIST_VIEW_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertContains(response, "first_driver")
        self.assertContains(response, "second_driver")
        self.assertContains(response, "third_driver")

    def test_driver_list_view_with_search(self):
        drivers = get_user_model().objects.all()
        response = self.client.get(DRIVER_LIST_VIEW_URL, {"username": "fir"})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertContains(response, "first_driver")
        self.assertNotContains(response, "second_driver")
        self.assertNotContains(response, "third_driver")

    def test_driver_detail_view(self):
        url = reverse("taxi:driver-detail", args=[self.driver.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["driver"], self.driver)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_driver_create_view(self):
        driver_data = {
            "username": "test_driver2",
            "password1": "GjnFR2452H",
            "password2": "GjnFR2452H",
            "first_name": "first_test",
            "last_name": "last_test",
            "license_number": "AMD22222"
        }
        response_get = self.client.get(DRIVER_CREATE_VIEW_URL)
        self.client.post(DRIVER_CREATE_VIEW_URL, data=driver_data)
        new_driver = get_user_model().objects.get(
            username=driver_data["username"]
        )
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "taxi/driver_form.html")
        self.assertEqual(new_driver.username, driver_data["username"])
        self.assertEqual(new_driver.first_name, driver_data["first_name"])
        self.assertEqual(new_driver.last_name, driver_data["last_name"])
        self.assertEqual(
            new_driver.license_number,
            driver_data["license_number"]
        )
        self.assertTrue(new_driver.check_password(driver_data["password1"]))
        self.assertEqual(get_user_model().objects.count(), 4)

    def test_driver_license_update_view(self):
        driver_license_update_data = {
            "license_number": "AMD99999"
        }
        url = reverse("taxi:driver-update", args=[self.driver.id])
        response_get = self.client.get(url)
        self.client.post(url, data=driver_license_update_data)
        updated_driver = get_user_model().objects.get(id=self.driver.id)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "taxi/driver_form.html")
        self.assertEqual(
            updated_driver.license_number,
            driver_license_update_data["license_number"]
        )

    def test_driver_delete_view(self):
        url = reverse("taxi:driver-delete", args=[self.driver.id])
        response_get = self.client.get(url)
        self.client.post(url)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(
            response_get,
            "taxi/driver_confirm_delete.html"
        )
        self.assertEqual(get_user_model().objects.count(), 2)
