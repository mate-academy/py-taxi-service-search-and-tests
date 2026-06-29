from typing import Any

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class BaseTaxiTestCase(TestCase):
    def create_driver(
            self,
            username: str = "test_driver",
            password: str = "pass12345",
            license_number: str = "ABC12345",
            **extra_fields: Any,
    ) -> Driver:
        return get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
            **extra_fields,
        )

    def create_manufacturer(
            self,
            name: str = "Test Manufacturer",
            country: str = "Test Country",
    ) -> Manufacturer:
        return Manufacturer.objects.create(
            name=name,
            country=country,
        )

    def create_car(
            self,
            model: str = "Test Car",
            manufacturer: Manufacturer | None = None,
    ) -> Car:
        if manufacturer is None:
            manufacturer = self.create_manufacturer()

        return Car.objects.create(
            model=model,
            manufacturer=manufacturer,
        )

    def login_user(self) -> Driver:
        self.user = self.create_driver(
            username="logged_user",
            license_number="LOG12345",
        )
        self.client.force_login(self.user)
        return self.user


class IndexViewTest(BaseTaxiTestCase):
    def test_index_redirects_if_not_logged_in(self) -> None:
        response = self.client.get(reverse("taxi:index"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('taxi:index')}",
        )

    def test_index_url_exists_for_logged_in_user(self) -> None:
        self.login_user()

        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)

    def test_index_context_contains_counts(self) -> None:
        user = self.login_user()

        manufacturer1 = self.create_manufacturer(
            name="Manufacturer 1",
            country="Country 1",
        )
        manufacturer2 = self.create_manufacturer(
            name="Manufacturer 2",
            country="Country 2",
        )

        driver2 = self.create_driver(
            username="driver_2",
            license_number="DRV22222",
        )
        driver3 = self.create_driver(
            username="driver_3",
            license_number="DRV33333",
        )

        car1 = self.create_car(
            model="Car 1",
            manufacturer=manufacturer1,
        )
        car1.drivers.set([user, driver3])

        car2 = self.create_car(
            model="Car 2",
            manufacturer=manufacturer2,
        )
        car2.drivers.set([driver2, driver3])

        self.create_car(
            model="Car 3",
            manufacturer=manufacturer2,
        )

        car4 = self.create_car(
            model="Car 4",
            manufacturer=manufacturer1,
        )
        car4.drivers.set([user, driver2, driver3])

        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_drivers"], 3)
        self.assertEqual(response.context["num_cars"], 4)
        self.assertEqual(response.context["num_manufacturers"], 2)


class ManufacturerListViewTest(BaseTaxiTestCase):
    def test_manufacturer_list_pagination_is_5(self) -> None:
        self.login_user()

        for number in range(6):
            self.create_manufacturer(
                name=f"Manufacturer {number}",
                country=f"Country {number}",
            )

        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(response.context["paginator"].count, 6)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_manufacturer_search_by_name(self) -> None:
        self.login_user()

        toyota = self.create_manufacturer(
            name="Toyota",
            country="Japan",
        )
        bmw = self.create_manufacturer(
            name="BMW",
            country="Germany",
        )
        tesla = self.create_manufacturer(
            name="Tesla",
            country="USA",
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "toy"},
        )

        manufacturers = response.context["manufacturer_list"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(manufacturers), 1)
        self.assertIn(toyota, manufacturers)
        self.assertNotIn(bmw, manufacturers)
        self.assertNotIn(tesla, manufacturers)

    def test_manufacturer_search_empty_query_returns_all(self) -> None:
        self.login_user()

        for name in ["Toyota", "BMW", "Tesla", "Audi"]:
            self.create_manufacturer(
                name=name,
                country="Test Country",
            )

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 4)


