from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy, reverse

from taxi.models import Manufacturer, Car

User = get_user_model()

CAR_CREATE = reverse("taxi:car-create")
CAR_LIST = reverse("taxi:car-list")
CAR_DETAIL = reverse("taxi:car-detail", kwargs={"pk": 1})
CAR_UPDATE = reverse("taxi:car-update", kwargs={"pk": 1})
CAR_DELETE = reverse("taxi:car-delete", kwargs={"pk": 1})
CAR_ASSIGN = reverse("taxi:car-assign", kwargs={"pk": 1})

URL_LIST = [
    CAR_CREATE,
    CAR_LIST,
    CAR_DETAIL,
    CAR_UPDATE,
    CAR_DELETE
]


class PublicCarTest(TestCase):
    def test_login_requirement_car_url(self):
        """
        Test that unauthorized user can't get access any car page
        """
        for url in URL_LIST:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertNotEqual(response.status_code, 200)
                self.assertIn("/accounts/login/", response.url)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test_user",
            password="test_password123"
        )
        self.client.force_login(self.user)
        self.some_user = User.objects.create_user(
            username="jonny.depth",
            first_name="jonny",
            last_name="Depth",
            password="test_password",
            license_number="12345678",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        self.car = Car.objects.create(
            model="BMW F90",
            manufacturer=self.manufacturer,
        )
        Car.objects.create(
            model="Audi A6",
            manufacturer=self.manufacturer,
        )

        self.car.drivers.set([self.some_user])

    def test_authorized_user_car_url(self):
        """
           Test that authorized user get access any car page
       """
        for url in URL_LIST:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_get_assign_car_view(self):
        """
           Test that GET request renders the assign confirmation template
           and passes the correct car object to the context.
        """
        response = self.client.get(CAR_ASSIGN)
        self.assertTemplateUsed(response, "taxi/assign_confirm.html")
        self.assertEqual(response.context["car"], self.car)

    def test_post_assign_car_view(self):
        """
            Test that POST request with 'assign=update'
            adds the user to the car's drivers
            and redirects to the car detail page.
        """
        response = self.client.post(CAR_ASSIGN, {"assign": "update"})
        self.assertRedirects(response, self.car.get_absolute_url())
        self.assertIn(self.user, self.car.drivers.all())

    def test_remove_driver_from_car(self):
        """
        Test that POST request with 'assign=remove'
        removes the user from the car's drivers
        and redirects to the car detail page.
        """
        response = self.client.post(CAR_ASSIGN, {"assign": "remove"})
        self.assertNotIn(self.user, self.car.drivers.all())
        self.assertRedirects(response, self.car.get_absolute_url())

    def test_retrieve_cars(self):
        response = self.client.get(CAR_LIST)
        self.assertEqual(list(
            response.context["car_list"]),
            list(Car.objects.all())
        )
