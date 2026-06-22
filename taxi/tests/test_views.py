from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    ManufacturerNameSearchForm,
    CarModelSearchForm,
    DriverUsernameSearchForm
)
from taxi.models import Driver, Car, Manufacturer


class TestIndexView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="qwerty",
            license_number="ABC12345",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertRedirects(response, "/accounts/login/?next=/")

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user == response.context["user"])
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_num_visits(self):
        self.client.login(username="test_user", password="qwerty")
        for _ in range(10):
            self.client.get(reverse("taxi:index"))
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_visits"], 11)

    def test_num_drivers(self):
        self.client.login(username="test_user", password="qwerty")
        for i in range(5):
            Driver.objects.create_user(
                username=f"test_user{i}",
                password="qwerty",
                license_number=f"ABC1234{i}",
            )
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_drivers"], 6)

    def test_num_cars(self):
        self.client.login(username="test_user", password="qwerty")

        manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="USA"
        )
        for i in range(5):
            Car.objects.create(
                model=f"test_car{i}",
                manufacturer=manufacturer,
            )
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_cars"], 5)

    def test_num_manufacturers(self):
        self.client.login(username="test_user", password="qwerty")
        for i in range(5):
            Manufacturer.objects.create(
                name=f"Manufacturer_{i}",
                country="USA"
            )
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_manufacturers"], 5)


class TestManufacturerListView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="qwerty",
            license_number="ABC12345",
        )

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="Toyota Motors", country="Japan")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertRedirects(response, "/accounts/login/?next=/manufacturers/")

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user == response.context["user"])
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_get_queryset_filter_by_name(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Toy"},
        )
        manufacturers = response.context["manufacturer_list"]
        form: ManufacturerNameSearchForm = response.context["search_form"]

        self.assertEqual(len(manufacturers), 2)
        self.assertQuerySetEqual(
            manufacturers,
            Manufacturer.objects.filter(name__icontains="Toy"),
        )
        self.assertIsInstance(form, ManufacturerNameSearchForm)
        self.assertEqual(form.initial["name"], "Toy")

    def test_search_form_in_context(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Toy"}
        )

        self.assertIn("search_form", response.context)
        self.assertEqual(
            response.context["search_form"].initial["name"],
            "Toy"
        )


