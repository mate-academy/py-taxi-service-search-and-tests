from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


class SearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="Testuser",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_car_correct_search(self):
        manufacturer_1 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        car_1 = Car.objects.create(
            model="TestCarA",
            manufacturer=manufacturer_1,
        )
        car_2 = Car.objects.create(
            model="TestCarA",
            manufacturer=manufacturer_1,
        )
        Car.objects.create(
            model="TestCarB",
            manufacturer=manufacturer_1,
        )
        url = reverse("taxi:car-list")
        res = self.client.get(f"{url}?model=TestCarA")
        self.assertEqual(list(res.context["car_list"]), [car_1, car_2])
        self.assertEqual(res.wsgi_request.GET.get("model"), "TestCarA")

        new_url = reverse("taxi:car-list")
        new_res = self.client.get(new_url)
        self.assertEqual(
            list(new_res.context["car_list"]),
            list(Car.objects.all()))

    def test_car_return_empty_search(self):
        manufacturer_1 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Car.objects.create(
            model="TestCarA",
            manufacturer=manufacturer_1,
        )
        Car.objects.create(
            model="TestCarA",
            manufacturer=manufacturer_1,
        )
        Car.objects.create(
            model="TestCarB",
            manufacturer=manufacturer_1,
        )
        url = reverse("taxi:car-list")
        res = self.client.get(f"{url}?model=TestCarG")
        self.assertEqual(list(res.context["car_list"]), [])

    def test_manufacturer_correct_search(self):
        manufacturer_1 = Manufacturer.objects.create(
            name="BMWT",
            country="Germany"
        )
        Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        manufacturer_2 = Manufacturer.objects.create(
            name="OpelT",
            country="Germany"
        )
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(f"{url}?name=t")
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            [manufacturer_1, manufacturer_2]
        )
        self.assertEqual(res.wsgi_request.GET.get("name"), "t")

        new_url = reverse("taxi:manufacturer-list")
        new_res = self.client.get(new_url)
        self.assertEqual(
            list(new_res.context["manufacturer_list"]),
            list(Manufacturer.objects.all()))

    def test_manufacturer_return_empty_search(self):
        Manufacturer.objects.create(
            name="BMWT",
            country="Germany"
        )
        Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        Manufacturer.objects.create(
            name="OpelT",
            country="Germany"
        )
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(f"{url}?name=G")
        self.assertEqual(list(res.context["manufacturer_list"]), [])

    def test_driver_correct_search(self):
        driver_1 = get_user_model().objects.create_user(
            username="John",
            password="testuser1",
            license_number="TES12345"
        )
        driver_2 = get_user_model().objects.create_user(
            username="Tom",
            password="testuser2",
            license_number="TES12346"
        )
        get_user_model().objects.create_user(
            username="Jeremmy",
            password="testuser3",
            license_number="TES12347"
        )
        url = reverse("taxi:driver-list")
        res = self.client.get(f"{url}?username=o")
        self.assertEqual(
            list(res.context["driver_list"]),
            [driver_1, driver_2]
        )
        self.assertEqual(res.wsgi_request.GET.get("username"), "o")

        new_url = reverse("taxi:driver-list")
        new_res = self.client.get(new_url)
        self.assertEqual(
            list(new_res.context["driver_list"]),
            list(get_user_model().objects.all()))

    def test_driver_return_empty_search(self):
        get_user_model().objects.create_user(
            username="John",
            password="testuser1",
            license_number="TES12345"
        )
        get_user_model().objects.create_user(
            username="Tom",
            password="testuser2",
            license_number="TES12346"
        )
        get_user_model().objects.create_user(
            username="Jeremmy",
            password="testuser3",
            license_number="TES12347"
        )
        url = reverse("taxi:driver-list")
        res = self.client.get(f"{url}?username=g")
        self.assertEqual(
            list(res.context["driver_list"]),
            []
        )
