from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class LoginRequiredMixinTest(TestCase):
    def test_car_login(self):
        url = reverse("taxi:car-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_driver_login(self):
        url = reverse("taxi:driver-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_login(self):
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateViewTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="name",
            password="password",
            license_number="ABC12345",
        )
        self.client.force_login(user)

    def test_manufacturer_objects_view(self):
        Manufacturer.objects.create(
            name="Test",
            country="Country Test"
        )
        Manufacturer.objects.create(
            name="Test321",
            country="Country 123Test"
        )

        manufacturer = Manufacturer.objects.all()

        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturer)
        )

    def test_manufacturer_template_view(self):
        Manufacturer.objects.create(
            name="Test",
            country="Country Test"
        )
        Manufacturer.objects.create(
            name="Test321",
            country="Country 123Test"
        )

        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_in_manufacturer_list(self):
        Manufacturer.objects.create(
            name="Lexus",
            country="Country Test"
        )
        Manufacturer.objects.create(
            name="Audi",
            country="Country 123Test"
        )
        Manufacturer.objects.create(
            name="BMW",
            country="Country 123Test"
        )

        searching = Manufacturer.objects.filter(name__icontains="a")

        url = reverse("taxi:manufacturer-list") + "?name=a"
        res = self.client.get(url)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(searching))
