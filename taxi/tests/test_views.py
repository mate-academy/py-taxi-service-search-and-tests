from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="AUDI", country="Germany")
        Manufacturer.objects.create(name="AKURA", country="Japan")

    def test_search_by_name(self):
        response = self.client.get(
            reverse(
                "taxi:manufacturer-list") + "?name=A"
        )
        self.assertEqual(response.status_code, 200)
        actual = response.context.get("manufacturer-list")
        expected = Manufacturer.objects.filter(name__icontains="A")
        self.assertEqual(list(actual), list(expected))
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=AUDI"
        )
        actual = response.context.get("manufacturer-list")
        expected = Manufacturer.objects.filter(name__icontains="AUDI")

        self.assertEqual(list(actual), list(expected))


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.force_login(self.user)
        bmw = Manufacturer.objects.create(name="BMW", country="Germany")
        audi = Manufacturer.objects.create(name="AUDI", country="Germany")

        Car.objects.create(model="X5", manufacturer=bmw)
        Car.objects.create(model="A4", manufacturer=audi)

    def test_search_by_model(self):
        response = self.client.get(
            reverse(
                "taxi:car-list") + "?model=A"
        )
        self.assertEqual(response.status_code, 200)
        actual = response.context.get("car-list")
        expected = Car.objects.filter(model__icontains="A")
        self.assertEqual(list(actual), list(expected))
        response = self.client.get(
            reverse("taxi:car-list") + "?model=A4"
        )
        actual = response.context.get("car-list")
        expected = Car.objects.filter(model__icontains="A4")

        self.assertEqual(list(actual), list(expected))


class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            license_number="ABC32145",
        )
        self.client.force_login(self.user)

        get_user_model().objects.create_user(
            username="valiandro",
            password="mukacco",
            license_number="POI98765",
        )
        get_user_model().objects.create_user(
            username="pedro",
            password="piccolino",
            license_number="IJU43257",
        )

    def test_search_by_model(self):
        response = self.client.get(
            reverse(
                "taxi:driver-list") + "?username=v"
        )
        self.assertEqual(response.status_code, 200)
        actual = response.context.get("driver-list")
        expected = get_user_model().objects.filter(username__icontains="v")
        self.assertEqual(list(actual), list(expected))
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=valiandro"
        )
        actual = response.context.get("driver-list")
        expected = get_user_model().objects.filter(
            username__icontains="valiandro")

        self.assertEqual(list(actual), list(expected))
