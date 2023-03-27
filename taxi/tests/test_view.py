from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
PAGINATION = 5


class PublicCarTest(TestCase):
    def test_login_required_driver(self) -> None:
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response, 200)

    def test_login_required_car(self) -> None:
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response, 200)

    def test_login_required_manufactarer(self) -> None:
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )
        self.client.force_login(self.user)

    def test_search_car(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Mazda", country="Japan"
        )
        key = "c"
        car = Car.objects.create(
            model="CX-5", manufacturer=manufacturer
        )
        car.drivers.add(self.user)
        response = self.client.get(
            reverse("taxi:car-list") + f"?model={key}")

        car_list = Car.objects.filter(model__icontains=key)
        self.assertEqual(
            list(response.context["car_list"]), list(car_list)
        )

    def test_template_for_car_list(self) -> None:
        response = self.client.get(CAR_URL)
        self.assertTemplateUsed(
            response, "taxi/car_list.html"
        )


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )
        self.client.force_login(self.user)

    def test_search_driver_by_username(self) -> None:
        get_user_model().objects.create_user(
            username="testUser",
            first_name="Test",
            last_name="User",
            license_number="SDF12345",
        )
        key = "testUser"
        response = self.client.get(
            reverse("taxi:driver-list") + f"?username={key}"
        )
        driver_list = Driver.objects.filter(
            username__icontains=key
        )
        self.assertEqual(
            list(response.context["driver_list"]), list(driver_list)
        )

    def test_template_for_driver_list(self) -> None:
        response = self.client.get(DRIVER_URL)
        self.assertTemplateUsed(
            response, "taxi/driver_list.html"
        )

    def test_correct_pagination(self) -> None:
        response = self.client.get(DRIVER_URL)
        self.assertEqual(
            len(response.context["driver_list"]), PAGINATION
        )


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )
        self.client.force_login(self.user)

    def test_manufacturer_search_by_name(self) -> None:
        Manufacturer.objects.create(
            name="Mazda", country="Japan"
        )
        key = "mazd"
        response = self.client.get(
            reverse("taxi:manufacturer-list"
                    ) + f"?model={key}")
        manufacturer_list = Manufacturer.objects.filter(
            name__icontains=key
        )
        self.assertEqual(
            list(
                response.context["manufacturer_list"]),
            list(manufacturer_list)
        )
