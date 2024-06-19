from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Car, Manufacturer


class CarSearchAccuracyTestCase(TestCase):
    def setUp(self) -> None:
        self.manufacturer1 = Manufacturer.objects.create(name="Bmw",
                                                         country="Dutch")
        self.manufacturer2 = Manufacturer.objects.create(name="Opel",
                                                         country="Dutch")
        self.manufacturer3 = Manufacturer.objects.create(name="Mers",
                                                         country="Dutch")

        self.car1 = Car.objects.create(model="M3",
                                       manufacturer=self.manufacturer1)

        self.car2 = Car.objects.create(model="astra",
                                       manufacturer=self.manufacturer2)

        self.car3 = Car.objects.create(model="e60",
                                       manufacturer=self.manufacturer3)

        self.car4 = Car.objects.create(model="zafira",
                                       manufacturer=self.manufacturer2)

        self.car5 = Car.objects.create(model="cls",
                                       manufacturer=self.manufacturer3)
        self.client = Client()
        self.driver = get_user_model().objects.create(
            username="test",
            email="<ilaruslanovich7@gmail.com>",
            password="<Gitarist2005>",
            first_name="test",
            last_name="test",
            license_number="ABC12345")
        self.client.force_login(self.driver)
        self.car1.drivers.add(self.driver)
        self.car2.drivers.add(self.driver)
        self.car3.drivers.add(self.driver)
        self.car4.drivers.add(self.driver)
        self.car5.drivers.add(self.driver)

    def test_search_exact_model(self) -> None:
        response = self.client.get(reverse("taxi:car-list"),
                                   {"model": "M3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car3.model)
        self.assertNotContains(response, self.car4.model)
        self.assertNotContains(response, self.car5.model)

    def test_view_without_search_parameters(self) -> None:
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)


class ManufacturerSearchTestCase(TestCase):
    def setUp(self) -> None:
        self.manufacturer1 = Manufacturer.objects.create(name="Bmw",
                                                         country="Dutch")
        self.manufacturer2 = Manufacturer.objects.create(name="Opel",
                                                         country="Dutch")
        self.manufacturer3 = Manufacturer.objects.create(name="Mers",
                                                         country="Dutch")
        self.driver = get_user_model().objects.create(
            username="test",
            email="<ilaruslanovich7@gmail.com>",
            password="<Gitarist2005>",
            first_name="test",
            last_name="test",
            license_number="ABC12345")
        self.client.force_login(self.driver)

    def test_search_exact_name(self) -> None:
        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"name": "Bmw"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer3.name)

        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"name": "Opel"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer2.name)
        self.assertNotContains(response, self.manufacturer3.name)


class DriverSearchTestCase(TestCase):
    def setUp(self) -> None:
        self.driver1 = get_user_model().objects.create(
            username="test",
            email="<ilaruslanovich7@gmail.com>",
            password="<Gitarist2005>",
            first_name="test",
            last_name="test",
            license_number="ABC12345")

        self.driver2 = get_user_model().objects.create(
            username="illia",
            email="<ilaruslanovich8@gmail.com>",
            password="<Gitarist2001>",
            first_name="lol",
            last_name="lol",
            license_number="QDC14146")
        self.client.force_login(self.driver1)

    def test_search_exact_username(self) -> None:
        response = self.client.get(reverse("taxi:driver-list"),
                                   {"username": "test"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.driver1, response.context.get("driver_list"))
        self.assertNotIn(self.driver2, response.context.get("driver_list"))

        response = self.client.get(reverse("taxi:driver-list"),
                                   {"username": "illia"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.driver2, response.context.get("driver_list"))

        self.assertNotIn(self.driver1, response.context.get("driver_list"))
