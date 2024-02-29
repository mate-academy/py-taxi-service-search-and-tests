from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")
CAR_DETAIL_URL = reverse("taxi:car-detail", kwargs={"pk": 1})
CAR_UPDATE_URL = reverse("taxi:car-update", kwargs={"pk": 1})
CAR_DELETE_URL = reverse("taxi:car-delete", kwargs={"pk": 1})
CAR_ASSIGN_URL = reverse("taxi:toggle-car-assign", kwargs={"pk": 1})


class PublicCarTest(TestCase):

    def test_login_required(self):
        for url in (
                CAR_LIST_URL,
                CAR_CREATE_URL,
                CAR_DETAIL_URL,
                CAR_UPDATE_URL,
                CAR_DELETE_URL,
                CAR_ASSIGN_URL
        ):
            res = self.client.get(url)

            self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test1234"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.first_car = Car.objects.create(
            model="i8",
            manufacturer=self.manufacturer
        )
        self.second_car = Car.objects.create(
            model="X6",
            manufacturer=self.manufacturer
        )

    def test_retrieve_cars(self):
        res = self.client.get(CAR_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]),
            list(Car.objects.all())
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_cars_search_filter(self):
        url = f"{CAR_LIST_URL}?model=8"
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertIn("search_form", res.context)
        self.assertEqual(list(res.context["car_list"]), [self.first_car])

    def test_toggle_car_assign(self):
        res = self.client.get(CAR_ASSIGN_URL)

        self.assertEqual(res.status_code, 302)
        self.assertEqual(list(self.first_car.drivers.all()), [self.user])

        res = self.client.get(CAR_ASSIGN_URL)

        self.assertEqual(res.status_code, 302)
        self.assertEqual(list(self.first_car.drivers.all()), [])
