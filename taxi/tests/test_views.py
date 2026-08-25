from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    CarModelSearchForm,
    DriverUsernameSearchForm,
    ManufacturerNameSearchForm,
)
from taxi.models import Car, Driver, Manufacturer


class BaseViewTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.driver = Driver.objects.create_user(
            username="test_driver",
            password="password123",
            license_number="ABC12345",
        )
        cls.driver_to_change = Driver.objects.create_user(
            username="driver_to_change",
            password="password123",
            license_number="XYZ12345",
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        cls.car = Car.objects.create(
            model="Audi A4",
            manufacturer=cls.manufacturer
        )

    def setUp(self):
        self.client.force_login(self.driver)


class LoginRequiredTests(BaseViewTests):
    def test_login_required_for_all_views(self):
        urls = [
            reverse("taxi:index"),
            reverse("taxi:manufacturer-list"),
            reverse("taxi:manufacturer-create"),
            reverse("taxi:manufacturer-update", kwargs={"pk": self.manufacturer.pk}),
            reverse("taxi:manufacturer-delete", kwargs={"pk": self.manufacturer.pk}),
            reverse("taxi:car-list"),
            reverse("taxi:car-detail", kwargs={"pk": self.car.pk}),
            reverse("taxi:car-create"),
            reverse("taxi:car-update", kwargs={"pk": self.car.pk}),
            reverse("taxi:car-delete", kwargs={"pk": self.car.pk}),
            reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk}),
            reverse("taxi:driver-list"),
            reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk}),
            reverse("taxi:driver-create"),
            reverse("taxi:driver-update", kwargs={"pk": self.driver.pk}),
            reverse("taxi:driver-delete", kwargs={"pk": self.driver.pk}),
        ]
        self.client.logout()

        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(
                response,
                f"{reverse('login')}?next={url}"
            )


class IndexViewTests(BaseViewTests):
    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")
        self.assertEqual(response.context["num_drivers"], 2)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)
        self.assertEqual(response.context["num_visits"], 1)

    def test_index_increases_number_of_visits(self):
        self.client.get(reverse("taxi:index"))
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.context["num_visits"], 2)


