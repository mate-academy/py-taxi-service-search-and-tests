from django.test import TestCase
from taxi.models import Manufacturer, Driver, Car
from django.urls import reverse


class ModelsTest(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="text_name",
            country="test_country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="test_username",
            first_name="test_f_name",
            last_name="test_l_name"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="text_name",
            country="test_country"
        )

        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )

        self.assertEqual(
            str(car),
            car.model
        )

    def test_if_drivers_detail_url_if_valid(self):
        driver = Driver.objects.create_user(
            username="testdriver",
            password="A-strong-test-password-123!",
            first_name="testname",
            last_name="testlastname",
            license_number="ABC12345"
        )
        valid_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), valid_url)

    def test_if_manufacturer_ordering_is_valid(self):
        manufacturer_1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        manufacturer_2 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(manufacturers),
            [manufacturer_2, manufacturer_1]
        )
