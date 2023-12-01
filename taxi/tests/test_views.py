import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.forms import (
    CarModelSearchForm,
    DriverUsernameSearchForm,
    ManufacturerNameSearchForm,
)
from taxi.models import Car, Manufacturer


MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
HOME_PAGE = reverse("taxi:index")


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url",
    [MANUFACTURER_URL, DRIVER_URL, CAR_URL, HOME_PAGE]
)
def test_public_page(client, url):
    response = client.get(url)
    assert response.status_code != 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url",
    [MANUFACTURER_URL, DRIVER_URL, CAR_URL, HOME_PAGE]
)
def test_private_page(client, url):
    user = get_user_model().objects.create(
        username="john11",
        first_name="John",
        last_name="Doe",
        password="111222John",
        license_number="ADM56984"
    )
    client.force_login(user)

    response = client.get(url)
    assert response.status_code == 200


class CarListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="john11",
            first_name="John",
            last_name="Doe",
            password="111222John",
            license_number="ADM56984"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Some Manufacturer",
            country="Some Country",
        )

        self.car1 = Car.objects.create(
            model="BMW",
            manufacturer=self.manufacturer,
        )
        self.car2 = Car.objects.create(
            model="Mercedes",
            manufacturer=self.manufacturer,
        )

    def test_car_list_view_with_search(self):
        response = self.client.get(CAR_URL, {"model": "BMW"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Mercedes")

    def test_car_list_view_without_search(self):
        response = self.client.get(CAR_URL)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")
        self.assertContains(response, "Mercedes")

    def test_car_list_view_context_data(self):
        response = self.client.get(CAR_URL)

        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"],
            CarModelSearchForm
        )


class DriverListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="john11",
            first_name="John",
            last_name="Doe",
            password="111222John",
            license_number="ADM56984"
        )
        self.client.force_login(self.user)

        self.driver1 = get_user_model().objects.create(
            username="driver1", password="11222John", license_number="BDM56984"
        )

        self.driver2 = get_user_model().objects.create(
            username="driver2", password="21222John", license_number="CDM56984"
        )

    def test_driver_list_view_with_search(self):
        response = self.client.get(DRIVER_URL, {"username": "driver1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver1")
        self.assertNotContains(response, "driver2")

    def test_driver_list_view_without_search(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver1")
        self.assertContains(response, "driver2")

    def test_driver_list_view_context_data(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"],
            DriverUsernameSearchForm
        )


class ManufacturerListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="john11",
            first_name="John",
            last_name="Doe",
            password="111222John",
            license_number="ADM56984"
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Some Manufacturer1", country="Some Country1"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Some Manufacturer2",
            country="Some Country2",
        )

    def test_manufacturer_list_view_with_search(self):
        response = self.client.get(
            MANUFACTURER_URL, {"name": "Some Manufacturer1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Some Manufacturer1")
        self.assertNotContains(response, "Some Manufacturer2")

    def test_manufacturer_list_view_without_search(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Some Manufacturer1")
        self.assertContains(response, "Some Manufacturer2")

    def test_manufacturer_list_view_context_data(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"], ManufacturerNameSearchForm
        )
