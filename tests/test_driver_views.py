from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


DRIVER_LIST_VIEW = "/drivers/"
DRIVER_DETAIL_VIEW = "/drivers/1/"
DRIVER_CREATE_VIEW = "/drivers/create/"
DRIVER_UPDATE_VIEW = "/drivers/1/update/"
DRIVER_DELETE_VIEW = "/drivers/1/delete/"


class PublicCarTest(TestCase):
    def test_driver_list_page_requires_login(self):
        response = self.client.get(DRIVER_LIST_VIEW)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_detail_page_requires_login(self):
        response = self.client.get(DRIVER_DETAIL_VIEW)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_create_page_requires_login(self):
        response = self.client.get(DRIVER_CREATE_VIEW)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_update_page_requires_login(self):
        response = self.client.get(DRIVER_UPDATE_VIEW)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_delete_page_requires_login(self):
        response = self.client.get(DRIVER_DELETE_VIEW)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create(
            username="john_doe",
            password="john123doe",
            license_number="JOH12345"
        )
        get_user_model().objects.create(
            username="jack_black",
            password="jack123black",
            license_number="JAC12345"
        )

    def setUp(self) -> None:
        user = get_user_model().objects.create(
            username="test_user",
            password="test123user"
        )
        self.client.force_login(user)

    # Test if all the pages are accessible
    def test_retrieve_driver_list(self):
        response = self.client.get(DRIVER_LIST_VIEW)
        cars_list = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(cars_list)
        )

    def test_retrieve_driver_detail_page(self):
        response = self.client.get(DRIVER_DETAIL_VIEW)
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["driver"], driver)

    def test_retrieve_driver_create_page(self):
        response = self.client.get(DRIVER_CREATE_VIEW)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_driver_update_page(self):
        response = self.client.get(DRIVER_UPDATE_VIEW)
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["driver"], driver)

    def test_retrieve_driver_delete_page(self):
        response = self.client.get(DRIVER_DELETE_VIEW)
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["driver"], driver)

    # Test if all the pages are accessible by their name
    def test_retrieve_driver_list_by_name(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)

    def test_retrieve_driver_detail_page_by_name(self):
        response = self.client.get(reverse("taxi:driver-detail", args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_retrieve_driver_create_page_by_name(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(response.status_code, 200)

    def test_retrieve_driver_update_page_by_name(self):
        response = self.client.get(reverse("taxi:driver-update", args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_retrieve_driver_delete_page_by_name(self):
        response = self.client.get(reverse("taxi:driver-delete", args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_search_driver_by_username(self):
        search_field = "username"
        search_value = "jack"
        url = f"{DRIVER_LIST_VIEW}?{search_field}={search_value}"
        response = self.client.get(url)

        expected_queryset = get_user_model().objects.filter(
            username__icontains=search_value
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["object_list"]),
            list(expected_queryset)
        )
