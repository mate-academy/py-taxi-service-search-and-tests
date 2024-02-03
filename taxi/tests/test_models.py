from django.test import TestCase


from taxi.models import Driver, Car, Manufacturer


class ModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create_user(
            username="test",
            password="<PASSWORD>",
            first_name="Test_first",
            last_name="Test_last",
            license_number="AAA11111",
        )
        Manufacturer.objects.create(
            name="manufacturer_test",
            country="test_country",
        )
        Car.objects.create(
            model="car_test",
            manufacturer=Manufacturer.objects.get(id=1)
        )

    def test_driver_creation(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.username, "test")
        self.assertEqual(driver.first_name, "Test_first")
        self.assertEqual(driver.last_name, "Test_last")
        self.assertEqual(driver.license_number, "AAA11111")
        self.assertTrue(driver.check_password("<PASSWORD>"))

    def test_driver_verbose_name(self):
        verbose_name = Driver._meta.verbose_name
        self.assertEqual(verbose_name, "driver")

    def test_driver_verbose_name_plural(self):
        verbose_name_plural = Driver._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, "drivers")

    def test_driver_str(self):
        driver = Driver.objects.get(id=1)
        expected_object_name = (f"{driver.username} "
                                f"({driver.first_name} {driver.last_name})")
        self.assertEqual(str(driver), expected_object_name)

    def test_driver_get_absolute_url(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        expected_object_name = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(str(manufacturer), expected_object_name)

    def test_car_str(self):
        car = Car.objects.get(id=1)
        expected_object_name = car.model
        self.assertEqual(str(car), expected_object_name)
