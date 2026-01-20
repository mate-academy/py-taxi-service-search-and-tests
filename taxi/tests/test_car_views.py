from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class PublicCarTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test country",
        )
        self.car = Car.objects.create(
            model="Test model",
            manufacturer=self.manufacturer,
        )

    def test_car_list_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_car_create_login_required(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertNotEqual(response.status_code, 200)

    def test_car_update_login_required(self):
        response = self.client.get(
            reverse("taxi:car-update", args=[self.car.id])
        )
        self.assertNotEqual(response.status_code, 200)

    def test_car_delete_login_required(self):
        response = self.client.get(
            reverse("taxi:car-delete", args=[self.car.id])
        )
        self.assertNotEqual(response.status_code, 200)


class BasePrivateCarTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test country",
        )
        self.car = Car.objects.create(
            model="Test model",
            manufacturer=self.manufacturer,
        )
        self.driver = get_user_model().objects.create_user(
            username="Test", password="Testpass123"
        )
        self.car.drivers.add(self.driver)
        self.client.force_login(self.driver)


class PrivateCarListTests(BasePrivateCarTests):
    CAR_LIST_URL = reverse("taxi:car-list")
    VIEW_PAGINATED_BY = 5

    def setUp(self):
        super().setUp()
        for i in range(1, 11):
            car = Car.objects.create(
                model=f"Test model {i}",
                manufacturer=self.manufacturer,
            )
            car.drivers.add(self.driver)

    def test_car_list_template(self):
        response = self.client.get(self.CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_pagination(self):
        response = self.client.get(self.CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(response.context["is_paginated"], True)
        self.assertEqual(
            len(response.context["car_list"]),
            self.VIEW_PAGINATED_BY
        )

    def test_car_list_search(self):
        response = self.client.get(self.CAR_LIST_URL + "?model=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 2)
        self.assertContains(response, "Test model 1")
        self.assertNotContains(response, "Test model 2")

    def test_manufacturer_search_pagination(self):
        response = self.client.get(self.CAR_LIST_URL + "?name=Test&page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(response.context["is_paginated"], True)
        self.assertEqual(
            len(response.context["car_list"]),
            self.VIEW_PAGINATED_BY
        )


class PrivateCarDetailTests(BasePrivateCarTests):
    def test_car_detail_uses_correct_template(self):
        response = self.client.get(
            reverse("taxi:car-detail", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")


class PrivateCarCreateTests(BasePrivateCarTests):
    def test_manufacturer_create_uses_correct_template(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_car_create_post(self):
        form_data = {
            "model": "Test new model",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id],
        }
        self.client.post(reverse("taxi:car-create"), data=form_data)
        new_car = Car.objects.get(model=form_data["model"])
        self.assertEqual(new_car.model, form_data["model"])
        self.assertEqual(new_car.manufacturer, self.manufacturer)
        self.assertIn(self.driver, new_car.drivers.all())


class PrivateCarUpdateTests(BasePrivateCarTests):
    def test_car_update_uses_correct_template(self):
        response = self.client.get(
            reverse("taxi:car-update", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_manufacturer_update_post(self):
        car = Car.objects.create(
            model="Test update model",
            manufacturer=self.manufacturer,
        )
        updated_manufacturer = Manufacturer.objects.create(
            name="Test update manufacturer",
            country="Test country",
        )
        new_driver = get_user_model().objects.create_user(
            username="Test new driver",
            password="Testpass123",
            license_number="TST12345",
        )
        form_data = {
            "model": "Updated model",
            "manufacturer": updated_manufacturer.id,
            "drivers": [self.driver.id, new_driver.id],
        }
        self.client.post(
            reverse("taxi:car-update", args=[car.id]),
            data=form_data
        )
        updated_car = Car.objects.get(id=car.id)
        self.assertEqual(updated_car.model, form_data["model"])
        self.assertEqual(updated_car.manufacturer, updated_manufacturer)
        self.assertIn(new_driver, updated_car.drivers.all())


class PrivateCarDeleteTests(BasePrivateCarTests):
    def test_car_delete_uses_correct_template(self):
        response = self.client.get(
            reverse("taxi:car-delete", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_confirm_delete.html")

    def test_car_delete_post(self):
        self.client.post(reverse("taxi:car-delete", args=[self.car.id]))
        manufacturers = Car.objects.filter(id=self.car.id)
        self.assertEqual(len(manufacturers), 0)
