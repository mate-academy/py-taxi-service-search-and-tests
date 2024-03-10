from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class TestLoginRequired(TestCase):
    def setUp(self):
        self.client = Client()
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="secret",
            license_number="UUU11111",
        )

    def test_login_required_for_manufacturer(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/manufacturers/")
        self.client.force_login(self.driver)
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_login_required_for_car(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/cars/")

    def test_login_required_for_driver(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/drivers/")


class AssertionForDrivers(TestCase):
    def setUp(self) -> None:
        num_drivers = 4
        num_manufacturers = 2
        for driver_id in range(num_drivers):
            get_user_model().objects.create_user(
                username=f"test user {driver_id}",
                password=f"test1111{driver_id}",
                license_number=f"UUU1111{driver_id}"
            )

        for manufacturer_id in range(num_manufacturers):
            Manufacturer.objects.create(
                name=f"test manufacturer {manufacturer_id}",
                country=f"test country {manufacturer_id}"
            )

        test_car1 = Car.objects.create(
            model="test car 1",
            manufacturer_id=1,
        )
        test_car2 = Car.objects.create(
            model="test car 2",
            manufacturer_id=2,
        )

        test_car1.drivers.set(get_user_model().objects.all()[:2])
        test_car1.drivers.set(get_user_model().objects.all()[2:])

        test_car1.save()
        test_car2.save()

        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_pass",
            license_number="UUU22222"
        )

        self.client.force_login(self.user)

    def test_toggle_assign_to_car_add_driver(self) -> None:
        driver = self.user
        car = Car.objects.get(pk=1)

        self.client.get(reverse("taxi:toggle-car-assign", args=[car.id]))
        response = self.client.get(reverse("taxi:car-detail", args=[car.id]))

        self.assertIn(driver, response.context["car"].drivers.all())

    def test_toggle_assign_to_car_remove_driver(self) -> None:
        driver = self.user
        car = Car.objects.get(pk=1)
        car.drivers.add(driver)

        self.client.get(reverse("taxi:toggle-car-assign", args=[car.id]))
        response = self.client.get(reverse("taxi:car-detail", args=[car.id]))

        self.assertNotIn(driver, response.context["car"].drivers.all())


class NumbersOfCreationsInIndex(TestCase):

    def test_number_of_drivers(self):
        Driver.objects.create(
            username="Tom",
            license_number="UUU11111"
        )
        Driver.objects.create(
            username="Jerry",
            license_number="UUU22222"
        )
        self.assertEqual(Driver.objects.count(), 2)

    def test_number_of_cars_and_manufactures(self):
        Manufacturer.objects.create(
            name="test manufacturer 1",
            country="test country 1"
        )
        Manufacturer.objects.create(
            name="test manufacturer 2",
            country="test country 2"
        )

        Car.objects.create(
            model="test car 1",
            manufacturer_id=1,
        )
        Car.objects.create(
            model="test car 2",
            manufacturer_id=2,
        )
        self.assertEqual(Car.objects.count(), 2)
