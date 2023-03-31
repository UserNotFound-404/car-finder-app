from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class ModelFilterForm(forms.Form):
	model = forms.ModelChoiceField(queryset=Model.objects.values_list('name', flat=True).distinct(), required=False, empty_label="Select model name")
	max_year = forms.IntegerField(required=False)
	min_year = forms.IntegerField(required=False)
	model_style = forms.ModelChoiceField(queryset=Model.objects.values_list('body_style', flat=True).distinct(), required=False, empty_label="Select body style")

class BrandFilterForm(forms.Form):
	brand = forms.ModelChoiceField(queryset=Brand.objects.values_list('name', flat=True).distinct(), empty_label="Select brand", required=False)
	country = forms.ModelChoiceField(queryset=Brand.objects.values_list('country', flat=True).distinct(), empty_label="Select country", required=False)

class CarFilterForm(ModelFilterForm, BrandFilterForm):
	min_price = forms.IntegerField(required = False)
	max_price = forms.IntegerField(required = False)
	min_mileage = forms.IntegerField(required = False)
	max_mileage = forms.IntegerField(required = False)
	select_extr_color = forms.BooleanField(label="Choose exterier color", required=False)
	extr_color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color', 'value': ''}))
	select_intr_color = forms.BooleanField(label="Choose interier color", required=False)
	intr_color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color', 'value': ''}))
	fuel_type = forms.ModelChoiceField(queryset=Car.objects.values_list('fuel_type', flat=True).distinct(), empty_label="Select fuel type", required=False)
