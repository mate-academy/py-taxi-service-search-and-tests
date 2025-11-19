import django.urls.exceptions
from django.contrib.admin.templatetags.admin_list import pagination
from django.test import TestCase
from taxi.models import Manufacturer, Car, Driver
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from taxi.urls import app_name


class PublicViewsTests(TestCase):
    models = (
        "manufacturer",
        "car",
        "driver",
    )

    templates_paths = (
        "list",
        "detail",
        "create",
        "update",
        "delete",
    )

    def test_required_login(self):
        for model in self.models:
            for name in self.templates_paths:
                try:
                    resp = self.client.get(
                        reverse(
                            f"{app_name}:{model}-{name}",
                            kwargs={"pk": 1} if name not in ("create", "list") else None
                        ),
                    )
                    self.assertNotEqual(
                        resp.status_code, 200,
                        msg=f"{model}-{name} returned code {resp.status_code} to an unregistered user"
                    )
                except NoReverseMatch:
                    print(f"model \"{model}\" no have a view \"{name}\"")


class PrivateViewsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_pagination = 7

        for num in range(test_pagination):
            Manufacturer.objects.create(
                name="test-manufacturer %s" % num,
                country="test-country",
            )


            Car.objects.create(
                model="test %s" % num,
                manufacturer_id=num + 1
            )

    def test_log(self):
        print("pass")