class TestManufacturerCreateView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="qwerty",
            license_number="ABC12345",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertRedirects(
            response, "/accounts/login/?next=/manufacturers/create/")

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(reverse("taxi:manufacturer-create"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user == response.context["user"])
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_create_manufacturer(self):
        self.client.login(username="test_user", password="qwerty")
        form_data = {
            "name": "Toyota",
            "country": "Japan",
        }

        self.client.post(reverse("taxi:manufacturer-create"), form_data)

        self.assertTrue(
            Manufacturer.objects.filter(name="Toyota").exists()
        )

    def test_create_manufacturer_redirect(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            {
                "name": "Toyota",
                "country": "Japan",
            },
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))

    def test_create_view_get_contains_form(self):
        self.client.login(username="test_user", password="qwerty")

        response = self.client.get(reverse("taxi:manufacturer-create"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_create_manufacturer_invalid_data(self):
        self.client.login(username="test_user", password="qwerty")

        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            {
                "name": "",
                "country": "Japan",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "name", "This field is required."
        )


class TestManufacturerUpdateView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="qwerty",
            license_number="ABC12345",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

    def test_redirect_if_not_logged_in(self):
        manufacturer_id = self.manufacturer.id
        response = self.client.get(reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": manufacturer_id}
        ))
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/manufacturers/{manufacturer_id}/update/"
        )

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": self.manufacturer.id}
        ))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user == response.context["user"])
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_update_manufacturer(self):
        self.client.login(username="test_user", password="qwerty")
        form_data = {
            "name": "Toyota_changed",
            "country": "Japan_changed",
        }

        self.client.post(
            reverse(
                "taxi:manufacturer-update",
                kwargs={"pk": self.manufacturer.id}),
            form_data
        )
        self.manufacturer.refresh_from_db()
        self.assertTrue(self.manufacturer.name == "Toyota_changed")
        self.assertTrue(self.manufacturer.country == "Japan_changed")

    def test_update_manufacturer_redirect(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.post(
            reverse(
                "taxi:manufacturer-update",
                kwargs={"pk": self.manufacturer.id}),
            {
                "name": "Toyota_changed",
                "country": "Japan_changed",
            },
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))

    def test_update_view_get_contains_filled_form(self):
        self.client.login(username="test_user", password="qwerty")

        response = self.client.get(reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": self.manufacturer.id}))

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertEqual(
            response.context["form"].initial["name"],
            self.manufacturer.name
        )
        self.assertEqual(
            response.context["form"].initial["country"],
            self.manufacturer.country
        )

    def test_update_manufacturer_invalid_data(self):
        self.client.login(username="test_user", password="qwerty")
        form_data = {
            "name": "",
            "country": "Japan_changed",
        }

        response = self.client.post(
            reverse(
                "taxi:manufacturer-update",
                kwargs={"pk": self.manufacturer.id}),
            form_data
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "name",
            "This field is required."
        )


class TestManufacturerDeleteView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="qwerty",
            license_number="ABC12345",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

    def test_redirect_if_not_logged_in(self):
        manufacturer_id = self.manufacturer.id
        response = self.client.get(reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": manufacturer_id}
        ))
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/manufacturers/{manufacturer_id}/delete/"
        )

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": self.manufacturer.id}
        ))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user == response.context["user"])
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_confirm_delete.html"
        )

    def test_delete_manufacturer(self):
        self.client.login(username="test_user", password="qwerty")
        manufacturer_id = self.manufacturer.id
        self.client.post(
            reverse(
                "taxi:manufacturer-delete",
                kwargs={"pk": manufacturer_id}),
        )
        self.assertEqual(
            len(Manufacturer.objects.filter(id=manufacturer_id)),
            0
        )

    def test_delete_manufacturer_redirect(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.post(
            reverse(
                "taxi:manufacturer-delete",
                kwargs={"pk": self.manufacturer.id}),
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))


class TestCarListView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="qwerty",
            license_number="ABC12345",
        )

        self.manufacturer = Manufacturer.objects.create(name="Toyota",
                                                        country="Japan")
        for i in range(3):
            Car.objects.create(model=f"Corolla_{i}",
                               manufacturer=self.manufacturer)
        Car.objects.create(model="Supra", manufacturer=self.manufacturer)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertRedirects(response, "/accounts/login/?next=/cars/")

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user == response.context["user"])
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_get_queryset_filter_by_model(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Cor"},
        )
        cars = response.context["car_list"]
        form = response.context["search_form"]

        self.assertEqual(len(cars), 3)
        self.assertQuerySetEqual(
            cars,
            Car.objects.filter(model__icontains="Cor"),
            ordered=False
        )
        self.assertIsInstance(form, CarModelSearchForm)
        self.assertEqual(form.initial["model"], "Cor")

    def test_search_form_in_context(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Cor"}
        )

        self.assertIn("search_form", response.context)
        self.assertEqual(
            response.context["search_form"].initial["model"],
            "Cor"
        )


