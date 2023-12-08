from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testpassword"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="FCA",
            country="Italy"
        )
        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testpassword"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        get_user_model().objects.create_user(
            username="driver1",
            password="driverpassword1",
            license_number="TC010101"
        )
        get_user_model().objects.create_user(
            username="driver2",
            password="driverpassword2",
            license_number="TC010100"
        )
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testpassword"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer1 = Manufacturer.objects.create(
            name="FCA",
            country="Italy"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        driver1 = get_user_model().objects.create(
            username="test1",
            password="testpassword1",
            first_name="first_test1",
            last_name="last_test1",
            license_number="TC000000"
        )

        driver2 = get_user_model().objects.create(
            username="test2",
            password="testpassword2",
            first_name="first_test2",
            last_name="last_test2",
            license_number="TC000001"
        )

        car1 = Car.objects.create(
            model="test",
            manufacturer=manufacturer1
        )
        car1.drivers.set([driver1, driver2])

        car2 = Car.objects.create(
            model="test",
            manufacturer=manufacturer2
        )
        car2.drivers.set((driver1,))

        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PaginationTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(username="admin", password="adminpass")
        self.client = Client()
        self.client.login(username="admin", password="adminpass")

        for i in range(15):
            manufacturer = Manufacturer.objects.create(name=f"Manufacturer {i}", country="Country {i}")
            driver = get_user_model().objects.create_user(
                username=f"driver{i}",
                password="testpassword",
                license_number=f"TC01010{i}")
            car = Car.objects.create(model=f'Car {i}', manufacturer=manufacturer)
            car.drivers.add(driver)

    def test_manufacturer_pagination(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['manufacturer_list']), 5)

    def test_car_pagination(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['car_list']), 5)

    def test_driver_pagination(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['driver_list']), 5)
