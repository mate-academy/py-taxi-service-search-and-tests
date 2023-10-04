from django.contrib.auth import get_user_model, login
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    DriverSearchForm,
    DriverLicenseUpdateForm,
    DriverCreationForm,
)


class PublicdriverViewsTest(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def test_login_required_protection_list(self):
        url = reverse("taxi:driver-list")
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_protection_detail(self):
        url = reverse("taxi:driver-detail", args=[2])
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_protection_driver_update(self):
        url = reverse("taxi:driver-update", args=[2])
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_protection_driver_delete(self):
        url = reverse("taxi:driver-delete", args=[2])
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)


DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", args=[2])
DRIVER_UPDATE_URL = reverse("taxi:driver-update", args=[2])
DRIVER_DELETE_URL = reverse("taxi:driver-delete", args=[2])
DRIVER_CREATE_URL = reverse("taxi:driver-create")
PAGINATION = 5


class PrivateDriverViewsTest(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.get(id=2)
        self.client.force_login(self.user)

    """Tests for the ListView"""

    def test_list_correct_pagination_content_listed(self):
        url = DRIVER_LIST_URL
        res = self.client.get(url)
        self.assertEquals(
            list(get_user_model().objects.all()[:PAGINATION]),
            list(res.context.get("driver_list")),
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_list_create_button_exists(self):
        url = DRIVER_LIST_URL
        res = self.client.get(url)
        self.assertContains(
            res,
            """a href="/drivers/create/" """
            "",
        )

    def test_list_searchbar_exists(self):
        url = DRIVER_LIST_URL
        res = self.client.get(url)
        self.assertTrue(
            isinstance(res.context.get("search_form"), DriverSearchForm)
        )

    def test_list_search_bar_works(self):
        url = DRIVER_LIST_URL
        form = DriverSearchForm(data={"username": "an"})
        self.assertTrue(form.is_valid())
        res = self.client.get(url, form.data)
        self.assertEquals(
            list(res.context.get("driver_list")),
            list(
                get_user_model().objects.filter(username__icontains="an")[
                    :PAGINATION
                ]
            ),
        )
        self.assertEquals(
            res.context.get("search_form").initial.get("username"), "an"
        )

    def test_list_pagination_does_not_break_search(self):
        url = DRIVER_LIST_URL
        res = self.client.get(url, data={"username": "a", "page": 2})
        self.assertEquals(
            list(res.context.get("driver_list")),
            list(
                get_user_model().objects.filter(username__icontains="a")[
                    PAGINATION:
                ]
            ),
        )

    """Tests for the DetailView"""

    def test_detail_correct_driver(self):
        url = DRIVER_DETAIL_URL
        res = self.client.get(url)
        self.assertEquals(res.context.get("driver"), self.user)

    def test_detail_correct_content(self):
        url = DRIVER_DETAIL_URL
        res = self.client.get(url)
        self.assertContains(res, self.user.first_name)
        self.assertContains(res, self.user.last_name)
        self.assertContains(res, self.user.license_number)
        self.assertContains(res, self.user.is_staff)
        self.assertContains(res, self.user.cars.last().model)

    def test_detail_correct_links(self):
        url = DRIVER_DETAIL_URL
        res = self.client.get(url)
        self.assertContains(res, "/drivers/2/delete/")
        self.assertContains(res, "/drivers/2/update/")

    """Test for the DeleteView"""

    def test_delete_correct_template_name(self):
        url = DRIVER_DELETE_URL
        res = self.client.get(url)
        self.assertTemplateUsed(res, "taxi/driver_confirm_delete.html")

    def test_delete_correct_success_url(self):
        user = get_user_model().objects.create_user(
            username="testorado", password="fafeafa4342@"
        )
        self.client.force_login(user)
        url = DRIVER_DELETE_URL
        res = self.client.post(url, follow=True)
        self.assertRedirects(res, DRIVER_LIST_URL)

    """Tests for the CreateView"""

    def test_create_correct_form(self):
        url = DRIVER_CREATE_URL
        res = self.client.get(url)
        self.assertTrue(
            isinstance(res.context.get("form"), DriverCreationForm)
        )

    """Tests for the UpdateView"""

    def test_update_correct_form(self):
        url = DRIVER_UPDATE_URL
        res = self.client.get(url)
        self.assertTrue(
            isinstance(res.context.get("form"), DriverLicenseUpdateForm)
        )

    def test_update_correct_success_url(self):
        url = DRIVER_UPDATE_URL
        res = self.client.post(url, data={"license_number": "ASD12346"})
        self.assertRedirects(res, DRIVER_LIST_URL)
