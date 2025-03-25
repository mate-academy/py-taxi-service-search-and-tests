from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    ManufacturerSearchForm,
    DriverSearchForm,
    CarSearchForm
)
from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicTest(TestCase):
    def assert_login_required(self, url):
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_login_required(self):
        self.assert_login_required(MANUFACTURER_URL)

    def test_car_login_required(self):
        self.assert_login_required(CAR_URL)
        manufacturer = Manufacturer.objects.create(
            name="test1",
            country="test1",
        )
        driver = get_user_model().objects.create_user(
            username="Test",
            password="test123",
        )
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)
        self.assert_login_required(reverse("taxi:car-detail", args=[car.id]))

    def test_driver_login_required(self):
        self.assert_login_required(DRIVER_URL)
        driver = get_user_model().objects.create_user(
            username="Test",
            password="test123",
        )
        self.assert_login_required(
            reverse(
                "taxi:driver-detail",
                args=[driver.id]
            )
        )


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test123",
        )
        self.client.force_login(self.user)

    @classmethod
    def setUpTestData(cls):
        for manufacturer_id in range(15):
            Manufacturer.objects.create(
                name=f"Manufacturer {manufacturer_id}",
                country=f"country {manufacturer_id}",
            )

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        paginator = response.context.get("paginator", None)
        if paginator:
            self.assertEqual(
                list(response.context["manufacturer_list"]),
                list(manufacturers[:paginator.per_page]),
            )
        else:
            self.assertEqual(
                list(response.context["manufacturer_list"]),
                list(manufacturers),
            )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_pagination_is_five(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_manufacturer_search_form_in_context(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"],
            ManufacturerSearchForm
        )


class ManufacturerCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_manufacturer_create(self):
        data = {
            "name": "Test",
            "country": "test",
        }
        response = self.client.post(reverse("taxi:manufacturer-create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Manufacturer.objects.filter(name="Test").exists()
        )


class ManufacturerUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Old Manufacturer",
            country="Old Country",
        )

    def test_manufacturer_update(self):
        data = {
            "name": "Updated Manufacturer",
            "country": "Updated Country"
        }
        response = self.client.post(
            reverse(
                "taxi:manufacturer-update", args=[self.manufacturer.id]),
            data
        )
        self.manufacturer.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.manufacturer.name, "Updated Manufacturer")


class ManufacturerDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Old Manufacturer",
            country="Old Country",
        )

    def test_manufacturer_delete(self):
        response = self.client.post(
            reverse("taxi:manufacturer-delete", args=[self.manufacturer.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(name="Old Manufacturer").exists()
        )


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test123",
        )
        self.client.force_login(self.user)

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="test1",
            country="test1",
        )
        driver = get_user_model().objects.create_user(
            username="test_list",
            password="test123",
            license_number="ABC12345"
        )
        for car_id in range(15):
            car = Car.objects.create(
                model=f"Car {car_id}",
                manufacturer=manufacturer
            )
            car.drivers.add(driver)

    def test_retrieve_cars(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        paginator = response.context.get("paginator", None)
        if paginator:
            self.assertEqual(
                list(response.context["car_list"]),
                list(cars[:paginator.per_page]),
            )
        else:
            self.assertEqual(
                list(response.context["car_list"]),
                list(cars),
            )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_pagination_is_five(self):
        response = self.client.get(CAR_URL)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_car_search_form_in_context(self):
        response = self.client.get(CAR_URL)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(response.context["search_form"], CarSearchForm)


class CarCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_car_create(self):
        manufacturer = Manufacturer.objects.create(
            name="test1",
            country="test1",
        )
        driver = get_user_model().objects.create(
            username="test_create",
            password="test123",
            license_number="ABC12345"
        )
        data = {
            "model": "Test",
            "manufacturer": manufacturer.id,
            "drivers": [driver.id]
        }
        response = self.client.post(reverse("taxi:car-create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Car.objects.filter(model="Test").exists()
        )


class CarUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="test1",
            country="test1",
        )
        self.driver = get_user_model().objects.create(
            username="test_update",
            password="test123",
            license_number="ABC12345",
        )
        self.car = Car.objects.create(
            model="Test",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_car_update(self):
        data = {
            "model": "Updated Car",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id]
        }
        response = self.client.post(
            reverse(
                "taxi:car-update", args=[self.car.id]),
            data
        )
        self.car.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.car.model, "Updated Car")


class CarDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test123",
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(
            name="test1",
            country="test1",
        )
        self.car = Car.objects.create(
            model="Test",
            manufacturer=manufacturer,
        )

    def test_car_delete(self):
        response = self.client.post(
            reverse("taxi:car-delete", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Car.objects.filter(model="Test").exists()
        )


class DriverListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test123",
        )
        self.client.force_login(self.user)

    @classmethod
    def setUpTestData(cls):
        for driver_id in range(10):
            get_user_model().objects.create(
                username=f"Driver {driver_id}",
                password=f"test123{driver_id}",
                license_number=f"ABC1234{driver_id}"
            )

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        paginator = response.context.get("paginator", None)
        if paginator:
            self.assertEqual(
                list(response.context["driver_list"]),
                list(drivers[:paginator.per_page]),
            )
        else:
            self.assertEqual(
                list(response.context["driver_list"]),
                list(drivers),
            )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_pagination_is_five(self):
        response = self.client.get(DRIVER_URL)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_driver_search_form_in_context(self):
        response = self.client.get(DRIVER_URL)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"],
            DriverSearchForm
        )


class DriverCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_driver_create(self):
        data = {
            "username": "test",
            "password1": "test1234!@#",
            "password2": "test1234!@#",
            "first_name": "first",
            "last_name": "last",
            "license_number": "ABC12345",
        }
        response = self.client.post(reverse("taxi:driver-create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            get_user_model().objects.filter(username="test").exists()
        )


class DriverLicenseUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.driver = get_user_model().objects.create(
            username="test",
            password="test123",
            license_number="ABC12345",
        )

    def test_driver_license_update(self):
        data = {
            "license_number": "CBA54321",
        }
        response = self.client.post(
            reverse(
                "taxi:driver-update", args=[self.driver.id]),
            data
        )
        self.driver.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.driver.license_number, "CBA54321")


class DriverDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.driver = get_user_model().objects.create(
            username="test",
            password="test123",
            license_number="ABC12345",
        )

    def test_driver_delete(self):
        response = self.client.post(
            reverse("taxi:driver-delete", args=[self.driver.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            get_user_model().objects.filter(username="test").exists()
        )
