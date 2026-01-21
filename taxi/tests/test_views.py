from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

car_url = reverse("taxi:car-list")
driver_url = reverse("taxi:driver-list")
manufacturer_url = reverse("taxi:manufacturer-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(car_url)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        Car.objects.create(model="Audi", manufacturer=manufacturer)
        Car.objects.create(model="Corolla", manufacturer=manufacturer)
        response = self.client.get(car_url)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(driver_url)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(
            username="driver1",
            password="password1",
            license_number="ABC12345"
        )
        Driver.objects.create(
            username="driver2",
            password="password2",
            license_number="NBH56487"
        )
        response = self.client.get(driver_url)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class PublicManufacturerTest(TestCase):
    def setUp(self):
        self.url = manufacturer_url

    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))


class PrivateManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="test123"
        )
        self.client.force_login(self.user)
        self.url = manufacturer_url

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")

    def test_retrieve_manufacturers(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.order_by("name")
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_context_contains_correct_data(self):
        response = self.client.get(self.url)
        self.assertIsNotNone(response.context["manufacturer_list"])
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            Manufacturer.objects.all().order_by("name"),
            transform=lambda x: x,
        )

    def test_page_contains_manufacturer_names(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Ford")
