from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacturer_model(self):
        obj = Manufacturer.objects.create(name="Volvo", country="sw")
        self.assertEqual(str(obj), f"{obj.name} {obj.country}")

    def test_driver_model(self):
        obj = Driver.objects.create(
            username="111",
            first_name="John",
            last_name="Smith",
            license_number="BBB12345"
        )
        self.assertEqual(
            str(obj),
            f"({obj.username} {obj.first_name} {obj.last_name})"
        )
        self.assertEqual(obj.license_number, "BBB12345")

    def test_car_model(self):
        manufacturer = Manufacturer.objects.create(name="Volvo")
        obj = Car.objects.create(model="test", manufacturer=manufacturer)
        self.assertEqual(str(obj), obj.model)

    def test_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)


class LoggedInViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="test", password="12345678"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_name(self):
        Manufacturer.objects.create(name="BMW", country="DE")
        Manufacturer.objects.create(name="Nissan", country="JP")
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        manufacturer_list = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer_list)
        )
        self.assertTemplateUsed(
            response, "taxi/manufacturer_list.html"
        )

    def test_search_manufacturer_name(self):
        Manufacturer.objects.create(name="BMW", country="DE")
        Manufacturer.objects.create(name="Nissan", country="JP")
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?title=b"
        )
        man_with_b = Manufacturer.objects.filter(name__startswith="b")
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(man_with_b)
        )
