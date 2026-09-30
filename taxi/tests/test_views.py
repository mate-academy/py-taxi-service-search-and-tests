from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer, Car


class IndexPageTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
        )

    def test_index_requires_login(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 302)

    def test_index_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)

    def test_num_visits(self):
        self.client.force_login(self.user)
        self.client.get(reverse("taxi:index"))
        self.client.get(reverse("taxi:index"))
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_visits"], 3)

    def test_statistics(self):
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        Manufacturer.objects.create(name="test2", country="test2")
        Car.objects.create(
            manufacturer=manufacturer,
            model="test",
        )
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_drivers"], 1)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_manufacturers"], 2)


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="BMW", country="Germany")

    def test_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "BMW"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Toyota")


class CarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
        )

        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )

        self.car1 = Car.objects.create(
            model="Yaris", manufacturer=manufacturer
        )
        self.car2 = Car.objects.create(
            model="Corolla", manufacturer=manufacturer
        )
        self.user.cars.add(self.car1)
        self.client.force_login(self.user)

    def test_search_on_list_view_page(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Yaris"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Yaris")
        self.assertNotContains(response, "Corolla")

    def test_toggle_assign_to_car_on_detail_view_page(self):
        self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": self.car2.pk})
        )

        self.assertIn(self.car2, self.user.cars.all())

    def test_toggle_delete_from_car_on_detail_view_page(self):
        self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": self.car1.pk})
        )

        self.assertNotIn(self.car1, self.user.cars.all())


class DriverListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
        )
        self.client.force_login(self.user)

        get_user_model().objects.create_user(
            username="Mark",
            password="testpassword1234",
            email="test@test.com",
            license_number="AAA12345",
        )
        get_user_model().objects.create_user(
            username="Lora",
            password="testpassword12546",
            email="testlora@test.com",
            license_number="LLL12345",
        )

    def test_search(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "Mark"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mark")
        self.assertNotContains(response, "Lora")
