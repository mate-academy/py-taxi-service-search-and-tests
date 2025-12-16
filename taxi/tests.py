from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Manufacturer, Car


class PublicSearchTests(TestCase):

    def test_login_required_for_car_search(self):
        response = self.client.get(reverse("taxi:car-list")
                                   + "?search_query=test")
        self.assertRedirects(response,
                             "/accounts/"
                             "login/?next=/cars/%3Fsearch_query%3Dtest")

    def test_login_required_for_manufacturer_search(self):
        response = self.client.get(reverse("taxi:manufacturer-list")
                                   + "?search_query=test")
        self.assertRedirects(response,
                             "/accounts/"
                             "login/?next=/"
                             "manufacturers/%3Fsearch_query%3Dtest")

    def test_login_required_for_driver_search(self):
        response = self.client.get(reverse("taxi:driver-list")
                                   + "?search_query=test")
        self.assertRedirects(response,
                             "/accounts/"
                             "login/?next=/drivers/%3Fsearch_query%3Dtest")


class PrivateSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
            license_number="TST00000"
        )
        self.client = Client()
        self.client.login(username="testuser",
                          password="testpassword123")

        self.manufacturer1 = (Manufacturer.objects.create
                              (name="BMW", country="Germany"))
        self.manufacturer2 = (Manufacturer.objects.create
                              (name="Mercedes", country="Germany"))

        self.car1 = Car.objects.create(model="X5",
                                       manufacturer=self.manufacturer1)
        self.car2 = Car.objects.create(model="A-Class",
                                       manufacturer=self.manufacturer2)

        self.driver1 = get_user_model().objects.create_user(
            username="ivan_driver",
            password="pass1",
            license_number="IVN12345"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="anna_kate",
            password="pass2",
            license_number="ANN98765"
        )

    def test_search_car_by_model(self):
        response = self.client.get(reverse("taxi:car-list")
                                   + "?search_query=X5")
        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)
        self.assertEqual(len(response.context["car_list"]), 1)

    def test_search_car_model_case_insensitive(self):
        response = self.client.get(reverse("taxi:car-list")
                                   + "?search_query=a-class")
        self.assertContains(response, self.car2.model)
        self.assertEqual(len(response.context["car_list"]), 1)

    def test_search_manufacturer_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list")
                                   + "?search_query=BMW")
        self.assertContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)

    def test_search_driver_by_username(self):
        response = self.client.get(reverse("taxi:driver-list")
                                   + "?search_query=ivan")
        self.assertContains(response, self.driver1.username)
        self.assertNotContains(response, self.driver2.username)
        self.assertEqual(len(response.context["driver_list"]), 1)

    def test_empty_search_shows_all_objects(self):
        response = self.client.get(reverse("taxi:driver-list")
                                   + "?search_query=")
        self.assertEqual(len(response.context["driver_list"]), 3)

    def test_toggle_assign_removes_driver(self):
        self.client.get(reverse("taxi:toggle-car-assign",
                                args=[self.car1.id]))
        self.client.get(reverse("taxi:toggle-car-assign",
                                args=[self.car1.id]))
        car = Car.objects.get(id=self.car1.id)
        self.assertNotIn(self.user, car.drivers.all())

    def test_successful_driver_license_update(self):
        new_license = "UPD77777"
        response = self.client.post(
            reverse("taxi:driver-update", args=[self.user.id]),
            {"license_number": new_license},
            follow=True
        )
        self.assertRedirects(response, reverse("taxi:driver-detail",
                                               args=[self.user.id]))
        self.user.refresh_from_db()
        self.assertEqual(self.user.license_number, new_license)
        self.assertContains(response, new_license)
