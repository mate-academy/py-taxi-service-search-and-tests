from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_LIST_VIEW = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_VIEW = reverse("taxi:manufacturer-create")
MANUFACTURER_UPDATE_VIEW = reverse("taxi:manufacturer-update",
                                   kwargs={"pk": 1})
MANUFACTURER_DELETE_VIEW = reverse("taxi:manufacturer-delete",
                                   kwargs={"pk": 1})
CAR_LIST_VIEW = reverse("taxi:car-list")
CAR_CREATE_VIEW = reverse("taxi:car-create")
CAR_UPDATE_VIEW = reverse("taxi:car-update",
                          kwargs={"pk": 1})
CAR_DELETE_VIEW = reverse("taxi:car-delete",
                          kwargs={"pk": 1})
DRIVER_LIST_VIEW = reverse("taxi:driver-list")
DRIVER_CREATE_VIEW = reverse("taxi:driver-create")
DRIVER_UPDATE_VIEW = reverse("taxi:driver-update",
                             kwargs={"pk": 1})
DRIVER_DELETE_VIEW = reverse("taxi:driver-delete",
                             kwargs={"pk": 2})


class PublicTaxiViewsTests(TestCase):
    def test_index_login_required(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertNotEquals(response.status_code, 200)

    def test_manufacturer_views_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_VIEW)
        self.assertNotEquals(response.status_code, 200)
        response = self.client.get(MANUFACTURER_CREATE_VIEW)
        self.assertNotEquals(response.status_code, 200)
        response = self.client.get(MANUFACTURER_UPDATE_VIEW)
        self.assertNotEquals(response.status_code, 200)
        response = self.client.get(MANUFACTURER_DELETE_VIEW)
        self.assertNotEquals(response.status_code, 200)

    def test_car_login_required(self):
        response = self.client.get(CAR_LIST_VIEW)
        self.assertNotEquals(response.status_code, 200)
        response = self.client.get(CAR_CREATE_VIEW)
        self.assertNotEquals(response.status_code, 200)
        response = self.client.get(CAR_UPDATE_VIEW)
        self.assertNotEquals(response.status_code, 200)
        response = self.client.get(CAR_DELETE_VIEW)
        self.assertNotEquals(response.status_code, 200)

    def test_driver_login_required(self):
        response = self.client.get(DRIVER_LIST_VIEW)
        self.assertNotEquals(response.status_code, 200)
        response = self.client.get(DRIVER_CREATE_VIEW)
        self.assertNotEquals(response.status_code, 200)
        response = self.client.get(DRIVER_UPDATE_VIEW)
        self.assertNotEquals(response.status_code, 200)
        response = self.client.get(DRIVER_DELETE_VIEW)
        self.assertNotEquals(response.status_code, 200)


class PrivateIndexTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        self.driver = Driver.objects.create(
            username="driver1",
            password="password123",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        self.client.force_login(self.driver)
        self.car = Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer
        )

    def test_index_view_status_code(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_index_view_context_data(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertEqual(response.context["num_drivers"], 1)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)

    def test_index_view_session_visits(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertEqual(self.client.session["num_visits"], 1)
        response = self.client.get(url)
        self.assertEqual(self.client.session["num_visits"], 2)
        self.assertEqual(response.context["num_visits"], 2)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.login(username="testuser", password="password123")
        self.manufacturer = Manufacturer.objects.create(
            name="ManufacturerTest",
            country="CountryTest"
        )

    def test_manufacturer_list_logged_in_access(self):
        response = self.client.get(MANUFACTURER_LIST_VIEW)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_pagination_is_five(self):
        number_of_manufacturers = 10
        for i in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name=f"Manufacturer{i}",
                country="Country{i}"
            )
        response = self.client.get(MANUFACTURER_LIST_VIEW)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_manufacturer_list_functionality(self):
        response = self.client.get(
            MANUFACTURER_LIST_VIEW + "?name=ManufacturerTest"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
        self.assertContains(response, "ManufacturerTest")

    def test_manufacturer_list_search_form_in_context(self):
        response = self.client.get(MANUFACTURER_LIST_VIEW)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("searchForm" in response.context)

    def test_manufacturer_create_login_success(self):
        response = self.client.get(MANUFACTURER_CREATE_VIEW)
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_created_success(self):
        data = {
            "name": "New Manufacturer",
            "country": "USA"
        }
        response = self.client.post(MANUFACTURER_CREATE_VIEW, data)
        self.assertRedirects(response, MANUFACTURER_LIST_VIEW)

    def test_manufacturer_update_login_success(self):
        response = self.client.get(MANUFACTURER_UPDATE_VIEW)
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_update_success(self):
        manufacturer = Manufacturer.objects.create(
            name="Old Manufacturer",
            country="Old Country"
        )
        data = {
            "name": "New Manufacturer2",
            "country": "USAaa"
        }
        response = self.client.post(reverse("taxi:manufacturer-update",
                                            args=[manufacturer.pk]), data)

        self.assertRedirects(response, MANUFACTURER_LIST_VIEW)

        manufacturer.refresh_from_db()
        self.assertEqual(manufacturer.name, "New Manufacturer2")
        self.assertEqual(manufacturer.country, "USAaa")

    def test_manufacturer_delete_success(self):
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer to delete",
            country="USA"
        )
        response = self.client.post(reverse("taxi:manufacturer-delete",
                                            args=[manufacturer.pk]))
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.login(username="testuser", password="password123")
        self.manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="USA"
        )
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="password123",
            license_number="ABC12345"

        )
        self.car = Car.objects.create(
            model="LAMBA",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_car_list_logged_in_access(self):
        response = self.client.get(CAR_LIST_VIEW)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_pagination_is_five(self):
        number_of_cars = 10
        for i in range(number_of_cars):
            car = Car.objects.create(
                model=f"testcar{i}",
                manufacturer=self.manufacturer
            )
            car.drivers.add(self.driver)
        response = self.client.get(CAR_LIST_VIEW)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_car_list_search_functionality(self):
        response = self.client.get(CAR_LIST_VIEW + "?model=LAMBA")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)
        self.assertContains(response, "LAMBA")

    def test_car_list_search_search_form_in_context(self):
        response = self.client.get(CAR_LIST_VIEW)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("searchForm" in response.context)

    def test_car_create_login_success(self):
        response = self.client.get(CAR_CREATE_VIEW)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_car_create_form_used(self):
        response = self.client.get(CAR_CREATE_VIEW)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context["form"], CarForm))

    def test_car_create_success(self):
        data = {
            "model": "Tesla",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id]
        }
        response = self.client.post(CAR_CREATE_VIEW, data)
        self.assertRedirects(response, CAR_LIST_VIEW)

    def test_car_update_login_success(self):
        response = self.client.get(CAR_UPDATE_VIEW)
        self.assertEqual(response.status_code, 200)

    def test_car_update_success(self):
        data = {
            "model": "Tesla",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id]
        }
        response = self.client.post(CAR_UPDATE_VIEW, data)
        self.assertRedirects(response, CAR_LIST_VIEW)

    def test_car_delete_login_success(self):
        response = self.client.get(CAR_DELETE_VIEW)
        self.assertEqual(response.status_code, 200)

    def test_car_delete_success(self):
        response = self.client.post(CAR_DELETE_VIEW)
        self.assertRedirects(response, CAR_LIST_VIEW)


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.login(username="testuser", password="password123")

        self.driver = Driver.objects.create_user(
            username="testdriver",
            password="password123",
            license_number="ABC12345"
        )

    def test_driver_list_logged_in_access(self):
        response = self.client.get(DRIVER_LIST_VIEW)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_list_pagination_is_five(self):
        number_of_drivers = 10
        for i in range(number_of_drivers):
            Driver.objects.create_user(
                username=f"testdriver{i}",
                password="password123",
                license_number=f"ABC123{100 - i}"
            )
        response = self.client.get(DRIVER_LIST_VIEW)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_driver_list_search_functionality(self):
        response = self.client.get(DRIVER_LIST_VIEW + "?username=testdriver")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertContains(response, "testdriver")

    def test_driver_list_search_search_form_in_context(self):
        response = self.client.get(DRIVER_LIST_VIEW)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("searchForm" in response.context)

    def test_driver_create_login_success(self):
        response = self.client.get(DRIVER_CREATE_VIEW)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_driver_create_form_used(self):
        response = self.client.get(DRIVER_CREATE_VIEW)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context["form"],
                                   DriverCreationForm))

    def test_driver_create_success(self):
        data = {
            "username": "newdriver",
            "password1": "412894kfkad()%$)@#KJFCFSP",
            "password2": "412894kfkad()%$)@#KJFCFSP",
            "license_number": "ABC98765"
        }
        response = self.client.post(DRIVER_CREATE_VIEW, data)
        self.assertEqual(response.status_code, 302)
        new_driver = Driver.objects.get(username="newdriver")
        self.assertRedirects(response, reverse("taxi:driver-detail",
                                               kwargs={"pk": new_driver.pk}))

    def test_driver_update_login_success(self):
        response = self.client.get(DRIVER_UPDATE_VIEW)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_driver_license_update_success(self):
        data = {
            "license_number": "BAC12345"
        }
        response = self.client.post(reverse("taxi:driver-update",
                                            kwargs={"pk": 2}), data)
        self.assertRedirects(response, DRIVER_LIST_VIEW)

    def test_driver_license_form_used(self):
        response = self.client.get(reverse("taxi:driver-update",
                                           kwargs={"pk": 2}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context["form"],
                                   DriverLicenseUpdateForm))

    def test_driver_delete_login_success(self):
        response = self.client.get(DRIVER_DELETE_VIEW)
        self.assertEqual(response.status_code, 200)

    def test_driver_delete_success(self):
        response = self.client.post(DRIVER_DELETE_VIEW)
        self.assertRedirects(response, DRIVER_LIST_VIEW)
