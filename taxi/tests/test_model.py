import random

from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class ManufacturerTest(TestCase):

    def test_ordering(self):
        self.assertEqual(Manufacturer._meta.ordering, ["name"])

        for i in range(5):
            Manufacturer.objects.create(name=f"name_{i}", country="country")

        queryset = Manufacturer.objects.all()
        self.assertEqual(list(queryset), list(queryset.order_by("name")))

    def test_str(self):
        name = "test_name"
        country = "test_country"
        manufacturer = Manufacturer.objects.create(name=name, country=country)
        self.assertEqual(str(manufacturer), f"{name} {country}")


class DriverTest(TestCase):
    def test_verbose_names(self):
        self.assertEqual(Driver._meta.verbose_name, "driver")
        self.assertEqual(Driver._meta.verbose_name_plural, "drivers")

    def test_str(self):
        username = "testname"
        password = "testpassword"
        user = Driver.objects.create_user(
            username=username,
            password=password,
            first_name=username,
            last_name=username)
        self.assertEqual(
            str(user),
            f"{username} ({username} {username})")

    def test_absolute_url(self):
        pk = 1
        username = "testname"
        password = "testpassword"
        user = Driver.objects.create_user(
            id=pk,
            username=username,
            password=password)

        url = user.get_absolute_url()
        self.assertEqual(url, reverse("taxi:driver-detail", kwargs={"pk": pk}))


class CarTest(TestCase):

    def test_str(self):
        Manufacturer.objects.create(id=1,
                                    name="test",
                                    country="test")
        car = Car.objects.create(model="test",
                                 manufacturer_id=1)
        self.assertEqual(str(car), "test")
