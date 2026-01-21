from django import forms

class SearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=255,
        required=False, 
        label="",  # Hide label for a cleaner UI
        widget=forms.TextInput(attrs={"placeholder": "Search..."})
    )
