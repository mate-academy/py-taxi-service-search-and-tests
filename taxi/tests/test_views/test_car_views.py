from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarSearchForm
from taxi.models import Manufacturer, Car

Driver = get_user_model()

LIST_VIEW_URL = reverse("taxi:car-list")


class CarListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cars_count = 8
        cls.manufacturers_count = 5

        Driver.objects.create_user(
            username="Username",
            password="test_password",
            license_number="AAA12345"
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
            "taxi/car_list.html"
        )

    def test_context_object_name(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL)
        self.assertIn(
            "car_list",
            response.context
        )

    def test_paginated_by_5(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL)
        self.assertIn("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 5)

        response = self.client.get(LIST_VIEW_URL + "?page=2")
        self.assertEqual(len(response.context["car_list"]), 3)

    def test_model(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL)

        for car in response.context["car_list"]:
            self.assertIsInstance(car, Car)

    def test_search_form_in_context(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL)

        self.assertIsInstance(
            response.context["search_form"],
            CarSearchForm
        )

    def test_search_form_use_apply_name_param(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL + "?model=4")

        self.assertEqual(
            response.context["search_form"].initial["model"],
            "4"
        )

        self.assertEqual(
            len(response.context["car_list"]),
            1
        )
        self.assertContains(
            response,
            "Car 4"
        )

    def test_search_form_check_for_contains(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL + "?model=AR")

        self.assertEqual(
            response.context["page_obj"].paginator.count,
            Car.objects.filter(model__icontains="AR").count()
        )

    def test_has_detail_anchors(self):
        cars = Car.objects.all()[:5]
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL)

        for car in cars:
            detail_url = reverse("taxi:car-detail", args=[car.id])
            self.assertContains(
                response,
                f'href="{detail_url}"'
            )

    def test_returns_nothing_for_bad_search(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(LIST_VIEW_URL + "?model=bad_search_param")

        self.assertEqual(
            response.context["page_obj"].paginator.count,
            0
        )
        self.assertEqual(
            len(response.context["car_list"]),
            0
        )


CREATE_VIEW_URL = reverse("taxi:car-create")


class CarCreateViewTest(TestCase):
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
            "taxi/car_form.html"
        )

    def test_creates_new_object(self):
        driver = Driver.objects.get(pk=1)
        self.client.force_login(driver)
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer 1",
            country="Country 1"
        )

        car_data = {
            "model": "Car 1",
            "manufacturer": manufacturer.id,
            "drivers": [driver.id]
        }
        response = self.client.post(
            CREATE_VIEW_URL,
            car_data
        )
        self.assertRedirects(response, reverse("taxi:car-list"))

        cars = list(
            Car.objects.filter(
                model=car_data["model"]
            ).values("model", "manufacturer_id", "drivers")
        )

        self.assertEqual(
            cars,
            [{
                "model": car_data["model"],
                "manufacturer_id": manufacturer.id,
                "drivers": driver.pk
            }]
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
                "model": ["This field is required."],
                "manufacturer": ["This field is required."],
                "drivers": ["This field is required."]
            }
        )


UPDATE_VIEW_URL = reverse(
    "taxi:car-update",
    args=[1]
)


class CarUpdateViewTest(TestCase):
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
            "taxi/car_form.html"
        )

    def test_show_data_from_car(self):
        self.client.force_login(Driver.objects.get(pk=1))
        car = Car.objects.get(pk=1)
        manufacturer_1 = Manufacturer.objects.get(pk=1)
        manufacturer_2 = Manufacturer.objects.get(pk=2)

        response = self.client.get(
            UPDATE_VIEW_URL
        )

        self.assertContains(
            response,
            f'value="{car.model}"'
        )

        self.assertContains(
            response,
            f'<option value="{manufacturer_1.id}" selected>'
        )
        self.assertContains(
            response,
            f'<option value="{manufacturer_2.id}">'
        )
        self.assertContains(
            response,
            f'name="drivers" value="{CarUpdateViewTest.drivers[0].id}"  '
            f'id="id_drivers_0" checked'
        )
        self.assertContains(
            response,
            f'name="drivers" value="{CarUpdateViewTest.drivers[1].id}"  '
            f'id="id_drivers_1"\n>'
        )

    def test_updates_object(self):
        self.client.force_login(Driver.objects.get(pk=1))

        cars_before = [{
            **car,
            "drivers": [car["drivers"]]
        } for car in list(
            Car.objects.all().values("model", "manufacturer", "drivers")
        )]

        cars_before[0]["model"] = "Car 3"
        cars_before[0]["drivers"] = [CarUpdateViewTest.drivers[1].id]

        response = self.client.post(
            UPDATE_VIEW_URL,
            cars_before[0]
        )
        self.assertRedirects(response, LIST_VIEW_URL)

        cars_after = [{
            **car,
            "drivers": [car["drivers"]]
        } for car in list(
            Car.objects.all().values("model", "manufacturer", "drivers")
        )]

        self.assertEqual(
            cars_after,
            cars_before
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
                "model": ["This field is required."],
                "manufacturer": ["This field is required."],
                "drivers": ["This field is required."]
            }
        )


