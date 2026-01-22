from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class PublicTaxiTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_list_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_update_login_required(self):
        response = self.client.get(
            reverse("taxi:manufacturer-update", kwargs={"pk": 1})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_delete_login_required(self):
        response = self.client.get(
            reverse("taxi:manufacturer-delete", kwargs={"pk": 1})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_create_login_required(self):
        response = self.client.get(
            reverse("taxi:manufacturer-create")
        )
        self.assertNotEqual(response.status_code, 200)

    def test_car_detail_login_required(self):
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": 1})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_car_list_login_required(self):
        response = self.client.get(
            reverse("taxi:car-list")
        )
        self.assertNotEqual(response.status_code, 200)

    def test_car_update_login_required(self):
        response = self.client.get(
            reverse("taxi:car-update", kwargs={"pk": 1})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_car_create_login_required(self):
        response = self.client.get(
            reverse("taxi:car-create")
        )
        self.assertNotEqual(response.status_code, 200)

    def test_car_delete_login_required(self):
        response = self.client.get(
            reverse("taxi:car-delete", kwargs={"pk": 1})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_driver_detail_login_required(self):
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": 1})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_driver_list_login_required(self):
        response = self.client.get(
            reverse("taxi:driver-list")
        )
        self.assertNotEqual(response.status_code, 200)

    def test_driver_update_login_required(self):
        response = self.client.get(
            reverse("taxi:driver-update", kwargs={"pk": 1})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_driver_create_login_required(self):
        response = self.client.get(
            reverse("taxi:driver-create")
        )
        self.assertNotEqual(response.status_code, 200)

    def test_driver_delete_login_required(self):
        response = self.client.get(
            reverse("taxi:driver-delete", kwargs={"pk": 1})
        )
        self.assertNotEqual(response.status_code, 200)


class PrivateTaxiTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="test1234",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer_name",
            country="test_country"
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        self.client.force_login(self.driver)

    def test_driver_detail(self):
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)

    def test_retrieve_drivers(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(
            list(response.context["driver_list"]),
            list(get_user_model().objects.all())
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_car_detail(self):
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)

    def test_retrieve_cars(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.all())
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_manufacturers(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.all())
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
