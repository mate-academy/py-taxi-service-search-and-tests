from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Driver, Car


class IndexViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )

    def test_index_view_status_code(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_context(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("taxi:index"))
        self.assertIn("num_drivers", response.context)
        self.assertIn("num_cars", response.context)


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_list_view(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")


class ManufacturerCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )

    def test_create_view(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertEqual(response.status_code, 200)

    def test_form_submission(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse("taxi:manufacturer-create"), {
            "name": "Ford",
            "country": "USA"
        })
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertTrue(Manufacturer.objects.filter(name="Ford").exists())


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )

    def test_list_view(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")


class CarDetailViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )

    def test_detail_view(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse(
            "taxi:car-detail",
            kwargs={"pk": self.car.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")


class DriverListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.driver = Driver.objects.create(
            username="johndoe",
            first_name="John",
            last_name="Doe",
            license_number="AB123456"
        )

    def test_list_view(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "johndoe")


class DriverCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )

    def test_create_view(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(response.status_code, 200)
