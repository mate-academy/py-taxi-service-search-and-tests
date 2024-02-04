from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarSearchForm, CarForm
from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")


class PublicCarTest(TestCase):
    def test_list_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_create_login_required(self):
        res = self.client.get(CAR_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_update_delete_login_required(self):
        manufacturer = Manufacturer.objects.create(
            name="Test_name",
            country="Test_country"
        )
        Car.objects.create(
            manufacturer=manufacturer,
            model="Test_model"
        )
        res = self.client.get(reverse(
            "taxi:car-update",
            kwargs={"pk": 1}
        ))
        self.assertNotEqual(res.status_code, 200)

        res = self.client.get(reverse(
            "taxi:car-delete",
            kwargs={"pk": 1}
        ))
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test_name",
            country="Test_country"
        )

    def test_retrieve_car_list(self):
        for i in range(3):
            Car.objects.create(
                manufacturer=self.manufacturer,
                model=f"Test_model{i}"
            )

        res = self.client.get(CAR_LIST_URL)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]),
            list(Car.objects.all())
        )

    def test_get_content_data(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertIsInstance(
            res.context["search_form"],
            CarSearchForm
        )

    def test_search_form_queryset(self):
        for i in range(5):
            Car.objects.create(
                manufacturer=self.manufacturer,
                model=f"Test_model{i}"
            )
        res = self.client.get(
            CAR_LIST_URL,
            {"model": "Test_model3"}
        )
        self.assertEqual(
            list(res.context["car_list"]),
            list(Car.objects.filter(model__icontains="Test_model3"))
        )
