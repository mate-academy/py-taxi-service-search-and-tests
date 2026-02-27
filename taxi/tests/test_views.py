from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

TAXI_INDEX_URL = reverse("taxi:index")
TAXI_MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
TAXI_MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
TAXI_CAR_LIST_URL = reverse("taxi:car-list")
TAXI_CAR_CREATE_URL = reverse("taxi:car-create")
TAXI_DRIVER_LIST_URL = reverse("taxi:driver-list")


class MainPageTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            first_name="John",
            last_name="Wick",
            email="john_wick@.lol"
        )

        self.client.force_login(self.driver)

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.car = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_index_page_status_code(self):
        response = self.client.get(TAXI_INDEX_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_index_login_required(self):
        self.client.logout()
        response = self.client.get(TAXI_INDEX_URL)

        self.assertRedirects(response, f"/accounts/login/?next={TAXI_INDEX_URL}")

    def test_index_context_data(self):
        response = self.client.get(TAXI_INDEX_URL)
        num_cars = response.context["num_cars"]
        num_drivers = response.context["num_drivers"]
        num_manufacturers = response.context["num_manufacturers"]

        self.assertEqual(num_cars, 1)
        self.assertEqual(num_drivers, 1)
        self.assertEqual(num_manufacturers, 1)


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            first_name="John",
            last_name="Wick",
            email="john_wick@.lol"
        )

        self.client.force_login(self.driver)

        Manufacturer.objects.bulk_create([
            Manufacturer(name=f"BMW {i}", country="Germany")
            for i in range(6)
        ])

    def test_manufacturer_status_code(self):
        response = self.client.get(TAXI_MANUFACTURER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_login_required(self):
        self.client.logout()
        response = self.client.get(TAXI_MANUFACTURER_LIST_URL)
        self.assertRedirects(response, f"/accounts/login/?next={TAXI_MANUFACTURER_LIST_URL}")

    def test_manufacturer_search(self):
        response = self.client.get(TAXI_MANUFACTURER_LIST_URL, {"name": "BMW 0"})

        self.assertEqual(len(response.context["manufacturer_list"]), 1)

    def test_manufacturer_pagination_search(self):
        response = self.client.get(TAXI_MANUFACTURER_LIST_URL, {"name": "BMW", "page": 2})

        self.assertEqual(len(response.context["manufacturer_list"]), 1)


class ManufacturerCRUDTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            first_name="John",
            last_name="Wick",
            email="john_wick@.lol"
        )

        self.client.force_login(self.driver)

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

    def test_create_manufacturer_status_code(self):
        response = self.client.get(TAXI_MANUFACTURER_CREATE_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_update_manufacturer_status_code(self):
        url = reverse("taxi:manufacturer-update", kwargs={"pk": self.manufacturer.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_delete_manufacturer_status_code(self):
        url = reverse("taxi:manufacturer-delete", kwargs={"pk": self.manufacturer.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_confirm_delete.html")

    def test_create_manufacturer_success(self):
        response = self.client.post(TAXI_MANUFACTURER_CREATE_URL, {"name": "Audi", "country": "Germany"})

        self.assertEqual(Manufacturer.objects.count(), 2)
        self.assertRedirects(response, TAXI_MANUFACTURER_LIST_URL)

    def test_update_manufacturer_success(self):
        url = reverse("taxi:manufacturer-update", kwargs={"pk": self.manufacturer.pk})
        response = self.client.post(url, {"name": "Audi", "country": "China"})
        self.manufacturer.refresh_from_db()

        self.assertEqual(self.manufacturer.name, "Audi")
        self.assertEqual(self.manufacturer.country, "China")
        self.assertRedirects(response, TAXI_MANUFACTURER_LIST_URL)

    def test_delete_manufacturer_success(self):
        url = reverse("taxi:manufacturer-delete", kwargs={"pk": self.manufacturer.pk})
        response = self.client.post(url)

        self.assertFalse(Manufacturer.objects.filter(pk=self.manufacturer.pk).exists())
        self.assertRedirects(response, TAXI_MANUFACTURER_LIST_URL)


class CarListViewTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            first_name="John",
            last_name="Wick",
            email="john_wick@.lol"
        )
        self.client.force_login(self.driver)
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        cars = Car.objects.bulk_create([
            Car(model=f"X{i}", manufacturer=self.manufacturer)
            for i in range(6)
        ])

        for car in cars:
            car.drivers.add(self.driver)

    def test_car_list_code_status(self):
        response = self.client.get(TAXI_CAR_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_login_user_required(self):
        self.client.logout()
        response = self.client.get(TAXI_CAR_LIST_URL)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={TAXI_CAR_LIST_URL}")

    def test_car_list_get_context(self):
        response = self.client.get(TAXI_CAR_LIST_URL, {"model": "X5"})

        self.assertEqual(len(list(response.context["car_list"])), 1)

    def test_car_list_paginator(self):
        response = self.client.get(TAXI_CAR_LIST_URL, {"model": "X", "page": 2})

        self.assertEqual(len(list(response.context["car_list"])), 1)


class CarCRUDTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            first_name="John",
            last_name="Wick",
            email="john_wick@.lol"
        )

        self.client.force_login(self.driver)

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.car = Car.objects.create(
            model="Suzuki Vitara",
            manufacturer=self.manufacturer
        )

        self.car.drivers.add(self.driver)

    def test_car_create_status_code(self):
        response = self.client.get(TAXI_CAR_CREATE_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_car_update_status_code(self):
        url = reverse("taxi:car-update", kwargs={"pk": self.car.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_car_delete_status_code(self):
        url = reverse("taxi:car-delete", kwargs={"pk": self.car.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_confirm_delete.html")

    def test_car_create_success(self):
        response = self.client.post(
            TAXI_CAR_CREATE_URL,
            {"model": "kitahara", "manufacturer": self.manufacturer.pk, "drivers": [self.driver.pk]})

        self.assertEqual(Car.objects.count(), 2)
        self.assertRedirects(response, TAXI_CAR_LIST_URL)

    def test_car_update_success(self):
        url = reverse("taxi:car-update", kwargs={"pk": self.car.pk})
        response = self.client.post(
            url,
            {"model": "origiri", "manufacturer": self.manufacturer.pk, "drivers": [self.driver.pk]})
        self.car.refresh_from_db()

        self.assertEqual(self.car.model, "origiri")
        self.assertRedirects(response, TAXI_CAR_LIST_URL)

    def test_car_delete_success(self):
        url = reverse("taxi:car-delete", kwargs={"pk": self.car.pk})
        response = self.client.post(url)

        self.assertEqual(Car.objects.count(), 0)
        self.assertRedirects(response, TAXI_CAR_LIST_URL)


class ToggleAssignToCarTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            first_name="John",
            last_name="Wick",
            email="john_wick@.lol"
        )

        self.client.force_login(self.driver)

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.car = Car.objects.create(
            model="Suzuki Vitara",
            manufacturer=self.manufacturer
        )

        self.car.drivers.add(self.driver)

    def test_toggle_assign_status_code(self):
        url = reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/cars/{self.car.pk}/")

    def test_toggle_assign_login_required(self):
        self.client.logout()
        url = reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next=/cars/{self.car.pk}/toggle-assign/")

    def test_toggle_remove_car(self):
        url = reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})
        response = self.client.post(url)

        self.assertFalse(self.driver.cars.filter(pk=self.car.pk).exists())
        self.assertRedirects(response, f"/cars/{self.car.pk}/")

    def test_toggle_add_car(self):
        url = reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})
        self.driver.cars.remove(self.car)
        response = self.client.post(url)

        self.assertTrue(self.driver.cars.filter(pk=self.car.pk).exists())
        self.assertRedirects(response, f"/cars/{self.car.pk}/")


class DriverListViewTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="testwow",
            password="test1234",
            first_name="John",
            last_name="Wick",
            email="john_wick@.lol"
        )

        self.client.force_login(self.driver)

        Driver.objects.bulk_create([
            Driver(
                username=f"test{i}",
                password=f"test123{i}",
                first_name="John",
                last_name="Wick",
                email="john_wick@.lol",
                license_number=f"ABC1234{i}"
            )
            for i in range(6)
        ])

    def test_driver_status_code(self):
        response = self.client.get(TAXI_DRIVER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_login_required(self):
        self.client.logout()
        response = self.client.get(TAXI_DRIVER_LIST_URL)
        self.assertRedirects(response, f"/accounts/login/?next={TAXI_DRIVER_LIST_URL}")

    def test_driver_search(self):
        response = self.client.get(TAXI_DRIVER_LIST_URL, {"username": "test0"})

        self.assertEqual(len(list(response.context["driver_list"])), 1)

    def test_driver_pagination_search(self):
        response = self.client.get(TAXI_DRIVER_LIST_URL, {"username": "test", "page": 2})

        self.assertEqual(len(list(response.context["driver_list"])), 2)
