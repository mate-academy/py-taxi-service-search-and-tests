from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class DriverListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.force_login(self.user)
        self.driver1 = get_user_model().objects.create(
            username="driver1",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        self.driver2 = get_user_model().objects.create(
            username="driver2",
            first_name="Alice",
            last_name="Smith",
            license_number="ADC12345")

    def test_driver_list_view(self):
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


class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_index_view(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to Best Taxi Ever!")

    def test_index_view_with_session(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have visited this page")
        self.assertContains(response, "1 time.")

    def test_index_view_with_logged_out_user(self):
        self.client.logout()
        url = reverse("taxi:index")
        response = self.client.get(url)
        login_url = reverse("login")
        self.assertRedirects(response, login_url + "?next=" + url)


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="Test",
            country="Test_country"
        )
        Manufacturer.objects.create(
            name="Test1",
            country="Test_country2"
        )

        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