class TestCarDetailView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="qwerty",
            license_number="ABC12345",
        )

        self.manufacturer = Manufacturer.objects.create(name="Toyota",
                                                        country="Japan")
        self.car = Car.objects.create(model="Corolla",
                                      manufacturer=self.manufacturer)
        self.car.drivers.add(self.user)

    def test_redirect_if_not_logged_in(self):
        car_id = self.car.id
        response = self.client.get(reverse(
            "taxi:car-detail",
            kwargs={"pk": car_id}
        ))
        self.assertRedirects(response,
                             f"/accounts/login/?next=/cars/{car_id}/")

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(reverse(
            "taxi:car-detail",
            kwargs={"pk": self.car.id}
        ))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user == response.context["user"])
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_response_contains_manufacturer(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(reverse(
            "taxi:car-detail",
            kwargs={"pk": self.car.id}
        ))
        self.assertContains(response, self.manufacturer.name)
        self.assertContains(response, self.manufacturer.country)

    def test_response_contains_drivers(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(reverse(
            "taxi:car-detail",
            kwargs={"pk": self.car.id}
        ))
        self.assertContains(response, self.car.drivers.first().first_name)
        self.assertContains(response, self.car.drivers.first().last_name)
        self.assertContains(response, self.car.drivers.first().username)


class TestCarCreateView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="qwerty",
            license_number="ABC12345",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertRedirects(response, "/accounts/login/?next=/cars/create/")

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(reverse("taxi:car-create"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user == response.context["user"])
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_create_car(self):
        self.client.login(username="test_user", password="qwerty")
        form_data = {
            "model": "Corolla",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id],
        }

        self.client.post(reverse("taxi:car-create"), form_data)
        self.assertTrue(
            Car.objects.filter(model="Corolla").exists()
        )

    def test_create_car_redirect(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "Corolla",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            },
        )
        self.assertRedirects(response, reverse("taxi:car-list"))

    def test_create_view_get_contains_form(self):
        self.client.login(username="test_user", password="qwerty")

        response = self.client.get(reverse("taxi:car-create"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_create_car_invalid_data(self):
        self.client.login(username="test_user", password="qwerty")

        response = self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "model",
            "This field is required."
        )


class TestCarUpdateView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="qwerty",
            license_number="ABC12345",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.user)

    def test_redirect_if_not_logged_in(self):
        car_id = self.car.id
        response = self.client.get(reverse(
            "taxi:car-update",
            kwargs={"pk": car_id}
        ))
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/cars/{car_id}/update/"
        )

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(reverse(
            "taxi:car-update",
            kwargs={"pk": self.car.id}
        ))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user == response.context["user"])
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_update_car(self):
        self.client.login(username="test_user", password="qwerty")
        manufacturer2 = Manufacturer.objects.create(
            name="Toyota2",
            country="Japan"
        )
        driver2 = get_user_model().objects.create_user(
            "test_user2",
            password="qwerty",
            license_number="ABC12346",
        )
        form_data = {
            "model": "Corolla_changed",
            "manufacturer": manufacturer2.id,
            "drivers": [self.user.id, driver2.id],
        }

        self.client.post(
            reverse(
                "taxi:car-update",
                kwargs={"pk": self.car.id}),
            form_data
        )
        self.car.refresh_from_db()
        self.assertTrue(self.car.model == "Corolla_changed")
        self.assertTrue(self.car.manufacturer == manufacturer2)
        self.assertTrue(list(self.car.drivers.all()) == [self.user, driver2])

    def test_update_car_redirect(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.post(
            reverse(
                "taxi:car-update",
                kwargs={"pk": self.car.id}),
            {
                "model": "Corolla_changed",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            },
        )
        self.assertRedirects(response, reverse("taxi:car-list"))

    def test_update_view_get_contains_filled_form(self):
        self.client.login(username="test_user", password="qwerty")

        response = self.client.get(reverse(
            "taxi:car-update",
            kwargs={"pk": self.car.id}))

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertEqual(
            response.context["form"].initial["model"],
            self.car.model
        )
        self.assertEqual(
            response.context["form"].initial["manufacturer"],
            self.car.manufacturer.id
        )
        self.assertEqual(
            response.context["form"].initial["drivers"],
            list(self.car.drivers.all())
        )

    def test_update_car_invalid_data(self):
        self.client.login(username="test_user", password="qwerty")
        form_data = {
            "model": "",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id],
        }

        response = self.client.post(
            reverse(
                "taxi:car-update",
                kwargs={"pk": self.car.id}),
            form_data
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "model",
            "This field is required."
        )


