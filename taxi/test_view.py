from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

TEST_URLS = [
    reverse("taxi:index"),
    reverse("taxi:car-list"),
    reverse("taxi:car-detail", args=[1]),
    reverse("taxi:car-create"),
    reverse("taxi:car-update", args=[1]),
    reverse("taxi:car-delete", args=[1]),
    reverse("taxi:driver-list"),
    reverse("taxi:driver-detail", args=[1]),
    reverse("taxi:driver-create"),
    reverse("taxi:driver-update", args=[1]),
    reverse("taxi:driver-delete", args=[1]),
    reverse("taxi:manufacturer-list"),
    reverse("taxi:manufacturer-update", args=[1]),
    reverse("taxi:manufacturer-create"),
    reverse("taxi:manufacturer-delete", args=[1]),
]


class TaxiViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass12345")
        self.driver = get_user_model().objects.create(
            username="testuser2",
            password="testpass12355",
            license_number="ABC12345")
        self.car = Car.objects.create(
            model="Model X",
            manufacturer=Manufacturer.objects.create(
                name="Tesla"
            ))
        self.url = reverse("taxi:index")

    def test_index_view_requires_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            "/accounts/login/?next=%2f",
            fetch_redirect_response=False)

    def test_index_view_displays_when_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class PublicViewsTests(TestCase):
    def test_login_required(self) -> None:
        self.assertTrue(all(
            1
            if self.client.get(url).status_code != 200
            else 0
            for url in TEST_URLS
        ))


class PrivateListsViewTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="john",
            password="john12345",
            first_name="John",
            last_name="Doe",
            license_number="JOD12345"
        )
        self.client.force_login(self.driver)

        # Create some test data
        get_user_model().objects.create(
            username="johndoe",
            first_name="John",
            last_name="Doe",
            license_number="JOD00001"
        )
        get_user_model().objects.create(
            username="janedoe",
            first_name="Jane",
            last_name="Doe",
            license_number="JOD00002"
        )
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer1,
        )
        self.car2 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer1,
        )
        self.car3 = Car.objects.create(
            model="3 Series",
            manufacturer=self.manufacturer2,
        )

    def test_search_field_correct_for_drivers(self) -> None:
        url = reverse("taxi:driver-list")
        search_query = "JoHn"
        response = self.client.get(url, {"username": search_query})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, search_query)

        drivers = response.context["object_list"]
        for driver in drivers:
            self.assertTrue(search_query.lower() in driver.username.lower())

    def test_search_field_correct_for_manufacturer(self) -> None:
        url = reverse("taxi:manufacturer-list")
        search_query = "toY"
        response = self.client.get(url, {"name": search_query})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, search_query)

        manufacturers = response.context["object_list"]
        for manufacturer in manufacturers:
            self.assertTrue(search_query.lower() in manufacturer.name.lower())

    def test_search_field_correct_for_cars(self) -> None:
        url = reverse("taxi:car-list")
        search_query = "cAm"
        response = self.client.get(url, {"model": search_query})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, search_query)

        cars = response.context["object_list"]
        for car in cars:
            self.assertTrue(search_query.lower() in car.model.lower())
