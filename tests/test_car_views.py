from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


CAR_LIST_VIEW = "/cars/"
CAR_DETAIL_VIEW = "/cars/1/"
CAR_CREATE_VIEW = "/cars/create/"
CAR_UPDATE_VIEW = "/cars/1/update/"
CAR_DELETE_VIEW = "/cars/1/delete/"
CAR_TOGGLE_ASSIGN_VIEW = "/cars/1/toggle-assign/"


class PublicCarTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="Nissan Motor Co.",
            country="Japan"
        )
        Car.objects.create(model="Nissan X-Trail", manufacturer=manufacturer)

    def test_car_list_page_requires_login(self):
        response = self.client.get(CAR_LIST_VIEW)
        self.assertNotEqual(response.status_code, 200)

    def test_car_detail_page_requires_login(self):
        response = self.client.get(CAR_DETAIL_VIEW)
        self.assertNotEqual(response.status_code, 200)

    def test_car_create_page_requires_login(self):
        response = self.client.get(CAR_CREATE_VIEW)
        self.assertNotEqual(response.status_code, 200)

    def test_car_update_page_requires_login(self):
        response = self.client.get(CAR_UPDATE_VIEW)
        self.assertNotEqual(response.status_code, 200)

    def test_car_delete_page_requires_login(self):
        response = self.client.get(CAR_DELETE_VIEW)
        self.assertNotEqual(response.status_code, 200)

    def test_car_toggle_assign_page_requires_login(self):
        response = self.client.get(CAR_TOGGLE_ASSIGN_VIEW)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="Nissan Motor Co.",
            country="Japan"
        )
        Car.objects.create(model="Nissan X-Trail", manufacturer=manufacturer)
        Car.objects.create(model="Nissan JUKE", manufacturer=manufacturer)

    def setUp(self) -> None:
        user = get_user_model().objects.create(
            username="test_user",
            password="test123user"
        )
        self.client.force_login(user)

    # Test if all the pages are accessible
    def test_retrieve_car_list(self):
        response = self.client.get(CAR_LIST_VIEW)
        cars_list = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars_list)
        )

    def test_retrieve_car_detail_page(self):
        response = self.client.get(CAR_DETAIL_VIEW)
        car = Car.objects.get(id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["car"], car)

    def test_retrieve_car_create_page(self):
        response = self.client.get(CAR_CREATE_VIEW)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_car_update_page(self):
        response = self.client.get(CAR_UPDATE_VIEW)
        car = Car.objects.get(id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["car"], car)

    def test_retrieve_car_delete_page(self):
        response = self.client.get(CAR_DELETE_VIEW)
        car = Car.objects.get(id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["car"], car)

    def test_retrieve_car_toggle_assign_page(self):
        response = self.client.get(CAR_UPDATE_VIEW)
        car = Car.objects.get(id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["car"], car)

    # Test if all the pages are accessible by their name
    def test_retrieve_car_list_by_name(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

    def test_retrieve_car_detail_page_by_name(self):
        response = self.client.get(reverse("taxi:car-detail", args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_retrieve_car_create_page_by_name(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(response.status_code, 200)

    def test_retrieve_car_update_page_by_name(self):
        response = self.client.get(reverse("taxi:car-update", args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_retrieve_car_delete_page_by_name(self):
        response = self.client.get(reverse("taxi:car-delete", args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_search_car_by_model(self):
        search_field = "model"
        search_value = "rail"
        url = f"{CAR_LIST_VIEW}?{search_field}={search_value}"
        response = self.client.get(url)

        expected_queryset = Car.objects.filter(
            model__icontains=search_value
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["object_list"]),
            list(expected_queryset)
        )

    def test_toggle_assign_to_car(self):
        car = Car.objects.get(id=1)
        user = get_user_model().objects.get(id=1)

        # Test assigning driver to the car
        self.client.get(CAR_TOGGLE_ASSIGN_VIEW)
        self.assertEqual(list(car.drivers.all()), [user])

        # Test deleting driver from the car
        self.client.get(CAR_TOGGLE_ASSIGN_VIEW)
        self.assertEqual(list(car.drivers.all()), [])
