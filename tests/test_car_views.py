from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class TestCarViewsLoginRequired(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TestCountry",
        )
        self.car = Car.objects.create(
            model="TestModel",
            manufacturer=self.manufacturer,
        )

    def test_car_list_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_car_detail_login_required(self):
        response = self.client.get(
            reverse("taxi:car-detail", args=[self.car.id])
        )
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


class BaseCarTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TestCountry",
        )
        self.car = Car.objects.create(
            model="TestModel",
            manufacturer=self.manufacturer,
        )
        self.driver = get_user_model().objects.create_user(
            username="TestUser1", password="TestPassword1"
        )
        self.car.drivers.add(self.driver)
        self.client.force_login(self.driver)


class TestCarList(BaseCarTest):
    car_list_url = reverse("taxi:car-list")
    paginated_by = 5

    def setUp(self):
        super().setUp()
        for i in range(1, 16):
            car = Car.objects.create(
                model=f"TestModel{i}",
                manufacturer=self.manufacturer,
            )
            car.drivers.add(self.driver)

    def test_car_list_template(self):
        response = self.client.get(self.car_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_pagination(self):
        response = self.client.get(self.car_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(response.context["is_paginated"], True)
        self.assertEqual(
            len(response.context["car_list"]), self.paginated_by
        )

    def test_car_list_search(self):
        response = self.client.get(self.car_list_url + "?model=4")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 2)
        self.assertContains(response, "TestModel4")
        self.assertNotContains(response, "TestModel5")


class TestCarDetail(BaseCarTest):
    def test_car_detail_tamplate(self):
        response = self.client.get(
            reverse("taxi:car-detail", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")


class TestCarCreate(BaseCarTest):
    def test_car_create_template(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_car_create(self):
        data = {
            "model": "NewTestModel",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id],
        }
        self.client.post(reverse("taxi:car-create"), data=data)
        new_car = Car.objects.get(model=data["model"])
        self.assertEqual(new_car.model, data["model"])
        self.assertEqual(new_car.manufacturer, self.manufacturer)
        self.assertIn(self.driver, new_car.drivers.all())


class TestCarUpdate(BaseCarTest):
    def test_car_update_template(self):
        response = self.client.get(
            reverse("taxi:car-update", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_car_update(self):
        car = Car.objects.create(
            model="OldTestModel",
            manufacturer=self.manufacturer,
        )
        new_manufacturer = Manufacturer.objects.create(
            name="NewTestManufacturer",
            country="TestCountry",
        )
        new_driver = get_user_model().objects.create_user(
            username="TestDriver2",
            password="TestPassword2",
            license_number="TST12345",
        )
        form_data = {
            "model": "NewTestModel",
            "manufacturer": new_manufacturer.id,
            "drivers": [self.driver.id, new_driver.id],
        }
        self.client.post(
            reverse("taxi:car-update", args=[car.id]),
            data=form_data
        )
        updated_car = Car.objects.get(id=car.id)
        self.assertEqual(updated_car.model, form_data["model"])
        self.assertEqual(updated_car.manufacturer, new_manufacturer)
        self.assertIn(new_driver, updated_car.drivers.all())


class TestCarDelete(BaseCarTest):
    def test_car_delete_template(self):
        response = self.client.get(
            reverse("taxi:car-delete", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_confirm_delete.html")

    def test_car_delete(self):
        self.client.post(reverse("taxi:car-delete", args=[self.car.id]))
        cars = Car.objects.filter(id=self.car.id)
        self.assertEqual(len(cars), 0)
