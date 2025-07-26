from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class PublicManufacturerFormatTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="test")
        self.urls = [
            reverse("taxi:manufacturer-list"),
            reverse("taxi:manufacturer-create"),
            reverse("taxi:manufacturer-update", args=[self.manufacturer.id]),
            reverse("taxi:manufacturer-delete", args=[self.manufacturer.id]),
        ]

    def test_login_required(self):
        for i in self.urls:
            res = self.client.get(i)
            self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerFormatTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12311",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="test", country="US")
        Manufacturer.objects.create(name="test2", country="Ukraine")
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(res.status_code, 200)
        manufacturer_list = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturer_list),
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")


class PublicDriverFormatTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create(
            username="test",
            license_number="test1233",
        )
        self.urls = [
            reverse("taxi:driver-list"),
            reverse("taxi:driver-detail", args=[self.driver.id]),
            reverse("taxi:driver-create"),
            reverse("taxi:driver-update", args=[self.driver.id]),
            reverse("taxi:driver-delete", args=[self.driver.id]),
        ]

    def test_login_required(self):
        for i in self.urls:
            res = self.client.get(i)
            self.assertNotEqual(res.status_code, 200)


class PrivateDriverFormatTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="test",
            password="test123123",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver_list(self):
        Driver.objects.create_user(
            username="test33",
            password="<PASSWORD>",
            license_number="ABC13144")
        Driver.objects.create_user(
            username="test2",
            password="<PASSWORD>",
            license_number="ABC13213")
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(res.status_code, 200)
        driver_list = Driver.objects.all()
        self.assertEqual(
            list(res.context["driver_list"]),
            list(driver_list),
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")


class PublicCarFormatTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test",
            country="test",
        )
        self.car = Car.objects.create(
            model="test",
            manufacturer=self.manufacturer
        )
        self.urls = [
            reverse("taxi:car-list"),
            reverse("taxi:car-detail", args=[self.car.id]),
            reverse("taxi:car-create"),
            reverse("taxi:car-update", args=[self.car.id]),
            reverse("taxi:car-delete", args=[self.car.id]),
            reverse("taxi:toggle-car-assign", args=[self.car.id])
        ]

    def test_login_required(self):
        for i in self.urls:
            res = self.client.get(i)
            self.assertNotEqual(res.status_code, 200)


class PrivateCarFormatTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="test",
            password="admin1233",
        )
        self.client.force_login(self.user)

    def test_retrieve_car_list(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test",
        )
        Car.objects.create(model="BMW", manufacturer=manufacturer)
        Car.objects.create(model="Audi", manufacturer=manufacturer)
        res = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(res.status_code, 200)
        car_list = Car.objects.all()
        self.assertEqual(
            list(res.context["car_list"]),
            list(car_list),
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")