class TestCarDeleteView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="qwerty",
            license_number="ABC12345",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer,
        )

    def test_redirect_if_not_logged_in(self):
        car_id = self.car.id
        response = self.client.get(reverse(
            "taxi:car-delete",
            kwargs={"pk": car_id}
        ))
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/cars/{car_id}/delete/"
        )

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(reverse(
            "taxi:car-delete",
            kwargs={"pk": self.car.id}
        ))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user == response.context["user"])
        self.assertTemplateUsed(response, "taxi/car_confirm_delete.html")

    def test_delete_car(self):
        self.client.login(username="test_user", password="qwerty")
        car_id = self.car.id
        self.client.post(
            reverse(
                "taxi:car-delete",
                kwargs={"pk": car_id}),
        )
        self.assertEqual(len(Car.objects.filter(id=car_id)), 0)

    def test_delete_car_redirect(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.post(
            reverse(
                "taxi:car-delete",
                kwargs={"pk": self.car.id}),
        )
        self.assertRedirects(response, reverse("taxi:car-list"))


class TestDriverListView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="qwerty",
            license_number="ABC12345",
        )

        for i in range(3):
            get_user_model().objects.create_user(
                username=f"test_user{i}",
                password="qwerty",
                license_number=f"ABB1234{i}",
            )
        get_user_model().objects.create_user(
            username="different_user",
            password="qwerty",
            license_number="ABB43213",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertRedirects(response, "/accounts/login/?next=/drivers/")

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user == response.context["user"])
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_get_queryset_filter_by_username(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "test"},
        )
        drivers = response.context["driver_list"]
        form = response.context["search_form"]

        self.assertEqual(len(drivers), 4)
        self.assertQuerySetEqual(
            drivers,
            get_user_model().objects.filter(username__icontains="test"),
            ordered=False
        )
        self.assertIsInstance(form, DriverUsernameSearchForm)
        self.assertEqual(form.initial["username"], "test")

    def test_search_form_in_context(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "test"}
        )

        self.assertIn("search_form", response.context)
        self.assertEqual(
            response.context["search_form"].initial["username"],
            "test"
        )


class TestDriverDetailView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="qwerty",
            license_number="ABC12345",
        )

    def test_redirect_if_not_logged_in(self):
        driver_id = self.user.id
        response = self.client.get(reverse(
            "taxi:driver-detail",
            kwargs={"pk": driver_id}
        ))
        self.assertRedirects(response,
                             f"/accounts/login/?next=/drivers/{driver_id}/")

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.user.id}
        ))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user == response.context["user"])
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_response_contains_driver(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.user.id}
        ))
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)

    def test_response_contains_cars(self):
        self.client.login(username="test_user", password="qwerty")
        self.user.cars.add(
            Car.objects.create(
                model="Corolla",
                manufacturer=Manufacturer.objects.create(
                    name="Toyota",
                    country="Japan",
                )
            )
        )
        response = self.client.get(reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.user.id}
        ))
        self.user.refresh_from_db()
        self.assertContains(response, self.user.cars.first().model)
        self.assertContains(response, self.user.cars.first().manufacturer.name)


