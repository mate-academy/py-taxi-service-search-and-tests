from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car


class IndexViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_login(self.user)

    def test_index_view_accessible(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Honda", country="Japan")

    def test_manufacturer_list_view_accessible(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_pagination(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertIn("manufacturer_list", response.context)
        self.assertEqual(len(response.context["manufacturer_list"]), 2)


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(name="Toyota",
                                                   country="Japan")
        Car.objects.create(model="Corolla", manufacturer=manufacturer)
        Car.objects.create(model="Civic", manufacturer=manufacturer)

    def test_car_list_view_accessible(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")


class DriverListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_login(self.user)

        user_model = get_user_model()

        user_model.objects.create_user(
            username="driver1",
            password="password123",
            license_number="ABC12345"
        )
        user_model.objects.create_user(
            username="driver2",
            password="password123",
            license_number="DEF67890"
        )

    def test_driver_list_view_accessible(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=driver1")
        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertEqual(
            response.context["driver_list"][0].username, "driver1")
