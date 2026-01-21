from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarSearchForm
from taxi.models import Car

CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", kwargs={"pk": 1})
CAR_CREATE_URL = reverse("taxi:car-create")
CAR_UPDATE_URL = reverse("taxi:car-update", kwargs={"pk": 1})
CAR_DELETE_URL = reverse("taxi:car-delete", kwargs={"pk": 1})


class CarListTests(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_correct_template_used(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_correct_pagination(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_correct_search_form_present(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertTrue("search_form" in response.context)
        self.assertTrue(
            isinstance(response.context["search_form"], CarSearchForm)
        )

    def test_search_form_correct_output(self):
        url = CAR_LIST_URL + "?" + urlencode({"model": "Mitsubishi"})
        response = self.client.get(url)
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__icontains="Mitsubishi")),
        )


class CarDetailTests(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_correct_template_used(self):
        response = self.client.get(CAR_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_toggle_assign(self):
        add = self.client.get(CAR_DETAIL_URL + "toggle-assign/")
        self.assertEqual(add.status_code, 302)
        # check if user is in the drivers list after toggle assign
        response = self.client.get(CAR_DETAIL_URL)
        self.assertTrue(self.user in response.context["car"].drivers.all())

        remove = self.client.get(CAR_DETAIL_URL + "toggle-assign/")
        self.assertEqual(remove.status_code, 302)
        # check if user was removed from the drivers list
        response = self.client.get(CAR_DETAIL_URL)
        self.assertFalse(self.user in response.context["car"].drivers.all())


class CarCreateTests(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_correct_template_used(self):
        response = self.client.get(CAR_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_correct_redirect_after_car_create(self):
        response = self.client.post(
            CAR_CREATE_URL,
            {
                "model": "test_model",
                "manufacturer": 1,
                "drivers": [1]
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, CAR_LIST_URL)


class CarUpdateTests(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_correct_template_used(self):
        response = self.client.get(CAR_UPDATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_correct_redirect_after_car_update(self):
        response = self.client.post(
            CAR_UPDATE_URL,
            {
                "model": "test_model2",
                "manufacturer": 2,
                "drivers": [2]
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, CAR_LIST_URL)


class CarDeleteTests(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_correct_template_used(self):
        response = self.client.get(CAR_DELETE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_confirm_delete.html")

    def test_car_deleted(self):
        response = self.client.post(CAR_DELETE_URL)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(pk=1).exists())

    def test_correct_redirect_after_car_delete(self):
        response = self.client.post(CAR_DELETE_URL)
        self.assertRedirects(response, reverse("taxi:car-list"))


class LoginRequiredTests(TestCase):
    def test_car_list_restricted_to_logged_in(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_detail_restricted_to_logged_in(self):
        response = self.client.get(CAR_DETAIL_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_create_restricted_to_logged_in(self):
        response = self.client.get(CAR_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_update_restricted_to_logged_in(self):
        response = self.client.get(CAR_UPDATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_delete_restricted_to_logged_in(self):
        response = self.client.get(CAR_DELETE_URL)
        self.assertNotEqual(response.status_code, 200)
