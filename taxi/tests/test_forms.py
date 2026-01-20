from django.contrib.auth import get_user_model

from django.test import TestCase

from taxi.models import Car, Manufacturer, Driver


class SearchFormTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "user", "user12345"
        )
        self.client.force_login(self.user)

    def test_car_search(self):
        response = self.client.get("/cars/?model=mercedes")
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["car_list"],
            Car.objects.filter(model__icontains="mercedes"),
        )

    def test_driver_serch(self):
        response = self.client.get("/drivers/?username=Johnny")
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["driver_list"],
            Driver.objects.filter(username__icontains="Johnny")
        )

    def test_manufacturer_search(self):
        response = self.client.get("/manufacturers/?name=Mitsu")
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            Manufacturer.objects.filter(name__icontains="Mitsu")
        )
