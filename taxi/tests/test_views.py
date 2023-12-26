from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_VIEW = reverse("taxi:driver-list")
INDEX_URL = reverse("taxi:index")


class PublicManufacturerView(TestCase):
    def test_login_required_list(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="123"
        )
        self.client.force_login(self.user)

        num_of_manufacturers = 9
        for man_id in range(num_of_manufacturers):
            Manufacturer.objects.create(
                name=f"MR {man_id}",
                country=f"Country {man_id}"
            )

    def test_view_uses_correct_template(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_context_has_search_form(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertIn("search_form", res.context)

    def test_pagination_is_five(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertTrue("is_paginated" in res.context)
        self.assertTrue(res.context["is_paginated"] is True)
        self.assertEqual(len(res.context["manufacturer_list"]), 5)

    def test_create_manufacturer(self):
        Manufacturer.objects.create(name="Test man", country="Test Country")
        self.assertTrue(Manufacturer.objects.filter(name="Test man").exists())


class PublicCarView(TestCase):
    def test_login_required_list(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="123"
        )
        self.client.force_login(self.user)
        num_of_cars = 9
        for car_id in range(num_of_cars):
            manufacturer = Manufacturer.objects.create(
                name=f"MR {car_id}",
                country=f"Country {car_id}"
            )
            Car.objects.create(
                model=f"Model {car_id}",
                manufacturer=manufacturer
            )

    def test_view_uses_correct_template(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed("taxi/car_list.html")

    def test_context_has_search_form(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertIn("search_form", res.context)

    def test_pagination_is_five(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertTrue("is_paginated" in res.context)
        self.assertTrue(res.context["is_paginated"] is True)
        self.assertEqual(len(res.context["car_list"]), 5)


class PublicDriverView(TestCase):
    def test_login_required_list(self):
        res = self.client.get(DRIVER_LIST_VIEW)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="123"
        )
        self.client.force_login(self.user)

    def test_view_uses_correct_template(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed("taxi/driver_list.html")

    def test_pagination_is_five(self):
        num_of_drivers = 9
        for driver_id in range(num_of_drivers):
            Driver.objects.create(
                username=f"Driver {driver_id}",
                license_number=f"ABC5678{driver_id}"
            )
        res = self.client.get(DRIVER_LIST_VIEW)
        self.assertTrue("is_paginated" in res.context)
        self.assertTrue(res.context["is_paginated"] is True)
        self.assertEqual(len(res.context["driver_list"]), 5)

    def test_create_driver(self):
        form_data = {
            "username": "test_user",
            "password1": "Gfhjkmjlby@",
            "password2": "Gfhjkmjlby@",
            "license_number": "ABC12345",
            "first_name": "Test",
            "last_name": "User"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        test_user = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertEqual(test_user.first_name, form_data["first_name"])
        self.assertEqual(test_user.last_name, form_data["last_name"])
        self.assertEqual(test_user.license_number, form_data["license_number"])

    def test_update_driver_license(self):
        form_data = {
            "license_number": "ABC12345"
        }
        self.client.post(reverse(
            "taxi:driver-update",
            args=[self.user.id]),
            data=form_data
        )
        test_user = get_user_model().objects.get(
            license_number=form_data["license_number"]
        )
        self.assertEqual(test_user.license_number, form_data["license_number"])


class ToggleAssignView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="123"
        )
        self.client.force_login(self.user)
        self.driver = Driver.objects.create(
            username="Test driver",
            license_number="ABC12345",
        )
        self.car = Car.objects.create(
            model="Test model",
            manufacturer=Manufacturer.objects.create(
                name="Test manufacturer"
            )
        )

    def test_toggle_assign_to_car(self):
        res = self.client.post(reverse(
            "taxi:toggle-car-assign",
            args=[self.car.id])
        )
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse(
            "taxi:car-detail",
            args=[self.car.id])
        )


class IndexViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="123"
        )
        self.driver = Driver.objects.create(
            username="Test driver",
            license_number="ABC12345",
        )
        self.car = Car.objects.create(
            model="Test model",
            manufacturer=Manufacturer.objects.create(
                name="Test manufacturer"
            )
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test man",
            country="Test country"
        )
        self.client.force_login(self.user)

    def test_correct_template(self):
        res = self.client.get(INDEX_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/index.html")

    def test_context_data(self):
        res = self.client.get(INDEX_URL)
        self.assertTrue("num_drivers" in res.context)
        self.assertTrue("num_cars" in res.context)
        self.assertTrue("num_manufacturers" in res.context)
        self.assertTrue("num_visits" in res.context)

    def test_count_of_visits(self):
        res = self.client.get(INDEX_URL)
        for visit in range(4):
            res = self.client.get(INDEX_URL)
        self.assertEqual(res.context["num_visits"], 5)
