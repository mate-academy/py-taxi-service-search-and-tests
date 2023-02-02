from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
CARS_URL = reverse("taxi:car-list")
DRIVERS_URL = reverse("taxi:driver-list")
INDEX_URL = reverse("taxi:index")


class LoginRequiredTest(TestCase):
    def test_login_required_for_manufacturer_list_view(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_car_list_view(self):
        response = self.client.get(CARS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_driver_list_view(self):
        response = self.client.get(DRIVERS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_for_index(self):
        response = self.client.get(INDEX_URL)
        self.assertNotEqual(response.status_code, 200)


class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_manufacturers = 2
        number_of_cars = 2
        number_of_drivers = 2

        for manufacturer_id in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name=f"Name {manufacturer_id}",
                country=f"Country {manufacturer_id}",
            )

        for car_id in range(number_of_cars):
            Car.objects.create(
                model=f"Model {car_id}",
                manufacturer=Manufacturer.objects.get(id=car_id + 1)
            )

        for driver_id in range(number_of_drivers):
            get_user_model().objects.create_user(
                username=f"Username {driver_id}",
                password="test12345",
                license_number=f"XXX1234{driver_id}"
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="UserName",
            password="Pass12345"
        )
        self.client.force_login(self.user)
        self.response = self.client.get(INDEX_URL)

    def test_index_view_url_exists_at_desired_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_index_view_url_accessible_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_index_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "taxi/index.html")

    def test_index_view_shows_correct_content(self):
        num_cars = self.response.context["num_cars"]
        num_drivers = self.response.context["num_drivers"]
        num_manufacturers = self.response.context["num_manufacturers"]
        num_visits = self.response.context["num_visits"]

        self.assertEqual(num_cars, 2)
        self.assertEqual(num_drivers, 3)
        self.assertEqual(num_manufacturers, 2)
        self.assertEqual(num_visits, 1)
