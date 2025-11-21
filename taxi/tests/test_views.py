from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car
from taxi.forms import (
    CarModelSearchForm,
    ManufacturerNameSearchForm,
    DriverUsernameSearchForm,
)
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from taxi.urls import app_name


class PublicViewsTests(TestCase):
    models = (
        "manufacturer",
        "car",
        get_user_model().__name__.lower(),
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
                            kwargs=(
                                {"pk": 1} if name not in ("create", "list") else None
                            ),
                        ),
                    )
                    self.assertNotEqual(
                        resp.status_code,
                        200,
                        msg=f"{model}-{name} returned code {resp.status_code} to an unregistered user",
                    )
                except NoReverseMatch:
                    print(f'model "{model}" have not a view "{name}"')


class PrivateViewsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_pagination = 7

        for num in range(test_pagination):
            Manufacturer.objects.create(
                name="test-manufacturer%s" % num,
                country="test-country",
            )

            Car.objects.create(model="test-car%s" % num, manufacturer_id=num + 1)
            get_user_model().objects.create_user(
                username="test-driver%s" % num,
            )

    def setUp(self):
        self.client.force_login(user=get_user_model().objects.get(pk=1))

    def test_pagination(self):
        for model in PublicViewsTests.models:
            resp = self.client.get(
                reverse(
                    f"{app_name}:{model}-list",
                )
            )
            if_error = f"for {model}-list"
            self.assertEqual(
                resp.status_code,
                200,
                msg=f"status code for autherized user not a 200, {if_error}"
            )
            self.assertTrue(
                "is_paginated" in resp.context,
                msg=f"No paginated in context response, {if_error}"
            )
            self.assertTrue(
                resp.context["is_paginated"] is True,
                msg=f"Paginate in context response no a True, {if_error}"
            )
            self.assertEqual(len(resp.context[f"{model}_list"]), 5)

            resp = self.client.get(
                reverse(
                    f"{app_name}:{model}-list",
                )
                + "?page=2",
            )
            self.assertEqual(len(resp.context[f"{model}_list"]), 2)

    def test_update_car_drivers(self):
        for num in range(2):
            self.client.get(
                reverse(
                    f"{app_name}:toggle-car-assign",
                    kwargs={"pk": 1},
                )
            )
            if num == 0:
                self.assertEqual(
                    get_user_model().objects.get(pk=1).cars.count(),
                    1,
                    msg="Request not add driver in car drivers",
                )
            if num == 1:
                self.assertEqual(
                    get_user_model().objects.get(pk=1).cars.count(),
                    0,
                    msg="Request not remove driver in car drivers",
                )

    def test_context_list(self):
        for model in PublicViewsTests.models:
            if model == "manufacturer":
                _data = "name"
            elif model == "car":
                _data = "model"
            elif model == get_user_model().__name__.lower():
                _data = "username"
            else:
                _data = None

            if _data:
                resp = self.client.get(
                    reverse(
                        f"{app_name}:{model}-list",
                    ),
                    {_data: f"test-{model}1"},
                )
                self.assertTrue("search_form" in resp.context)
                self.assertEqual(len(resp.context[f"{model}_list"]), 1, msg=model)
            else:
                raise NameError(f"{model}-{_data} is not a valid model")