class ListAndDetailViewTests(BaseViewTests):
    def test_manufacturer_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            [self.manufacturer]
        )
        self.assertIsInstance(
            response.context["search_form"],
            ManufacturerNameSearchForm
        )

    def test_car_list_view(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertEqual(list(response.context["car_list"]), [self.car])
        self.assertIsInstance(
            response.context["search_form"],
            CarModelSearchForm
        )

    def test_car_detail_view(self):
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": self.car.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
        self.assertEqual(response.context["car"], self.car)

    def test_driver_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertEqual(
            set(response.context["driver_list"]),
            {self.driver, self.driver_to_change}
        )
        self.assertIsInstance(
            response.context["search_form"],
            DriverUsernameSearchForm
        )

    def test_driver_detail_view(self):
        response = self.client.get(
            reverse(
                "taxi:driver-detail",
                kwargs={"pk": self.driver_to_change.pk}
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
        self.assertEqual(response.context["driver"], self.driver_to_change)


class ManufacturerCrudViewTests(BaseViewTests):
    def test_manufacturer_create_view_get(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_manufacturer_create_view_post(self):
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            {"name": "Toyota", "country": "Japan"}
        )

        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertTrue(
            Manufacturer.objects.filter(name="Toyota", country="Japan").exists()
        )

    def test_manufacturer_update_view_get(self):
        response = self.client.get(
            reverse("taxi:manufacturer-update", kwargs={"pk": self.manufacturer.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")
        self.assertEqual(response.context["object"], self.manufacturer)

    def test_manufacturer_update_view_post(self):
        response = self.client.post(
            reverse("taxi:manufacturer-update", kwargs={"pk": self.manufacturer.pk}),
            {"name": "Audi updated", "country": "Germany updated"}
        )
        self.manufacturer.refresh_from_db()

        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertEqual(self.manufacturer.name, "Audi updated")
        self.assertEqual(self.manufacturer.country, "Germany updated")

    def test_manufacturer_delete_view_get(self):
        response = self.client.get(
            reverse("taxi:manufacturer-delete", kwargs={"pk": self.manufacturer.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_confirm_delete.html")
        self.assertTrue(Manufacturer.objects.filter(pk=self.manufacturer.pk).exists())

    def test_manufacturer_delete_view_post(self):
        response = self.client.post(
            reverse("taxi:manufacturer-delete", kwargs={"pk": self.manufacturer.pk})
        )

        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertFalse(Manufacturer.objects.filter(pk=self.manufacturer.pk).exists())


class CarCrudViewTests(BaseViewTests):
    def test_car_create_view_get(self):
        response = self.client.get(reverse("taxi:car-create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_car_create_view_post(self):
        response = self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "BMW X5",
                "manufacturer": self.manufacturer.pk,
                "drivers": [self.driver.pk]
            }
        )

        self.assertRedirects(response, reverse("taxi:car-list"))
        car = Car.objects.get(model="BMW X5")
        self.assertEqual(car.manufacturer, self.manufacturer)
        self.assertIn(self.driver, car.drivers.all())

    def test_car_update_view_get(self):
        response = self.client.get(
            reverse("taxi:car-update", kwargs={"pk": self.car.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")
        self.assertEqual(response.context["object"], self.car)

    def test_car_update_view_post(self):
        response = self.client.post(
            reverse("taxi:car-update", kwargs={"pk": self.car.pk}),
            {
                "model": "Audi A6",
                "manufacturer": self.manufacturer.pk,
                "drivers": [self.driver.pk]
            }
        )
        self.car.refresh_from_db()

        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertEqual(self.car.model, "Audi A6")
        self.assertIn(self.driver, self.car.drivers.all())

    def test_car_delete_view_get(self):
        response = self.client.get(
            reverse("taxi:car-delete", kwargs={"pk": self.car.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_confirm_delete.html")
        self.assertTrue(Car.objects.filter(pk=self.car.pk).exists())

    def test_car_delete_view_post(self):
        response = self.client.post(
            reverse("taxi:car-delete", kwargs={"pk": self.car.pk})
        )

        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertFalse(Car.objects.filter(pk=self.car.pk).exists())


class DriverCrudViewTests(BaseViewTests):
    def test_driver_create_view_get(self):
        response = self.client.get(reverse("taxi:driver-create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_driver_create_view_post(self):
        response = self.client.post(
            reverse("taxi:driver-create"),
            {
                "username": "new_driver",
                "password1": "StrongPassword123",
                "password2": "StrongPassword123",
                "license_number": "QWE12345",
                "first_name": "Test first name",
                "last_name": "Test last name"
            }
        )

        driver = Driver.objects.get(username="new_driver")
        self.assertRedirects(
            response,
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        )
        self.assertEqual(driver.license_number, "QWE12345")
        self.assertTrue(driver.check_password("StrongPassword123"))

    def test_driver_update_view_get(self):
        response = self.client.get(
            reverse("taxi:driver-update", kwargs={"pk": self.driver_to_change.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")
        self.assertEqual(response.context["object"], self.driver_to_change)

    def test_driver_update_view_post(self):
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.driver_to_change.pk}),
            {"license_number": "NEW12345"}
        )
        self.driver_to_change.refresh_from_db()

        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.assertEqual(self.driver_to_change.license_number, "NEW12345")

    def test_driver_delete_view_get(self):
        response = self.client.get(
            reverse("taxi:driver-delete", kwargs={"pk": self.driver_to_change.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_confirm_delete.html")
        self.assertTrue(Driver.objects.filter(pk=self.driver_to_change.pk).exists())

    def test_driver_delete_view_post(self):
        response = self.client.post(
            reverse("taxi:driver-delete", kwargs={"pk": self.driver_to_change.pk})
        )

        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.assertFalse(Driver.objects.filter(pk=self.driver_to_change.pk).exists())


class ToggleAssignToCarViewTests(BaseViewTests):
    def test_get_method_is_not_allowed(self):
        response = self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})
        )

        self.assertEqual(response.status_code, 405)
        self.assertNotIn(self.driver, self.car.drivers.all())

    def test_post_assigns_driver_to_car(self):
        response = self.client.post(
            reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})
        )

        self.assertRedirects(
            response,
            reverse("taxi:car-detail", kwargs={"pk": self.car.pk})
        )
        self.assertIn(self.driver, self.car.drivers.all())

    def test_post_removes_driver_from_car(self):
        self.car.drivers.add(self.driver)

        response = self.client.post(
            reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})
        )

        self.assertRedirects(
            response,
            reverse("taxi:car-detail", kwargs={"pk": self.car.pk})
        )
        self.assertNotIn(self.driver, self.car.drivers.all())


class DriverSearchTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.driver1 = Driver.objects.create_user(
            username="john_driver",
            password="password123",
            license_number="ABC12345",
        )
        cls.driver2 = Driver.objects.create_user(
            username="peter_driver",
            password="password123",
            license_number="XYZ12345",
        )

    def setUp(self):
        self.client.force_login(self.driver1)

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_driver")
        self.assertNotContains(response, "peter_driver")
        self.assertEqual(
            response.context["search_form"].initial["username"],
            "john"
        )


class CarSearchTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.driver = Driver.objects.create_user(
            username="test_driver",
            password="password123",
            license_number="ABC12345",
        )
        manufacturer = Manufacturer.objects.create(
            name="Test manufacturer",
            country="Test country"
        )
        cls.car1 = Car.objects.create(model="Audi A4", manufacturer=manufacturer)
        cls.car2 = Car.objects.create(model="BMW X5", manufacturer=manufacturer)

    def setUp(self):
        self.client.force_login(self.driver)

    def test_search_car_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "audi"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Audi A4")
        self.assertNotContains(response, "BMW X5")
        self.assertEqual(
            response.context["search_form"].initial["model"],
            "audi"
        )


class ManufacturerSearchTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.driver = Driver.objects.create_user(
            username="test_driver",
            password="password123",
            license_number="ABC12345",
        )
        cls.manufacturer1 = Manufacturer.objects.create(name="Audi", country="Germany")
        cls.manufacturer2 = Manufacturer.objects.create(name="Toyota", country="Japan")

    def setUp(self):
        self.client.force_login(self.driver)

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "audi"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Audi")
        self.assertNotContains(response, "Toyota")
        self.assertEqual(
            response.context["search_form"].initial["name"],
            "audi"
        )
