from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

from taxi.models import Car, Manufacturer

URLS = {
    "taxi:index": reverse("taxi:index"),
    "taxi:manufacturer-list": reverse("taxi:manufacturer-list"),
    "taxi:driver-list": reverse("taxi:driver-list"),
    "taxi:car-list": reverse("taxi:car-list")
}


class UnauthorizedAccessTests(TestCase):
    def test_login_required(self):
        for name, url in URLS.items():
            response = self.client.get(url)
            self.assertNotEqual(
                response.status_code,
                200,
                msg=f"Error accessing URL ({name}): "
                    f"{url} returned {response.status_code}"
            )


class AuthorizedAccessTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="testuser",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

    def test_retrieve(self):
        for name, url in URLS.items():
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                200,
                msg=f"Error accessing URL ({name}): "
                    f"{url} returned {response.status_code}"
            )

    def test_driver_list(self):
        driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="password1",
            license_number="AFC12345"
        )
        get_user_model().objects.create_user(
            username="driver2",
            password="password2",
            license_number="DFF67890"
        )

        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(get_user_model().objects.all())
        )

        response_with_search = self.client.get(
            reverse("taxi:driver-list") + "?username=driver1"
        )
        self.assertEqual(response_with_search.status_code, 200)
        self.assertEqual(
            list(response_with_search.context["driver_list"]),
            [driver1]
        )

        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_car_list(self):
        manufacturer = Manufacturer.objects.create(name="VAG",
                                                   country="Germany"
                                                   )
        car1 = Car.objects.create(model="Seat", manufacturer=manufacturer)
        Car.objects.create(model="Skoda", manufacturer=manufacturer)

        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.all())
        )

        response_with_search = self.client.get(
            reverse("taxi:car-list") + "?model=Seat"
        )
        self.assertEqual(response_with_search.status_code, 200)
        self.assertEqual(
            list(response_with_search.context["car_list"]),
            [car1]
        )

        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_manufacturer_list(self):
        Manufacturer.objects.create(name="VAG", country="Germany")
        manufacturer2 = Manufacturer.objects.create(name="Renault",
                                                    country="France"
                                                    )

        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.all())
        )

        response_with_search = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Renault"
        )
        self.assertEqual(response_with_search.status_code, 200)
        self.assertEqual(
            list(response_with_search.context["manufacturer_list"]),
            [manufacturer2]
        )

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
