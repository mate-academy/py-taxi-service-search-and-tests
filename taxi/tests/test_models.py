from typing import List

from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ManufacturerTest(TestCase):
    def setUp(self) -> None:
        objs = (
            Manufacturer(name="btest", country="btest country"),
            Manufacturer(name="atest", country="atest country")
        )
        Manufacturer.objects.bulk_create(objs)

    def test_model_str(self) -> None:
        manufacturer = Manufacturer.objects.filter(name="atest").first()
        self.assertEqual(str(manufacturer), "atest atest country")

    def test_check_ordering(self) -> None:
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(manufacturers[0].name, "atest")
        self.assertEqual(manufacturers[1].name, "btest")

    def test_verbose_name(self) -> None:
        self.assertEqual(Manufacturer._meta.verbose_name, "manufacturer")

    def test_verbose_name_plural(self) -> None:
        self.assertEqual(
            Manufacturer._meta.verbose_name_plural,
            "manufacturers"
        )


class DriverTest(TestCase):
    def setUp(self) -> None:
        objs = (
            Driver(
                first_name="btest_name",
                last_name="btest_last_name",
                username="busername",
                email="btest@gmail.com",
                license_number="FHG17564"
            ),
            Driver(
                first_name="atest_name",
                last_name="atest_last_name",
                username="ausername",
                email="atest@gmail.com",
                license_number="FHG12939"
            )
        )
        Driver.objects.bulk_create(objs)

    def test_model_str(self) -> None:
        driver = Driver.objects.filter(username="busername").first()
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
            )

    def test_verbose_name(self) -> None:
        self.assertEqual(Driver._meta.verbose_name, "driver")

    def test_verbose_name_plural(self) -> None:
        self.assertEqual(
            Driver._meta.verbose_name_plural,
            "drivers"
        )

    def test_absolute_url(self) -> None:
        driver = Driver.objects.get(pk=1)
        self.assertEqual(
            driver.get_absolute_url(),
            "/drivers/1/"
        )


class CarTest(TestCase):
    def setUp(self) -> None:
        manufacturers = self.createManufactures()
        drivers = self.createDrivers()
        self.createCars(drivers, manufacturers)

    @staticmethod
    def createManufactures() -> List[Manufacturer]:
        manufacturers = (
            Manufacturer(name="btest", country="btest country"),
            Manufacturer(name="atest", country="atest country")
        )
        Manufacturer.objects.bulk_create(manufacturers)
        return Manufacturer.objects.all()

    @staticmethod
    def createDrivers() -> List[Driver]:
        drivers = (
            Driver(
                first_name="btest_name",
                last_name="btest_last_name",
                username="busername",
                email="btest@gmail.com",
                license_number="FHG17564"
            ),
            Driver(
                first_name="atest_name",
                last_name="atest_last_name",
                username="ausername",
                email="atest@gmail.com",
                license_number="FHG12939"
            )
        )
        Driver.objects.bulk_create(drivers)

        return Driver.objects.all()

    @staticmethod
    def createCars(
        drivers: List[Driver],
        manufacturers: List[Manufacturer]
    ) -> List[Car]:
        for i in range(2):
            car = Car.objects.create(
                model=f"model_{i}",
                manufacturer=manufacturers[i]
            )
            car.drivers.set([drivers[i]])

        return Car.objects.all()

    def test_model_str(self):
        car = Car.objects.first()
        self.assertEqual(str(car), car.model)

    def test_verbose_name(self):
        self.assertEqual(Car._meta.verbose_name, "car")

    def test_verbose_name_plural(self):
        self.assertEqual(Car._meta.verbose_name_plural,"cars")
