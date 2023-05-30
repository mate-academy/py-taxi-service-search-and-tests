from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


class TestCarListView(TestCase):
    def setUp(self):
        megamanufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )
        self.client = Client()
        Car.objects.create(model="supercar", manufacturer=megamanufacturer)
        Car.objects.create(model="megacar", manufacturer=megamanufacturer)
        Car.objects.create(model="ubercar", manufacturer=megamanufacturer)
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )

    def test_search_field(self):
        self.client.force_login(self.user)
        get_value = "MeGa"
        url = reverse("taxi:car-list") + f"?model={get_value}"

        response = self.client.get(url)
        car_query = Car.objects.filter(model__icontains=get_value)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(car_query))

    def test_login_required(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)

        self.assertNotEquals(response.status_code, 200)
