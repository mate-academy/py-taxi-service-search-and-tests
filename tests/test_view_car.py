from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = "taxi:car-detail"
CAR_CREATE_URL = reverse("taxi:car-create")
CAR_UPDATE_URL = "taxi:car-update"
CAR_DELETE_URL = "taxi:car-delete"
PAGINATION = 5

TestCase.fixtures = ["taxi_service_db_data.json", ]


class PublicCarViewsTests(TestCase):
    def test_login_required_for_car_list_view(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_car_detail_view(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_car_create_view(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_car_update_view(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_car_delete_view(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarListViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password_123"
        )
        self.client.force_login(self.user)

    def test_car_list_response_with_correct_template(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_view_is_paginated(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["car_list"]), PAGINATION)

    def test_car_list_view_search_by_model(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertTrue(
            "model" in response.context_data["search_form"].fields
        )

    def test_retrieve_cars(self):
        response = self.client.get(CAR_LIST_URL)
        car_list = list(Car.objects.all()[:PAGINATION])
        self.assertEqual(
            list(response.context["car_list"]), car_list
        )


class PrivateCarDetailViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password_123"
        )
        self.client.force_login(self.user)

    def test_car_detail_view_response_with_correct_template(self):
        response = self.client.get(reverse(CAR_DETAIL_URL, args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")


class PrivateCarCreateViewTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password_123"
        )
        self.client.force_login(self.user)

    def test_car_create_view_response_with_correct_template(self):
        response = self.client.get(CAR_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_car_create_view_has_correct_success_url(self):
        response = self.client.get(CAR_CREATE_URL)
        self.assertEqual(
            response.context_data["view"].success_url,
            CAR_LIST_URL
        )

    def test_create_car(self):
        manufacturer = Manufacturer.objects.get(id=1)
        form_data = {
            "model": "test_model",
            "manufacturer": manufacturer.id,
            "drivers": [self.user.id]
        }
        response = self.client.post(CAR_CREATE_URL, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Car.objects.get(id=self.user.cars.first().id).model,
            form_data["model"]
        )


class PrivateCarUpdateViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password_123"
        )
        self.client.force_login(self.user)

    def test_car_update_view_response_with_correct_template(self):
        car = Car.objects.get(id=1)
        response = self.client.get(
            reverse(CAR_UPDATE_URL, kwargs={"pk": car.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_car_update_view_has_correct_success_url(self):
        car = Car.objects.get(id=1)
        response = self.client.get(
            reverse(CAR_UPDATE_URL, kwargs={"pk": car.id})
        )
        self.assertEqual(
            response.context_data["view"].success_url,
            CAR_LIST_URL
        )

    def test_update_car(self):
        car = Car.objects.get(id=1)
        response = self.client.post(
            reverse(CAR_UPDATE_URL, kwargs={"pk": car.id}),
            {
                "model": "updated_model",
                "manufacturer": Manufacturer.objects.last().id,
                "drivers": [self.user.id]
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Car.objects.get(id=1).model, "updated_model")


class PrivateCarDeleteViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password_123"
        )
        self.client.force_login(self.user)

    def test_car_delete_view_response_with_correct_template(self):
        car = Car.objects.get(id=1)
        response = self.client.get(
            reverse(CAR_DELETE_URL, kwargs={"pk": car.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_confirm_delete.html")

    def test_car_delete_view_has_correct_success_url(self):
        car = Car.objects.get(id=1)
        response = self.client.get(
            reverse(CAR_DELETE_URL, kwargs={"pk": car.id})
        )
        self.assertEqual(
            response.context_data["view"].success_url,
            CAR_LIST_URL
        )

    def test_delete_car(self):
        manufacturer = Manufacturer.objects.get(id=1)
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )
        response = self.client.post(
            reverse(CAR_DELETE_URL, kwargs={"pk": car.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(model="test_model").exists())
