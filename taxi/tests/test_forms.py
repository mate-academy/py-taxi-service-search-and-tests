from django.test import TestCase

from taxi.forms import SearchForm


class SearchFormTests(TestCase):
    def test_form_placeholder(self):
        form = SearchForm()
        self.assertIn('placeholder="Search"', form.as_p())
