from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm, CarSearchForm, DriverSearchForm
from taxi.models import Manufacturer, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicManufacturerViewTest(TestCase):
    def test_manufacturer_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(res.status_code, 302)


class PublicCarViewTest(TestCase):
    def test_car_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertEqual(res.status_code, 302)


class PublicDriverViewTest(TestCase):
    def test_driver_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(res.status_code, 302)


class PrivateManufacturerViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            license_number="AA12345",
        )
        self.client.force_login(self.user)

    def test_manufacturer_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_search_form_valid(self):
        form_data = {
            "name": "test_name",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_context_valid(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertIn("search_form", res.context)

    def test_manufacturer_search(self):
        test_filter = "B"
        Manufacturer.objects.create(
            name="test_C",
            country="test_country",
        )
        Manufacturer.objects.create(
            name="test_B",
            country="test_country",
        )
        res = self.client.get(
            MANUFACTURER_LIST_URL,
            {"name": test_filter},
        )
        self.assertEqual(
            list(res.context["object_list"]),
            list(Manufacturer.objects.filter(name__icontains=test_filter))
        )


class PrivateCarViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            license_number="AA12345",
        )
        self.client.force_login(self.user)

    def test_car_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertEqual(res.status_code, 200)

    def test_car_search_form_valid(self):
        form_data = {
            "model": "test_model",
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_context_valid(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertIn("search_form", res.context)

    def test_car_search(self):
        test_filter = "B"
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country",
        )
        Car.objects.create(
            model="test_C",
            manufacturer=manufacturer,
        )
        Car.objects.create(
            model="test_B",
            manufacturer=manufacturer,
        )
        res = self.client.get(
            CAR_LIST_URL,
            {"model": test_filter},
        )
        self.assertEqual(
            list(res.context["object_list"]),
            list(Car.objects.filter(model__icontains=test_filter))
        )


class PrivateDriverViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            license_number="AA12345",
        )
        self.client.force_login(self.user)

    def test_driver_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(res.status_code, 200)

    def test_driver_search_form_valid(self):
        form_data = {
            "username": "test_username",
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_context_valid(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertIn("search_form", res.context)

    def test_driver_search(self):
        test_filter = "B"
        get_user_model().objects.create(
            username="test_B",
            password="test123",
            license_number="AA12346",
        )
        get_user_model().objects.create(
            username="test_C",
            password="test123",
            license_number="AA12347",
        )
        res = self.client.get(
            DRIVER_LIST_URL,
            {"username": test_filter},
        )
        self.assertEqual(
            list(res.context["object_list"]),
            (list(get_user_model()
                  .objects
                  .filter(username__icontains=test_filter)))
        )
