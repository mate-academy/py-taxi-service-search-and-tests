from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Car, Manufacturer


CAR_FORMATS_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")


class PublicCarFormatTests(TestCase):
    @classmethod
    def setUp(cls) -> None:
        manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany",
        )
        Car.objects.create(
            model="EQS",
            manufacturer=manufacturer
        )

    def test_login_requirement_car_list(self):
        res_list = self.client.get(CAR_FORMATS_URL)

        self.assertNotEquals(res_list.status_code, 200)

    def test_login_requirement_create_car(self):
        res_create = self.client.get(CAR_CREATE_URL)

        self.assertNotEquals(res_create.status_code, 200)

    def test_login_requirement_car_detail(self):
        res_create = self.client.get(CAR_CREATE_URL)

        self.assertNotEquals(res_create.status_code, 200)

    def test_update_delete_car_without_login(self):
        car = Car.objects.get(id=1)
        url_1 = reverse("taxi:car-update", kwargs={"pk": car.pk})
        url_2 = reverse("taxi:car-delete", kwargs={"pk": car.pk})
        res_1 = self.client.get(url_1)
        res_2 = self.client.get(url_2)
        self.assertNotEquals(res_1.status_code, 200)
        self.assertNotEquals(res_2.status_code, 200)


class PrivateCarFormatTests(TestCase):

    def setUp(self) -> None:
        number_of_car = 7
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            password="qwe12345"
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany",
        )
        for car_id in range(number_of_car):
            Car.objects.create(
                model=f"EQS{car_id}",
                manufacturer=manufacturer
            )

    def test_retrieve_car(self):
        response = self.client.get(CAR_FORMATS_URL + "?page=1")
        response_2 = self.client.get(CAR_FORMATS_URL + "?page=2")
        car = Car.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            (list(response.context["car_list"])
             + list(response_2.context["car_list"])
             )
            , list(car)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_if_search_car_name_is_a_character_eqs1(self):
        response = self.client.get(CAR_FORMATS_URL + "?model=eqs1")
        manufacturer = Car.objects.filter(
            model__icontains="eqs1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEquals(
            list(response.context["car_list"]), list(manufacturer)
        )
        self.assertTrue("search_form" in response.context)
        self.assertEqual(
            response.context["search_form"].initial["model"],
            "eqs1"
        )

    def test_view_url_car_exists_at_desired_location(self):
        response = self.client.get("/cars/")
        self.assertEquals(response.status_code, 200)

    def test_pagination_in_car_is_five(self):
        response = self.client.get(CAR_FORMATS_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_pagination_in_car_is_second_page_five(self):
        response = self.client.get(CAR_FORMATS_URL + "?page=2")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(len(response.context["car_list"]), 2)

    def test_create_car(self):
        manufacturer = Manufacturer.objects.first()

        response = self.client.get(CAR_CREATE_URL)
        self.assertEquals(response.status_code, 200)
        data_crate = {
            "model": "test",
            "manufacturer": manufacturer.id
        }
        response = self.client.post(CAR_CREATE_URL, data=data_crate)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))

    def test_update_delete_car_with_login(self):
        car = Car.objects.first()
        url_1 = reverse("taxi:car-update", kwargs={"pk": car.pk})
        url_2 = reverse("taxi:car-delete", kwargs={"pk": car.pk})
        res_1 = self.client.get(url_1)
        res_2 = self.client.get(url_2)
        self.assertEquals(res_1.status_code, 200)
        self.assertEquals(res_2.status_code, 200)
