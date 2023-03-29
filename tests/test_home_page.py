from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Car, Manufacturer


TestCase.fixtures = ["taxi_service_db_data.json", ]
HOME_PAGE_URL = "taxi:index"


class PublicHomePageTests(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse(HOME_PAGE_URL))
        self.assertNotEqual(response.status_code, 200)


class PrivateHomePageTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password_123"
        )
        self.client.force_login(self.user)

    def test_login_required(self):
        response = self.client.get(reverse(HOME_PAGE_URL))
        self.assertEqual(response.status_code, 200)

    def test_index_response_with_correct_template(self):
        response = self.client.get(reverse(HOME_PAGE_URL))
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_index_displays_data_correctly(self):
        response = self.client.get(reverse(HOME_PAGE_URL))

        num_drivers = get_user_model().objects.count()
        num_cars = Car.objects.count()
        num_manufacturers = Manufacturer.objects.count()

        self.assertEqual(response.context["num_drivers"], num_drivers)
        self.assertEqual(response.context["num_cars"], num_cars)
        self.assertEqual(
            response.context["num_manufacturers"], num_manufacturers
        )
