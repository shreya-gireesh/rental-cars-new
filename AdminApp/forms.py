from django import forms
from .models import *


class AdminModelForm(forms.ModelForm):
    class Meta:
        model = AdminModel
        fields =['admin_name', 'admin_mail', 'admin_password']

        labels = {
            'admin_name': 'Name',
            'admin_mail': 'Email',
            'admin_password': 'Password',
        }

        widgets = {
            'admin_password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'admin_name': forms.TextInput(attrs={'class': 'form-control'}),
            'admin_mail': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class CarModelForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = ['car_name', 'car_company', 'car_type', 'car_fuel', 'car_seats', 'car_price', 'status' ]

        labels = {
            'car_name': 'Car Name',
            'car_company': 'Company',
            'car_type': 'Type',
            'car_fuel': 'Fuel',
            'car_seats': 'Seats',
            'car_price': 'Price',
            'status': 'Status',
        }

        widgets = {
            'car_name': forms.TextInput(attrs={'class': 'form-control'}),
            'car_company': forms.TextInput(attrs={'class': 'form-control'}),
            'car_type': forms.Select(choices=CarModel.CAR_TYPE_CHOICES, attrs={'class': 'form-control'}),
            'car_fuel': forms.Select(choices=CarModel.CAR_FUEL_CHOICES, attrs={'class': 'form-control'}),
            'car_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'car_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_car_name(self):
        car_name = self.cleaned_data.get('car_name')
        if CarModel.objects.filter(car_name=car_name).exists():
            raise forms.ValidationError("Car already exists. Please choose a different one.")
        return car_name


class CarImgModelForm(forms.ModelForm):
    class Meta:
        model = CarImgModel
        fields = ['car', 'car_img']

        labels = {
            'car': 'Car Name',
            'car_img': 'Car Image'
        }

        widgets = {
            'car': forms.Select(attrs={'class': 'form-control'}),
            'car_img': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CarImgModelForm, self).__init__(*args, **kwargs)
        self.fields['car'].queryset = CarModel.objects.all()  # Set queryset for car dropdown


class CarInteriorsModelForm(forms.ModelForm):
    class Meta:
        model = CarInteriorsModel
        fields = ['car', 'car_interior']

        labels = {
            'car': 'Car Name',
            'car_interior': 'Car Interior Image'
        }

        widgets = {
            'car': forms.Select(attrs={'class': 'form-control'}),
            'car_interior': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CarInteriorsModelForm, self).__init__(*args, **kwargs)
        self.fields['car'].queryset = CarModel.objects.all()  # Set queryset for car dropdown


class PlacesModelForm(forms.ModelForm):
    class Meta:
        model = PlacesModel
        fields = ['places']

        labels = {
            'places': 'Place',
        }

        widgets = {
            'places': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_places(self):
        places = self.cleaned_data.get('places')
        if PlacesModel.objects.filter(places=places).exists():
            raise forms.ValidationError("This place already exists. Please choose a different one.")
        return places