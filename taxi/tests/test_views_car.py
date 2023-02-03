from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
CARS_URL = reverse("taxi:car-list")
DRIVERS_URL = reverse("taxi:driver-list")
INDEX_URL = reverse("taxi:index")


class CarListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="Porsche",
            country="Germany",
        )

        number_of_cars = 7

        for car_id in range(number_of_cars):
            Car.objects.create(
                model=f"Model {car_id}",
                manufacturer=manufacturer,
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="UserName",
            password="Pass12345"
        )

        self.driver = get_user_model().objects.create_user(
            username="DriverName",
            password="Pass12345",
            first_name="Firstname",
            last_name="Lastname",
            license_number="XXX12345"
        )

        self.client.force_login(self.user)
        self.list_response = self.client.get(CARS_URL)
        self.create_response = self.client.get(
            reverse("taxi:car-create"))
        self.update_response = self.client.get(reverse(
            "taxi:car-update", args=[1]))
        self.delete_response = self.client.get(reverse(
            "taxi:car-delete", args=[1]))

    def test_car_views_url_exists_at_desired_location(self):
        list_view_response = self.client.get("/cars/")
        create_view_response = self.client.get("/cars/create/")
        update_view_response = self.client.get("/cars/3/update/")
        delete_view_response = self.client.get("/cars/6/delete/")

        self.assertEqual(list_view_response.status_code, 200)
        self.assertEqual(create_view_response.status_code, 200)
        self.assertEqual(update_view_response.status_code, 200)
        self.assertEqual(delete_view_response.status_code, 200)

    def test_car_views_url_accessible_by_name(self):
        self.assertEqual(self.list_response.status_code, 200)
        self.assertEqual(self.create_response.status_code, 200)
        self.assertEqual(self.update_response.status_code, 200)
        self.assertEqual(self.delete_response.status_code, 200)

    def test_car_views_uses_correct_template(self):
        self.assertTemplateUsed(self.list_response, "taxi/car_list.html")
        self.assertTemplateUsed(self.create_response, "taxi/car_form.html")
        self.assertTemplateUsed(self.update_response, "taxi/car_form.html")
        self.assertTemplateUsed(self.delete_response,
                                "taxi/car_confirm_delete.html")

    def test_car_list_view_pagination_is_five(self):
        self.assertTrue("is_paginated" in self.list_response.context)
        self.assertTrue(self.list_response.context["is_paginated"] is True)
        self.assertEqual(
            len(self.list_response.context["car_list"]), 5)

    def test_car_list_view_lists_all_cars(self):
        response_sec_page = self.client.get(CARS_URL + "?page=2")
        cars = Car.objects.all()

        self.assertEqual(
            list(
                self.list_response.context["car_list"]
            ) + list(
                response_sec_page.context["car_list"]
            ), list(cars))

    def test_car_list_view_search(self):
        manufacturer = Manufacturer.objects.create(
            name="Opel",
            country="Germany",
        )
        number_of_cars = 7
        for car_id in range(number_of_cars):
            Car.objects.create(
                model=f"Astra {car_id}",
                manufacturer=manufacturer,
            )
        response_list = []
        for page_number in range(1, 3):
            search_result = self.client.get(
                CARS_URL + "?model=Model" + f"&page={page_number}",
            )
            response_list += list(search_result.context["car_list"])
        filter_result = Car.objects.filter(
            model__icontains="Model"
        )

        self.assertEqual(response_list, list(filter_result))

    def test_car_create_view_creates_car(self):
        manufacturer = Manufacturer.objects.get(name="Porsche")
        form_data = {
            "model": "911",
            "manufacturer": manufacturer.id,
            "drivers": [self.driver.id]
        }
        self.client.post(reverse("taxi:car-create"), data=form_data)
        new_car = Car.objects.get(model=form_data["model"])

        self.assertEqual(new_car.model, form_data["model"])
        self.assertEqual(new_car.manufacturer, manufacturer)

    def test_car_update_view_updates_car(self):
        new_manufacturer = Manufacturer.objects.create(
            name="KRAZ",
            country="Ukraine",
        )
        new_driver = get_user_model().objects.create_user(
            username="Kozak",
            password="23f#gf34",
            first_name="Petro",
            last_name="Nezlamnyi",
            license_number="ZXD48139"
        )
        form_data = {
            "model": "Cougar",
            "manufacturer": new_manufacturer.id,
            "drivers": [new_driver.id]
        }
        car_id_for_update = Car.objects.get(model="Model 1").id
        self.client.post(reverse(
            "taxi:car-update",
            args=[car_id_for_update]),
            data=form_data)
        updated_car = Car.objects.get(id=car_id_for_update)

        self.assertEqual(updated_car.model, form_data["model"])
        self.assertEqual(updated_car.manufacturer, new_manufacturer)

    def test_car_delete_view_deletes_car(self):
        car_id_for_delete = Car.objects.get(model="Model 1").id
        self.client.post(reverse(
            "taxi:car-delete",
            args=[car_id_for_delete]))

        self.assertEqual(list(Car.objects.filter(model="Model 1")), [])

    def test_car_detail_view_show_all_content(self):
        car1 = Car.objects.get(model="Model 5")
        car2 = Car.objects.get(model="Model 6")
        car1.drivers.add(self.driver)
        car2.drivers.add(self.driver)
        car_context_response = self.client.get(reverse(
            "taxi:car-detail",
            args=[car1.id])).context["car"]

        self.assertEqual(
            car_context_response.model,
            car1.model
        )
        self.assertEqual(
            car_context_response.manufacturer,
            car1.manufacturer
        )
        self.assertEqual(
            list(car_context_response.drivers.all()),
            list(car1.drivers.all())
        )
