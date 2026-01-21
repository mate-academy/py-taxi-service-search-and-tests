from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class PublicManufacturerTest(TestCase):
    def test_login_required_manufacturer_list_view(self) -> None:
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_manufacturer_create_view(self) -> None:
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_manufacturer_update_view(self) -> None:
        response = self.client.get(reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": 1})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_manufacturer_delete_view(self) -> None:
        response = self.client.get(reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": 1})
        )
        self.assertNotEqual(response.status_code, 200)


class PublicCarTest(TestCase):
    def test_login_required_car_list_view(self) -> None:
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_car_detail_view(self) -> None:
        response = self.client.get(reverse(
            "taxi:car-detail",
            kwargs={"pk": 1})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_car_create_view(self) -> None:
        response = self.client.get(reverse("taxi:car-create"))
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_car_update_view(self) -> None:
        response = self.client.get(reverse(
            "taxi:car-update",
            kwargs={"pk": 1})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_car_delete_view(self) -> None:
        response = self.client.get(reverse(
            "taxi:car-delete",
            kwargs={"pk": 1})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_toggle_assign_to_car(self) -> None:
        response = self.client.get(reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": 1})
        )
        self.assertNotEqual(response.status_code, 200)


class PublicDriverTest(TestCase):
    def test_login_required_driver_list_view(self) -> None:
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_driver_detail_view(self) -> None:
        response = self.client.get(reverse(
            "taxi:driver-detail",
            kwargs={"pk": 1})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_driver_create_view(self) -> None:
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_driver_update_view(self) -> None:
        response = self.client.get(reverse(
            "taxi:driver-update",
            kwargs={"pk": 1})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_driver_delete_view(self) -> None:
        response = self.client.get(reverse(
            "taxi:driver-delete",
            kwargs={"pk": 1})
        )
        self.assertNotEqual(response.status_code, 200)


class PrivateTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Eren",
            password="12345",
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        drivers = Driver.objects.create_user(
            username="Test",
            password="12345",
            license_number="12345test"
        )
        Car.objects.create(
            model="BMW X5",
            manufacturer=manufacturer
        ).drivers.add(drivers)

    def test_retrieve_manufacturer_list_view(self) -> None:
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_car_list_view(self) -> None:
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

        car = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(car))

        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_driver_list_view(self) -> None:
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)

        drivers = Driver.objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(drivers))

        self.assertTemplateUsed(response, "taxi/driver_list.html")
