from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from parametrize import parametrize

from taxi.models import Manufacturer, Car


class PublicLoginTest(TestCase):
    @parametrize("url, arg", [("taxi:index", ""),
                              ("taxi:manufacturer-list", ""),
                              ("taxi:car-list", ""),
                              ("taxi:car-detail", "1"),
                              ("taxi:driver-list", ""),
                              ("taxi:driver-detail", "1"),
                              ("taxi:driver-create", ""),
                              ("taxi:driver-update", "1"),
                              ("taxi:driver-delete", "1"),
                              ("taxi:car-create", ""),
                              ("taxi:car-update", "1"),
                              ("taxi:car-delete", "1"),
                              ("taxi:manufacturer-create", ""),
                              ("taxi:manufacturer-update", "1"),
                              ("taxi:manufacturer-delete", "1")])
    def test_no_login_required(self, url, arg):
        res = self.client.get(reverse(url, args=arg))
        self.assertEqual(res.status_code, 302)


class PrivateLoginTest(TestCase):
    def setUp(self) -> None:
        manufact = Manufacturer.objects.create(name="Fiat", country="Italy")
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        car = Car.objects.create(model="testModel",
                                 manufacturer=manufact,)
        car.drivers.set([self.user])
        self.client.force_login(self.user)

    @parametrize("url, arg", [("taxi:index", ""),
                              ("taxi:manufacturer-list", ""),
                              ("taxi:car-list", ""),
                              ("taxi:car-detail", "1"),
                              ("taxi:driver-list", ""),
                              ("taxi:driver-detail", "1"),
                              ("taxi:driver-create", ""),
                              ("taxi:driver-update", "1"),
                              ("taxi:driver-delete", "1"),
                              ("taxi:car-create", ""),
                              ("taxi:car-update", "1"),
                              ("taxi:car-delete", "1"),
                              ("taxi:manufacturer-create", ""),
                              ("taxi:manufacturer-update", "1"),
                              ("taxi:manufacturer-delete", "1")])
    def test_login_required(self, url, arg):
        res = self.client.get(reverse(url, args=arg))
        self.assertEqual(res.status_code, 200)

    def test_index_context(self):
        response = self.client.get(reverse("taxi:index"))
        context = {"num_cars": Car.objects.all().count(),
                   "num_drivers": get_user_model().objects.all().count(),
                   "num_manufacturers": Manufacturer.objects.all().count(),
                   "num_visits": 1}
        self.assertEqual(list(response.context[3].dicts[3].items()),
                         list(context.items()))


class TemplateUsedTest(TestCase):
    def setUp(self) -> None:
        manufact = Manufacturer.objects.create(name="Fiat", country="Italy")
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        car = Car.objects.create(model="testModel",
                                 manufacturer=manufact,)
        car.drivers.set([self.user])
        self.client.force_login(self.user)

    @parametrize("url, template, arg",
                 [("taxi:index", "taxi/index.html", ""),
                  ("taxi:driver-list", "taxi/driver_list.html", ""),
                  ("taxi:driver-detail", "taxi/driver_detail.html", "1"),
                  ("taxi:driver-create", "taxi/driver_form.html", ""),
                  ("taxi:driver-update", "taxi/driver_form.html", "1"),
                  ("taxi:driver-delete",
                   "taxi/drivers_confirm_delete.html", "1"),
                  ("taxi:car-list", "taxi/car_list.html", ""),
                  ("taxi:car-detail", "taxi/car_detail.html", "1"),
                  ("taxi:car-create", "taxi/cars_form.html", ""),
                  ("taxi:car-update", "taxi/cars_form.html", "1"),
                  ("taxi:car-delete", "taxi/cars_confirm_delete.html", "1"),
                  ("taxi:manufacturer-list",
                   "taxi/manufacturer_list.html", ""),
                  ("taxi:manufacturer-create",
                   "taxi/manufacturer_form.html", ""),
                  ("taxi:manufacturer-update",
                   "taxi/manufacturer_form.html", "1"),
                  ("taxi:manufacturer-delete",
                   "taxi/manufacturer_confirm_delete.html", "1")],
                 )
    def test_templates_used_test(self, url, template, arg):
        response = self.client.get(reverse(url, args=arg))
        self.assertTemplateUsed(response, template)
