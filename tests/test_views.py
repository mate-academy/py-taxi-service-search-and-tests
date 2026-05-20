from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class PrivateViewsTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="test_driver",
            password="12345",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)

    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")
        self.assertIn("num_drivers", response.context)
        self.assertIn("num_cars", response.context)
        self.assertIn("num_manufacturers", response.context)
        self.assertIn("num_visits", response.context)

    def test_manufacturer_list_view(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")

        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertIn("manufacturer_list", response.context)

    def test_car_list_view(self):
        manufacturer = Manufacturer.objects.create(name="BMW",
                                                   country="Germany")
        Car.objects.create(model="X5", manufacturer=manufacturer)

        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertIn("car_list", response.context)

    def test_driver_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertIn("driver_list", response.context)

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "BMW"}
        )

        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Audi")

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Car.objects.create(model="X5", manufacturer=manufacturer)
        Car.objects.create(model="A4", manufacturer=manufacturer)

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "X5"}
        )

        self.assertContains(response, "X5")
        self.assertNotContains(response, "A4")

    def test_search_driver_by_username(self):
        Driver.objects.create_user(
            username="john_driver",
            password="12345",
            license_number="ABC12346",
        )
        Driver.objects.create_user(
            username="bob_driver",
            password="12345",
            license_number="DEF12345",
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"}
        )

        self.assertContains(response, "john_driver")
        self.assertNotContains(response, "bob_driver")
