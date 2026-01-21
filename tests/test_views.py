from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

CAR_URL = reverse("taxi:car-list")
MANUFACTURE_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)

        res = self.client.get(MANUFACTURE_URL)
        self.assertNotEqual(res.status_code, 200)

        res = self.client.get(DRIVER_URL)
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

        resource = self.client.get(DRIVER_URL)
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



    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="Tesla", country="USA")

        response = self.client.get(MANUFACTURE_URL + "?name=Tes")
        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.filter(name__icontains="Tes")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(name="BMW", country="Germany")
        Car.objects.create(model="X5", manufacturer=manufacturer)
        Car.objects.create(model="A3", manufacturer=manufacturer)
        Car.objects.create(model="Model S", manufacturer=manufacturer)

        response = self.client.get(CAR_URL + "?model=Model")
        self.assertEqual(response.status_code, 200)

        cars = Car.objects.filter(model__icontains="Model")
        self.assertEqual(
            list(response.context["object_list"]),
            list(cars),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


    def test_search_driver_by_username(self):
        Driver.objects.create_user(username="john_doe", password="pass123", license_number="JDE12345")
        Driver.objects.create_user(username="jane_smith", password="pass123", license_number="TDE12345")
        Driver.objects.create_user(username="model_driver", password="pass123", license_number="GDE12345")

        response = self.client.get(DRIVER_URL + "?username=model")
        self.assertEqual(response.status_code, 200)

        drivers = Driver.objects.filter(username__icontains="model")
        self.assertEqual(
            list(response.context["object_list"]),
            list(drivers),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")