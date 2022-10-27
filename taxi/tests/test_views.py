
from django.contrib.auth import get_user_model
from django.test import TestCase


from django.urls import reverse

import taxi.views
from taxi.forms import CarSearchForm
from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Mazda", country="Japan")
        Manufacturer.objects.create(name="BMW", country="Germany")

        resp = self.client.get(MANUFACTURER_URL)
        manufacturer_ = Manufacturer.objects.all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["manufacturer_list"]),
            list(manufacturer_)
        )
        self.assertTemplateUsed(resp, "taxi/manufacturer_list.html")


class PublicCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    @staticmethod
    def create_objects_for_tests(class_obj, **kwargs):
        return class_obj.objects.create(**kwargs)

    def test_search_for_a_car_by_symbols_from_the_model(self):
        man_1 = self.create_objects_for_tests(Manufacturer, name="Lincoln", country="USA")
        man_2 = self.create_objects_for_tests(Manufacturer, name="BMW", country="Germany")
        self.create_objects_for_tests(Car, model="LincolnX Navigator", manufacturer=man_1)
        self.create_objects_for_tests(Car, model="X7", manufacturer=man_2)

        resp = self.client.get(reverse("taxi:car-list") + "?model=x")
        cars = Car.objects.filter(model__icontains="x")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["car_list"]),
            list(cars)
        )

        self.assertTemplateUsed(resp, "taxi/car_list.html")
