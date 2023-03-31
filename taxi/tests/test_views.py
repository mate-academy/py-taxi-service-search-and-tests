from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")


class PublicManufacturerListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerListTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="TestUser",
            password="Password",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="Test", country="Test1")

        response = self.client.get(MANUFACTURER_LIST_URL)
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


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="TestUser",
            password="Password",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "Username",
            "password1": "Pass123-wrd",
            "password2": "Pass123-wrd",
            "first_name": "First Name",
            "last_name": "Last Name",
            "license_number": "ABC12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        created_user = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(created_user.first_name, form_data["first_name"])
        self.assertEqual(created_user.last_name, form_data["last_name"])
        self.assertEqual(
            created_user.license_number,
            form_data["license_number"]
        )


class PrivateDriverListTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="TestUser",
            password="Password",
        )
        self.client.force_login(self.user)

        Driver.objects.create(
            username="Test1",
            first_name="Test1",
            last_name="Driver",
            license_number="GHT45678"
        )

        Driver.objects.create(
            username="Test2",
            first_name="Test2",
            last_name="Driver",
            license_number="GHT45658"
        )

        Driver.objects.create(
            username="Test3",
            first_name="Test3",
            last_name="Driver",
            license_number="GHT46678"
        )

        Driver.objects.create(
            username="Test45",
            first_name="Test4",
            last_name="Driver",
            license_number="GHT45578"
        )

        Driver.objects.create(
            username="Test5",
            first_name="Test5",
            last_name="Driver",
            license_number="GHT45698"
        )

    def test_driver_list_pagination_is_five(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_lists_all_drivers(self):
        response = self.client.get(DRIVER_LIST_URL + "?page=2")
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["driver_list"]), 1)

    def test_drivers_filter_by_username_is_valid(self):
        driver7 = Driver.objects.create(
            username="Test7",
            first_name="Test7",
            last_name="Driver",
            license_number="GHT45690"
        )
        driver8 = Driver.objects.create(
            username="Test77",
            first_name="Test77",
            last_name="Driver",
            license_number="GHT40690"
        )

        response = self.client.get(DRIVER_LIST_URL + "?username=7")
        self.assertEqual(
            list(response.context["driver_list"]),
            [driver7, driver8]
        )


class PrivateCarListTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="TestUser",
            password="Password",
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TestCountry"
        )

        Car.objects.create(
            model="Model1",
            manufacturer=manufacturer,
        ).drivers.add(self.user)

        Car.objects.create(
            model="Model2",
            manufacturer=manufacturer,
        ).drivers.add(self.user)

        Car.objects.create(
            model="Model3",
            manufacturer=manufacturer,
        ).drivers.add(self.user)

        Car.objects.create(
            model="Model4",
            manufacturer=manufacturer,
        ).drivers.add(self.user)

        Car.objects.create(
            model="Model5",
            manufacturer=manufacturer,
        ).drivers.add(self.user)

        Car.objects.create(
            model="Model6",
            manufacturer=manufacturer,
        ).drivers.add(self.user)

    def test_car_list_pagination_is_five(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_lists_all_cars(self):
        response = self.client.get(CAR_LIST_URL + "?page=2")
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["car_list"]), 1)

    def test_cars_filter_by_model_is_valid(self):
        manufacturer = Manufacturer.objects.create(
            name="ModelManufacturer",
            country="TestCountry"
        )
        car7 = Car.objects.create(
            model="ModelOne",
            manufacturer=manufacturer,
        )
        car7.drivers.add(self.user)

        car8 = Car.objects.create(
            model="ModelOneTwo",
            manufacturer=manufacturer,
        )
        car8.drivers.add(self.user)

        response = self.client.get(CAR_LIST_URL + "?model=one")
        self.assertEqual(list(response.context["car_list"]), [car7, car8])
