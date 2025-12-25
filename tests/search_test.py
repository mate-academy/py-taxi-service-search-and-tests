from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

DRIVER_LIST_URL = reverse("taxi:driver-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
FIRST_LETTER_SEARCH = "J"


class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )

        self.client.force_login(self.user)

        self.driver1 = get_user_model().objects.create(
            username=FIRST_LETTER_SEARCH + "ohn Test",
            password="test123",
            license_number="AAA12345")
        self.driver2 = get_user_model().objects.create(
            username=FIRST_LETTER_SEARCH + "ane Test",
            password="test123",
            license_number="BBB12345")
        self.driver3 = get_user_model().objects.create(
            username="Bob Test",
            password="test123",
            license_number="CCC12345")

    def test_empty_search_return_all(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver1.get_username())
        self.assertContains(response, self.driver2.get_username())
        self.assertContains(response, self.driver3.get_username())

    def test_search_work_with_part_of_request(self):
        response = self.client.get(
            DRIVER_LIST_URL,
            {
                "search_field":
                    self.driver1.get_username()[:len(FIRST_LETTER_SEARCH)]})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver1.get_username())
        self.assertContains(response, self.driver2.get_username())
        self.assertNotContains(response, self.driver3.get_username())

    def test_search_not_found_nothing_return_empty_list(self):
        response = self.client.get(DRIVER_LIST_URL, {"search_field": "123aaa"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.driver1.get_username())
        self.assertNotContains(response, self.driver2.get_username())
        self.assertNotContains(response, self.driver3.get_username())

    def test_search_case_insensitive(self):
        response = self.client.get(
            DRIVER_LIST_URL,
            {"search_field": self.driver1.get_username().upper()})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver1.get_username())
        self.assertNotContains(response, self.driver2.get_username())
        self.assertNotContains(response, self.driver3.get_username())


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )

        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(name="test manufacturer")

        self.car1 = Car.objects.create(
            model=FIRST_LETTER_SEARCH + "aguar",
            manufacturer=manufacturer)
        self.car2 = Car.objects.create(
            model=FIRST_LETTER_SEARCH + "et",
            manufacturer=manufacturer)
        self.car3 = Car.objects.create(
            model="BWM",
            manufacturer=manufacturer)

    def test_empty_search_return_all(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car1.model)
        self.assertContains(response, self.car2.model)
        self.assertContains(response, self.car3.model)

    def test_search_work_with_part_of_request(self):
        response = self.client.get(
            CAR_LIST_URL,
            {
                "search_field":
                    self.car1.model[:len(FIRST_LETTER_SEARCH)]})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car1.model)
        self.assertContains(response, self.car2.model)
        self.assertNotContains(response, self.car3.model)

    def test_search_not_found_nothing_return_empty_list(self):
        response = self.client.get(CAR_LIST_URL, {"search_field": "123aaa"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)
        self.assertNotContains(response, self.car3.model)

    def test_search_case_insensitive(self):
        response = self.client.get(
            CAR_LIST_URL,
            {"search_field": self.car1.model.upper()})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)
        self.assertNotContains(response, self.car3.model)


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )

        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name=FIRST_LETTER_SEARCH + "aguar")
        self.manufacturer2 = Manufacturer.objects.create(
            name=FIRST_LETTER_SEARCH + "et")
        self.manufacturer3 = Manufacturer.objects.create(name="BMW")

    def test_empty_search_return_all(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer1.name)
        self.assertContains(response, self.manufacturer2.name)
        self.assertContains(response, self.manufacturer3.name)

    def test_search_work_with_part_of_request(self):
        response = self.client.get(
            MANUFACTURER_LIST_URL,
            {
                "search_field":
                    self.manufacturer1.name[:len(FIRST_LETTER_SEARCH)]})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer1.name)
        self.assertContains(response, self.manufacturer2.name)
        self.assertNotContains(response, self.manufacturer3.name)

    def test_search_not_found_nothing_return_empty_list(self):
        response = self.client.get(MANUFACTURER_LIST_URL,
                                   {"search_field": "123aaa"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)
        self.assertNotContains(response, self.manufacturer3.name)

    def test_search_case_insensitive(self):
        response = self.client.get(
            MANUFACTURER_LIST_URL,
            {"search_field": self.manufacturer1.name.upper()})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)
        self.assertNotContains(response, self.manufacturer3.name)
