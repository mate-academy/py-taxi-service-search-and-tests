import uuid
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car, Driver


class ManufacturerListViewTests(TestCase):
    url = reverse("taxi:manufacturer-list")

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(
            name=f"Toyota-{uuid.uuid4()}", country="Japan"
        )
        Manufacturer.objects.create(name=f"Ford-{uuid.uuid4()}", country="USA")

    def test_manufacturer_list_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_list_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_view_context(self):
        response = self.client.get(self.url)
        self.assertIn("manufacturer_list", response.context)
        self.assertIn("search_form_manufacturer", response.context)
        self.assertEqual(len(response.context["manufacturer_list"]), 2)

    def test_manufacturer_list_view_search(self):
        toyota_name = Manufacturer.objects.filter(
            name__startswith="Toyota").first().name
        response = self.client.get(self.url, {"name": "Toyota"})
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
        self.assertTrue(
            response.context["manufacturer_list"][0].name.startswith(
                toyota_name
            )
        )

    def test_manufacturer_list_view_search_negative(self):
        response = self.client.get(self.url, {"name": "NonExistent"})
        self.assertEqual(len(response.context["manufacturer_list"]), 0)
        self.assertIn("search_form_manufacturer", response.context)

    def test_toggle_assign_to_car_view(self):
        driver = get_user_model().objects.create_user(
            username="driver", password="pass123", license_number="ABC12345"
        )
        self.client.force_login(driver)
        manufacturer = Manufacturer.objects.create(
            name=f"TestManuf-{uuid.uuid4()}", country="Country"
        )
        car = Car.objects.create(model="ModelX", manufacturer=manufacturer)

        url = reverse("taxi:toggle-car-assign", args=[car.pk])
        response = self.client.get(url)

        driver.refresh_from_db()
        self.assertIn(car, driver.cars.all())
        self.assertEqual(response.status_code, 302)

        expected_url = reverse("taxi:car-detail", args=[car.pk])
        self.assertRedirects(response, expected_url)

        response = self.client.get(url)
        driver.refresh_from_db()
        self.assertNotIn(car, driver.cars.all())


class CarListViewTests(TestCase):
    url = reverse("taxi:car-list")

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name=f"TestMan-{uuid.uuid4()}", country="Testland"
        )
        Car.objects.create(
            model="Toyota Corolla", manufacturer=self.manufacturer
        )
        Car.objects.create(model="Ford Focus", manufacturer=self.manufacturer)

    def test_car_list_view_baseline(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 2)
        self.assertIn("search_form_car", response.context)

    def test_car_list_view_search_positive(self):
        response = self.client.get(self.url, {"model": "Toyota"})
        self.assertEqual(len(response.context["car_list"]), 1)
        self.assertEqual(
            response.context["car_list"][0].model, "Toyota Corolla"
        )

    def test_car_list_view_search_negative(self):
        response = self.client.get(self.url, {"model": "BMW"})
        self.assertEqual(len(response.context["car_list"]), 0)


class DriverListViewTests(TestCase):
    url = reverse("taxi:driver-list")

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="admin", password="admin123"
        )
        self.client.force_login(self.user)
        Driver.objects.create_user(
            username="driver1",
            password="pass123",
            license_number="ABC12345"
        )
        Driver.objects.create_user(
            username="driver2",
            password="pass123",
            license_number="DEF67890"
        )

    def test_driver_list_view_baseline(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 3)
        self.assertIn("search_form_driver", response.context)

    def test_driver_list_view_search_positive(self):
        response = self.client.get(self.url, {"username": "driver1"})
        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertEqual(
            response.context["driver_list"][0].username, "driver1"
        )

    def test_driver_list_view_search_negative(self):
        response = self.client.get(self.url, {"username": "nonexistent"})
        self.assertEqual(len(response.context["driver_list"]), 0)
