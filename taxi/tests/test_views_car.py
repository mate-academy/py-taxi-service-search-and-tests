from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Manufacturer, Car

CAR_LIST = reverse("taxi:car-list")


class PublicCarTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        """test client login on list_car"""
        response = self.client.get(CAR_LIST)
        self.assertNotEqual(response.status_code, 200)

    def test_create_car_list_required(self):
        """test client create the user profile on list_car"""
        response = self.client.get("taxi:car-create")
        self.assertNotEqual(response.status_code, 200)


class PrivetCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="qwer1234"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Countrytest"
        )

    def test_create_required_car_with_login(self):
        """test should create the name and country and expect it"""
        Car.objects.create(model="test", manufacturer=self.manufacturer)
        response = self.client.get(CAR_LIST)

        self.assertEqual(response.status_code, 200)

    def test_required_queryset_in_db_car_with_login(self):
        """test should required the model in db"""
        Car.objects.create(model="test", manufacturer=self.manufacturer)
        car_all = Car.objects.all()
        response = self.client.get(CAR_LIST)

        self.assertEqual(list(response.context["car_list"]), list(car_all))

    def test_link_template_should_be_car_list_with_login(self):
        """test should required template in right link"""
        Car.objects.create(model="test", manufacturer=self.manufacturer)
        response = self.client.get(CAR_LIST)

        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_update_required_in_detail_manufacturer_with_login(self):
        """test should update the car in detail list"""
        car_update = Car.objects.create(
            model="test", manufacturer=self.manufacturer
        )
        url_to_car = reverse(
            "taxi:car-update", args=[car_update.id]
        )
        response = self.client.get(url_to_car)
        self.assertEqual(response.status_code, 200)

    def test_delete_required_in_detail_manufacturer_with_login(self):
        """test should delete the car in detail list"""
        car_delete = Car.objects.create(
            model="test", manufacturer=self.manufacturer
        )
        url_to_delete = reverse(
            "taxi:car-delete", args=[car_delete.id]
        )
        response = self.client.post(url_to_delete)
        self.assertEqual(response.status_code, 302)


class SearchCarTests(TestCase):
    """test the search car field"""
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345",
        )
        self.client.force_login(self.user)

    def test_car_search_field(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=test")
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__icontains="test")),
        )
