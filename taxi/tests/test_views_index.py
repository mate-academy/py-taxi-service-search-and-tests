from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


INDEX_URL = reverse("taxi:index")


class PublicIndexTest(TestCase):
    def test_driver_login_required(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEquals(res, 200)


class IndexViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="Test123",
        )
        self.client.force_login(self.user)

    def test_index_view_url_exists_at_desired_location(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)

    def test_index_view_url_accessible_by_name(self):
        res = self.client.get(INDEX_URL)
        self.assertEqual(res.status_code, 200)

    def test_index_uses_correct_template_name(self):
        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, "taxi/index.html")

    def test_index_has_correct_count_manufacturers(self):
        numbers_of_manufacturers = 7
        for manufacturer_id in range(numbers_of_manufacturers):
            Manufacturer.objects.create(
                name=f"Test{manufacturer_id}",
                country=f"Country{manufacturer_id}",
            )
        res = self.client.get(INDEX_URL)
        self.assertEqual(
            res.context["num_manufacturers"],
            numbers_of_manufacturers
        )

    def test_index_has_correct_count_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        numbers_of_cars = 8
        for car_id in range(numbers_of_cars):
            Car.objects.create(
                model=f"Test{car_id}",
                manufacturer=manufacturer,
            )
        res = self.client.get(INDEX_URL)
        self.assertEqual(res.context["num_cars"], numbers_of_cars)

    def test_index_has_correct_count_drivers(self):
        numbers_of_drivers = 9
        for driver_id in range(numbers_of_drivers):
            get_user_model().objects.create_user(
                username=f"User{driver_id}",
                password="qwe",
                license_number=f"QWE1234{driver_id}"
            )
        res = self.client.get(INDEX_URL)
        self.assertEqual(res.context["num_drivers"], numbers_of_drivers + 1)
