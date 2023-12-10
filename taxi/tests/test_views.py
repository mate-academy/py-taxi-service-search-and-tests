from typing import List

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    @classmethod
    def setUpTestData(cls):
        number_of_manufacturers = 13

        for manufacturer_id in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name=f"manufacturer_{manufacturer_id}",
                country=f"country_{manufacturer_id}"
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/manufacturers/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_redirect_if_user_is_guest(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_pagination_is_5(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_lists_last_page_manufacturers(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?page=3"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 3)

    def test_lists_with_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?search=manufacturer_0"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form_search" in response.context)
        self.assertEqual(
            response.context["form_search"].initial.get("search"),
            "manufacturer_0"
        )
        self.assertEqual(len(response.context["manufacturer_list"]), 1)

    def test_lists_with_search_by_country(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?search=country_0"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form_search" in response.context)
        self.assertEqual(
            response.context["form_search"].initial.get("search"),
            "country_0"
        )
        self.assertEqual(len(response.context["manufacturer_list"]), 1)


class ManufacturerCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/manufacturers/create/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertEqual(response.status_code, 200)

    def test_view_redirect_if_user_is_guest(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_create_valid_new_manufacturer(self):
        data = {
            "name": "Manufacturer_new",
            "country": "Country_new"
        }
        response = self.client.post(reverse("taxi:manufacturer-create"), data)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))

    def test_create_invalid_new_manufacturer(self):
        data = {
            "name": "",
            "country": ""
        }
        response = self.client.post(reverse("taxi:manufacturer-create"), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "name",
            "This field is required."
        )
        self.assertFormError(
            response.context["form"],
            "country",
            "This field is required."
        )


class ManufacturerUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(
            name=f"manufacturer_1",
            country=f"country_1"
        )

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/manufacturers/1/update/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-update", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)

    def test_view_redirect_if_user_is_guest(self):
        self.client.logout()
        response = self.client.get(
            reverse("taxi:manufacturer-update", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        response = self.client.get(
            reverse("taxi:manufacturer-update", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_update_valid_manufacturer(self):
        data = {
            "name": "Manufacturer_new",
            "country": "Country_new"
        }
        response = self.client.post(
            reverse("taxi:manufacturer-update", kwargs={"pk": 1}),
            data
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))

    def test_update_invalid_manufacturer(self):
        data = {
            "name": "",
            "country": ""
        }
        response = self.client.post(
            reverse("taxi:manufacturer-update", kwargs={"pk": 1}),
            data
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "name",
            "This field is required."
        )
        self.assertFormError(
            response.context["form"],
            "country",
            "This field is required."
        )


class ManufacturerDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(
            name=f"manufacturer_1",
            country=f"country_1"
        )

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/manufacturers/1/delete/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-delete", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)

    def test_view_redirect_if_user_is_guest(self):
        self.client.logout()
        response = self.client.get(
            reverse("taxi:manufacturer-delete", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        response = self.client.get(
            reverse("taxi:manufacturer-delete", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_confirm_delete.html"
        )

    def test_delete_manufacturer(self):
        response = self.client.post(
            reverse("taxi:manufacturer-delete", kwargs={"pk": 1})
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    @classmethod
    def setUpTestData(cls):
        manufacturers = cls.createManufactures()
        drivers = cls.createDrivers()
        cls.createCars(drivers, manufacturers)

    @staticmethod
    def createManufactures() -> List[Manufacturer]:
        manufacturers = (
            Manufacturer(name="btest", country="btest country"),
            Manufacturer(name="atest", country="atest country")
        )
        Manufacturer.objects.bulk_create(manufacturers)
        return Manufacturer.objects.all()

    @staticmethod
    def createDrivers() -> List[Driver]:
        drivers = (
            Driver(
                first_name="btest_name",
                last_name="btest_last_name",
                username="busername",
                email="btest@gmail.com",
                license_number="FHG17564"
            ),
            Driver(
                first_name="atest_name",
                last_name="atest_last_name",
                username="ausername",
                email="atest@gmail.com",
                license_number="FHG12939"
            )
        )
        Driver.objects.bulk_create(drivers)

        return Driver.objects.all()

    @staticmethod
    def createCars(
        drivers: List[Driver],
        manufacturers: List[Manufacturer],
        number_of_cars: int = 13
    ) -> List[Car]:
        for i in range(number_of_cars):
            car = Car.objects.create(
                model=f"model_{i}",
                manufacturer=manufacturers[i % 2]
            )
            car.drivers.set([drivers[i % 2]])

        return Car.objects.all()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/cars/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_redirect_if_user_is_guest(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_pagination_is_5(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_lists_last_page_cars(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?page=3"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 3)

    def test_lists_with_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?search=model_0"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form_search" in response.context)
        self.assertEqual(
            response.context["form_search"].initial.get("search"),
            "model_0"
        )
        self.assertEqual(len(response.context["car_list"]), 1)

    def test_lists_with_search_by_manufacturer(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?search=atest"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form_search" in response.context)
        self.assertEqual(
            response.context["form_search"].initial.get("search"),
            "atest"
        )
        self.assertEqual(len(response.context["car_list"]), 5)


class CarCreateViewTest(TestCase):
    @staticmethod
    def createManufacturer() -> Manufacturer:
        return Manufacturer.objects.create(
            name="btest",
            country="btest country"
        )

    @staticmethod
    def createDrivers() -> List[Driver]:
        drivers = (
            Driver(
                first_name="btest_name",
                last_name="btest_last_name",
                username="busername",
                email="btest@gmail.com",
                license_number="FHG17564"
            ),
            Driver(
                first_name="atest_name",
                last_name="atest_last_name",
                username="ausername",
                email="atest@gmail.com",
                license_number="FHG12939"
            )
        )
        Driver.objects.bulk_create(drivers)

        return Driver.objects.all()

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/cars/create/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(response.status_code, 200)

    def test_view_redirect_if_user_is_guest(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_create_valid_new_car(self):
        data = {
            "model": "Model_new",
            "manufacturer": self.createManufacturer().pk,
            "drivers": [driver.pk for driver in self.createDrivers()]
        }
        response = self.client.post(reverse("taxi:car-create"), data)
        self.assertRedirects(response, reverse("taxi:car-list"))

    def test_create_invalid_new_car(self):
        data = {
            "model": "",
            "manufacturer": "",
            "drivers": []
        }
        response = self.client.post(reverse("taxi:car-create"), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "model",
            "This field is required."
        )
        self.assertFormError(
            response.context["form"],
            "manufacturer",
            "This field is required."
        )
        self.assertFormError(
            response.context["form"],
            "drivers",
            "This field is required."
        )


class CarUpdateViewTest(TestCase):
    manufacturers: List[Manufacturer]
    drivers: List[Driver]

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    @classmethod
    def setUpTestData(cls):
        cls.drivers = cls.createDrivers()
        cls.manufacturers = cls.createManufacturers()
        cls.createCar([cls.drivers[0]], cls.manufacturers[0])

    @staticmethod
    def createManufacturers() -> List[Manufacturer]:
        manufacturers = (
            Manufacturer(name="btest", country="btest country"),
            Manufacturer(name="atest", country="atest country")
        )
        Manufacturer.objects.bulk_create(manufacturers)
        return Manufacturer.objects.all()

    @staticmethod
    def createDrivers() -> List[Driver]:
        drivers = (
            Driver(
                first_name="btest_name",
                last_name="btest_last_name",
                username="busername",
                email="btest@gmail.com",
                license_number="FHG17564"
            ),
            Driver(
                first_name="atest_name",
                last_name="atest_last_name",
                username="ausername",
                email="atest@gmail.com",
                license_number="FHG12939"
            )
        )
        Driver.objects.bulk_create(drivers)

        return Driver.objects.all()

    @staticmethod
    def createCar(
        drivers: List[Driver],
        manufacturer: Manufacturer,
    ) -> Car:
        car = Car.objects.create(
            model=f"model_0",
            manufacturer=manufacturer
        )
        car.drivers.set(drivers)

        return car

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/cars/1/update/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(
            reverse("taxi:car-update", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)

    def test_view_redirect_if_user_is_guest(self):
        self.client.logout()
        response = self.client.get(
            reverse("taxi:car-update", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        response = self.client.get(
            reverse("taxi:car-update", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_update_valid_car(self):
        data = {
            "model": "Model_new",
            "manufacturer": self.manufacturers[1].pk,
            "drivers": [self.drivers[1].pk]
        }
        response = self.client.post(
            reverse("taxi:car-update", kwargs={"pk": 1}),
            data
        )
        self.assertRedirects(response, reverse("taxi:car-list"))

    def test_update_invalid_car(self):
        data = {
            "model": "",
            "manufacturer": "",
            "drivers": []
        }
        response = self.client.post(
            reverse("taxi:car-update", kwargs={"pk": 1}),
            data
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "model",
            "This field is required."
        )
        self.assertFormError(
            response.context["form"],
            "manufacturer",
            "This field is required."
        )
        self.assertFormError(
            response.context["form"],
            "drivers",
            "This field is required."
        )


class CarDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="btest",
            country="btest country"
        )
        driver = Driver.objects.create(
            first_name="btest_name",
            last_name="btest_last_name",
            username="busername",
            email="btest@gmail.com",
            license_number="FHG17564"
        )
        car = Car.objects.create(
            model=f"model_0",
            manufacturer=manufacturer
        )
        car.drivers.set([driver])

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/cars/1/delete/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(
            reverse("taxi:car-delete", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)

    def test_view_redirect_if_user_is_guest(self):
        self.client.logout()
        response = self.client.get(
            reverse("taxi:car-delete", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        response = self.client.get(
            reverse("taxi:car-delete", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/car_confirm_delete.html"
        )

    def test_delete_car(self):
        response = self.client.post(
            reverse("taxi:car-delete", kwargs={"pk": 1})
        )
        self.assertRedirects(response, reverse("taxi:car-list"))


class DriverListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    @classmethod
    def setUpTestData(cls):
        number_drivers = 13
        for i in range(number_drivers):
            Driver.objects.create(
                first_name=f"test_name_{i}",
                last_name=f"test_last_name_{i}",
                username=f"username_{i}",
                email=f"test@gmail.com_{i}",
                license_number=f"FHG1756{i}"
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/drivers/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_redirect_if_user_is_guest(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_pagination_is_5(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_lists_last_page_cars(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?page=3"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 4)

    def test_lists_with_search_by_first_name(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?search=test_name_0"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form_search" in response.context)
        self.assertEqual(
            response.context["form_search"].initial.get("search"),
            "test_name_0"
        )
        self.assertEqual(len(response.context["driver_list"]), 1)

    def test_lists_with_search_by_last_name(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?search=test_last_name_0"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form_search" in response.context)
        self.assertEqual(
            response.context["form_search"].initial.get("search"),
            "test_last_name_0"
        )
        self.assertEqual(len(response.context["driver_list"]), 1)

    def test_lists_with_search_by_license_number(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?search=FHG17560"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form_search" in response.context)
        self.assertEqual(
            response.context["form_search"].initial.get("search"),
            "FHG17560"
        )
        self.assertEqual(len(response.context["driver_list"]), 1)


class DriverCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/drivers/create/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(response.status_code, 200)

    def test_view_redirect_if_user_is_guest(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_create_valid_new_driver(self):
        data = {
            "first_name": "btest_name",
            "last_name": "btest_last_name",
            "username": "busername",
            "license_number": "FHG17564",
            "password1": "testpass1",
            "password2": "testpass1"
        }
        response = self.client.post(reverse("taxi:driver-create"), data)
        self.assertRedirects(response, reverse("taxi:driver-detail", kwargs={"pk": 2}))

    def test_create_invalid_new_driver(self):
        data = {
            "username": "",
            "license_number": "",
            "password1": "",
            "password2": ""
        }
        response = self.client.post(reverse("taxi:driver-create"), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "username",
            "This field is required."
        )
        self.assertFormError(
            response.context["form"],
            "license_number",
            "This field is required."
        )
        self.assertFormError(
            response.context["form"],
            "password1",
            "This field is required."
        )
        self.assertFormError(
            response.context["form"],
            "password2",
            "This field is required."
        )


class DriverLicenseUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    @classmethod
    def setUpTestData(cls):
        Driver.objects.create(
            first_name=f"test_name_1",
            last_name=f"test_last_name_1",
            username=f"username_1",
            email=f"test@gmail.com_1",
            license_number=f"FHG17561"
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/drivers/1/update/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(
            reverse("taxi:driver-update", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)

    def test_view_redirect_if_user_is_guest(self):
        self.client.logout()
        response = self.client.get(
            reverse("taxi:driver-update", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        response = self.client.get(
            reverse("taxi:driver-update", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_update_valid_driver_license_number(self):
        data = {
            "license_number": "FHG17564",
        }
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": 1}),
            data
        )
        self.assertRedirects(response, reverse("taxi:driver-list"))

    def test_update_invalid_driver_license_number(self):
        data = {
            "license_number": "",
        }
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": 1}),
            data
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "license_number",
            "This field is required."
        )


class DriverDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create(
            first_name=f"test_name_1",
            last_name=f"test_last_name_1",
            username=f"username_1",
            email=f"test@gmail.com_1",
            license_number=f"FHG17561"
        )

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/drivers/1/delete/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(
            reverse("taxi:driver-delete", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)

    def test_view_redirect_if_user_is_guest(self):
        self.client.logout()
        response = self.client.get(
            reverse("taxi:driver-delete", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        response = self.client.get(
            reverse("taxi:driver-delete", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/driver_confirm_delete.html"
        )

    def test_delete_driver(self):
        response = self.client.post(
            reverse("taxi:driver-delete", kwargs={"pk": 1})
        )
        self.assertRedirects(response, reverse("taxi:driver-list"))
