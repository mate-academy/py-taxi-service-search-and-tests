from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


CAR_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_car_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEquals(res, 200)


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        numbers_of_cars = 6
        for car_id in range(numbers_of_cars):
            Car.objects.create(
                model=f"test{car_id}",
                manufacturer=manufacturer
            )

    def test_car_view_url_exists_at_desired_location(self):
        response = self.client.get("/cars/")
        self.assertEqual(response.status_code, 200)

    def test_car_view_url_accessible_by_name(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)

    def test_car_uses_correct_template_name(self):
        res = self.client.get(CAR_URL)
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_car_pagination_is_five(self):
        res = self.client.get(CAR_URL)
        self.assertTrue("is_paginated" in res.context)
        self.assertTrue(res.context["is_paginated"])
        self.assertEqual(len(res.context["car_list"]), 5)
        self.assertEqual(
            list(res.context["car_list"]),
            list(Car.objects.filter(pk__lte=5))
        )

    def test_lists_all_car(self):
        res = self.client.get(CAR_URL + "?page=2")
        self.assertEqual(res.status_code, 200)
        self.assertTrue("is_paginated" in res.context)
        self.assertTrue(res.context["is_paginated"])
        self.assertEqual(len(res.context["car_list"]), 1)


class CarCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.car_create_url = reverse("taxi:car-create")

    def test_car_create_view_url_exists_at_desired_location(self):
        res = self.client.get("/cars/create/")
        self.assertEqual(res.status_code, 200)

    def test_car_create_view_url_accessible_by_name(self):
        res = self.client.get(self.car_create_url)
        self.assertEqual(res.status_code, 200)

    def test_car_create_uses_correct_template_name(self):
        res = self.client.get(self.car_create_url)
        self.assertTemplateUsed(res, "taxi/car_form.html")

    def test_car_create(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        res = self.client.post(
            self.car_create_url, {
                "model": "X5",
                "manufacturer": manufacturer.id,
                "drivers": [self.user.id],
            }
        )
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "/cars/")
        self.assertEqual(Car.objects.get(pk=1).model, "X5")


class CarUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(
            name="BMW",

            country="Germany"
        )
        self.car = Car.objects.create(model="X5", manufacturer=manufacturer)
        self.car_update_url = reverse("taxi:car-update", args=[self.car.id])

    def test_car_update_view_url_exists_at_desired_location(self):
        res = self.client.get(f"/cars/{self.car.id}/update/")
        self.assertEqual(res.status_code, 200)

    def test_car_update_view_url_accessible_by_name(self):
        res = self.client.get(self.car_update_url)
        self.assertEqual(res.status_code, 200)

    def test_car_update_uses_correct_template_name(self):
        res = self.client.get(self.car_update_url)
        self.assertTemplateUsed(res, "taxi/car_form.html")

    def test_car_update(self):
        res = self.client.post(
            self.car_update_url, {
                "model": "X6",
                "manufacturer": self.car.manufacturer.id,
                "drivers": [self.user.id]
            }
        )
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "/cars/")
        self.assertEqual(self.car.model, "X5")
        self.car.refresh_from_db()
        self.assertEqual(self.car.model, "X6")


class CarDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.car = Car.objects.create(model="X5", manufacturer=manufacturer)
        self.car_delete_url = reverse("taxi:car-delete", args=[self.car.id])

    def test_car_delete_view_url_exists_at_desired_location(self):
        res = self.client.get(f"/cars/{self.car.id}/delete/")
        self.assertEqual(res.status_code, 200)

    def test_car_delete_view_url_accessible_by_name(self):
        res = self.client.get(self.car_delete_url)
        self.assertEqual(res.status_code, 200)

    def test_car_delete_uses_correct_template_name(self):
        res = self.client.get(self.car_delete_url)
        self.assertTemplateUsed(res, "taxi/car_confirm_delete.html")

    def test_car_delete(self):
        res = self.client.post(self.car_delete_url)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "/cars/")
        self.assertFalse(Car.objects.filter(id=self.car.id))


class CarDetailViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(
            name="BMW",

            country="Germany"
        )
        self.car = Car.objects.create(model="X5", manufacturer=manufacturer)
        self.car_detail_url = reverse("taxi:car-detail", args=[self.car.id])

    def test_car_detail_view_url_exists_at_desired_location(self):
        res = self.client.get(f"/cars/{self.user.id}/")
        self.assertEqual(res.status_code, 200)

    def test_car_detail_view_url_accessible_by_name(self):
        res = self.client.get(self.car_detail_url)
        self.assertEqual(res.status_code, 200)

    def test_car_detail_uses_correct_template_name(self):
        res = self.client.get(self.car_detail_url)
        self.assertTemplateUsed(res, "taxi/car_detail.html")
