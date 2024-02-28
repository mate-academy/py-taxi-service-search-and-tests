from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_PK = 1
CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", kwargs={"pk": CAR_PK})
CAR_ASSIGN_URL = reverse("taxi:toggle-car-assign", kwargs={"pk": CAR_PK})


class PublicCarViewsTest(TestCase):
    def test_login_required(self):
        for url in [CAR_DETAIL_URL, CAR_LIST_URL]:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)


class PrivateCarViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="papajoe",
            password="$ecreT_550",
            license_number="MAN99901"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Bumga Gamga",
            country="Poltava"
        )
        self.car = Car.objects.create(
            model="Enzo",
            manufacturer=self.manufacturer
        )
        self.another_car = Car.objects.create(
            model="McQueen",
            manufacturer=self.manufacturer
        )

    def test_car_list_url_response(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_has_cars(self):
        response = self.client.get(CAR_LIST_URL)
        all_cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(all_cars)
        )

    def test_car_search_form_exists(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertContains(response, "Search by model")


    def test_car_detail_view_shows_relation_fields(self):
        self.car.drivers.add(self.user)
        response = self.client.get(CAR_DETAIL_URL)
        page_content = response.content.decode("utf-8")

        self.assertIn(str(self.user), page_content)
        self.assertIn(
            f"{self.manufacturer.name}, {self.manufacturer.country}",
            page_content
        )

    def test_car_detail_view_assign_driver_button(self):
        self.client.get(CAR_ASSIGN_URL)
        car = Car.objects.get(pk=CAR_PK)
        self.assertEqual(
            list(car.drivers.all()), [self.user]
        )

        self.client.get(CAR_ASSIGN_URL)
        car.refresh_from_db()
        self.assertEqual(
            list(car.drivers.all()), []
        )