class TestDriverCreateView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="qwerty",
            license_number="ABC12345",
        )
        self.manufacturer = Manufacturer.objects.create(name="Toyota",
                                                        country="Japan")
        self.car = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertRedirects(response,
                             "/accounts/login/?next=/drivers/create/")

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(reverse("taxi:driver-create"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user == response.context["user"])
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_create_driver(self):
        self.client.login(username="test_user", password="qwerty")
        form_data = {
            "username": "test_driver",
            "password1": "aghJ764Y",
            "password2": "aghJ764Y",
            "license_number": "QWE54321",
        }

        self.client.post(reverse("taxi:driver-create"), form_data)
        self.assertTrue(
            get_user_model().objects.filter(username="test_driver").exists()
        )

    def test_create_driver_redirect(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.post(
            reverse("taxi:driver-create"),
            {
                "username": "test_driver",
                "password1": "aghJ764Y",
                "password2": "aghJ764Y",
                "license_number": "QWE54321",
            },
        )
        self.assertRedirects(response, reverse("taxi:driver-list") + "2/")

    def test_create_view_get_contains_form(self):
        self.client.login(username="test_user", password="qwerty")

        response = self.client.get(reverse("taxi:driver-create"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_create_driver_invalid_data(self):
        self.client.login(username="test_user", password="qwerty")

        response = self.client.post(
            reverse("taxi:driver-create"),
            {
                "username": "",
                "password1": "aghJ764Y",
                "password2": "aghJ764Y",
                "license_number": "QWE54321",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "username",
            "This field is required."
        )


class TestDriverLicenseUpdateView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="qwerty",
            license_number="ABC12345",
        )

    def test_redirect_if_not_logged_in(self):
        driver_id = self.user.id
        response = self.client.get(reverse(
            "taxi:driver-update",
            kwargs={"pk": driver_id}
        ))
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/drivers/{driver_id}/update/"
        )

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(reverse(
            "taxi:driver-update",
            kwargs={"pk": self.user.id}
        ))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user == response.context["user"])
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_update_driver_license(self):
        self.client.login(username="test_user", password="qwerty")
        form_data = {
            "license_number": "QWE54321",
        }

        self.client.post(
            reverse(
                "taxi:driver-update",
                kwargs={"pk": self.user.id}),
            form_data
        )
        self.user.refresh_from_db()
        self.assertTrue(self.user.license_number == "QWE54321")

    def test_update_driver_license_redirect(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.post(
            reverse(
                "taxi:driver-update",
                kwargs={"pk": self.user.id}),
            {
                "license_number": "QWE54321",
            },
        )
        self.assertRedirects(response, reverse("taxi:driver-list"))

    def test_update_view_get_contains_filled_form(self):
        self.client.login(username="test_user", password="qwerty")

        response = self.client.get(reverse(
            "taxi:driver-update",
            kwargs={"pk": self.user.id}))

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertEqual(
            response.context["form"].initial["license_number"],
            self.user.license_number
        )

    def test_update_driver_license_number_invalid_data(self):
        self.client.login(username="test_user", password="qwerty")
        form_data = {
            "license_number": "",
        }

        response = self.client.post(
            reverse(
                "taxi:driver-update",
                kwargs={"pk": self.user.id}),
            form_data
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "license_number",
            "This field is required."
        )


class TestDriverDeleteView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="qwerty",
            license_number="ABC12345",
        )
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="qwerty",
            license_number="QWE12345",
        )

    def test_redirect_if_not_logged_in(self):
        driver_id = self.driver.id
        response = self.client.get(reverse(
            "taxi:driver-delete",
            kwargs={"pk": driver_id}
        ))
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/drivers/{driver_id}/delete/"
        )

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.get(reverse(
            "taxi:driver-delete",
            kwargs={"pk": self.driver.id}
        ))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user == response.context["user"])
        self.assertTemplateUsed(response, "taxi/driver_confirm_delete.html")

    def test_delete_driver(self):
        self.client.login(username="test_user", password="qwerty")
        driver_id = self.driver.id
        self.client.post(
            reverse(
                "taxi:driver-delete",
                kwargs={"pk": self.driver.id}),
        )
        self.assertFalse(
            get_user_model().objects.filter(id=driver_id).exists()
        )

    def test_delete_driver_redirect(self):
        self.client.login(username="test_user", password="qwerty")
        response = self.client.post(
            reverse(
                "taxi:driver-delete",
                kwargs={"pk": self.driver.id}),
        )
        self.assertRedirects(response, reverse("taxi:driver-list"))
