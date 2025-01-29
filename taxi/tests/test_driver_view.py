from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class PublicDriverTests(TestCase):
    def test_driver_list_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_driver_detail_login_required(self):
        url = reverse("taxi:driver-detail", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_create_login_required(self):
        url = reverse("taxi:driver-create")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_update_login_required(self):
        url = reverse("taxi:driver-update", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_delete_login_required(self):
        url = reverse("taxi:driver-delete", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            license_number="AAA11111",
            first_name="FirstTest",
            last_name="LastTest",
        )
        get_user_model().objects.create_user(
            username="test1",
            password="test1234",
            license_number="AAA11112",
            first_name="FirstTest1",
            last_name="LastTest1",
        )
        self.client.force_login(driver)

    def test_driver_list_view(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(get_user_model().objects.all())
        )

    def test_driver_search_view(self):
        url = reverse("taxi:driver-list") + "?search=1"
        response = self.client.get(url)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(get_user_model().objects.filter(username__icontains="1"))
        )
