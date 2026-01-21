from multiprocessing.connection import Client

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class PublicCarTests(TestCase):
    def test_car_list_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_car_detail_login_required(self):
        url = reverse("taxi:car-detail", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_car_create_login_required(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertNotEqual(response.status_code, 200)

    def test_car_update_login_required(self):
        url = reverse("taxi:car-update", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_car_delete_login_required(self):
        url = reverse("taxi:car-delete", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            license_number="AAA11111"
        )
        self.client.force_login(driver)
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country",
        )
        Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        Car.objects.create(
            model="test1",
            manufacturer=manufacturer,
        )

    def test_car_list_view(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.all())
        )

    def test_car_detail_view(self):
        url = reverse("taxi:car-detail", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertContains(response, str(Car.objects.get(pk=1)))

    def test_car_search_view(self):
        response = self.client.get(reverse("taxi:car-list") + "?search=1")
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__icontains="1"))
        )
