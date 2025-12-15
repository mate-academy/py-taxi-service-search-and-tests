from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Manufacturer, Car


def create_user(username="user1", password="testpass123", license_number=None):
    user = get_user_model()
    if license_number is None:
        suffix = sum(ord(c) for c in username) % 100000
        license_number = f"ABC{suffix:05d}"
    return user.objects.create_user(
        username=username,
        password=password,
        license_number=license_number,
        first_name="John",
        last_name="Doe",
    )


class PublicAccessTests(TestCase):
    def test_login_required_views(self):
        protected_urls = [
            reverse("taxi:index"),
            reverse("taxi:manufacturer-list"),
            reverse("taxi:car-list"),
            reverse("taxi:driver-list"),
        ]
        for url in protected_urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)
            self.assertIn("/accounts/login/", response.url)


class PrivateIndexViewTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client.login(username=self.user.username, password="testpass123")

    def test_index_counts_and_visits(self):

        man1 = Manufacturer.objects.create(name="Audi", country="Germany")
        car1 = Car.objects.create(model="A6", manufacturer=man1)
        car1.drivers.add(self.user)

        url = reverse("taxi:index")
        resp1 = self.client.get(url)
        self.assertEqual(resp1.status_code, 200)

        self.assertEqual(
            resp1.context["num_drivers"], get_user_model().objects.count()
        )
        self.assertEqual(resp1.context["num_cars"], Car.objects.count())
        self.assertEqual(
            resp1.context["num_manufacturers"], Manufacturer.objects.count()
        )

        first_visits = resp1.context["num_visits"]
        resp2 = self.client.get(url)
        self.assertEqual(resp2.context["num_visits"], first_visits + 1)


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client.login(username=self.user.username, password="testpass123")
        Manufacturer.objects.create(name="Audi", country="Germany")
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Volkswagen", country="Germany")

    def test_search_by_name_filters_queryset(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"q": "w"})
        self.assertEqual(response.status_code, 200)

        content = response.content.decode()
        self.assertIn("BMW", content)
        self.assertIn("Volkswagen", content)
        self.assertNotIn("Audi", content)


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client.login(username=self.user.username, password="testpass123")
        manufacturer = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )
        Car.objects.create(model="A4", manufacturer=manufacturer)
        Car.objects.create(model="A6", manufacturer=manufacturer)
        Car.objects.create(model="Q7", manufacturer=manufacturer)

    def test_search_by_model_filters_queryset(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"q": "A"})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("A4", content)
        self.assertIn("A6", content)
        self.assertNotIn("Q7", content)


class DriverSearchTests(TestCase):
    def setUp(self):
        self.password = "testpass123"
        self.user = create_user(username="john", password=self.password)
        self.client.login(username=self.user.username, password=self.password)

        create_user(username="johnny")
        create_user(username="alice")
        create_user(username="jo")

    def test_search_by_username_filters_queryset(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"q": "jo"})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("john", content)
        self.assertIn("johnny", content)
        self.assertIn("jo", content)
        self.assertNotIn("alice", content)


class ToggleAssignToCarTests(TestCase):
    def setUp(self):
        self.password = "testpass123"
        self.user = create_user(username="driver1", password=self.password)
        self.m = Manufacturer.objects.create(name="Audi", country="Germany")
        self.car = Car.objects.create(model="A4", manufacturer=self.m)
        self.client.login(username=self.user.username, password=self.password)

    def test_toggle_assign_adds_and_removes_driver(self):
        toggle_url = reverse("taxi:toggle-car-assign", args=[self.car.id])

        self.assertNotIn(self.car, self.user.cars.all())

        resp1 = self.client.post(toggle_url, follow=True)
        self.user.refresh_from_db()
        self.assertIn(self.car, self.user.cars.all())
        self.assertEqual(resp1.status_code, 200)

        resp2 = self.client.post(toggle_url, follow=True)
        self.user.refresh_from_db()
        self.assertNotIn(self.car, self.user.cars.all())
        self.assertEqual(resp2.status_code, 200)

    def test_car_detail_displays_driver_list(self):
        self.user.cars.add(self.car)
        detail_url = reverse("taxi:car-detail", args=[self.car.id])
        resp = self.client.get(detail_url)
        self.assertContains(resp, self.user.username)
