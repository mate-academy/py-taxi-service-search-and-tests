# flake8: noqa
from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from taxi.models import Driver, Manufacturer, Car
from django.contrib.auth import get_user_model


class PublicViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_index_public_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(response.status_code, 200)

    def test_driver_delete_public_view(self):
        Driver.objects.create(
            id=1,
            username="test_username",
            password="test_password",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        response = self.client.get(reverse("taxi:driver-delete", kwargs={"pk": 1}))
        self.assertNotEqual(response.status_code, 200)
        self.assertIn("/login/", response.url)

    def test_driver_list_public_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)


class PrivateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password"
        )
        self.client.force_login(self.user)

    def test_index_private_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_visits"], 1)

        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_visits"], 2)
        
        self.assertEqual(response.context["num_drivers"], Driver.objects.all().count())
        self.assertEqual(response.context["num_cars"], Car.objects.all().count())
        self.assertEqual(response.context["num_manufacturers"], Manufacturer.objects.all().count())

    def test_driver_delete_private_view(self):
        driver_id=Driver.objects.create_user(
            username="test_delete_username",
            password="test_password",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="ABC12345"
        ).id
        exitsts_begin = True if Driver.objects.filter(id=driver_id).first() else False
        self.assertEqual(exitsts_begin, True)

        self.client.post(reverse("taxi:driver-delete", kwargs={"pk": driver_id}))
        exitsts_begin = True if Driver.objects.filter(id=driver_id).first() else False
        self.assertEqual(exitsts_begin, False)


class TestSearchSystem(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password"
        )
        self.client.force_login(self.user)
        for i in range(0, 25):
            Driver.objects.create_user(
                username=f"test_username_{i}",
                password="test_passoword",
                license_number=f"ABC1234{i}"
            )
            Manufacturer.objects.create(
                name=f"test_name_{i}",
                country="test_country"
            )
            Car.objects.create(
                model=f"test_model_{i}",
                manufacturer=Manufacturer.objects.get(id=1)
            )

    def test_driver_search_system_by_username(self):
        response = self.client.get(reverse("taxi:driver-list") + "?username=1")
        drivers = Driver.objects.filter(username__icontains="1")[:5]
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_car_search_system_by_model(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=1")
        cars = Car.objects.filter(model__icontains="1")[:5]
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_manufacturer_search_system_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list") + "?name=1")
        manufacturers = Manufacturer.objects.filter(name__icontains="1")[:5]
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )






