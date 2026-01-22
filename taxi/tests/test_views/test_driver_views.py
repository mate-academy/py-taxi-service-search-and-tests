from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm, CarSearchForm, DriverSearchForm
from taxi.models import Manufacturer, Car

Driver = get_user_model()

LIST_VIEW_URL = reverse("taxi:driver-list")


class DriverListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cars_count = 8
        cls.manufacturers_count = 5
        cls.drivers_count = 8

        for driver_copy in range(cls.drivers_count):
            Driver.objects.create_user(
                username=f"Username {driver_copy}",
                password="test_password",
                license_number=f"AAA1234{driver_copy}"
            )

        for manufacturer_copy in range(cls.manufacturers_count):
            Manufacturer.objects.create(
                name=f"Manufacturer {manufacturer_copy}",
                country=f"Country {manufacturer_copy}"
            )

        for car_copy in range(cls.cars_count):
            Car.objects.create(
                model=f"Car {car_copy}",
                manufacturer=Manufacturer.objects.get(
                    pk=car_copy % cls.manufacturers_count + 1
                )
            )

    def test_login_required(self):
        response = self.client.get(LIST_VIEW_URL)
        self.assertRedirects(
            response,
            reverse("login") + f"?next={LIST_VIEW_URL}"
        )

    def test_correct_template(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL)
        self.assertTemplateUsed(
            response,
            "taxi/driver_list.html"
        )

    def test_context_object_name(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL)
        self.assertIn(
            "driver_list",
            response.context
        )

    def test_paginated_by_5(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL)
        self.assertIn("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 5)

        response = self.client.get(LIST_VIEW_URL + "?page=2")
        self.assertEqual(len(response.context["driver_list"]), 3)

    def test_model(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL)

        for driver in response.context["driver_list"]:
            self.assertIsInstance(driver, Driver)

    def test_search_form_in_context(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL)

        self.assertIsInstance(
            response.context["search_form"],
            DriverSearchForm
        )

    def test_search_form_use_username_param(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL + "?username=4")

        self.assertEqual(
            response.context["search_form"].initial["username"],
            "4"
        )

        self.assertEqual(
            len(response.context["driver_list"]),
            1
        )
        self.assertContains(
            response,
            "Username 4"
        )

    def test_search_form_check_for_contains(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL + "?username=RNA")

        self.assertEqual(
            response.context["page_obj"].paginator.count,
            Driver.objects.filter(username__icontains="RNA").count()
        )

    def test_has_detail_anchors(self):
        drivers = Driver.objects.all()[:5]
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL)

        for driver in drivers:
            detail_url = reverse(
                "taxi:driver-detail",
                args=[driver.id]
            )
            self.assertContains(
                response,
                f'href="{detail_url}"'
            )

    def test_returns_nothing_for_bad_search(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(
            LIST_VIEW_URL + "?username=bad_search_param"
        )

        self.assertEqual(
            response.context["page_obj"].paginator.count,
            0
        )
        self.assertEqual(
            len(response.context["driver_list"]),
            0
        )


CREATE_VIEW_URL = reverse("taxi:driver-create")


class DriverCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create_user(
            username="Username",
            password="test_password",
            license_number="AAA12345"
        )

    def test_login_required(self):
        response = self.client.get(CREATE_VIEW_URL)
        self.assertRedirects(
            response,
            reverse("login") + f"?next={CREATE_VIEW_URL}"
        )

    def test_uses_correct_template(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(CREATE_VIEW_URL)
        self.assertTemplateUsed(
            response,
            "taxi/driver_form.html"
        )

    def test_creates_new_object(self):
        driver = Driver.objects.get(pk=1)
        self.client.force_login(driver)

        driver_data = {
            "username": "Driver_2",
            "password1": "SecureCode1",
            "password2": "SecureCode1",
            "license_number": "AAA12346",
            "first_name": "First name",
            "last_name": "Last name"
        }
        response = self.client.post(
            CREATE_VIEW_URL,
            driver_data
        )
        self.assertRedirects(response, reverse("taxi:driver-detail", args=[2]))

        self.assertIsNotNone(
            Driver.objects.get(
                username=driver_data["username"],
                first_name=driver_data["first_name"],
                last_name=driver_data["last_name"],
                license_number=driver_data["license_number"]
            )
        )

    def test_should_not_create_if_data_is_invalid(self):
        driver = Driver.objects.get(pk=1)
        self.client.force_login(driver)
        car_data = {}
        response = self.client.post(
            CREATE_VIEW_URL,
            car_data
        )

        self.assertEqual(
            response.context["form"].errors,
            {
                "username": ["This field is required."],
                "license_number": ["This field is required."],
                "password1": ["This field is required."],
                "password2": ["This field is required."]
            }
        )


UPDATE_VIEW_URL = reverse(
    "taxi:driver-update",
    args=[1]
)


class DriverUpdateLicenseViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.drivers = [
            Driver.objects.create_user(
                username="Username",
                password="test_password",
                license_number="AAA12345"
            ),
            Driver.objects.create_user(
                username="Username2",
                password="test_password",
                license_number="AAA12346"
            )
        ]

    def test_login_required(self):
        response = self.client.get(
            UPDATE_VIEW_URL
        )
        self.assertRedirects(
            response,
            reverse("login")
            + f"?next={UPDATE_VIEW_URL}"
        )

    def test_uses_correct_template(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(
            UPDATE_VIEW_URL
        )
        self.assertTemplateUsed(
            response,
            "taxi/driver_form.html"
        )

    def test_show_correct_license_number(self):
        driver = Driver.objects.get(pk=1)
        self.client.force_login(driver)

        response = self.client.get(
            UPDATE_VIEW_URL
        )

        self.assertContains(
            response,
            f'value="{driver.license_number}"'
        )

    def test_updates_object(self):
        self.client.force_login(Driver.objects.get(pk=1))

        drivers_before = list(
            Driver.objects.all().values("license_number")
        )

        drivers_before[0]["license_number"] = "ABC56789"

        response = self.client.post(
            UPDATE_VIEW_URL,
            drivers_before[0]
        )
        self.assertRedirects(response, LIST_VIEW_URL)

        drivers_after = list(
            Driver.objects.all().order_by("id").values("license_number")
        )

        self.assertEqual(
            drivers_after,
            drivers_before
        )

    def test_should_not_update_if_data_is_invalid(self):
        self.client.force_login(Driver.objects.get(pk=1))

        response = self.client.post(
            UPDATE_VIEW_URL,
            {}
        )

        self.assertEqual(
            response.context["form"].errors,
            {
                "license_number": ["This field is required."],
            }
        )


DELETE_VIEW_URL = reverse(
    "taxi:driver-delete",
    args=[1]
)


class DriverDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.drivers = [
            Driver.objects.create_user(
                username="Username",
                password="test_password",
                license_number="AAA12345"
            ),
            Driver.objects.create_user(
                username="Username2",
                password="test_password",
                license_number="AAA12346"
            )
        ]

    def test_login_required(self):
        response = self.client.get(
            DELETE_VIEW_URL
        )
        self.assertRedirects(
            response,
            reverse("login")
            + f"?next={DELETE_VIEW_URL}"
        )

    def test_uses_correct_template(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(
            DELETE_VIEW_URL
        )
        self.assertTemplateUsed(
            response,
            "taxi/driver_confirm_delete.html"
        )

    def test_show_404_for_invalid_id(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(
            reverse("taxi:driver-delete", args=[123])
        )

        self.assertEqual(response.status_code, 404)


DETAIL_VIEW_URL = reverse("taxi:driver-detail", args=[1])


class DriverDetailsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.drivers = [
            Driver.objects.create_user(
                username="Username",
                password="test_password",
                license_number="AAA12345",
                first_name="First name",
                last_name="Last name",
            ),
            Driver.objects.create_user(
                username="Username2",
                password="test_password",
                license_number="AAA12346",
                first_name="First name 2",
                last_name="Last name 2",
            )
        ]

        cls.manufacturers_count = 2
        cls.cars_count = 2

        for manufacturer_copy in range(cls.manufacturers_count):
            Manufacturer.objects.create(
                name=f"Manufacturer {manufacturer_copy}",
                country=f"Country {manufacturer_copy}"
            )

        for car_copy in range(cls.cars_count):
            car = Car.objects.create(
                model=f"Car {car_copy}",
                manufacturer=Manufacturer.objects.get(
                    pk=car_copy % cls.manufacturers_count + 1
                )
            )
            car.drivers.set([cls.drivers[car_copy % 2]])

    def test_login_required(self):
        response = self.client.get(
            DETAIL_VIEW_URL
        )
        self.assertRedirects(
            response,
            reverse("login")
            + f"?next={DETAIL_VIEW_URL}"
        )

    def test_uses_correct_template(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(
            DETAIL_VIEW_URL
        )
        self.assertTemplateUsed(
            response,
            "taxi/driver_detail.html"
        )

    def test_show_404_for_invalid_id(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(
            reverse("taxi:driver-detail", args=[123])
        )

        self.assertEqual(response.status_code, 404)

    def test_contains_driver_cars(self):
        driver = Driver.objects.get(pk=1)

        self.client.force_login(driver)
        response = self.client.get(DETAIL_VIEW_URL)

        for car in driver.cars.all():
            self.assertContains(
                response,
                car.model
            )

            self.assertContains(
                response,
                car.manufacturer.name
            )

    def test_contains_driver_info(self):
        driver = Driver.objects.get(pk=1)

        self.client.force_login(driver)
        response = self.client.get(DETAIL_VIEW_URL)

        self.assertContains(
            response,
            driver.first_name
        )

        self.assertContains(
            response,
            driver.last_name
        )

        self.assertContains(
            response,
            driver.license_number
        )

    def test_has_update_and_delete_anchors(self):
        car = Car.objects.get(pk=1)

        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(DETAIL_VIEW_URL)

        update_url = reverse(
            "taxi:driver-update",
            args=[car.id]
        )

        self.assertContains(
            response,
            f'href="{update_url}"'
        )

        delete_url = reverse(
            "taxi:driver-delete",
            args=[car.id]
        )

        self.assertContains(
            response,
            f'href="{delete_url}"'
        )
