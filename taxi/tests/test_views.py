from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car
from taxi.tests.helpers import create_test_data


class LoginViewsTest(TestCase):

    def setUp(self):
        self.manufacturer, self.driver, self.car = create_test_data()

        self.urls = {
            "taxi:manufacturer-list": None,
            "taxi:manufacturer-create": None,
            "taxi:manufacturer-update": self.manufacturer.id,
            "taxi:manufacturer-delete": self.manufacturer.id,
            "taxi:car-list": None,
            "taxi:car-detail": self.car.id,
            "taxi:car-create": None,
            "taxi:car-update": self.car.id,
            "taxi:car-delete": self.car.id,
            "taxi:toggle-car-assign": self.car.id,
            "taxi:driver-list": None,
            "taxi:driver-detail": self.driver.id,
            "taxi:driver-create": None,
            "taxi:driver-update": self.driver.id,
            "taxi:driver-delete": self.driver.id,

        }

    def test_login_required(self):
        for url, pk in self.urls.items():
            with self.subTest(url=url):
                response = self.client.get(
                    reverse(url, args=[pk]) if pk else reverse(url)
                )
                self.assertNotEqual(response.status_code, 200)

    def test_access_when_logged_in(self):
        self.client.force_login(self.driver)

        for url, pk in self.urls.items():
            with self.subTest(url=url):
                response = self.client.get(
                    reverse(
                        url, args=[pk]
                    ) if pk else reverse(url), follow=True
                )
                self.assertEqual(response.status_code, 200)


class ManufacturerViewsTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="test_user",
            password="test1234",
        )
        self.client.force_login(user)

        for i in range(10):
            Manufacturer.objects.create(
                name=f"Manufacturer {i}",
                country=f"Country {i}"
            )

    def test_retrieve_manufacturer(self):
        manufacturers = Manufacturer.objects.all()
        response = self.client.get(reverse("taxi:manufacturer-list"))
        if response.context["is_paginated"]:
            per_page = response.context["paginator"].per_page
            self.assertQuerysetEqual(
                response.context["manufacturer_list"],
                manufacturers[:per_page]
            )
        else:
            self.assertQuerysetEqual(
                response.context["manufacturer_list"],
                manufacturers
            )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )

    def test_pagination_is_five(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(
            len(response.context["manufacturer_list"]), 5
        )

    def test_manufacturer_get_context_data(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Manufacturer 1"
        )
        self.assertEqual(
            response.context["form"].initial["name"],
            "Manufacturer 1"
        )

    def test_manufacturer_get_queryset_with_filter(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Manufacturer 1"
        )
        self.assertEqual(
            len(response.context["manufacturer_list"]), 1
        )
        self.assertEqual(
            response.context["manufacturer_list"][0].name,
            "Manufacturer 1"
        )

    def test_manufacturer_create(self):
        response = self.client.post(
            reverse("taxi:manufacturer-create"), {
                "name": "New Manufacturer",
                "country": "New Country"
            }
        )
        self.assertTrue(
            Manufacturer.objects.filter(name="New Manufacturer").exists()
        )
        self.assertEqual(response.status_code, 302)

    def test_manufacturer_update(self):
        manufacturer = Manufacturer.objects.create(name="New Manufacturer")
        response = self.client.post(
            reverse("taxi:manufacturer-update", args=[manufacturer.id]),
            {
                "name": "Updated Manufacturer",
                "country": "Updated Country"
            }
        )
        self.assertTrue(
            Manufacturer.objects.filter(name="Updated Manufacturer").exists()
        )
        self.assertEqual(response.status_code, 302)

    def test_manufacturer_delete(self):
        manufacturer = Manufacturer.objects.create(name="Delete Manufacturer")
        response = self.client.post(
            reverse("taxi:manufacturer-delete",
                    args=[manufacturer.id])
        )
        self.assertFalse(
            Manufacturer.objects.filter(id=manufacturer.id).exists()
        )
        self.assertEqual(response.status_code, 302)


class CarViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test1234",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer"
        )

        for i in range(10):
            car = Car.objects.create(
                model=f"Car {i}",
                manufacturer=self.manufacturer
            )
            car.drivers.add(self.user)

    def test_retrieve_car(self):
        cars = Car.objects.all()
        response = self.client.get(reverse("taxi:car-list"))
        if response.context["is_paginated"]:
            per_page = response.context["paginator"].per_page
            self.assertEqual(
                list(response.context["car_list"]),
                list(cars[:per_page])
            )
        else:
            self.assertEqual(
                list(response.context["car_list"]),
                list(cars)
            )
        self.assertTemplateUsed(
            response, "taxi/car_list.html"
        )

    def test_pagination_is_five(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_car_get_context_data(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?model=Car 1"
        )
        self.assertEqual(
            response.context["form"].initial["model"], "Car 1"
        )

    def test_car_get_queryset_with_filter(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?model=Car 1"
        )
        self.assertEqual(
            len(response.context["car_list"]), 1
        )
        self.assertEqual(
            response.context["car_list"][0].model, "Car 1"
        )

    def test_car_create(self):
        response = self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "New Model",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id]
            }
        )
        self.assertTrue(
            Car.objects.filter(model="New Model").exists()
        )
        self.assertEqual(response.status_code, 302)

    def test_car_update(self):
        car = Car.objects.get(id=1)
        response = self.client.post(
            reverse("taxi:car-update", args=[car.id]), {
                "model": "Updated Model",
                "manufacturer": car.manufacturer.id,
                "drivers": [driver.id for driver in car.drivers.all()]
            }
        )
        self.assertTrue(
            Car.objects.filter(model="Updated Model").exists()
        )
        self.assertEqual(
            response.status_code, 302
        )

    def test_car_delete(self):
        car = Car.objects.get(id=1)
        response = self.client.post(
            reverse("taxi:car-delete", args=[car.id])
        )
        self.assertFalse(Car.objects.filter(id=car.id).exists())
        self.assertEqual(response.status_code, 302)


class DriverViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test1234",
        )
        self.client.force_login(self.user)

        for i in range(10):
            get_user_model().objects.create(
                license_number=f"ABC0000{i}",
                username=f"driver_{i}",
                password="test1234",
                first_name=f"Name {i}",
                last_name=f"Surname {i}",
            )

    def test_retrieve_driver(self):
        drivers = get_user_model().objects.all()
        response = self.client.get(reverse("taxi:driver-list"))
        if response.context["is_paginated"]:
            per_page = response.context["paginator"].per_page
            self.assertEqual(
                list(response.context["driver_list"]), list(drivers[:per_page])
            )
        else:
            self.assertEqual(
                list(response.context["driver_list"]), list(drivers)
            )
        self.assertTemplateUsed(
            response, "taxi/driver_list.html"
        )

    def test_pagination_is_five(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_driver_get_context_data(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=driver_1"
        )
        self.assertEqual(
            response.context["form"].initial["username"], "driver_1"
        )

    def test_driver_get_queryset_with_filter(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=driver_1"
        )
        self.assertEqual(
            len(response.context["driver_list"]), 1
        )
        self.assertEqual(
            response.context["driver_list"][0].username, "driver_1"
        )

    def test_driver_create(self):
        form_data = {
            "username": "new_driver",
            "password1": "test1234!@#",
            "password2": "test1234!@#",
            "first_name": "new_first_name",
            "last_name": "new_last_name",
            "license_number": "NEW00001",
        }
        response = self.client.post(
            reverse("taxi:driver-create"),
            data=form_data,
        )
        new_user = get_user_model().objects.get(username="new_driver")
        self.assertEqual(new_user.first_name, "new_first_name")
        self.assertEqual(new_user.last_name, "new_last_name")
        self.assertEqual(new_user.license_number, "NEW00001")
        self.assertEqual(response.status_code, 302)

    def test_driver_license_update(self):
        driver = get_user_model().objects.get(id=1)
        response = self.client.post(
            reverse("taxi:driver-update", args=[driver.id]), {
                "license_number": "UPD00001",
            }
        )
        self.assertTrue(
            get_user_model().objects.filter(license_number="UPD00001").exists()
        )
        self.assertEqual(response.status_code, 302)

    def test_driver_delete(self):
        driver = get_user_model().objects.get(id=1)
        response = self.client.post(
            reverse("taxi:driver-delete", args=[driver.id])
        )
        self.assertFalse(
            get_user_model().objects.filter(id=driver.id).exists()
        )
        self.assertEqual(response.status_code, 302)

    def test_driver_assign_car_(self):
        manufacturer = Manufacturer.objects.create(
            name="Assign Manufacturer"
        )
        car = Car.objects.create(
            model="Assign Model",
            manufacturer=manufacturer
        )
        url = reverse(
            "taxi:toggle-car-assign", args=[car.id]
        )

        with self.subTest("Assign Driver to car"):
            self.assertFalse(self.user in car.drivers.all())
            self.client.get(url)
            car.refresh_from_db()
            self.assertTrue(self.user in car.drivers.all())

        with self.subTest("Unassign Driver from car"):
            self.client.get(url)
            car.refresh_from_db()
            self.assertFalse(self.user in car.drivers.all())
