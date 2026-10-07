from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

INDEX_URL = reverse("taxi:index")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicViewsTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        for url in (
            INDEX_URL,
            MANUFACTURER_LIST_URL,
            CAR_LIST_URL,
            DRIVER_LIST_URL,
        ):
            with self.subTest(url=url):
                res = self.client.get(url)
                self.assertRedirects(res, f"/accounts/login/?next={url}")


class PrivateIndexTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_index_counters(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )
        Car.objects.create(model="test_model", manufacturer=manufacturer)

        res = self.client.get(INDEX_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/index.html")
        self.assertEqual(res.context["num_drivers"], 1)
        self.assertEqual(res.context["num_cars"], 1)
        self.assertEqual(res.context["num_manufacturers"], 1)

    def test_index_counts_visits(self):
        self.client.get(INDEX_URL)
        res = self.client.get(INDEX_URL)
        self.assertEqual(res.context["num_visits"], 2)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Toyoda", country="Japan")

    def test_retrieve_manufacturers(self):
        res = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(Manufacturer.objects.all()),
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_search_manufacturers_by_name(self):
        res = self.client.get(MANUFACTURER_LIST_URL, {"name": "toyo"})

        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains="toyo")),
        )
        self.assertEqual(len(res.context["manufacturer_list"]), 2)
        self.assertNotContains(res, "BMW")

    def test_search_manufacturers_without_matches(self):
        res = self.client.get(MANUFACTURER_LIST_URL, {"name": "audi"})

        self.assertEqual(len(res.context["manufacturer_list"]), 0)
        self.assertContains(res, "There are no manufacturers in the service.")

    def test_search_form_keeps_entered_value(self):
        res = self.client.get(MANUFACTURER_LIST_URL, {"name": "toyo"})
        self.assertEqual(
            res.context["search_form"].initial["name"], "toyo"
        )

    def test_create_manufacturer(self):
        res = self.client.post(
            reverse("taxi:manufacturer-create"),
            {"name": "Audi", "country": "Germany"},
        )

        self.assertRedirects(res, MANUFACTURER_LIST_URL)
        self.assertTrue(Manufacturer.objects.filter(name="Audi").exists())

    def test_update_manufacturer(self):
        manufacturer = Manufacturer.objects.get(name="BMW")
        res = self.client.post(
            reverse("taxi:manufacturer-update", args=[manufacturer.id]),
            {"name": "BMW", "country": "USA"},
        )
        manufacturer.refresh_from_db()

        self.assertRedirects(res, MANUFACTURER_LIST_URL)
        self.assertEqual(manufacturer.country, "USA")

    def test_delete_manufacturer(self):
        manufacturer = Manufacturer.objects.get(name="BMW")
        res = self.client.post(
            reverse("taxi:manufacturer-delete", args=[manufacturer.id])
        )

        self.assertRedirects(res, MANUFACTURER_LIST_URL)
        self.assertFalse(Manufacturer.objects.filter(name="BMW").exists())


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        for model in ("Camry", "Corolla", "Yaris"):
            Car.objects.create(model=model, manufacturer=self.manufacturer)

    def test_retrieve_cars(self):
        res = self.client.get(CAR_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]),
            list(Car.objects.all()),
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_search_cars_by_model(self):
        res = self.client.get(CAR_LIST_URL, {"model": "c"})

        self.assertEqual(
            list(res.context["car_list"]),
            list(Car.objects.filter(model__icontains="c")),
        )
        self.assertEqual(len(res.context["car_list"]), 2)
        self.assertNotContains(res, "Yaris")

    def test_search_cars_without_matches(self):
        res = self.client.get(CAR_LIST_URL, {"model": "Prius"})

        self.assertEqual(len(res.context["car_list"]), 0)
        self.assertContains(res, "There are no cars in taxi")

    def test_search_form_keeps_entered_value(self):
        res = self.client.get(CAR_LIST_URL, {"model": "Camry"})
        self.assertEqual(
            res.context["search_form"].initial["model"], "Camry"
        )

    def test_pagination_keeps_search_value(self):
        for number in range(6):
            Car.objects.create(
                model=f"Prius {number}",
                manufacturer=self.manufacturer,
            )

        res = self.client.get(CAR_LIST_URL, {"model": "prius"})

        self.assertTrue(res.context["is_paginated"])
        self.assertEqual(len(res.context["car_list"]), 5)
        self.assertContains(res, "?model=prius&amp;page=2")

        res = self.client.get(CAR_LIST_URL, {"model": "prius", "page": 2})

        self.assertEqual(len(res.context["car_list"]), 1)

    def test_retrieve_car_detail(self):
        car = Car.objects.get(model="Camry")
        res = self.client.get(reverse("taxi:car-detail", args=[car.id]))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["car"], car)
        self.assertTemplateUsed(res, "taxi/car_detail.html")

    def test_create_car(self):
        res = self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "Prius",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            },
        )
        car = Car.objects.get(model="Prius")

        self.assertRedirects(res, CAR_LIST_URL)
        self.assertEqual(list(car.drivers.all()), [self.user])

    def test_delete_car(self):
        car = Car.objects.get(model="Camry")
        res = self.client.post(reverse("taxi:car-delete", args=[car.id]))

        self.assertRedirects(res, CAR_LIST_URL)
        self.assertFalse(Car.objects.filter(model="Camry").exists())

    def test_toggle_assign_to_car(self):
        car = Car.objects.get(model="Camry")
        url = reverse("taxi:toggle-car-assign", args=[car.id])

        res = self.client.get(url)

        self.assertRedirects(res, reverse("taxi:car-detail", args=[car.id]))
        self.assertIn(car, self.user.cars.all())

        self.client.get(url)

        self.assertNotIn(car, self.user.cars.all())


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            password="test123",
            license_number="ADM12345",
        )
        self.client.force_login(self.user)
        self.driver = get_user_model().objects.create_user(
            username="john.doe",
            password="test123",
            license_number="JHN12345",
        )
        get_user_model().objects.create_user(
            username="john.smith",
            password="test123",
            license_number="SMT12345",
        )

    def test_retrieve_drivers(self):
        res = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["driver_list"]),
            list(get_user_model().objects.all()),
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_search_drivers_by_username(self):
        res = self.client.get(DRIVER_LIST_URL, {"username": "JOHN"})

        self.assertEqual(
            list(res.context["driver_list"]),
            list(
                get_user_model().objects.filter(username__icontains="john")
            ),
        )
        self.assertEqual(len(res.context["driver_list"]), 2)
        self.assertNotContains(res, "ADM12345")

    def test_search_drivers_without_matches(self):
        res = self.client.get(DRIVER_LIST_URL, {"username": "nobody"})

        self.assertEqual(len(res.context["driver_list"]), 0)
        self.assertContains(res, "There are no drivers in the service.")

    def test_search_form_keeps_entered_value(self):
        res = self.client.get(DRIVER_LIST_URL, {"username": "john"})
        self.assertEqual(
            res.context["search_form"].initial["username"], "john"
        )

    def test_retrieve_driver_detail(self):
        res = self.client.get(
            reverse("taxi:driver-detail", args=[self.driver.id])
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["driver"], self.driver)
        self.assertTemplateUsed(res, "taxi/driver_detail.html")

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TST12345",
        }
        res = self.client.post(reverse("taxi:driver-create"), form_data)
        new_user = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertRedirects(res, new_user.get_absolute_url())
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_update_driver_license_number(self):
        res = self.client.post(
            reverse("taxi:driver-update", args=[self.driver.id]),
            {"license_number": "NEW12345"},
        )
        self.driver.refresh_from_db()

        self.assertRedirects(res, DRIVER_LIST_URL)
        self.assertEqual(self.driver.license_number, "NEW12345")

    def test_update_driver_with_invalid_license_number(self):
        res = self.client.post(
            reverse("taxi:driver-update", args=[self.driver.id]),
            {"license_number": "new12345"},
        )
        self.driver.refresh_from_db()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.driver.license_number, "JHN12345")

    def test_delete_driver(self):
        res = self.client.post(
            reverse("taxi:driver-delete", args=[self.driver.id])
        )

        self.assertRedirects(res, DRIVER_LIST_URL)
        self.assertFalse(
            get_user_model().objects.filter(id=self.driver.id).exists()
        )
