from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.views import index
from taxi.models import Car, Manufacturer


HOME_URL = reverse("taxi:index")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
DRIVERS_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")


class TestViewsStatusCode(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get(HOME_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturers_page_status_code(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_drivers_page_status_code(self):
        response = self.client.get(DRIVERS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_cars_page_status_code(self):
        response = self.client.get(CARS_URL)
        self.assertNotEqual(response.status_code, 200)


class IndexViewTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="admin123"
        )
        self.client.force_login(self.admin_user)
        self.url = reverse("taxi:index")
        self.response = self.client.get(self.url)

    def test_index_response(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_index_correct_num_visits(self) -> None:
        for visit in range(1, 25):
            self.response = self.client.get(self.url)
        self.assertEqual(self.response.context.get("num_visits"), 25)


class ManufacturerViewTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        manufacturers_num = 14

        get_user_model().objects.create_user(  # type: ignore
            username="test_user", password="test_password"
        )

        for manufacturer_id in range(manufacturers_num):
            Manufacturer.objects.create(
                name=f"test_name_{manufacturer_id}",
                country="test_country",
            )

    def test_manufacturer_list_redirect_if_not_logged_in(self) -> None:
        resp = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertRedirects(
            resp,
            "/accounts/login/?next=/manufacturers/",
        )

    def test_manufacturer_list_if_logged_in(self) -> None:
        test_user = get_user_model().objects.get(pk=1)
        self.client.force_login(test_user)
        resp = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(resp.context["user"].pk, test_user.pk)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "taxi/manufacturer_list.html")

    def test_manufacturer_list_pagination(self) -> None:
        test_user = get_user_model().objects.get(pk=1)
        self.client.force_login(test_user)
        resp = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(resp.status_code, 200)
        self.assertTrue("is_paginated" in resp.context)
        self.assertEqual(resp.context["is_paginated"], True)
        self.assertEqual(len(resp.context["manufacturer_list"]), 5)

    def test_manufacturer_list_pagination_last_page(self) -> None:
        test_user = get_user_model().objects.get(pk=1)
        self.client.force_login(test_user)
        resp = self.client.get(reverse("taxi:manufacturer-list") + "?page=3")

        self.assertEqual(resp.status_code, 200)
        self.assertTrue("is_paginated" in resp.context)
        self.assertEqual(resp.context["is_paginated"], True)
        self.assertEqual(len(resp.context["manufacturer_list"]), 4)


class TestDriversListView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin",
        )
        self.client.force_login(self.user)

    def test_driver_list_view(self):
        get_user_model().objects.create_user(
            username="admin2",
            password="admin2",
            license_number="JON26231",
        )
        response = self.client.get(DRIVERS_URL)
        drivers = get_user_model().objects.all()
        self.assertEqual(list(response.context["object_list"]), list(drivers))


class TestToggleAssignToCar(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin",
            license_number="JON26231",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )
        self.car = Car.objects.create(
            model="A6", manufacturer=self.manufacturer
        )

    def test_toggle_assign_to_car_when_not_assigned(self):
        response = self.client.post(
            reverse("taxi:toggle-car-assign", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.car in self.user.cars.all())

    def test_toggle_assign_to_car_when_already_assigned(self):
        self.car.drivers.add(self.user)
        response = self.client.post(
            reverse("taxi:toggle-car-assign", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.car in self.user.cars.all())


class SearchTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username", password="test_password"
        )
        self.client.force_login(self.user)

    def test_search_manufacturer_by_name(self) -> None:
        Manufacturer.objects.create(name="test_name", country="test_country")

        res = self.client.get(MANUFACTURERS_URL, {"name": "test_name"})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name="test_name")),
        )

    def test_search_driver_by_username(self) -> None:
        res = self.client.get(DRIVERS_URL, {"username": "test_username"})

        self.assertEquals(res.status_code, 200)
        self.assertEquals(
            list(res.context["driver_list"]),
            list(get_user_model().objects.filter(username="test_username")),
        )

    def test_search_from_car(self) -> None:
        Car.objects.create(
            model="test_model",
            manufacturer=Manufacturer.objects.create(
                country="test", name="test"
            ),
        )

        res = self.client.get(CARS_URL, {"model": "test_model"})

        self.assertEquals(res.status_code, 200)
        self.assertEquals(
            list(res.context["car_list"]),
            list(Car.objects.filter(model="test_model")),
        )
