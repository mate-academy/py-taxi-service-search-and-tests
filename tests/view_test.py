from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


DRIVER_LIST_URL = reverse("taxi:driver-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")


class PublicAccessTests(TestCase):
    def test_diver_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_car_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateAccessTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )

        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="test1")
        Manufacturer.objects.create(name="test2")
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(name="manufacturer test")
        Car.objects.create(model="test1", manufacturer=manufacturer)
        Car.objects.create(model="test2", manufacturer=manufacturer)
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_drivers(self):
        get_user_model().objects.create_user(
            username="driver1",
            password="testdriver",
            license_number="AAA12345"
        )
        get_user_model().objects.create_user(
            username="driver2",
            password="testdriver",
            license_number="BBB12345"
        )

        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        users = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(users)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class CreateTest(TestCase):
    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "AAA12345",
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class ToggleAssignToCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )

        self.client.force_login(self.user)

        self.car = Car.objects.create(model="test car",
                                      manufacturer=Manufacturer.objects.create(
                                          name="test manufacturer"))
        self.url = reverse("taxi:car-detail", args=[self.car.id])

    def test_assign_car_to_driver(self):
        response = self.client.post(reverse("taxi:toggle-car-assign",
                                            args=[self.car.pk]))
        self.assertIn(self.car, self.user.cars.all())
        self.assertRedirects(response, self.url)

    def test_remove_car_from_driver(self):
        self.user.cars.add(self.car)
        response = self.client.post(reverse("taxi:toggle-car-assign",
                                            args=[self.car.pk]))
        self.assertNotIn(self.car, self.user.cars.all())
        self.assertRedirects(response, self.url)
