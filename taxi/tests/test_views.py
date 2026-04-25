from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


INDEX_URL = reverse("taxi:index")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicViewsTests(TestCase):
    """Tests for public views"""

    def test_login_required(self):
        """Check that the login is required to access the page"""
        urls_to_test = [
            INDEX_URL,
            MANUFACTURER_LIST_URL,
            CAR_LIST_URL,
            DRIVER_LIST_URL,
        ]

        for url in urls_to_test:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertNotEqual(response.status_code, 200)
                self.assertRedirects(
                    response, f"/accounts/login/?next={url}"
                )


class PrivateViewsTests(TestCase):
    """Tests for private views"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123",
            first_name="John",
            last_name="Doe",
            license_number="XYZ12345"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )

    def test_index_view(self):
        """Check main page and counters events"""
        response = self.client.get(INDEX_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")

        self.assertIn("num_drivers", response.context)
        self.assertIn("num_cars", response.context)
        self.assertIn("num_manufacturers", response.context)

        self.assertEqual(response.context["num_visits"], 1)
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.context["num_visits"], 2)

    def test_manufacturer_list_view_search(self):
        """Check searching for manufacturers"""
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")

        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 3)

        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "bmw"})
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
        self.assertEqual(response.context["manufacturer_list"][0].name, "BMW")

    def test_car_list_view_search(self):
        """Check searching for cars"""
        Car.objects.create(model="Corolla", manufacturer=self.manufacturer)

        response = self.client.get(CAR_LIST_URL, {"model": "cam"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)
        self.assertEqual(response.context["car_list"][0].model, "Camry")

    def test_driver_list_view_search(self):
        """Check searching for drivers"""
        get_user_model().objects.create_user(
            username="another_driver",
            password="password123",
            license_number="ABC98765"
        )

        response = self.client.get(DRIVER_LIST_URL, {"username": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertEqual(
            response.context["driver_list"][0].username,
            "testuser")

    def test_toggle_assign_to_car(self):
        """Check logic adding car to driver and removing a car from him"""
        toggle_url = reverse("taxi:toggle-car-assign", args=[self.car.id])
        car_detail_url = reverse("taxi:car-detail", args=[self.car.id])

        response = self.client.get(toggle_url)
        self.assertRedirects(response, car_detail_url)
        self.assertIn(self.car, self.user.cars.all())

        response = self.client.get(toggle_url)
        self.assertRedirects(response, car_detail_url)
        self.assertNotIn(self.car, self.user.cars.all())
