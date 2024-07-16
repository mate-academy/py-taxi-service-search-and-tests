from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from taxi.models import Car, Manufacturer
from taxi.views import CarListView

CAR_URL = reverse("taxi:car-list")


class TestLoginRequired(TestCase):

    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class TestCarListView(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test", password="testpass"
        )
        self.client.force_login(self.user)

    def test_handles_empty_car_list(self):
        user = get_user_model().objects.create_user(
            username="testuser2", password="12345", license_number="ASC12345"
        )
        self.client.login(username="testuser2", password="12345")
        request = RequestFactory().get(reverse("taxi:car-list"))
        request.user = user
        response = CarListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context_data["object_list"], [])

    def test_display_correct_car_list_information(self):
        manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        Car.objects.create(model="Test Model", manufacturer=manufacturer)
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Manufacturer")
        self.assertContains(response, "Test Model")

    def test_correct_html(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertTemplateUsed(response, "taxi/car_list.html")


class TestCarDetailedView(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test", password="testpass"
        )
        self.client.force_login(self.user)

    def test_display_correct_car_model_information(self):
        manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        car = Car.objects.create(model="Test Model", manufacturer=manufacturer)
        response = self.client.get(reverse(
            "taxi:car-detail",
            kwargs={"pk": car.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Model")
        self.assertContains(response, "Test Manufacturer")
