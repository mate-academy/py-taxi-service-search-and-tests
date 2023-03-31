from django.urls import reverse
from taxi.forms import CarSearchForm
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy
from taxi.models import Car, Manufacturer


class ToggleAssignToCarTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        self.driver = self.user_model.objects.create_superuser(
            username="testuser", password="testpass"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )

    def test_toggle_assign_to_car(self):
        self.assertEqual(self.driver.cars.count(), 0)

        self.client.login(username="testuser", password="testpass")

        response = self.client.post(
            reverse_lazy("taxi:toggle-car-assign", args=[self.car.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Car.objects.get(pk=self.car.pk) in self.driver.cars.all()
        )

        response = self.client.post(
            reverse_lazy("taxi:toggle-car-assign", args=[self.car.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Car.objects.get(pk=self.car.pk) in self.driver.cars.all()
        )

        self.client.logout()

    def tearDown(self):
        self.driver.delete()
        self.car.delete()


class CarListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_superuser(
            username="testuser", password="testpass"
        )
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Honda",
            country="Japan"
        )
        self.car1 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer1,
        )
        self.car2 = Car.objects.create(
            model="Civic",
            manufacturer=self.manufacturer2,
        )

    def test_car_list_view_with_search_query(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Camry"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Civic")
        self.assertIsInstance(response.context["search_form"], CarSearchForm)

    def test_car_list_view_without_search_query(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertContains(response, "Civic")
        self.assertIsInstance(response.context["search_form"], CarSearchForm)

    def test_get_queryset_without_query_params(self):
        # Test that the method returns all cars without any filters applied
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 2)
        self.assertQuerysetEqual(
            response.context["object_list"],
            [self.car1, self.car2],
            ordered=False
        )

    def test_get_queryset_with_query_params(self):
        # Test that the method filters cars based on query params
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("taxi:car-list"), {"model": "Camry"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 1)
        self.assertEqual(response.context["object_list"][0], self.car1)


