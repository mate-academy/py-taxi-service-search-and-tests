from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicViewTest(TestCase):
    def test_public_car_list(self):
        url = reverse("taxi:car-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_public_manufacturer_list(self):
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_public_driver_list(self):
        url = reverse("taxi:driver-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="test_superuser",
            password="test_password",
            license_number="test_license_number",
        )
        self.client.force_login(self.user)

    def test_manufacturer_content(self):
        Manufacturer.objects.create(
            name="test_manufacturer1",
            country="test_country1",
        )
        Manufacturer.objects.create(
            name="test_manufacturer2",
            country="test_country2",
        )
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(Manufacturer.objects.all()),
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_driver_content(self):
        get_user_model().objects.create_user(
            username="test_user",
            password="password",
        )
        url = reverse("taxi:driver-list")
        res = self.client.get(url)
        users = get_user_model().objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["driver_list"]), list(users))
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_car_content(self):
        test_manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country",
        )
        Car.objects.create(model="test_model1", manufacturer=test_manufacturer)
        Car.objects.create(model="test_model2", manufacturer=test_manufacturer)
        url = reverse("taxi:car-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(res.context["car_list"]), list(cars))
        self.assertTemplateUsed(res, "taxi/car_list.html")
