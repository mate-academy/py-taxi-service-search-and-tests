from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerNameSearchForm
from taxi.models import Manufacturer, Car


class TestValidSearchForm(TestCase):
    def test_form_valid(self):
        form = ManufacturerNameSearchForm(data={"name": "bmw"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "bmw")

    def test_form_empty_valid(self):
        form = ManufacturerNameSearchForm(data={"filter": "audi"})
        self.assertTrue(form.is_valid())


class TestSearchForm(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Vladislav",
            password="testpassword",
            license_number="USR00001",
        )
        self.client.login(username="Vladislav", password="testpassword")

        self.user2 = get_user_model().objects.create_user(
            username="Maxim",
            password="testpassword2",
            license_number="USR00002",
        )
        self.user3 = get_user_model().objects.create_user(
            username="Danylo",
            password="testpassword3",
            license_number="USR00003",
        )
        self.user4 = get_user_model().objects.create_user(
            username="Kyryllo",
            password="testpassword4",
            license_number="USR00004",
        )

        self.m1 = Manufacturer.objects.create(name="bmw", country="DE")
        self.m2 = Manufacturer.objects.create(name="Zchiguli", country="USSR")
        self.m3 = Manufacturer.objects.create(name="hammer", country="USA")

        self.c1 = Car.objects.create(
            model="M5 F90",
            manufacturer=self.m1,
        )
        self.c2 = Car.objects.create(
            model="Kopeika",
            manufacturer=self.m2,
        )
        self.c3 = Car.objects.create(
            model="Hammer",
            manufacturer=self.m3,
        )
        self.c1.drivers.add(self.user)
        self.c2.drivers.add(self.user2)
        self.c3.drivers.add(self.user3)

    def test_manufacturer_search(self):
        url = reverse("taxi:manufacturer-list") + "?name=b"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        result = response.context["manufacturer_list"]

        self.assertIn(self.m1, result)
        self.assertNotIn(self.m2, result)
        self.assertNotIn(self.m3, result)
        self.assertEqual(len(result), 1)

    def test_cars_search(self):
        url = reverse("taxi:car-list") + "?model_name=M"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        result = response.context["car_list"]

        self.assertIn(self.c1, result)
        self.assertNotIn(self.c2, result)
        self.assertIn(self.c3, result)
        self.assertEqual(len(result), 2)

    def test_driver_search(self):
        url = reverse("taxi:driver-list") + "?username=I"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        result = response.context["driver_list"]

        self.assertIn(self.user, result)
        self.assertIn(self.user2, result)
        self.assertNotIn(self.user3, result)
        self.assertNotIn(self.user4, result)
        self.assertEqual(len(result), 2)
