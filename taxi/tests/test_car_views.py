from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", kwargs={"pk": 1})


class PublicCarListTests(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCarListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="ABBA", country="Sweden")
        Car.objects.create(model="Fast Car", manufacturer_id=1)
        Car.objects.create(model="Slow Car", manufacturer_id=1)
        Car.objects.create(model="Slower Car", manufacturer_id=1)

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_car_by_model(self):
        search_param = "slow"
        search_car_url = CAR_LIST_URL + "?model=" + search_param

        response = self.client.get(search_car_url)
        cars = Car.objects.filter(
            model__icontains=search_param
        )

        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )


class PublicCarDetailTests(TestCase):
    def test_login_required(self):
        Manufacturer.objects.create(name="ABBA", country="Sweden")
        Car.objects.create(model="Fast Car", manufacturer_id=1)

        response = self.client.get(CAR_DETAIL_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarDetailTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="ABBA", country="Sweden")
        Car.objects.create(model="Fast Car", manufacturer_id=1)

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        response = self.client.get(CAR_DETAIL_URL)
        car_detail = Car.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["car"], car_detail)
        self.assertTemplateUsed(response, "taxi/car_detail.html")


class PublicCarCreateTests(TestCase):
    def test_public_login_required(self):
        response = self.client.get(reverse("taxi:car-create"))

        self.assertNotEqual(response.status_code, 200)


class PrivateCarCreateTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_create_car(self):
        response = self.client.get(reverse("taxi:car-create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")


class PublicCarUpdateTests(TestCase):
    def test_public_login_required(self):
        Manufacturer.objects.create(name="ABBA", country="Sweden")
        Car.objects.create(model="Fast Car", manufacturer_id=1)
        response = self.client.get(
            reverse("taxi:car-update", kwargs={"pk": 1})
        )

        self.assertNotEqual(response.status_code, 200)


class PrivateCarUpdateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="ABBA", country="Sweden")
        Car.objects.create(model="Fast Car", manufacturer_id=1)

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_update_car(self):
        response = self.client.get(
            reverse("taxi:car-update", kwargs={"pk": 1})
        )
        car = Car.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["car"], car)
        self.assertTemplateUsed(response, "taxi/car_form.html")


class PublicCarDeleteTests(TestCase):
    def test_public_login_required(self):
        Manufacturer.objects.create(name="ABBA", country="Sweden")
        Car.objects.create(model="Fast Car", manufacturer_id=1)
        response = self.client.get(
            reverse("taxi:car-delete", kwargs={"pk": 1})
        )

        self.assertNotEqual(response.status_code, 200)


class PrivateCarDeleteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="ABBA", country="Sweden")
        Car.objects.create(model="Fast Car", manufacturer_id=1)

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_delete_car(self):
        response = self.client.get(
            reverse("taxi:car-delete", kwargs={"pk": 1})
        )
        car = Car.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["car"], car)
        self.assertTemplateUsed(response, "taxi/car_confirm_delete.html")


class PublicCarToggleAssignTests(TestCase):
    def test_public_login_required(self):
        response = self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": 1})
        )

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            "/accounts/login/?next=%2Fcars%2F1%2Ftoggle-assign%2F",
            302
        )


class PrivateCarToggleAssignTests(TestCase):
    def setUp(self) -> None:
        Manufacturer.objects.create(name="ABBA", country="Sweden")
        Car.objects.create(model="Fast Car", manufacturer_id=1)
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_assing_to_driver(self):
        driver = get_user_model().objects.get(id=1)
        car = Car.objects.get(id=1)
        response = self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": 1})
        )

        self.assertRedirects(
            response, reverse("taxi:car-detail", kwargs={"pk": 1}), 302
        )
        self.assertEqual(list(car.drivers.all()), [driver])

    def test_unassign_from_driver(self):
        driver = get_user_model().objects.get(id=1)
        car = Car.objects.get(id=1)
        driver.cars.add(car)

        response = self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": 1})
        )

        self.assertRedirects(
            response, reverse("taxi:car-detail", kwargs={"pk": 1}), 302
        )
        self.assertNotEqual(list(car.drivers.all()), [driver])
