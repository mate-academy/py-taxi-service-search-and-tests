from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL_WITH_SEARCH = (
    reverse("taxi:manufacturer-list") + "?name=toyota"
)
DRIVER_URL_WITH_SEARCH = reverse("taxi:driver-list") + "?username=admin"
CAR_URL_WITH_SEARCH = reverse("taxi:car-list") + "?model=c"
CAR_DETAIL_URL = reverse("taxi:car-detail", kwargs={"pk": 1})
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", kwargs={"pk": 1})
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicManufacturerTest(TestCase):
    def test_list_manufacturers(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_list_manufacturers_with_search(self):
        res = self.client.get(MANUFACTURER_URL_WITH_SEARCH)
        self.assertNotEqual(res.status_code, 200)


class PublicDriverTest(TestCase):
    def test_list_drivers(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_list_drivers_with_search(self):
        res = self.client.get(DRIVER_URL_WITH_SEARCH)
        self.assertNotEqual(res.status_code, 200)

    def test_driver_detail(self):
        res = self.client.get(DRIVER_DETAIL_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicCarTest(TestCase):
    def test_list_cars(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_list_cars_with_search(self):
        res = self.client.get(CAR_URL_WITH_SEARCH)
        self.assertNotEqual(res.status_code, 200)

    def test_car_detail(self):
        res = self.client.get(CAR_DETAIL_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Toyota", country="Japan")

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_manufacturers_with_search(self):
        response = self.client.get(MANUFACTURER_URL_WITH_SEARCH)
        manufacturers = Manufacturer.objects.filter(name="Toyota")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="123456789",
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_drivers_with_search(self):
        response = self.client.get(DRIVER_URL_WITH_SEARCH)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_detail(self):
        response = self.client.get(DRIVER_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_create_driver(self):
        payload = {
            "username": "testuser2",
            "password1": "testpass123",
            "password2": "testpass123",
            "license_number": "ABC12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=payload)
        user_new = get_user_model().objects.get(username=payload["username"])
        self.assertEqual(user_new.license_number, payload["license_number"])


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="123456789",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Car.objects.create(
            model="testmodel",
            manufacturer=Manufacturer.objects.get(name="Toyota")
        )

    def test_retrieve_cars(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_cars_with_search(self):
        response = self.client.get(CAR_URL_WITH_SEARCH)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_detail(self):
        response = self.client.get(CAR_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
