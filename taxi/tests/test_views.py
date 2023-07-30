from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
DRIVERS_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="pwd1234pwd",
            license_number="TST98765"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="BYD", country="China")

        response = self.client.get(MANUFACTURERS_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )

    def test_retrieve_manufacturers_search(self):
        search_param = "?name=o"
        manufacturers_list = [
            ("BMW", "Germany"),
            ("Chevrolet", "USA"),
            ("Ford Motors", "USA"),
            ("Cherry", "China"),
            ("KIA", "Korea"),
            ("Volkswagen", "Germany")
        ]
        for item in manufacturers_list:
            Manufacturer.objects.create(name=item[0], country=item[1])

        response = self.client.get(MANUFACTURERS_URL + search_param)
        manufacturers = Manufacturer.objects.filter(name__icontains="o")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="pwd1234pwd",
            license_number="TST98765"
        )
        self.client.force_login(self.user)

        for i in range(10):
            get_user_model().objects.create(
                username=f"username{i}",
                password=f"pwd1234{i}!",
                license_number=f"TST1234{i}"
            )

    def test_retrieve_drivers_paginated(self):
        paginated_by = 5
        response = self.client.get(DRIVERS_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)[:paginated_by]
        )
        self.assertTemplateUsed(
            response,
            "taxi/driver_list.html"
        )

    def test_retrieve_manufacturers_search(self):
        search_param = "?username=5"

        response = self.client.get(DRIVERS_URL + search_param)
        drivers = Driver.objects.filter(username__icontains="5")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_create_driver(self):
        form_data = {
            "username": "driver",
            "password1": "pwd12345pwd",
            "password2": "pwd12345pwd",
            "first_name": "Tester",
            "last_name": "Testenko",
            "license_number": "TST56789"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class PrivateCarTests(TestCase):
    def setUp(self):
        for i in range(10):
            manufacturer = Manufacturer.objects.create(
                name=f"manufacturer{i}",
                country=f"country{i}"
            )
            Car.objects.create(
                model=f"model{i}",
                manufacturer=manufacturer
            )

        self.user = get_user_model().objects.create_user(
            username="Test",
            password="pwd1234pwd",
            license_number="TST98765"
        )
        self.client.force_login(self.user)

    def test_retrieve_car_paginated(self):
        paginated_by = 5
        response = self.client.get(CARS_URL)
        cars = Car.objects.select_related("manufacturer")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)[:paginated_by]
        )

    def test_retrieve_car_search(self):
        search_param = "?model=5"
        response = self.client.get(CARS_URL + search_param)
        cars = Car.objects.filter(model__icontains="5")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_toggle_assign_to_car(self):
        car = Car.objects.get(id=3)
        driver = get_user_model().objects.get(id=1)
        self.client.get(reverse("taxi:toggle-car-assign", kwargs={"pk": 3}))
        self.assertEqual(driver.cars.first(), car)
        self.client.get(reverse("taxi:toggle-car-assign", kwargs={"pk": 3}))
        self.assertEqual(driver.cars.count(), 0)
