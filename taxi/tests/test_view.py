from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class PublicViewTest(TestCase):
    def test_access_to_private_car_list(self):
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_result_search_manufacture(self):
        user = Driver.objects.create_superuser(
            username="admin",
            password="123",
        )
        self.client.force_login(user)
        Manufacturer.objects.create(
            name="bmw",
            country="germany"
        )
        Manufacturer.objects.create(
            name="tesla",
            country="USA",
        )
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url, {"name": "bmw"})

        self.assertEqual(res.status_code, 200)

        manufacturs = res.context["manufacturer_list"]

        self.assertEqual(manufacturs[0].name, "bmw")

    def test_result_search_cars(self):
        user = Driver.objects.create_superuser(
            username="admin",
            password="123",
        )
        self.client.force_login(user)
        obj1 = Manufacturer.objects.create(
            name="wd",
            country="ewfwef",
        )
        man1 = Car.objects.create(
            model="bmw",
            manufacturer=obj1
        )
        man1.drivers.add(user)
        man2 = Car.objects.create(
            model="tesla",
            manufacturer=obj1
        )
        man2.drivers.add(user)
        man1.save()
        man2.save()
        url = reverse("taxi:car-list")
        res = self.client.get(url, {"model": "bmw"})

        self.assertEqual(res.status_code, 200)

        car = res.context["car_list"]

        self.assertEqual(car[0].model, "bmw")

    def test_result_search_driver(self):
        user = Driver.objects.create_superuser(
            username="admin",
            password="123",
        )
        self.client.force_login(user)
        Driver.objects.create(
            username="admin2",
            password="123",
            license_number="JFJ33333"
        )
        Driver.objects.create(
            username="admin3",
            password="123",
            license_number="JFJ22222"
        )
        url = reverse("taxi:driver-list")
        res = self.client.get(url, {"username": "admin2"})

        self.assertEqual(res.status_code, 200)

        drivers = res.context["driver_list"]

        self.assertEqual(drivers[0].username, "admin2")

    def test_search_when_request_empty_car(self):
        user = Driver.objects.create_superuser(
            username="admin",
            password="123",
        )
        self.client.force_login(user)
        obj1 = Manufacturer.objects.create(
            name="wd",
            country="ewfwef",
        )
        man1 = Car.objects.create(
            model="bmw",
            manufacturer=obj1
        )
        man1.drivers.add(user)
        man2 = Car.objects.create(
            model="tesla",
            manufacturer=obj1
        )
        man2.drivers.add(user)
        man1.save()
        man2.save()
        url = reverse("taxi:car-list")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

        car = res.context["car_list"]

        self.assertEqual(len(car), 2)
