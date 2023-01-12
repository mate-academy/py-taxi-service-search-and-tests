from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicViewsTests(TestCase):

    def test_index_login_required(self):
        index_url = reverse("taxi:index")
        self.client = Client()
        response = self.client.get(index_url)

        self.assertNotEqual(response.status_code, 200)


class PrivateViewsTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user_test_views",
            password="testuserpassword",
            license_number="KAT12345",
        )
        self.client = Client()
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Mitsubishi", country="Japan"
        )

        self.manufacturer2 = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )

        self.manufacturer3 = Manufacturer.objects.create(
            name="Renault", country="France"
        )

        self.car1 = Car.objects.create(
            model="Eclipse", manufacturer=self.manufacturer1
        )

        self.car2 = Car.objects.create(
            model="Lancer", manufacturer=self.manufacturer1
        )

        self.car3 = Car.objects.create(
            model="Pajero", manufacturer=self.manufacturer1
        )

        self.driver1 = get_user_model().objects.create(
            username="test_driver_1",
            password="test_driver_1_password",
            license_number="QWE12345"
        )

        self.driver2 = get_user_model().objects.create(
            username="test_driver_12",
            password="test_driver_12_password",
            license_number="QWE12346"
        )

        self.driver3 = get_user_model().objects.create(
            username="test_driver_2",
            password="test_driver_2_password",
            license_number="QWE12347"
        )

    def test_index_correct_objects_counting(self):
        index_url = reverse("taxi:index")
        response = self.client.get(index_url)
        quant_db_objects = {
            "manufacturers": Manufacturer.objects.count(),
            "drivers": get_user_model().objects.count(),
            "cars": Car.objects.count()
        }

        self.assertEqual(
            response.context["num_manufacturers"],
            quant_db_objects["manufacturers"]
        )
        self.assertEqual(
            response.context["num_drivers"],
            quant_db_objects["drivers"]
        )
        self.assertEqual(
            response.context["num_cars"],
            quant_db_objects["cars"]
        )
        self.assertEqual(
            response.context["num_visits"],
            1
        )
        self.assertEqual(
            response.context["num_visits"],
            1
        )

    def test_manufacturer_list_view_search_by_name(self):

        form_data = {
            "name": "t"
        }
        response = self.client.get(
            reverse("taxi:manufacturer-list") + f"?name={form_data['name']}"
        )
        expected_queryset = Manufacturer.objects.filter(
            name__icontains=form_data["name"]
        )

        self.assertQuerysetEqual(
            list(response.context["manufacturer_list"]),
            list(expected_queryset)
        )

    def test_car_list_view_search_by_model(self):

        form_data = {
            "model": "l"
        }
        response = self.client.get(
            reverse("taxi:car-list") + f"?model_={form_data['model']}"
        )
        expected_queryset = Car.objects.filter(
            model__icontains=form_data["model"]
        )

        self.assertQuerysetEqual(
            list(response.context["car_list"]),
            list(expected_queryset)
        )

    def test_driver_list_view_search_by_username(self):

        form_data = {
            "username": "2"
        }
        response = self.client.get(
            reverse("taxi:driver-list") + f"?username={form_data['username']}"
        )
        expected_queryset = get_user_model().objects.filter(
            username__icontains=form_data["username"]
        )

        self.assertQuerysetEqual(
            list(response.context["driver_list"]),
            list(expected_queryset))

    def test_toggle_assign_view_on_car_detail(self):

        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": self.car1.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign me to this car", html=True)

        self.client.get(reverse("taxi:car-detail", kwargs={"pk": self.car1.pk})
                        + "toggle-assign/")

        response_after_assign = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": self.car1.pk})
        )
        self.assertTrue(self.user in self.car1.drivers.all())
        self.assertContains(
            response_after_assign, "Delete me from this car", html=True
        )

        self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": self.car1.pk})
            + "toggle-assign/"
        )

        response_after_remove = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": self.car1.pk})
        )
        self.assertFalse(self.user in self.car1.drivers.all())
        self.assertContains(
            response_after_remove,
            "Assign me to this car",
            html=True
        )