DELETE_VIEW_URL = reverse(
    "taxi:car-delete",
    args=[1]
)


class CarDeleteViewTest(TestCase):
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
            "taxi/car_confirm_delete.html"
        )

    def test_deletes_only_selected_car(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.post(
            DELETE_VIEW_URL
        )

        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertEqual(Car.objects.filter(pk=1).count(), 0)
        self.assertEqual(Car.objects.count(), 1)

    def test_show_404_for_invalid_id(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(
            reverse("taxi:car-delete", args=[123])
        )

        self.assertEqual(response.status_code, 404)


DETAIL_VIEW_URL = reverse("taxi:car-detail", args=[1])


class CarDetailsViewTest(TestCase):
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
            "taxi/car_detail.html"
        )

    def test_show_404_for_invalid_id(self):
        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(
            reverse("taxi:car-detail", args=[123])
        )

        self.assertEqual(response.status_code, 404)

    def test_assign_unassign_driver(self):
        driver = Driver.objects.get(pk=2)
        car = Car.objects.get(pk=1)

        self.client.force_login(driver)
        response = self.client.get(DETAIL_VIEW_URL)

        toggle_assign_url = reverse(
            "taxi:toggle-car-assign",
            args=[car.id]
        )

        self.assertContains(
            response,
            "Assign me from this car",
        )
        self.assertContains(
            response,
            f'href="{toggle_assign_url}"'
        )

        response = self.client.get(toggle_assign_url)

        self.assertRedirects(
            response,
            DETAIL_VIEW_URL
        )

        response = self.client.get(DETAIL_VIEW_URL)

        self.assertContains(
            response,
            "Delete me from this car",
        )
        self.assertContains(
            response,
            f'href="{toggle_assign_url}"'
        )

        response = self.client.get(toggle_assign_url)

        self.assertRedirects(
            response,
            DETAIL_VIEW_URL
        )

        response = self.client.get(DETAIL_VIEW_URL)

        self.assertContains(
            response,
            "Assign me from this car",
        )
        self.assertContains(
            response,
            f'href="{toggle_assign_url}"'
        )

    def test_contains_car_manufacture_name(self):
        driver = Driver.objects.get(pk=1)
        car = Car.objects.get(pk=1)

        self.client.force_login(driver)
        response = self.client.get(DETAIL_VIEW_URL)

        self.assertContains(
            response,
            car.manufacturer.name
        )

    def test_contains_car_drivers(self):
        driver = Driver.objects.get(pk=1)
        car = Car.objects.get(pk=1)
        car.drivers.add(*CarDetailsViewTest.drivers)

        self.client.force_login(driver)
        response = self.client.get(DETAIL_VIEW_URL)

        for driver in car.drivers.all():
            self.assertContains(
                response,
                f"{driver.username} "
                f"({driver.first_name} {driver.last_name})"
            )

    def test_has_update_and_delete_anchors(self):
        car = Car.objects.get(pk=1)

        self.client.force_login(Driver.objects.get(pk=1))
        response = self.client.get(DETAIL_VIEW_URL)

        update_url = reverse(
            "taxi:car-update",
            args=[car.id]
        )

        self.assertContains(
            response,
            f'href="{update_url}"'
        )

        delete_url = reverse(
            "taxi:car-delete",
            args=[car.id]
        )

        self.assertContains(
            response,
            f'href="{delete_url}"'
        )
