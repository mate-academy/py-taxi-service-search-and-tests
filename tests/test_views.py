from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class PublicIndexTest(TestCase):
    def test_index_login_required(self) -> None:
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/"
        )


class PrivateIndexTest(TestCase):
    def setUp(self) -> None:
        num_drivers = 4
        num_manufacturers = 2
        for driver_id in range(num_drivers):
            get_user_model().objects.create_user(
                username=f"test username {driver_id}",
                password=f"test12{driver_id}",
                license_number=f"AAA1234{driver_id}"
            )

        for manufacturer_id in range(num_manufacturers):
            Manufacturer.objects.create(
                name=f"test manufacturer {manufacturer_id}",
                country=f"test country {manufacturer_id}"
            )

        test_car1 = Car.objects.create(
            model="test car 1",
            manufacturer_id=1,
        )
        test_car2 = Car.objects.create(
            model="test car 2",
            manufacturer_id=2,
        )

        test_car1.drivers.set(get_user_model().objects.all()[:2])
        test_car1.drivers.set(get_user_model().objects.all()[2:])

        test_car1.save()
        test_car2.save()

        self.client.login(
            username="test username 0",
            password="test120",
            license_number="AAA12340"
        )

    def test_index_correct_template(self) -> None:
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(str(response.context["user"]), "test username 0 ( )")

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "taxi/index.html")

    def test_index_num_drivers(self) -> None:
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.context["num_drivers"], 4)

    def test_index_num_cars(self) -> None:
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.context["num_cars"], 2)

    def test_index_num_manufacturers(self) -> None:
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.context["num_manufacturers"], 2)

    def test_index_num_visits(self) -> None:
        for _ in range(5):
            self.client.get(reverse("taxi:index"))
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.context["num_visits"], 6)
