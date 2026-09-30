from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class TaxiViewsTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="test_driver",
            license_number="ADM12345",
        )
        self.client.force_login(self.user)

        self.jim = Driver.objects.create_user(
            username="jim.hopper",
            first_name="Jim",
            last_name="Hopper",
            license_number="ABC12345",
        )
        self.jimmy = Driver.objects.create_user(
            username="jimmy",
            license_number="DEF12345",
        )

        self.bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        self.bmw_motorrad = Manufacturer.objects.create(
            name="BMW Motorrad",
            country="Germany",
        )
        self.honda = Manufacturer.objects.create(
            name="Honda",
            country="Japan",
        )

        self.civic = Car.objects.create(
            model="Civic",
            manufacturer=self.honda,
        )
        self.civic_type_r = Car.objects.create(
            model="Civic Type R",
            manufacturer=self.honda,
        )
        self.x5 = Car.objects.create(
            model="X5",
            manufacturer=self.bmw,
        )

    def check_search_results(
        self,
        url_name,
        context_name,
        query,
        expected_objects,
    ):
        response = self.client.get(
            reverse(url_name),
            {"q": query},
        )

        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.context[context_name],
            expected_objects,
        )
        self.assertEqual(
            response.context["search_query"],
            query,
        )

    def test_manufacturer_search(self):
        all_manufacturers = [
            self.bmw,
            self.bmw_motorrad,
            self.honda,
        ]

        cases = [
            ("BMW", [self.bmw, self.bmw_motorrad]),
            ("bmw", [self.bmw, self.bmw_motorrad]),
            ("Mot", [self.bmw_motorrad]),
            ("  bmw  ", [self.bmw, self.bmw_motorrad]),
            ("Tesla", []),
            ("Germany", []),
            ("", all_manufacturers),
            ("   ", all_manufacturers),
        ]

        for query, expected_objects in cases:
            with self.subTest(query=query):
                self.check_search_results(
                    url_name="taxi:manufacturer-list",
                    context_name="manufacturer_list",
                    query=query,
                    expected_objects=expected_objects,
                )

    def test_manufacturer_list_without_search_parameter(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.context["manufacturer_list"],
            [self.bmw, self.bmw_motorrad, self.honda],
        )
        self.assertEqual(response.context["search_query"], "")

    def test_car_search(self):
        all_cars = [
            self.civic,
            self.civic_type_r,
            self.x5,
        ]

        cases = [
            ("Civic", [self.civic, self.civic_type_r]),
            ("cIvIc", [self.civic, self.civic_type_r]),
            ("Type", [self.civic_type_r]),
            ("  civic  ", [self.civic, self.civic_type_r]),
            ("nonexistent-model", []),
            ("Honda", []),
            ("", all_cars),
            ("   ", all_cars),
        ]

        for query, expected_objects in cases:
            with self.subTest(query=query):
                self.check_search_results(
                    url_name="taxi:car-list",
                    context_name="car_list",
                    query=query,
                    expected_objects=expected_objects,
                )

    def test_car_list_without_search_parameter(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.context["car_list"],
            [self.civic, self.civic_type_r, self.x5],
        )
        self.assertEqual(response.context["search_query"], "")

    def test_driver_search(self):
        all_drivers = [
            self.user,
            self.jim,
            self.jimmy,
        ]

        cases = [
            ("jim", [self.jim, self.jimmy]),
            ("JIM", [self.jim, self.jimmy]),
            ("hopper", [self.jim]),
            ("  jim  ", [self.jim, self.jimmy]),
            ("unknown-driver", []),
            ("ABC12345", []),
            ("", all_drivers),
            ("   ", all_drivers),
        ]

        for query, expected_objects in cases:
            with self.subTest(query=query):
                self.check_search_results(
                    url_name="taxi:driver-list",
                    context_name="driver_list",
                    query=query,
                    expected_objects=expected_objects,
                )

    def test_driver_list_without_search_parameter(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.context["driver_list"],
            [self.user, self.jim, self.jimmy],
        )
        self.assertEqual(response.context["search_query"], "")

    def test_manufacturer_search_with_pagination(self):
        matching_manufacturers = []

        for index in range(7):
            manufacturer = Manufacturer.objects.create(
                name=f"Search Brand {index}",
                country="Germany",
            )
            matching_manufacturers.append(manufacturer)

        url = reverse("taxi:manufacturer-list")

        first_response = self.client.get(
            url,
            {"q": "Search Brand"},
        )
        second_response = self.client.get(
            url,
            {"q": "Search Brand", "page": 2},
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)

        first_page = list(
            first_response.context["manufacturer_list"]
        )
        second_page = list(
            second_response.context["manufacturer_list"]
        )

        self.assertEqual(len(first_page), 5)
        self.assertEqual(len(second_page), 2)
        self.assertEqual(
            first_response.context["paginator"].count,
            7,
        )
        self.assertCountEqual(
            first_page + second_page,
            matching_manufacturers,
        )
        self.assertContains(
            first_response,
            'href="?page=2&amp;q=Search%20Brand"',
        )

    def test_index_displays_object_counts(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_drivers"], 3)
        self.assertEqual(response.context["num_cars"], 3)
        self.assertEqual(
            response.context["num_manufacturers"],
            3,
        )

    def test_index_increments_visit_count(self):
        url = reverse("taxi:index")

        first_response = self.client.get(url)

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(first_response.context["num_visits"], 1)
        self.assertEqual(self.client.session["num_visits"], 1)

        second_response = self.client.get(url)

        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(second_response.context["num_visits"], 2)
        self.assertEqual(self.client.session["num_visits"], 2)

    def test_car_detail_displays_assigned_drivers(self):
        self.civic.drivers.add(self.jim)

        response = self.client.get(
            reverse(
                "taxi:car-detail",
                args=[self.civic.pk],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["car"], self.civic)
        self.assertContains(response, self.jim.username)

    def test_driver_detail_displays_assigned_cars(self):
        self.civic.drivers.add(self.jim)

        response = self.client.get(
            reverse(
                "taxi:driver-detail",
                args=[self.jim.pk],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["driver"], self.jim)
        self.assertContains(response, self.civic.model)
        self.assertNotContains(response, self.x5.model)

    def test_pages_require_login(self):
        self.client.logout()

        pages = [
            ("taxi:index", []),
            ("taxi:manufacturer-list", []),
            ("taxi:manufacturer-create", []),
            ("taxi:manufacturer-update", [self.bmw.pk]),
            ("taxi:manufacturer-delete", [self.bmw.pk]),
            ("taxi:car-list", []),
            ("taxi:car-detail", [self.civic.pk]),
            ("taxi:car-create", []),
            ("taxi:car-update", [self.civic.pk]),
            ("taxi:car-delete", [self.civic.pk]),
            ("taxi:driver-list", []),
            ("taxi:driver-detail", [self.jim.pk]),
            ("taxi:driver-create", []),
            ("taxi:driver-update", [self.jim.pk]),
            ("taxi:driver-delete", [self.jim.pk]),
        ]

        login_url = reverse("login")

        for url_name, args in pages:
            with self.subTest(url_name=url_name):
                url = reverse(url_name, args=args)
                response = self.client.get(url)

                self.assertRedirects(
                    response,
                    f"{login_url}?next={url}",
                    fetch_redirect_response=False,
                )

    def test_toggle_assign_adds_current_driver(self):
        self.civic.drivers.add(self.jim)

        url = reverse(
            "taxi:toggle-car-assign",
            args=[self.civic.pk],
        )

        response = self.client.post(url)

        self.assertRedirects(
            response,
            reverse(
                "taxi:car-detail",
                args=[self.civic.pk],
            ),
            fetch_redirect_response=False,
        )
        self.assertCountEqual(
            self.civic.drivers.all(),
            [self.jim, self.user],
        )

    def test_toggle_assign_removes_current_driver(self):
        self.civic.drivers.add(self.jim, self.user)

        url = reverse(
            "taxi:toggle-car-assign",
            args=[self.civic.pk],
        )

        response = self.client.post(url)

        self.assertRedirects(
            response,
            reverse(
                "taxi:car-detail",
                args=[self.civic.pk],
            ),
            fetch_redirect_response=False,
        )
        self.assertCountEqual(
            self.civic.drivers.all(),
            [self.jim],
        )
