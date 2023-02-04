from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car, Driver

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
CARS_URL = reverse("taxi:car-list")
DRIVERS_URL = reverse("taxi:driver-list")
INDEX_URL = reverse("taxi:index")


class DriverListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_drivers = 7

        for driver_id in range(number_of_drivers):
            get_user_model().objects.create_user(
                username=f"UserName {driver_id}",
                password="Pass12345",
                first_name=f"Firstname {driver_id}",
                last_name=f"Lastname {driver_id}",
                license_number=f"XXX1234{driver_id}"
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="UserName",
            password="Pass12345"
        )
        self.client.force_login(self.user)
        self.list_response = self.client.get(DRIVERS_URL)
        self.create_response = self.client.get(
            reverse("taxi:driver-create")
        )
        self.update_response = self.client.get(reverse(
            "taxi:driver-update", args=[1])
        )
        self.delete_response = self.client.get(reverse(
            "taxi:driver-delete", args=[1])
        )

    def test_driver_views_url_exists_at_desired_location(self):
        list_view_response = self.client.get("/drivers/")
        create_view_response = self.client.get("/drivers/create/")
        update_view_response = self.client.get("/drivers/3/update/")
        delete_view_response = self.client.get("/drivers/6/delete/")

        self.assertEqual(list_view_response.status_code, 200)
        self.assertEqual(create_view_response.status_code, 200)
        self.assertEqual(update_view_response.status_code, 200)
        self.assertEqual(delete_view_response.status_code, 200)

    def test_driver_views_url_accessible_by_name(self):
        self.assertEqual(self.list_response.status_code, 200)
        self.assertEqual(self.create_response.status_code, 200)
        self.assertEqual(self.update_response.status_code, 200)
        self.assertEqual(self.delete_response.status_code, 200)

    def test_driver_views_uses_correct_template(self):
        self.assertTemplateUsed(self.list_response, "taxi/driver_list.html")
        self.assertTemplateUsed(self.create_response, "taxi/driver_form.html")
        self.assertTemplateUsed(self.update_response, "taxi/driver_form.html")
        self.assertTemplateUsed(
            self.delete_response,
            "taxi/driver_confirm_delete.html"
        )

    def test_driver_list_view_pagination_is_five(self):
        self.assertTrue("is_paginated" in self.list_response.context)
        self.assertTrue(self.list_response.context["is_paginated"] is True)
        self.assertEqual(
            len(self.list_response.context["driver_list"]), 5
        )

    def test_driver_list_view_lists_all_cars(self):
        response_sec_page = self.client.get(DRIVERS_URL + "?page=2")
        drivers = Driver.objects.all()
        self.assertEqual(
            list(
                self.list_response.context["driver_list"]
            ) + list(
                response_sec_page.context["driver_list"]
            ), list(drivers)
        )

    def test_driver_list_view_search(self):
        number_of_drivers = 7

        for driver_id in range(number_of_drivers):
            get_user_model().objects.create_user(
                username=f"Name {driver_id}",
                password="Pass12345",
                first_name=f"Firstname {driver_id}",
                last_name=f"Lastname {driver_id}",
                license_number=f"XXX1230{driver_id}"
            )
        response_list = []
        for page_number in range(1, 3):
            search_result = self.client.get(
                "/drivers/", {"username": "User", "page": f"{page_number}"}
            )
            response_list += list(search_result.context["driver_list"])
        filter_result = get_user_model().objects.filter(
            username__icontains="User"
        )

        self.assertEqual(response_list, list(filter_result))

    def test_driver_create_view_creates_driver(self):
        form_data = {
            "username": "Kozak",
            "password1": "23f#gf34",
            "password2": "23f#gf34",
            "first_name": "Petro",
            "last_name": "Nezlamnyi",
            "license_number": "ZXD48139"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(new_driver.username, form_data["username"])
        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )

    def test_driver_update_view_updates_license_number(self):
        form_data = {"license_number": "ZXD48139"}
        driver_id_for_update = get_user_model().objects.get(
            username="UserName 1"
        ).id
        self.client.post(reverse(
            "taxi:driver-update",
            args=[driver_id_for_update]
        ),
            data=form_data
        )
        updated_driver = get_user_model().objects.get(id=driver_id_for_update)

        self.assertEqual(
            updated_driver.license_number,
            form_data["license_number"]
        )

    def test_driver_delete_view_deletes_driver(self):
        driver_id_for_update = get_user_model().objects.get(
            username="UserName 0").id
        self.client.post(
            reverse("taxi:driver-delete",
                    args=[driver_id_for_update]
                    )
        )

        self.assertEqual(
            list(get_user_model().objects.filter(username="UserName 0")), []
        )

    def test_driver_detail_view_show_all_content(self):
        manufacturer1 = Manufacturer.objects.create(
            name="Kraz",
            country="Ukraine",
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Opel",
            country="Germany",
        )
        driver = get_user_model().objects.get(username="UserName 4")
        car1 = Car.objects.create(
            model="Cougar",
            manufacturer=manufacturer1,
        )
        car2 = Car.objects.create(
            model="Astra",
            manufacturer=manufacturer2,
        )
        car1.drivers.add(driver)
        car2.drivers.add(driver)
        driver_context_response = self.client.get(reverse(
            "taxi:driver-detail",
            args=[driver.id])
        ).context["driver"]

        self.assertEqual(
            driver_context_response.username,
            driver.username
        )
        self.assertEqual(
            driver_context_response.first_name,
            driver.first_name
        )
        self.assertEqual(
            driver_context_response.last_name,
            driver.last_name
        )
        self.assertEqual(
            driver_context_response.license_number,
            driver.license_number
        )
        self.assertEqual(
            list(driver_context_response.cars.all()),
            list(driver.cars.all())
        )
