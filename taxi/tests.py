from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.forms import validate_license_number
from taxi.models import Driver, Manufacturer, Car


class SearchTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="angel", country="Ukraine"
        )
        self.driver = Driver.objects.create(
            username="john", license_number="341RWQTW"
        )
        self.car = Car.objects.create(
            model="Volvo", manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

        self.manufacturer2 = Manufacturer.objects.create(
            name="Velik", country="USA"
        )
        self.driver2 = Driver.objects.create(
            username="Cena", license_number="745ESYSF"
        )
        self.car2 = Car.objects.create(
            model="BMW", manufacturer=self.manufacturer2
        )
        self.car2.drivers.add(self.driver2)
        self.client.force_login(self.driver)

    def test_manufacturer_search(self):
        res = self.client.get(reverse("taxi:manufacturer-list", ),
                              {"name": "angel"})
        self.assertContains(res, "angel")
        self.assertNotContains(res, "Velik")

    def test_driver_search(self):
        res = self.client.get(reverse("taxi:driver-list"),
                              {"username": "john"})
        self.assertContains(res, "john")
        self.assertNotContains(res, "Cena")

    def test_car_search(self):
        res = self.client.get(reverse("taxi:car-list"), {"model": "Volvo"})
        self.assertContains(res, "Volvo")
        self.assertNotContains(res, "BMW")

    def test_toggle_assign_to_car(self):
        res = self.client.get(reverse("taxi:toggle-car-assign",
                                      kwargs={"pk": self.car.id}))
        expected_url = reverse("taxi:car-detail", kwargs={"pk": self.car.id})
        self.assertRedirects(res, expected_url)
        self.assertNotIn(self.car, self.driver.cars.all())

    def test_license_number_validation_error_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABCiid7685")

    def test_license_number_validation_error_isupper_isalpha(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ksi85943")

    def test_license_number_validation_error_isdigit(self):
        with self.assertRaises(ValidationError):
            validate_license_number("OWRRIERS")

    def test_license_number_correct(self):
        func = validate_license_number("OSU35124")
        self.assertEqual(func, "OSU35124")
