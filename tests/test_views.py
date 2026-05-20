from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

Driver = get_user_model()


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser",
            password="testpass",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

    def test_manufacturer_list_page_loads(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_list_login_required(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_list_template(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_search(self):
        Manufacturer.objects.create(name="Zaporozhec", country="Ukraine")
        Manufacturer.objects.create(name="Ferrari", country="Italy")
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Zaporozhec"}
        )
        self.assertEqual(len(response.context["manufacturer_list"]), 1)

    def test_manufacturer_list_non_exist_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Ducia"}
        )
        self.assertEqual(len(response.context["manufacturer_list"]), 0)

    def test_manufacturer_list_search_empty(self):
        Manufacturer.objects.create(name="Zaporozhec", country="Ukraine")
        Manufacturer.objects.create(name="Ferrari", country="Italy")
        response = self.client.get(
            reverse("taxi:manufacturer-list")
        )
        self.assertEqual(len(response.context["manufacturer_list"]), 2)


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser",
            password="testpass",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

    def test_car_list_page_loads(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

    def test_car_list_login_required(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_car_list_template(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_search(self):
        manufacturer = Manufacturer.objects.create(
            name="Nissan", country="Japan"
        )
        Car.objects.create(model="GTR", manufacturer=manufacturer)
        Car.objects.create(model="Samara", manufacturer=manufacturer)
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "GTR"}
        )
        self.assertEqual(len(response.context["car_list"]), 1)

    def test_car_list_non_exist_search(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Zonda"}
        )
        self.assertEqual(len(response.context["car_list"]), 0)

    def test_car_list_search_empty(self):
        manufacturer = Manufacturer.objects.create(
            name="Nissan", country="Japan"
        )
        Car.objects.create(model="GTR", manufacturer=manufacturer)

        Manufacturer.objects.create(name="Ferrari", country="Italy")
        Car.objects.create(model="Samara", manufacturer=manufacturer)
        response = self.client.get(
            reverse("taxi:car-list")
        )
        self.assertEqual(len(response.context["car_list"]), 2)


class DriverListViewTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser",
            password="testpass",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

    def test_driver_list_page_loads(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)

    def test_driver_list_login_required(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_driver_list_template(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_list_search(self):
        Driver.objects.create_user(
            username="john_doe",
            password="testpass",
            license_number="DEF67890",
        )
        Driver.objects.create_user(
            username="jane_doe",
            password="testpass",
            license_number="GHI11111",
        )
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "john"}
        )
        self.assertEqual(len(response.context["driver_list"]), 1)

    def test_driver_list_non_exist_search(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "nobody"}
        )
        self.assertEqual(len(response.context["driver_list"]), 0)

    def test_driver_list_search_empty(self):
        Driver.objects.create_user(
            username="john_doe",
            password="testpass",
            license_number="DEF67890",
        )
        Driver.objects.create_user(
            username="jane_doe",
            password="testpass",
            license_number="GHI11111",
        )
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(len(response.context["driver_list"]), 3)
