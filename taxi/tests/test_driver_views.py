# flake8: noqa: E731

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = lambda pk: reverse("taxi:driver-detail", args=[pk])
DRIVER_CREATE_URL = reverse("taxi:driver-create")
DRIVER_LICENSE_UPDATE_URL = lambda pk: reverse("taxi:driver-update", args=[pk])
DRIVER_DELETE_URL = lambda pk: reverse("taxi:driver-delete", args=[pk])


class PublicDriverTests(TestCase):
    def test_login_required(self):
        """Test that login is required to access the driver list view"""
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self):
        """Set up a logged-in user and test data"""
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123",
        )
        self.client.force_login(self.user)

        self.driver = get_user_model().objects.create_user(
            username="driver1",
            password="password123",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
        )

    def test_retrieve_driver_list(self):
        """Test retrieving the list of drivers"""
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.driver, response.context["driver_list"])
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_driver_by_username(self):
        """Test searching drivers by username"""
        get_user_model().objects.create_user(
            username="driver2",
            password="password123",
            license_number="DEF67890",
        )
        response = self.client.get(DRIVER_LIST_URL, {"username": "driver1"})
        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertEqual(response.context["driver_list"][0], self.driver)

    def test_retrieve_driver_detail(self):
        """Test retrieving a driver's detail view"""
        url = DRIVER_DETAIL_URL(self.driver.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["driver"], self.driver)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_create_driver(self):
        """Test creating a new driver"""
        form_data = {
            "username": "new_driver",
            "password1": "Strongpassword123",
            "password2": "Strongpassword123",
            "license_number": "XYZ67890",
            "first_name": "Jane",
            "last_name": "Smith",
        }
        response = self.client.post(DRIVER_CREATE_URL, data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(
            get_user_model().objects.filter(username="new_driver").exists()
        )

    def test_update_driver_license(self):
        """Test updating a driver's license"""
        form_data = {"license_number": "XYZ67890"}
        url = DRIVER_LICENSE_UPDATE_URL(self.driver.id)
        response = self.client.post(url, data=form_data)
        self.driver.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(self.driver.license_number, "XYZ67890")

    def test_delete_driver(self):
        """Test deleting a driver"""
        url = DRIVER_DELETE_URL(self.driver.id)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertFalse(
            get_user_model().objects.filter(id=self.driver.id).exists()
        )
