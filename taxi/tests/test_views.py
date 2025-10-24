from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm, CarSearchForm, DriverSearchForm
from taxi.models import Manufacturer, Car

MANUFACTURER_URL = "/manufacturers/"
CAR_URL = "/cars/"
DRIVER_URL = "/drivers/"


class PublicIndexTest(TestCase):
    def test_login_required(self):
        response = self.client.get("/")
        self.assertNotEqual(response.status_code, 200)


class PrivateIndexTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password",
        )
        self.client.force_login(self.user)


class PublicManufacturerViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_objects = 6
        for i in range(number_of_objects):
            Manufacturer.objects.create(
                name=f"Test name {i}", country=f"Test country {i}"
            )

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password",
        )
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_view_uses_correct_context_object_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertIn("manufacturer_list", response.context)

    def test_pagination_is_five(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_lists_all_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)

    def test_context_contains_search_form_with_initial(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        form = response.context["search_form"]
        self.assertIsInstance(form, ManufacturerSearchForm)
        self.assertEqual(form.initial["name"], "test")

    def test_search_form_search_without_name(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_search_form_search_by_name_icontains(self):
        Manufacturer.objects.create(name="It name", country="Test country")
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "it name"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)


class PublicManufacturerCreateViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password",
        )
        self.client.force_login(self.user)

    def test_create_manufacturer(self):
        form_data = {
            "name": "Test name",
            "country": "Test country",
        }
        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(new_manufacturer.name, form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])


class PublicCarViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_objects = 6
        cls.manufacturer = Manufacturer.objects.create(
            name="Test name", country="Test country"
        )
        for i in range(number_of_objects):
            Car.objects.create(
                model=f"Test model {i}",
                manufacturer=cls.manufacturer,
            )

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password",
        )
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_five(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_lists_all_car(self):
        response = self.client.get(CAR_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertEqual(len(response.context["car_list"]), 1)

    def test_context_contains_search_form_with_initial(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        form = response.context["search_form"]
        self.assertIsInstance(form, CarSearchForm)
        self.assertEqual(form.initial["model"], "test")

    def test_search_form_search_without_model(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_search_form_search_by_model_icontains(self):
        manufacturer = Manufacturer.objects.get(id=1)
        Car.objects.create(model="It model", manufacturer=manufacturer)
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "it"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)


class PublicCarCreateViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertNotEqual(response.status_code, 200)


class PrivateCarCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password",
        )
        self.client.force_login(self.user)

    def test_create_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Test name", country="Test country"
        )
        driver = get_user_model().objects.create_user(
            username="test_driver",
            password="password",
            license_number="ABC12345",
        )
        form_data = {
            "model": "Test mode",
            "manufacturer": manufacturer.id,
            "drivers": [
                driver.id,
            ],
        }
        self.client.post(reverse("taxi:car-create"), data=form_data)
        new_car = Car.objects.get(model=form_data["model"])

        self.assertEqual(new_car.model, form_data["model"])
        self.assertEqual(new_car.manufacturer.id, form_data["manufacturer"])


class PublicDriverViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_objects = 6
        digits = 00000
        for i in range(number_of_objects):
            digits += 1
            get_user_model().objects.create_user(
                username=f"test_user_{i}",
                password="password",
                license_number=f"ABC{digits}",
            )

    def setUp(self):
        self.user = get_user_model().objects.get(id=1)
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_five(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_lists_all_drivers(self):
        response = self.client.get(DRIVER_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertEqual(len(response.context["driver_list"]), 1)

    def test_context_contains_search_form_with_initial(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "user"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        form = response.context["search_form"]
        self.assertIsInstance(form, DriverSearchForm)
        self.assertEqual(form.initial["username"], "user")

    def test_search_form_search_without_username(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_search_form_search_by_username_icontains(self):
        get_user_model().objects.create_user(
            username="it user",
            password="password",
            license_number="ABC12345",
        )
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "it user"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)


class PublicDriverCreateViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "Justi",
            "password1": "password123",
            "password2": "password123",
            "first_name": "first",
            "last_name": "last",
            "license_number": "ABC12445",
        }
        self.client.post(
            reverse("taxi:driver-create"),
            data=form_data
        )
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(
            new_driver.username,
            form_data["username"]
        )
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )
