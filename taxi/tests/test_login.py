from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class PublicCarLoginTest(TestCase):
    def test_car_list(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 302)

    def test_car_detail(self):
        response = (self.client.get
                    (reverse("taxi:car-detail",
                             kwargs={"pk": 1})))
        self.assertEqual(response.status_code, 302)

    def test_car_create(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(response.status_code, 302)

    def test_car_update(self):
        response = (self.client.get
                    (reverse("taxi:car-update",
                             kwargs={"pk": 1})))
        self.assertEqual(response.status_code, 302)

    def test_car_delete(self):
        response = (self.client.get
                    (reverse("taxi:car-delete",
                             kwargs={"pk": 1})))
        self.assertEqual(response.status_code, 302)


class PublicDriverLoginTest(TestCase):
    def test_driver_list(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 302)

    def test_driver_detail(self):
        response = (self.client.get
                    (reverse("taxi:driver-detail",
                             kwargs={"pk": 1})))
        self.assertEqual(response.status_code, 302)

    def test_driver_create(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(response.status_code, 302)

    def test_driver_update(self):
        response = (self.client.get
                    (reverse("taxi:driver-update",
                             kwargs={"pk": 1})))
        self.assertEqual(response.status_code, 302)

    def test_driver_delete(self):
        response = (self.client.get
                    (reverse("taxi:driver-delete",
                             kwargs={"pk": 1})))
        self.assertEqual(response.status_code, 302)


class PublicManufacturerLoginTest(TestCase):
    def test_manufacturer_list(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 302)

    def test_manufacturer_create(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertEqual(response.status_code, 302)

    def test_manufacturer_update(self):
        response = self.client.get(
            reverse("taxi:manufacturer-update",
                    kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 302)

    def test_manufacturer_delete(self):
        response = self.client.get(
            reverse("taxi:manufacturer-delete",
                    kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 302)


class PrivateCarLoginTest(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="Admin", password="hard"
        )
        self.client.force_login(self.admin_user)

    @classmethod
    def setUpTestData(cls):
        manufacturer = (Manufacturer.objects.
                        create(name="Mercedes",
                               country="Germany"))
        Car.objects.create(model="Mercedes_G", manufacturer=manufacturer)

    def test_car_list(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

    def test_car_detail(self):
        response = (self.client.get
                    (reverse("taxi:car-detail",
                             kwargs={"pk": 1})))
        self.assertEqual(response.status_code, 200)

    def test_car_create(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(response.status_code, 200)

    def test_car_update(self):
        response = (self.client.get
                    (reverse("taxi:car-update",
                             kwargs={"pk": 1})))
        self.assertEqual(response.status_code, 200)

    def test_car_delete(self):
        response = (self.client.post
                    (reverse("taxi:car-delete",
                             args=(1,))))
        self.assertEqual(response.status_code, 302)


class PrivateManufacturerLoginTest(TestCase):

    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="Admin", password="hard"
        )
        self.client.force_login(self.admin_user)

    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="Mercedes",
                                    country="Germany")

    def test_manufacturer_list(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_create(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_update(self):
        response = self.client.get(
            reverse("taxi:manufacturer-update",
                    kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_delete(self):
        response = self.client.post(
            reverse("taxi:manufacturer-delete",
                    kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 302)


class PrivateDriverLoginTest(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="Admin", password="hard"
        )
        self.client.force_login(self.admin_user)

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(
            username="Admin1", password="hard1", license_number="1111"
        )

    def test_driver_list(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)

    def test_driver_detail(self):
        response = (self.client.get
                    (reverse("taxi:driver-detail",
                             kwargs={"pk": 1})))
        self.assertEqual(response.status_code, 200)

    def test_driver_create(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(response.status_code, 200)

    def test_driver_update(self):
        response = (self.client.get
                    (reverse("taxi:driver-update",
                             kwargs={"pk": 1})))
        self.assertEqual(response.status_code, 200)

    def test_driver_delete(self):
        response = self.client.post(
            reverse("taxi:driver-delete",
                    kwargs={"pk": self.user.pk})
        )
        self.assertEqual(response.status_code, 302)
