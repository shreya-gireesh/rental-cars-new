from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import *
from UserApp.models import *
from .forms import *


# Create your views here.

def carimg_reg(request):
    if request.method == 'POST':
        form_obj = CarImgModelForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('admin_car')
    else:
        form_obj = CarImgModelForm()
    return render(request, 'admin-carimg-reg.html', {'form': form_obj})


def carinterior_reg(request):
    if request.method == 'POST':
        form_obj = CarInteriorsModelForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('admin_car')
    else:
        form_obj = CarInteriorsModelForm()
    return render(request, 'admin-carinterior-reg.html', {'form': form_obj})




def places_reg(request):
    if request.method == 'POST':
        form_obj = PlacesModelForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('car_admin')
    else:
        form_obj = PlacesModelForm()
    return render(request, 'admin_places_reg.html', {'form': form_obj})


# custom admin
def admin_home(request):
    booking = BookingModel.objects.all()
    users = UserRegModel.objects.count()
    cars = CarModel.objects.count()
    bookings = BookingModel.objects.count()
    payment = PaymentModel.objects.all().aggregate(Sum('amount'))
    amount = payment['amount__sum']/100
    return render(request, 'admin_home.html', {'users': users, 'cars': cars,'book': booking, 'bookings': bookings, 'payment': amount})


def admin_car(request):
    car = CarModel.objects.all()
    return render(request, 'admin-car.html', {'cars': car})



def admin_car_reg(request):
    if request.method == 'POST':
        form_obj = CarModelForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('/admin_car')
    else:
        form_obj = CarModelForm()
    return render(request, 'admin-car-reg.html', {'form': form_obj})


def admin_car_images(request):
    car = CarImgModel.objects.all()
    return render(request, 'admin-car-images.html', {'cars': car})


def admin_car_interiors(request):
    car = CarInteriorsModel.objects.all()
    return render(request, 'admin-car-interiors.html', {'cars': car})


def admin_bookings(request):
    bookings = BookingModel.objects.all()
    return render(request, 'admin-bookings.html', {'booking': bookings})


def admin_payment(request):
    payments = PaymentModel.objects.all()
    return render(request, 'admin-payment.html', {'payment': payments})


def admin_places(request):
    places = PlacesModel.objects.all()
    return render(request, 'admin-places.html', {'places': places})