from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

User = get_user_model()


class ManufacturerViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.client.login(
            username="testuser",
            password="testpass"
        )

        self.manufacturer = Manufacturer.objects.create(
            name="BMW Group",
            country="Germany"
        )

    def test_manufacturer_create_view(self):
        response = self.client.post(reverse("taxi:manufacturer-create"), {
            "name": "Audi Group",
            "country": "Germany"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Manufacturer.objects.filter(name="Audi Group").exists())

    def test_manufacturer_update_view(self):
        response = self.client.post(
            reverse("taxi:manufacturer-update", args=[self.manufacturer.id]), {
                "name": "BMW Updated",
                "country": "Germany Updated"
            })
        self.assertEqual(response.status_code, 302)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "BMW Updated")
        self.assertEqual(self.manufacturer.country, "Germany Updated")

    def test_manufacturer_delete_view(self):
        response = self.client.post(
            reverse("taxi:manufacturer-delete", args=[self.manufacturer.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(id=self.manufacturer.id).exists())


class CarListViewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

        # Create a test manufacturer
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer"
        )

        # Create test cars
        self.car1 = Car.objects.create(
            model="Toyota Camry", manufacturer=self.manufacturer)
        self.car2 = Car.objects.create(
            model="Honda Accord", manufacturer=self.manufacturer)
        self.car3 = Car.objects.create(
            model="Ford Focus", manufacturer=self.manufacturer)
        self.car4 = Car.objects.create(
            model="Toyota Corolla", manufacturer=self.manufacturer)
        self.car5 = Car.objects.create(
            model="Honda Civic", manufacturer=self.manufacturer)
        self.car6 = Car.objects.create(
            model="Nissan Altima", manufacturer=self.manufacturer)

    def test_car_list_view_pagination(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(len(response.context["object_list"]), 5)

        response = self.client.get(reverse("taxi:car-list") + "?page=2")
        self.assertEqual(len(response.context["object_list"]), 1)

    def test_car_list_view_filtering(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Toyota"}
        )
        self.assertEqual(len(response.context["object_list"]), 2)
        self.assertContains(response, "Toyota Camry")
        self.assertContains(response, "Toyota Corolla")

        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Honda"}
        )
        self.assertEqual(len(response.context["object_list"]), 2)
        self.assertContains(response, "Honda Accord")
        self.assertContains(response, "Honda Civic")

    def test_car_list_view_redirects_when_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f'/accounts/login/?next={reverse("taxi:car-list")}'
        )