class CarListViewTest(BaseTaxiTestCase):
    def test_car_list_pagination_is_5(self) -> None:
        self.login_user()

        manufacturer = self.create_manufacturer()

        for number in range(6):
            self.create_car(
                model=f"Car {number}",
                manufacturer=manufacturer,
            )

        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(response.context["paginator"].count, 6)
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_car_search_by_model(self) -> None:
        self.login_user()

        manufacturer = self.create_manufacturer()

        toyota_camry = self.create_car(
            model="Toyota Camry",
            manufacturer=manufacturer,
        )
        bmw_x5 = self.create_car(
            model="BMW X5",
            manufacturer=manufacturer,
        )
        audi_a6 = self.create_car(
            model="Audi A6",
            manufacturer=manufacturer,
        )

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "camry"},
        )

        cars = response.context["car_list"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(cars), 1)
        self.assertIn(toyota_camry, cars)
        self.assertNotIn(bmw_x5, cars)
        self.assertNotIn(audi_a6, cars)

    def test_car_search_empty_query_returns_all(self) -> None:
        self.login_user()

        manufacturer = self.create_manufacturer()

        for model in [
            "Toyota Camry",
            "BMW X5",
            "Audi A6",
            "Tesla Model S",
        ]:
            self.create_car(
                model=model,
                manufacturer=manufacturer,
            )

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 4)


class DriverListViewTest(BaseTaxiTestCase):
    def test_driver_list_pagination_is_5(self) -> None:
        self.login_user()

        for number in range(5):
            self.create_driver(
                username=f"driver_{number}",
                license_number=f"DRV{number}1111",
            )

        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(response.context["paginator"].count, 6)
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_driver_search_by_username(self) -> None:
        self.login_user()

        john = self.create_driver(
            username="john_kitty_driver",
            license_number="JOH12345",
        )
        anna = self.create_driver(
            username="anna_kitty_driver",
            license_number="ANN12345",
        )
        test_user = self.create_driver(
            username="test_user",
            license_number="TST12345",
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "kitty"},
        )

        drivers = response.context["driver_list"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(drivers), 2)
        self.assertIn(john, drivers)
        self.assertIn(anna, drivers)
        self.assertNotIn(test_user, drivers)

    def test_driver_search_empty_query_returns_all(self) -> None:
        self.login_user()

        self.create_driver(
            username="john_kitty_driver",
            license_number="JOH12345",
        )
        self.create_driver(
            username="anna_kitty_driver",
            license_number="ANN12345",
        )
        self.create_driver(
            username="test_user",
            license_number="TST12345",
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 4)


