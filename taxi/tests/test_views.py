from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL_WITH_SEARCH = reverse("taxi:driver-list") + "?username=admin"
CAR_URL_WITH_SEARCH = reverse("taxi:car-list") + "?model=c"
CAR_DETAIL_URL = reverse("taxi:car-detail", kwargs={"pk": 1})
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", kwargs={"pk": 1})
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicManufacturerTest(TestCase):
    def test_list_manufacturers(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicDriverTest(TestCase):
    def test_list_drivers(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_driver_detail(self):
        res = self.client.get(DRIVER_DETAIL_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicCarTest(TestCase):
    def test_list_cars(self):
        res = self.client.get(CAR_URL)
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
        Manufacturer.objects.create(name="Honda", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="BMW", country="Germany")

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
        response = self.client.get(MANUFACTURER_URL + "?manufacturer=to")
        manufacturers = Manufacturer.objects.filter(name__icontains="to")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="123456789",
        )
        user1 = get_user_model().objects.create_user(
            username="testuser2",
            password="testpass123",
            license_number="1234567a",
        )
        user2 = get_user_model().objects.create_user(
            username="testuser3",
            password="testpass123",
            license_number="1234567s",
        )
        self.client.force_login(self.user)
        self.client.force_login(user1)
        self.client.force_login(user2)

    def test_retrieve_drivers_with_search(self):
        response = self.client.get(DRIVER_URL + "?username=testuser2")
        drivers = get_user_model().objects.filter(
            username__icontains="testuser2"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))

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
        Car.objects.create(
            model="testmodel2",
            manufacturer=Manufacturer.objects.get(name="Toyota")
        )
        Car.objects.create(
            model="testmodel3",
            manufacturer=Manufacturer.objects.get(name="Toyota")
        )

    def test_retrieve_cars_with_search(self):
        response = self.client.get(CAR_URL + "?model=3")
        cars = Car.objects.filter(model__icontains="3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))

    def test_car_detail(self):
        response = self.client.get(CAR_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
