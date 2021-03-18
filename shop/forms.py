from django import forms
from .models import Filter, Support, Profile, Review


class FilterForm(forms.ModelForm):
    class Meta:
        model = Filter
        fields = ['Color', 'Price_range', 'Size', 'Brand']


class SupportCreateForm(forms.ModelForm):
    class Meta:
        model = Support
        fields = ['product', 'author', 'first_name', 'last_name',
                  'email', 'phone', 'query']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email',
                  'phone', 'gender')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('product', 'author', 'stars', 'title', 'description',
                  )
