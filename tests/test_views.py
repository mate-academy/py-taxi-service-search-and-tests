from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


DRIVER = get_user_model()
USERNAME = "username"
PASSWORD = "password"


class LoginRequiredTests(TestCase):
    def test_not_auth_user_access(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_auth_user_access(self):
        DRIVER.objects.create_user(
            username=USERNAME,
            password=PASSWORD,
        )
        self.client.login(username=USERNAME, password=PASSWORD)
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(res.status_code, 200)


class DriverViewsTests(TestCase):
    def setUp(self):
        self.drivers = list()

        self.drivers.append(
            DRIVER.objects
            .create_user(
                username=USERNAME,
                password=PASSWORD,
            )
        )
        self.client.login(
            username=USERNAME,
            password=PASSWORD,
        )
        for i in range(5):
            self.drivers.append(
                DRIVER.objects.create_user(
                    username=f"{USERNAME}{i}",
                    password=PASSWORD,
                    license_number=f"ABC12"
                                   f"34{i}",
                )
            )

    def test_list_view_template(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_list_view_paginate(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertTemplateUsed(res, "includes/pagination.html")

    def test_update_view_template(self):
        res = self.client.get(reverse("taxi:driver-update", kwargs={"pk": 1}))
        self.assertTemplateUsed(res, "taxi/driver_form.html")

    def test_create_view_template(self):
        res = self.client.get(reverse("taxi:driver-create"))
        self.assertTemplateUsed(res, "taxi/driver_form.html")

    def test_delete_view_template(self):
        res = self.client.get(reverse("taxi:driver-delete", kwargs={"pk": 1}))
        self.assertTemplateUsed(res, "taxi/driver_confirm_delete.html")

    def test_detail_view_template(self):
        res = self.client.get(reverse("taxi:driver-detail", kwargs={"pk": 1}))
        self.assertTemplateUsed(res, "taxi/driver_detail.html")

    def test_is_paginated_view_by_five(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(res.context.get("paginator").per_page, 5)

    def test_drivers_list_in_list_view(self):
        res = self.client.get(reverse("taxi:driver-list"))
        per_page = res.context["paginator"].per_page
        self.assertEqual(
            self.drivers[:per_page],
            list(res.context["driver_list"])
        )

    def test_driver_in_detail_view(self):
        res = self.client.get(reverse("taxi:driver-detail", kwargs={"pk": 1}))
        self.assertIn(
            res.context["driver"],
            self.drivers,
        )

    def test_search_by_name(self):
        res = self.client.get(
            reverse("taxi:driver-list"),
            {"username": f"{USERNAME}0"}
        )
        self.assertContains(res, f"{USERNAME}0")
        self.assertNotContains(res, "username1")

    def test_search_form_in_context(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertIn("search_form", res.context)


class ManufacturerViewsTests(TestCase):
    def setUp(self):
        DRIVER.objects.create_user(
            username=USERNAME,
            password=PASSWORD,
        )
        self.client.login(
            username=USERNAME,
            password=PASSWORD,
        )
        self.manufacturers = list()
        for i in range(6):
            self.manufacturers.append(
                Manufacturer.objects.create(
                    name=f"testmanufacturer{i}",
                    country="testcountry"
                )
            )

    def test_list_view_template(self):
        res = self.client.get(
            reverse("taxi:manufacturer-list")
        )
        self.assertTemplateUsed(
            res,
            "taxi/manufacturer_list.html"
        )

    def test_list_view_paginate(self):
        res = self.client.get(
            reverse("taxi:manufacturer-list")
        )
        self.assertTemplateUsed(
            res,
            "includes/pagination.html"
        )

    def test_update_view_template(self):
        res = self.client.get(
            reverse(
                "taxi:manufacturer-update",
                kwargs={"pk": 1})
        )
        self.assertTemplateUsed(
            res,
            "taxi/manufacturer_form.html"
        )

    def test_create_view_template(self):
        res = self.client.get(
            reverse("taxi:manufacturer-create")
        )
        self.assertTemplateUsed(
            res,
            "taxi/manufacturer_form.html"
        )

    def test_delete_view_template(self):
        res = self.client.get(
            reverse(
                "taxi:manufacturer-delete",
                kwargs={"pk": 1}
            )
        )
        self.assertTemplateUsed(
            res,
            "taxi/manufacturer_confirm_delete.html"
        )

    def test_is_paginated_by_five(self):
        res = self.client.get(
            reverse("taxi:manufacturer-list")
        )
        self.assertEqual(
            res.context.get("paginator").per_page,
            5
        )

    def test_manufacturer_list_in_list_view(self):
        res = self.client.get(
            reverse("taxi:manufacturer-list")
        )
        per_page = res.context["paginator"].per_page
        self.assertEqual(
            self.manufacturers[:per_page],
            list(res.context["manufacturer_list"])
        )

    def test_search_by_name(self):
        res = self.client.get(
            reverse("taxi:manufacturer-list"),
            {
                "name": "testmanufacturer0"
            }
        )
        self.assertContains(res, "testmanufacturer0")
        self.assertNotContains(res, "testmanufacturer1")

    def test_search_form_in_context(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertIn("search_form", res.context)


class CarViewsTests(TestCase):
    def setUp(self):
        DRIVER.objects.create_user(
            username=USERNAME,
            password=PASSWORD,
        )
        self.client.login(
            username=USERNAME,
            password=PASSWORD,
        )
        manufacturer = Manufacturer.objects.create(
            name="testmanufacturer", country="testcountry"
        )
        self.cars = list()
        for i in range(6):
            self.cars.append(
                Car.objects.create(
                    model=f"testmodel{i}",
                    manufacturer=manufacturer,
                )
            )

    def test_list_view_template(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_list_view_paginate(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertTemplateUsed(res, "includes/pagination.html")

    def test_update_view_template(self):
        res = self.client.get(reverse("taxi:car-update", kwargs={"pk": 1}))
        self.assertTemplateUsed(res, "taxi/car_form.html")

    def test_create_view_template(self):
        res = self.client.get(reverse("taxi:car-create"))
        self.assertTemplateUsed(res, "taxi/car_form.html")

    def test_detail_view_template(self):
        res = self.client.get(reverse("taxi:car-detail", kwargs={"pk": 1}))
        self.assertTemplateUsed(res, "taxi/car_detail.html")

    def test_delete_view_template(self):
        res = self.client.get(reverse("taxi:car-delete", kwargs={"pk": 1}))
        self.assertTemplateUsed(res, "taxi/car_confirm_delete.html")

    def test_is_paginated_by_five(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(res.context.get("paginator").per_page, 5)

    def test_car_list_in_list_view(self):
        res = self.client.get(reverse("taxi:car-list"))
        per_page = res.context["paginator"].per_page
        self.assertEqual(self.cars[:per_page], list(res.context["car_list"]))

    def test_car_in_detail_view(self):
        res = self.client.get(
            reverse(
                "taxi:car-detail",
                kwargs={"pk": 1}
            )
        )
        self.assertIn(res.context["car"], self.cars)

    def test_search_by_model(self):
        res = self.client.get(
            reverse("taxi:car-list"),
            {"model": "testmodel0"}
        )
        self.assertContains(res, "testmodel0")
        self.assertNotContains(res, "testmodel1")

    def test_search_form_in_context(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertIn("search_form", res.context)
