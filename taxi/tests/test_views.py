from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class PublicViewsTests(TestCase):
    def test_login_required_for_index_page(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_driver_list_page(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_car_list_page(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_manufacturer_list_page(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertNotEqual(response.status_code, 200)


class PrivateViewsTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="admin",
            password="testpass123",
            license_number="ADM12345"
        )
        self.client.force_login(self.user)

    def test_index_page_displays_correct_context(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        Car.objects.create(
            model="Camry",
            manufacturer=manufacturer
        )
        Driver.objects.create_user(
            username="john",
            password="testpass123",
            license_number="JOH12345"
        )

        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_manufacturers"], 1)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_drivers"], 2)

    def test_manufacturer_list_page_uses_correct_template(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_car_list_page_uses_correct_template(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_driver_list_page_uses_correct_template(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
