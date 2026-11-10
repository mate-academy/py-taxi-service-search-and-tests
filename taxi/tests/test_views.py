from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

INDEX_URL = reverse("taxi:index")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicViewsTests(TestCase):
    def test_login_required(self) -> None:
        for url in (
            INDEX_URL,
            MANUFACTURER_LIST_URL,
            CAR_LIST_URL,
            DRIVER_LIST_URL,
        ):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertIn(reverse("login"), response.url)


class PrivateViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test.user",
            password="Test12345!",
            license_number="TST12345",
        )
        self.client.force_login(self.user)
        self.lincoln = Manufacturer.objects.create(
            name="Lincoln",
            country="USA",
        )
        self.bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        Car.objects.create(model="Continental", manufacturer=self.lincoln)
        Car.objects.create(model="X5", manufacturer=self.bmw)

    def test_index_counts_visits(self) -> None:
        for visit in range(1, 4):
            response = self.client.get(INDEX_URL)
            self.assertEqual(response.context["num_visits"], visit)

    def test_manufacturer_list_search_by_name(self) -> None:
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "lin"})
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            [self.lincoln],
        )

    def test_car_list_search_by_model(self) -> None:
        response = self.client.get(CAR_LIST_URL, {"model": "x"})
        self.assertEqual(
            [car.model for car in response.context["car_list"]],
            ["X5"],
        )

    def test_driver_list_search_by_username(self) -> None:
        get_user_model().objects.create_user(
            username="another",
            password="Test12345!",
            license_number="ANT12345",
        )
        response = self.client.get(DRIVER_LIST_URL, {"username": "TEST"})
        self.assertEqual(list(response.context["driver_list"]), [self.user])

    def test_empty_search_returns_all(self) -> None:
        response = self.client.get(CAR_LIST_URL, {"model": ""})
        self.assertEqual(len(response.context["car_list"]), 2)

    def test_search_form_keeps_entered_value(self) -> None:
        response = self.client.get(CAR_LIST_URL, {"model": "x5"})
        self.assertEqual(
            response.context["search_form"].initial["model"],
            "x5",
        )

    def test_pagination_keeps_search_query(self) -> None:
        for number in range(6):
            Car.objects.create(
                model=f"Model {number}",
                manufacturer=self.bmw,
            )
        response = self.client.get(CAR_LIST_URL, {"model": "model"})
        self.assertContains(response, "?model=model&amp;page=2")

    def test_toggle_assign_to_car(self) -> None:
        car = Car.objects.get(model="X5")
        url = reverse("taxi:toggle-car-assign", args=[car.id])
        self.client.get(url)
        self.assertIn(self.user, car.drivers.all())
        self.client.get(url)
        self.assertNotIn(self.user, car.drivers.all())

    def test_create_driver(self) -> None:
        form_data = {
            "username": "new_user",
            "password1": "User12345test",
            "password2": "User12345test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "NEW12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username="new_user")
        self.assertEqual(new_user.license_number, "NEW12345")
        self.assertTrue(new_user.check_password("User12345test"))
