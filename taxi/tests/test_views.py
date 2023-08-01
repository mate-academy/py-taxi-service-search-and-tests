from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy, reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_LIST = reverse_lazy("taxi:manufacturer-list")
CREATE_MANUFACTURER = reverse_lazy("taxi:manufacturer-create")

CAR_LIST = reverse_lazy("taxi:car-list")
CREATE_CAR = reverse_lazy("taxi:car-create")

DRIVER_LIST = reverse_lazy("taxi:driver-list")
CREATE_DRIVER = reverse_lazy("taxi:driver-create")
TOGGLE_CAR_ASSIGN = reverse_lazy("taxi:toggle-car-assign")


class PublicManufacturerTest(TestCase):
    def test_manufacturer_login_required(self):

        response = self.client.get(MANUFACTURER_LIST)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.user = get_user_model().objects.create_user(
            username="test_username", password="test_1234"
        )
        self.client.force_login(self.user)

        self.is_paginated_by = 5

    def test_receive_list_of_manufacturers(self):
        for i in range(10):
            Manufacturer.objects.create(
                name=f"TestName{i}",
                country="TestCountry"
            )

        response = self.client.get(MANUFACTURER_LIST)
        manufacturers = Manufacturer.objects.all()[:self.is_paginated_by]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_receive_manufacturers_by_search_bar(self):
        Manufacturer.objects.create(name="Manufacturer1", country="Test1")
        Manufacturer.objects.create(name="Manufacturer2", country="Test2")
        searched = Manufacturer.objects.create(
            name="SearchedManufacturer",
            country="Test3"
        )

        response = self.client.get(MANUFACTURER_LIST, data={
            "name": "Searched"
        })

        self.assertEqual(response.status_code, 200)
        manufacturer_list = response.context["manufacturer_list"]
        self.assertEqual(len(manufacturer_list), 1)
        self.assertEqual(
            manufacturer_list[0].name,
            searched.name
        )

    def test_create_manufacturer(self):
        form_data = {
            "name": "Power",
            "country": "Ukraine"
        }

        response = self.client.post(CREATE_MANUFACTURER, data=form_data)
        created_manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertRedirects(
            response,
            MANUFACTURER_LIST,
            status_code=302,
            target_status_code=200
        )
        self.assertEqual(created_manufacturer.name, form_data["name"])


class PublicCarTest(TestCase):
    def test_manufacturer_login_required(self):

        response = self.client.get(CAR_LIST)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.user = get_user_model().objects.create_user(
            username="test_username", password="test_1234"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="USA"
        )

        self.is_paginated_by = 5

    def test_receive_list_of_cars(self):
        for i in range(10):
            Car.objects.create(
                model=f"Mercedes{i}",
                manufacturer=self.manufacturer
            )

        response = self.client.get(CAR_LIST)
        cars = Car.objects.all()[:self.is_paginated_by]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_receive_car_by_search_bar(self):
        Car.objects.create(
            model="Mercedes",
            manufacturer=self.manufacturer
        )
        Car.objects.create(
            model="BMW",
            manufacturer=self.manufacturer
        )

        response = self.client.get(CAR_LIST, data={
            "model": "BMW"
        })

        self.assertEqual(response.status_code, 200)
        car_list = response.context["car_list"]
        self.assertEqual(len(car_list), 1)
        self.assertEqual(
            car_list[0].model,
            "BMW"
        )

    def test_create_car(self):
        driver = get_user_model().objects.create_user(
            username="TestUsername",
            password="test_1234",
            license_number="AAA12345"
        )

        form_data = {
            "model": "Ford",
            "manufacturer": self.manufacturer.pk,
            "drivers": driver.pk
        }

        response = self.client.post(CREATE_CAR, data=form_data)

        self.assertRedirects(
            response,
            CAR_LIST,
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(Car.objects.filter(
            model=form_data["model"],
            manufacturer=form_data["manufacturer"]
        ).exists())

    def test_assign_me_to_this_car(self):
        new_car = Car.objects.create(
            model="BMW",
            manufacturer=self.manufacturer,
        )

        url = reverse("taxi:car-detail", args=[new_car.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
        self.assertContains(response, "Assign me to this car")

    def test_delete_me_from_this_car(self):
        driver = get_user_model().objects.create_user(
            username="TestUsername",
            password="Test1235",
            license_number="DDD12345"
        )
        new_car = Car.objects.create(
            model="BMW",
            manufacturer=self.manufacturer,
        )
        driver.cars.add(new_car)

        toggle_url = reverse("taxi:toggle-car-assign", args=[new_car.id])
        self.client.get(toggle_url)

        url = reverse("taxi:car-detail", args=[new_car.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
        driver.refresh_from_db()
        self.assertContains(response, "Delete me from this car")


class PublicDriverTest(TestCase):
    def test_manufacturer_login_required(self):

        response = self.client.get(DRIVER_LIST)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.user = get_user_model().objects.create_user(
            username="test_username", password="test_1234"
        )
        self.client.force_login(self.user)

        for i in range(10):
            get_user_model().objects.create_user(
                username=f"TestUsername{i}",
                password=f"test1234{i}",
                license_number=f"AAA1234{i}"
            )
        self.driver = get_user_model().objects.create_user(
            username="MainDriver",
            password="Driver123",
            license_number="BBB1234"
        )

        self.is_paginated_by = 5

    def test_receive_list_of_drivers(self):
        response = self.client.get(DRIVER_LIST)
        drivers = get_user_model().objects.all()[:self.is_paginated_by]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_receive_driver_by_search_bar(self):

        response = self.client.get(DRIVER_LIST, data={
            "username": f"{self.driver.username}"
        })

        self.assertEqual(response.status_code, 200)
        driver_list = response.context["driver_list"]
        self.assertEqual(len(driver_list), 1)
        self.assertEqual(
            driver_list[0].username,
            self.driver.username
        )

    def test_create_driver(self):
        form_data = {
            "username": "UniqueUsername",
            "password1": "test_1234",
            "password2": "test_1234",
            "license_number": "UNI12345",
            "first_name": "TestName",
            "last_name": "TestLastName",
        }

        response = self.client.post(CREATE_DRIVER, data=form_data)

        self.assertRedirects(
            response,
            reverse(
                "taxi:driver-detail",
                args=[get_user_model().objects.last().id]
            ),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(get_user_model().objects.filter(
            username=form_data["username"]
        ).exists())
