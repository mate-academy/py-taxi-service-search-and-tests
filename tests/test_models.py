from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car

Driver = get_user_model()


class ModelsStrTests(TestCase):
    def test_manufacturer_str(self):
        man = Manufacturer.objects.create(name="Audi", country="Germany")
        self.assertIn("Audi", str(man))

    def test_car_str(self):
        man = Manufacturer.objects.create(name="Ford", country="USA")
        cer = Car.objects.create(model="Focus", manufacturer=man)
        self.assertIn("Focus", str(cer))

    def test_driver_str_contains_username(self):
        driv = Driver.objects.create_user(
            username="lev",
            password="p",
            license_number="LEV00001"
        )
        self.assertIn("lev", str(driv))


class ModelsRelationsTests(TestCase):
    def test_car_add_driver(self):
        man = Manufacturer.objects.create(name="Tesla", country="USA")
        cer = Car.objects.create(model="Model S", manufacturer=man)
        driv = Driver.objects.create_user(
            username="alice",
            password="p", license_number="ALICE001")
        cer.drivers.add(driv)
        self.assertIn(driv, cer.drivers.all())
