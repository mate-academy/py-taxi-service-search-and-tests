from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

CAR_URL = reverse("taxi:car-list")
MANUFACTURE_URL = reverse("taxi:manufacturer-list")
DRIVERS_URL = reverse("taxi:driver-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)

        res = self.client.get(MANUFACTURE_URL)
        self.assertNotEqual(res.status_code, 200)

        res = self.client.get(DRIVERS_URL)
        self.assertNotEqual(res.status_code, 200)





class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="<PASSWORD>",
        )
        self.client.login(username="testuser", password="<PASSWORD>")

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Audi")

        resource = self.client.get(MANUFACTURE_URL)
        self.assertEqual(resource.status_code, 200)

        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(resource.context["manufacturer_list"]),
            list(manufacturer),
        )
        self.assertTemplateUsed(resource, "taxi/manufacturer_list.html")


    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(name="BMW")
        Car.objects.create(model="x5", manufacturer=manufacturer)
        Car.objects.create(model="A3", manufacturer=manufacturer)

        resource = self.client.get(CAR_URL)
        self.assertEqual(resource.status_code, 200)
        car = Car.objects.all()
        self.assertEqual(
            list(resource.context["object_list"]),
            list(car),
        )
        self.assertTemplateUsed(resource, "taxi/car_list.html")

    def test_retrieve_driver(self):
        Driver.objects.create(username="name1", license_number="QQQ11111")
        Driver.objects.create(username="name2", license_number="WWW22222")

        resource = self.client.get(DRIVERS_URL)
        self.assertEqual(resource.status_code, 200)

        drivers = Driver.objects.all()
        self.assertEqual(
            list(resource.context["object_list"]),
            list(drivers),
        )
        self.assertTemplateUsed(resource, "taxi/driver_list.html")


    def test_regular_user_cannot_access_admin(self):
        res = self.client.get("/admin/")
        self.assertNotEqual(res.status_code, 200)
