from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


test_user = {
    "username": "driver",
    "password": "password",
    "license_number": "AAA11111",
}


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            **test_user
        )
        self.client.force_login(self.user)
        self.url = reverse("taxi:car-list")
        self.manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_get_car_list(self):
        Car.objects.create(
            model="Ford Focus",
            manufacturer=self.manufacturer,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertEqual(
            list(Car.objects.all()),
            list(response.context["object_list"]),
        )

    def test_search_car_list(self):
        ford_focus = Car.objects.create(
            model="Ford Focus",
            manufacturer=self.manufacturer,
        )
        ford_fusion = Car.objects.create(
            model="Ford Fusion",
            manufacturer=self.manufacturer,
        )
        response = self.client.get(self.url, {"model": "focus"})
        self.assertIn(ford_focus, response.context["object_list"])
        self.assertNotIn(ford_fusion, response.context["object_list"])

    def test_search_empty_car_list(self):
        Car.objects.create(
            model="Ford Focus",
            manufacturer=self.manufacturer,
        )
        response = self.client.get(self.url, {"model": "fusion"})
        self.assertEqual(0, len(response.context["object_list"]))


class CarCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            **test_user
        )
        self.client.force_login(self.user)
        self.url = reverse("taxi:car-create")
        self.manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_create_car_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_can_create_car(self):
        response = self.client.post(
            self.url,
            data={
                "model": "Ford Focus",
                "manufacturer": self.manufacturer.pk,
                "drivers": (self.user.pk,),
            }
        )
        car = Car.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertEqual(Car.objects.count(), 1)
        self.assertEqual(car.model, "Ford Focus")
        self.assertEqual(car.manufacturer, self.manufacturer)
        self.assertTrue(self.user in car.drivers.all())

    def test_create_errors(self):
        response = self.client.post(
            self.url,
            data={"model": ""}
        )
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFormError(form, "drivers", "This field is required.")
        self.assertFormError(form, "model", "This field is required.")
        self.assertFormError(form, "manufacturer", "This field is required.")


class CarUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            **test_user
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA",
        )
        self.car = Car.objects.create(
            model="Ford Fusion",
            manufacturer=self.manufacturer,
        )
        self.url = reverse("taxi:car-update", kwargs={"pk": self.car.pk})

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_update_car_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")
        self.assertEqual(self.car, response.context["object"])

    def test_can_update_car(self):
        response = self.client.post(
            self.url,
            data={
                "model": "Ford Focus",
                "manufacturer": self.manufacturer.pk,
                "drivers": (self.user.pk,),
            }
        )
        self.car.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertEqual("Ford Focus", self.car.model)
        self.assertEqual(self.manufacturer, self.car.manufacturer)
        self.assertTrue(self.user in self.car.drivers.all())


class CarDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            **test_user
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA",
        )
        self.car = Car.objects.create(
            model="Ford Fusion",
            manufacturer=self.manufacturer,
        )
        self.url = reverse("taxi:car-delete", kwargs={"pk": self.car.pk})

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_delete_car_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_confirm_delete.html")
        self.assertEqual(self.car, response.context["object"])

    def test_can_delete_car(self):
        response = self.client.post(
            self.url,
        )
        pk = self.car.pk
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertFalse(Car.objects.filter(pk=pk).exists())


class CarDetailViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            **test_user
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA",
        )
        self.car = Car.objects.create(
            model="Ford Fusion",
            manufacturer=self.manufacturer,
        )
        self.url = reverse("taxi:car-detail", kwargs={"pk": self.car.pk})

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_detail_car_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
        self.assertEqual(self.car, response.context["object"])

    def test_assign_car(self):
        self.car.drivers.remove(self.user)
        response = self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})
        )
        self.assertTrue(self.user in self.car.drivers.all())
        self.assertEqual(response.status_code, 302)

    def test_unassign_car(self):
        self.car.drivers.add(self.user)
        response = self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})
        )
        self.assertFalse(self.user in self.car.drivers.all())
        self.assertEqual(response.status_code, 302)
