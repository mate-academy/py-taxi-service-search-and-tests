from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerTest(TestCase):
    def test_object_str(self):
        obj = Manufacturer.objects.create(
            name="Test",
            country="Country"
        )

        self.assertEquals(str(obj), f"{obj.name} {obj.country}")


class DriverTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="Test",
            password="Test12345",
            first_name="First",
            last_name="Last",
        )

    def test_object_str(self):
        obj = get_user_model().objects.get(id=1)

        self.assertEquals(
            str(obj),
            f"{obj.username} ({obj.first_name} {obj.last_name})"
        )

    def test_absolute_url(self):
        obj = get_user_model().objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), "/drivers/1/")


class CarTest(TestCase):
    def test_object_str(self):
        obj_man = Manufacturer.objects.create(
            name="Test",
            country="Country"
        )

        obj = Car.objects.create(
            model="Test",
            manufacturer=obj_man,
        )
        self.assertEquals(str(obj), obj.model)