class DetailViewsTest(BaseTaxiTestCase):
    def test_car_detail_url_exists_for_logged_in_user(self) -> None:
        self.login_user()

        car = self.create_car(model="Toyota Camry")

        response = self.client.get(
            reverse("taxi:car-detail", args=[car.pk]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
        self.assertEqual(response.context["car"], car)

    def test_driver_detail_url_exists_for_logged_in_user(self) -> None:
        driver = self.login_user()

        response = self.client.get(
            reverse("taxi:driver-detail", args=[driver.pk]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
        self.assertEqual(response.context["driver"], driver)


class ManufacturerCRUDTest(BaseTaxiTestCase):
    def test_manufacturer_create_view_creates_manufacturer(self) -> None:
        self.login_user()

        old_count = Manufacturer.objects.count()

        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            data={
                "name": "New Manufacturer",
                "country": "New Country",
            },
        )

        self.assertRedirects(
            response,
            reverse("taxi:manufacturer-list"),
        )
        self.assertEqual(Manufacturer.objects.count(), old_count + 1)
        self.assertTrue(
            Manufacturer.objects.filter(
                name="New Manufacturer",
                country="New Country",
            ).exists()
        )

    def test_manufacturer_update_view_updates_manufacturer(self) -> None:
        self.login_user()

        manufacturer = self.create_manufacturer(
            name="Old Manufacturer",
            country="Old Country",
        )

        response = self.client.post(
            reverse(
                "taxi:manufacturer-update",
                args=[manufacturer.pk],
            ),
            data={
                "name": "Updated Manufacturer",
                "country": "Updated Country",
            },
        )

        manufacturer.refresh_from_db()

        self.assertRedirects(
            response,
            reverse("taxi:manufacturer-list"),
        )
        self.assertEqual(manufacturer.name, "Updated Manufacturer")
        self.assertEqual(manufacturer.country, "Updated Country")

    def test_manufacturer_delete_view_deletes_manufacturer(self) -> None:
        self.login_user()

        manufacturer = self.create_manufacturer()

        response = self.client.post(
            reverse(
                "taxi:manufacturer-delete",
                args=[manufacturer.pk],
            ),
        )

        self.assertRedirects(
            response,
            reverse("taxi:manufacturer-list"),
        )
        self.assertEqual(Manufacturer.objects.count(), 0)


class CarCRUDTest(BaseTaxiTestCase):
    def test_car_create_view_creates_car(self) -> None:
        driver = self.login_user()
        manufacturer = self.create_manufacturer()

        old_count = Car.objects.count()

        response = self.client.post(
            reverse("taxi:car-create"),
            data={
                "model": "Toyota Camry",
                "manufacturer": manufacturer.pk,
                "drivers": [driver.pk],
            },
        )

        car = Car.objects.get(model="Toyota Camry")

        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertEqual(Car.objects.count(), old_count + 1)
        self.assertEqual(car.manufacturer, manufacturer)
        self.assertIn(driver, car.drivers.all())

    def test_car_update_view_updates_car(self) -> None:
        driver = self.login_user()
        driver2 = self.create_driver(
            username="second_driver",
            license_number="SEC12345",
        )
        manufacturer = self.create_manufacturer()

        car = self.create_car(
            model="Toyota Camry",
            manufacturer=manufacturer,
        )
        car.drivers.set([driver])

        response = self.client.post(
            reverse("taxi:car-update", args=[car.pk]),
            data={
                "model": "Updated Toyota Camry",
                "manufacturer": manufacturer.pk,
                "drivers": [driver.pk, driver2.pk],
            },
        )

        car.refresh_from_db()

        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertEqual(car.model, "Updated Toyota Camry")
        self.assertEqual(car.drivers.count(), 2)
        self.assertIn(driver, car.drivers.all())
        self.assertIn(driver2, car.drivers.all())

    def test_car_delete_view_deletes_car(self) -> None:
        self.login_user()

        car = self.create_car(model="Toyota Camry")

        response = self.client.post(
            reverse("taxi:car-delete", args=[car.pk]),
        )

        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertEqual(Car.objects.count(), 0)


class DriverCRUDTest(BaseTaxiTestCase):
    def test_driver_create_view_creates_driver(self) -> None:
        self.login_user()

        old_count = Driver.objects.count()

        response = self.client.post(
            reverse("taxi:driver-create"),
            data={
                "username": "new_driver",
                "first_name": "New",
                "last_name": "Driver",
                "password1": "pass12345",
                "password2": "pass12345",
                "license_number": "NEW12345",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Driver.objects.count(), old_count + 1)
        self.assertTrue(
            Driver.objects.filter(username="new_driver").exists()
        )

    def test_driver_license_update_updates_license_number(self) -> None:
        driver = self.login_user()

        response = self.client.post(
            reverse("taxi:driver-update", args=[driver.pk]),
            data={
                "license_number": "UPD12345",
            },
        )

        driver.refresh_from_db()

        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.assertEqual(driver.license_number, "UPD12345")


class ToggleAssignToCarTest(BaseTaxiTestCase):
    def test_toggle_assign_to_car_assigns_car_to_logged_in_driver(
            self,
    ) -> None:
        driver = self.login_user()
        car = self.create_car(model="Toyota Camry")

        self.assertNotIn(car, driver.cars.all())

        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[car.pk]),
        )

        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[car.pk]),
        )
        self.assertIn(car, driver.cars.all())

    def test_toggle_assign_to_car_removes_car_from_logged_in_driver(
            self,
    ) -> None:
        driver = self.login_user()
        car = self.create_car(model="Toyota Camry")
        car.drivers.add(driver)

        self.assertIn(car, driver.cars.all())

        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[car.pk]),
        )

        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[car.pk]),
        )
        self.assertNotIn(car, driver.cars.all())
