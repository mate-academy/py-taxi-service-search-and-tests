from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class PublicManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="1", country="USA"
        )

    def test_login_required(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_create(self):
        resp = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertNotEqual(resp.status_code, 200)

    def test_login_required_update_delete(self):
        urls = ["taxi:manufacturer-update", "taxi:manufacturer-delete"]
        for url in urls:
            resp = self.client.get(reverse(url, args=[self.manufacturer.id]))
            self.assertNotEqual(resp.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password1234"
        )
        self.client.force_login(self.user)
        self.manufacturer1 = Manufacturer.objects.create(
            name="Tesla", country="USA"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford", country="USA"
        )

    def test_retrieve_manufacturer_list(self):

        manufacturers = Manufacturer.objects.all()

        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_manufacturer_create(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_retrieve_manufacturer_update(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-update", args=[self.manufacturer1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "taxi/manufacturer_form.html"
        )

    def test_retrieve_manufacturer_delete(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-delete", args=[self.manufacturer1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "taxi/manufacturer_confirm_delete.html"
        )


class PublicCarTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="1", country="USA"
        )
        self.car = Car.objects.create(
            model="S", manufacturer=self.manufacturer
        )

    def test_login_required_list(self):
        resp = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(resp.status_code, 200)

    def test_login_required_create(self):
        resp = self.client.get(reverse("taxi:car-create"))
        self.assertNotEqual(resp.status_code, 200)

    def test_login_required_detail_update_delete(self):
        urls = ["taxi:car-detail",
                "taxi:car-update",
                "taxi:car-delete"]
        for url in urls:
            resp = self.client.get(reverse(url, args=[self.car.id]))
            self.assertNotEqual(resp.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password1234"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="1", country="USA"
        )
        self.car = Car.objects.create(
            model="S", manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="S1", manufacturer=self.manufacturer
        )

    def test_retrieve_car_list(self):
        cars = Car.objects.all()
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_car_create(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_retrieve_car_detail(self):
        response = self.client.get(reverse(
            "taxi:car-detail", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_retrieve_car_update(self):
        response = self.client.get(reverse(
            "taxi:car-update", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_retrieve_car_delete(self):
        response = self.client.get(reverse(
            "taxi:car-delete", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_confirm_delete.html")


class PublicDriverTest(TestCase):
    def setUp(self) -> None:
        self.driver = Driver.objects.create(
            username="test", password="password123"
        )

    def test_login_required_list(self):
        resp = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(resp.status_code, 200)

    def test_login_required_create(self):
        resp = self.client.get(reverse("taxi:driver-create"))
        self.assertNotEqual(resp.status_code, 200)

    def test_login_required_detail_update_delete(self):
        urls = ["taxi:driver-detail",
                "taxi:driver-update",
                "taxi:driver-delete"]
        for url in urls:
            resp = self.client.get(reverse(url, args=[self.driver.id]))
            self.assertNotEqual(resp.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password1234"
        )
        self.client.force_login(self.user)
        self.driver = Driver.objects.create_user(
            username="test1",
            password="password1234",
            license_number="ASD22345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="1", country="USA"
        )
        self.car = Car.objects.create(
            model="S", manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="S1", manufacturer=self.manufacturer
        )

    def test_retrieve_driver_list(self):
        drivers = Driver.objects.all()
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_driver_create(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_retrieve_driver_detail(self):
        response = self.client.get(reverse(
            "taxi:driver-detail", args=[self.driver.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_retrieve_driver_update(self):
        response = self.client.get(reverse(
            "taxi:driver-update", args=[self.driver.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_retrieve_car_delete(self):
        response = self.client.get(reverse(
            "taxi:driver-delete", args=[self.driver.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                "taxi/driver_confirm_delete.html")
