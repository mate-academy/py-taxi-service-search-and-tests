from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer


class PublicManufacturerViewsTest(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def test_login_required_protection_list(self):
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_protection_manufacturer_update(self):
        url = reverse("taxi:manufacturer-update", args=[2])
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_protection_manufacturer_delete(self):
        url = reverse("taxi:manufacturer-delete", args=[2])
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)


MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_UPDATE_URL = reverse("taxi:manufacturer-update", args=[2])
MANUFACTURER_DELETE_URL = reverse("taxi:manufacturer-delete", args=[2])
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
PAGINATION = 5


class PrivateManufacturerViewsTest(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.get(id=2)
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.get(id=2)

    """Tests for the ListView"""

    def test_list_correct_pagination_content_listed(self):
        url = MANUFACTURER_LIST_URL
        res = self.client.get(url)
        self.assertEquals(
            list(Manufacturer.objects.all()[:PAGINATION]),
            list(res.context.get("manufacturer_list")),
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_list_create_button_exists(self):
        url = MANUFACTURER_LIST_URL
        res = self.client.get(url)
        self.assertContains(
            res,
            """a href="/manufacturers/create/" """
        )

    def test_list_searchbar_exists(self):
        url = MANUFACTURER_LIST_URL
        res = self.client.get(url)
        self.assertTrue(
            isinstance(res.context.get("search_form"), ManufacturerSearchForm)
        )

    def test_list_search_bar_works(self):
        url = MANUFACTURER_LIST_URL
        form = ManufacturerSearchForm(data={"name": "m"})
        self.assertTrue(form.is_valid())
        res = self.client.get(url, form.data)
        self.assertEquals(
            list(res.context.get("manufacturer_list")),
            list(
                Manufacturer.objects.filter(name__icontains="m")[:PAGINATION]
            ),
        )
        self.assertEquals(
            res.context.get("search_form").initial.get("name"), "m"
        )

    def test_list_pagination_does_not_break_search(self):
        url = MANUFACTURER_LIST_URL
        res = self.client.get(url, data={"name": "a", "page": 2})
        self.assertEquals(
            list(res.context.get("manufacturer_list")),
            list(
                Manufacturer.objects.filter(name__icontains="a")[PAGINATION:]
            ),
        )

    """Tests for the DeleteView"""

    def test_delete_correct_template_name(self):
        url = MANUFACTURER_DELETE_URL
        res = self.client.get(url)
        self.assertTemplateUsed(res, "taxi/manufacturer_confirm_delete.html")

    def test_delete_correct_success_url(self):
        user = get_user_model().objects.create_user(
            username="testorado",
            password="fafeafa4342@",
            license_number="VDZ32456",
        )
        self.client.force_login(user)
        url = MANUFACTURER_DELETE_URL
        res = self.client.post(url, follow=True)
        self.assertRedirects(res, MANUFACTURER_LIST_URL)

    """Test for the CreateView"""

    def test_create_correct_success_url(self):
        url = MANUFACTURER_CREATE_URL
        res = self.client.post(
            url,
            data={
                "name": "test",
                "country": "some",
            },
        )
        self.assertRedirects(res, MANUFACTURER_LIST_URL)

    """Tests for the UpdateView"""

    def test_update_correct_success_url(self):
        url = MANUFACTURER_UPDATE_URL
        res = self.client.post(
            url,
            data={
                "name": "other",
                "country": "one",
            },
        )
        self.assertRedirects(res, MANUFACTURER_LIST_URL)
