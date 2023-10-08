from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


def login_for_tests(self) -> None:
    self.user_for_login = get_user_model().objects.create_user(
        username="user_for_login",
        password="user_for_login",
        license_number="AAA11111",
    )
    self.client.force_login(self.user_for_login)


class DriverViewTests(TestCase):
    def setUp(self) -> None:
        login_for_tests(self)

        self.user1 = get_user_model().objects.create_user(
            username="Anton11", password="password", license_number="ABC12345"
        )
        self.user2 = get_user_model().objects.create_user(
            username="Andriy22", password="password", license_number="ABC54321"
        )

    def test_retrieve_drivers(self):
        response = self.client.get(reverse("taxi:driver-list"))
        drivers = get_user_model().objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_driver_detail_info(self):
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": self.user1.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["driver"], self.user1)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_retrieve_driver_using_search(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "andr"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Andriy22")
        self.assertNotContains(response, "Anton11")


class ManufacturerViewTests(TestCase):
    def setUp(self) -> None:
        login_for_tests(self)

        self.manufacturer1 = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )
        self.manufacturer1 = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )

    def test_retrieve_manufacturers(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_manufacturer_using_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "bm"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Audi")


class CarViewTest(TestCase):
    def setUp(self) -> None:
        login_for_tests(self)

        self.manufacturer1 = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )

        self.car1 = Car.objects.create(
            model="X5", manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="A6", manufacturer=self.manufacturer2
        )

    def test_retrieve_cars(self):
        response = self.client.get(reverse("taxi:car-list"))
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_car_detail_info(self):
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": self.car1.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["car"], self.car1)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_retrieve_car_using_search(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "x"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "X5")
        self.assertNotContains(response, "A6")

    def test_assing_to_car(self):
        response = self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": self.car1.pk})
        )
        self.assertEqual(response.status_code, 302)
        driver_of_car1 = self.car1.drivers.get(username=self.user_for_login.username)
        self.assertEqual(driver_of_car1, self.user_for_login)

    def test_delete_from_car(self):
        self.car1.drivers.add(self.user_for_login)
        response = self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": self.car1.pk})
        )
        self.assertEqual(response.status_code, 302)
        driver_of_car1 = self.car1.drivers.filter(username=self.user_for_login.username).first()
        self.assertIsNone(driver_of_car1)
