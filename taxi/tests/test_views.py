from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicAccessTests(TestCase):
    def test_login_required_for_lists(self):
        for name in (
            "taxi:driver-list",
            "taxi:car-list",
            "taxi:manufacturer-list",
        ):
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 302)


class PrivateAccessTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="test12345",
            license_number="TST12345",
        )
        self.client.force_login(self.user)

    def test_index_page(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_drivers"], 1)

    def test_manufacturer_list(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_car_list(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        Car.objects.create(model="Camry", manufacturer=manufacturer)
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")

    def test_driver_list(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tester")

    def test_toggle_assign_to_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        car = Car.objects.create(model="Camry", manufacturer=manufacturer)
        url = reverse("taxi:toggle-car-assign", args=[car.pk])
        self.client.get(url)
        self.assertIn(self.user, car.drivers.all())
        self.client.get(url)
        self.assertNotIn(self.user, car.drivers.all())

    def test_driver_delete_redirects_to_list(self):
        other = get_user_model().objects.create_user(
            username="other",
            password="test12345",
            license_number="OTH12345",
        )
        response = self.client.post(
            reverse("taxi:driver-delete", args=[other.pk])
        )
        self.assertRedirects(response, reverse("taxi:driver-list"))
