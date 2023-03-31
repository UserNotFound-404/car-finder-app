from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

widget_select = forms.Select(attrs={'class': 'form-control'})
widget_number = forms.NumberInput(attrs={'class': 'form-control'})
widget_checkbox = forms.CheckboxInput(attrs={'class': 'form-check-input'})
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
	model = forms.ModelChoiceField(queryset=Model.objects.values_list('name', flat=True).distinct(), required=False, empty_label="Select model name", widget=widget_select)
	max_year = forms.IntegerField(min_value=1900, max_value=3000, required=False, widget=widget_number)
	min_year = forms.IntegerField(min_value=1900, max_value=3000, required=False, widget=widget_number)
	model_style = forms.ModelChoiceField(queryset=Model.objects.values_list('body_style', flat=True).distinct(), required=False, empty_label="Select body style", widget=widget_select)

class BrandFilterForm(forms.Form):
	brand = forms.ModelChoiceField(queryset=Brand.objects.values_list('name', flat=True).distinct(), empty_label="Select brand", required=False, widget=widget_select)
	country = forms.ModelChoiceField(queryset=Brand.objects.values_list('country', flat=True).distinct(), empty_label="Select country", required=False, widget=widget_select)

class CarFilterForm(ModelFilterForm, BrandFilterForm):
	min_price = forms.IntegerField(min_value=0, max_value=10000000, required = False, widget=widget_number)
	max_price = forms.IntegerField(min_value=0, max_value=10000000, required = False, widget=widget_number)
	min_mileage = forms.IntegerField(min_value=0, max_value=10000000, required = False, widget=widget_number)
	max_mileage = forms.IntegerField(min_value=0, max_value=10000000, required = False, widget=widget_number)
	select_extr_color = forms.BooleanField(label="Choose exterier color", required=False, widget=widget_checkbox)
	extr_color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))
	select_intr_color = forms.BooleanField(label="Choose interier color", required=False, widget=widget_checkbox)
	intr_color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))
	fuel_type = forms.ModelChoiceField(queryset=Car.objects.values_list('fuel_type', flat=True).distinct(), empty_label="Select fuel type", required=False, widget=widget_select)
