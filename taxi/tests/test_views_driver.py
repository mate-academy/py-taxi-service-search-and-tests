from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Driver


class DriverListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.force_login(self.user)

    def test_driver_list_view(self):
        driver1 = get_user_model().objects.create(
            username="driver1",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        driver2 = get_user_model().objects.create(
            username="driver2",
            first_name="Alice",
            last_name="Smith",
            license_number="ADC12345")

        url = reverse("taxi:driver-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "John")
        self.assertContains(response, "Doe")
        self.assertContains(response, "Alice")
        self.assertContains(response, "Smith")


class DriverDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_login(self.user)
        self.driver = Driver.objects.create(
            username="driver1",
            first_name="John",
            last_name="Doe",
            license_number="ABC01876"
        )

    def test_driver_detail_view(self):
        url = reverse("taxi:driver-detail", args=[self.driver.pk])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "John")
        self.assertContains(response, "Doe")


class DriverCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_login(self.user)

    def test_driver_create_view_get(self):
        url = reverse("taxi:driver-create")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Create driver")
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="first_name"')
        self.assertContains(response, 'name="last_name"')

    def test_driver_create_view_post(self):
        self.client.force_login(self.user)

        url = reverse("taxi:driver-create")

        data = {
            "username": "newdriver",
            "first_name": "New",
            "last_name": "Driver",
            "email": "newdriver@example.com",
            "years_of_experience": 2,
            "license_number": "ACS12344",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        new_driver = Driver.objects.get(username="newdriver")
        self.assertRedirects(response, new_driver.get_absolute_url())


class DriverDeleteViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_login(self.user)
        self.driver = Driver.objects.create(
            username="driver1",
            first_name="John",
            last_name="Doe",
            license_number="BCS12344",
        )

    def test_driver_delete_view_post(self):
        url = reverse("taxi:driver-delete", kwargs={"pk": self.driver.pk})

        response = self.client.post(url)

        self.assertFalse(Driver.objects.filter(pk=self.driver.pk).exists())

        self.assertRedirects(response, reverse("taxi:driver-list"))
