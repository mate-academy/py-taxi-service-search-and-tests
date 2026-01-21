from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

LOGIN_REQUIRED_DIRECT_PATHS = [
    "index",
    "manufacturer-list",
    "manufacturer-create",
    "car-list",
    "car-create",
    "driver-list",
    "driver-create"
]

LOGIN_REQUIRED_PARAMETRIZED_PATHS = [
    "manufacturer-update",
    "manufacturer-delete",
    "car-detail",
    "car-update",
    "car-delete",
    "driver-detail",
    "driver-update",
    "driver-delete"
]


class PublicTaxiTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="test_username",
            license_number="test_license_number",
            password="test_password"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer
        )

    def test_login_required(self) -> None:
        respond_logs = dict()
        for path in LOGIN_REQUIRED_DIRECT_PATHS:
            client_response = self.client.get(reverse(f"taxi:{path}"))
            respond_logs.update({path: client_response.status_code})
        for path in LOGIN_REQUIRED_PARAMETRIZED_PATHS:
            client_response = self.client.get(
                reverse(f"taxi:{path}", kwargs={"pk": 1})
            )
            respond_logs.update({path: client_response.status_code})
        for path, status in respond_logs.items():
            self.assertNotEqual(
                status,
                200,
                msg=f"Path {path} is free without login!"
            )


class PrivateTaxiTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="test_username",
            license_number="test_license_number",
            password="test_password"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer
        )
        self.car.drivers.set((self.user,))
        self.client.force_login(self.user)

    def test_toggle_index(self) -> None:
        num_drivers = Driver.objects.count()
        num_cars = Car.objects.count()
        num_manufacturers = Manufacturer.objects.count()

        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(
            response.context["num_drivers"],
            num_drivers
        )
        self.assertEqual(
            response.context["num_cars"],
            num_cars
        )
        self.assertEqual(
            response.context["num_manufacturers"],
            num_manufacturers
        )

    def test_toggle_manufacturer_list(self) -> None:
        manufacturers = Manufacturer.objects.all()
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(
            list(response.context.get("manufacturer_list", [])),
            list(manufacturers)
        )

    def test_toggle_car_list(self) -> None:
        cars = Car.objects.all()
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(
            list(response.context.get("car_list", [])),
            list(cars)
        )

    def test_toggle_driver_list(self) -> None:
        drivers = Driver.objects.all()
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(
            list(response.context.get("driver_list", [])),
            list(drivers)
        )

    def test_template(self) -> None:
        for path in LOGIN_REQUIRED_DIRECT_PATHS:
            client_response = self.client.get(reverse(f"taxi:{path}"))
            template = path.replace("-", "_").replace("create", "form")
            self.assertTemplateUsed(
                client_response,
                f"taxi/{template}.html"
            )
        for path in LOGIN_REQUIRED_PARAMETRIZED_PATHS:
            client_response = self.client.get(
                reverse(f"taxi:{path}", kwargs={"pk": 1})
            )
            template = path.replace("-", "_").replace("update", "form")
            template = template.replace("delete", "confirm_delete")
            self.assertTemplateUsed(
                client_response,
                f"taxi/{template}.html"
            )
