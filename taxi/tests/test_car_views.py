from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class PublicCarTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        self.manufacturer.save()

        self.driver = get_user_model().objects.create_user(
            username="Test Driver",
            password="TestPassword123",
        )
        self.driver.save()

        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer,
        )
        self.car.save()
        self.car.drivers.add(self.driver)

        self.urls_list = [
            reverse("taxi:car-list"),
            reverse(
                "taxi:car-detail",
                kwargs={"pk": self.car.id}
            ),
            reverse("taxi:car-create"),
            reverse(
                "taxi:car-update",
                kwargs={"pk": self.car.id}
            ),
            reverse(
                "taxi:car-delete",
                kwargs={"pk": self.car.id}
            )
        ]

    def test_login_required(self):
        response_list = [self.client.get(url) for url in self.urls_list]
        for res in response_list:
            self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Some Country",
        )
        self.manufacturer.save()

        self.driver = get_user_model().objects.create_user(
            username="TestDriver",
            first_name="Test First",
            last_name="Test Last",
            password="TestPassword123",
            license_number="ABC12345",
        )
        self.driver.save()

        self.car1 = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer,
        )
        self.car1.save()
        self.car1.drivers.add(self.driver)

        self.car2 = Car.objects.create(
            model="Other Model",
            manufacturer=self.manufacturer,
        )
        self.car2.save()
        self.car2.drivers.add(self.driver)

        self.client.force_login(self.driver)

        self.urls_list = [
            reverse("taxi:car-list"),
            reverse(
                "taxi:car-detail",
                kwargs={"pk": self.car1.id}
            ),
            reverse("taxi:car-create"),
            reverse(
                "taxi:car-update",
                kwargs={"pk": self.car1.id}
            ),
            reverse(
                "taxi:car-delete",
                kwargs={"pk": self.car1.id}
            )
        ]

        self.response_list = [self.client.get(url) for url in self.urls_list]

        self.templates_list = [
            "taxi/car_list.html",
            "taxi/car_detail.html",
            "taxi/car_form.html",
            "taxi/car_form.html",
            "taxi/car_confirm_delete.html"
        ]

        self.car_list_url = reverse("taxi:car-list")
        self.car_list_response = self.client.get(self.car_list_url)

    def test_user_logged_in_required(self):
        for res in self.response_list:
            self.assertEqual(res.status_code, 200)

    def test_display_all_cars(self):
        cars = Car.objects.all()
        self.assertEqual(
            list(self.car_list_response.context["car_list"]),
            list(cars)
        )

    def test_search_car(self):
        search_car = Car.objects.filter(model__icontains="Test")
        search_car_response = self.client.get(
            self.car_list_url + "?model=Test"
        )
        self.assertEqual(
            list(search_car),
            list(search_car_response.context["car_list"])
        )

    def test_correct_templates(self):
        for num in range(len(self.templates_list)):
            self.assertTemplateUsed(
                self.response_list[num],
                self.templates_list[num]
            )
