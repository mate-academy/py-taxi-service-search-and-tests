from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")
NUMBER_OF_OBJECT = 10
NUMBER_PER_PAGE = 5
USER = get_user_model()


class PublicAccessibilityTest(TestCase):
    def test_manufacturers_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_cars_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_drivers_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = USER.objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

        for i in range(NUMBER_OF_OBJECT):
            Manufacturer.objects.create(
                name=f"BMW{i}",
                country="Germany",
            )
        self.manufacturers = Manufacturer.objects.all()

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW1")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(self.manufacturers)[:NUMBER_PER_PAGE]
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_paginate_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(
            len(list(response.context["manufacturer_list"])),
            NUMBER_PER_PAGE
        )

    def test_search_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "BMW1"})
        self.assertContains(response, "BMW1")

    def test_search_manufacturers_partial_match(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "BMW1"})
        self.assertContains(response, "BMW")


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = USER.objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

        bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        for i in range(NUMBER_OF_OBJECT):
            Car.objects.create(
                manufacturer=bmw,
                model=f"X{i}",
            )
        self.cars = Car.objects.all()

    def test_retrieve_cars(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(self.cars)[:NUMBER_PER_PAGE]
        )
        self.assertContains(response, "X1")
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_paginate_cars(self):
        response = self.client.get(CAR_URL)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(
            len(list(response.context["car_list"])),
            NUMBER_PER_PAGE
        )

    def test_search_cars(self):
        response = self.client.get(CAR_URL, {"model": "X1"})
        self.assertContains(response, "X1")

    def test_cars_search_partial_match(self):
        response = self.client.get(CAR_URL, {"model": "X5"})
        self.assertContains(response, "X")


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = USER.objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

        for i in range(NUMBER_OF_OBJECT):
            USER.objects.create_user(
                username=f"test{i}",
                license_number=f"DSS3241{i}"
            )
        self.drivers = USER.objects.all()

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(self.drivers)[:NUMBER_PER_PAGE]

        )
        self.assertContains(response, "DSS32413")
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_paginate_drivers(self):
        response = self.client.get(DRIVER_URL)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(
            len(list(response.context["driver_list"])),
            NUMBER_PER_PAGE
        )

    def test_search_drivers(self):
        response = self.client.get(DRIVER_URL, {"username": "test1"})
        self.assertContains(response, "test1")
        self.assertNotContains(response, "test2")

    def test_search_drivers_partial_match(self):
        response = self.client.get(DRIVER_URL, {"username": "test1"})
        self.assertContains(response, "est1")
