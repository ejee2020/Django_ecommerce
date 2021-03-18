from django import forms
# Show client the input form
# Validate client's info


class AddProductForm(forms.Form):
    quantity = forms.IntegerField()
    is_update = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput)
