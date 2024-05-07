from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from AdminApp.models import *
from RentalCar import settings
from UserApp.models import *
import razorpay


# Create your views here.
def home(request):
    cars = CarImgModel.objects.all()
    places = PlacesModel.objects.all()
    user_authenticated = 'user' in request.session
    username = request.session.get('user', None)
    if request.method == 'POST':
        if request.POST.get('book-now'):
            request.session['pickup_location'] = request.POST.get('pickup_location')
            request.session['pickup_date'] = request.POST.get('pickup_date')
            request.session['dropoff_location'] = request.POST.get('dropoff_location')
            request.session['dropoff_date'] = request.POST.get('dropoff_date')
            return redirect('booking')
        if request.POST.get('loginbtn'):
            mailid = request.POST.get('mailid')
            pasw = request.POST.get('pasw')
            user = UserRegModel.objects.get(user_mail=mailid, user_pasw=pasw)
            request.session['user'] = user.user_name
            return redirect('/')
        if request.POST.get('regbtn'):
            uname = request.POST.get('uname')
            usermail = request.POST.get('usermail')
            upasw = request.POST.get('upasw')
            pno = request.POST.get('pno')
            licenseno = request.POST.get('licenseno')
            try:
                validate_password(upasw)
            except ValidationError as e:
                # Handle the validation error (e.g., display error message)
                error_message = str(e)
                return render(request, 'home.html',
                              {'error_message': error_message, 'cars': cars, 'user': user_authenticated,
                               'name': username, 'places': places})
            newuser = UserRegModel()
            newuser.user_name = uname
            newuser.user_mail = usermail
            newuser.user_pasw = upasw
            newuser.user_pno = pno
            newuser.license_no = licenseno
            newuser.save()
            return redirect('/')
    return render(request, 'home.html', {'cars': cars, 'user': user_authenticated, 'name': username, 'places': places})


def logout(request):
    del request.session['user']
    return redirect('/')


def booking(request):
    user_authenticated = 'user' in request.session
    username = request.session.get('user', None)
    pickup_loc = request.session.get('pickup_location')
    pickup_date = request.session.get('pickup_date')
    dropoff_loc = request.session.get('dropoff_location')
    dropoff_date = request.session.get('dropoff_date')

    pickup = PlacesModel.objects.filter(places_id=pickup_loc)
    dropoff = PlacesModel.objects.filter(places_id=dropoff_loc)

    # to find available cars
    car_id = BookingModel.objects.filter(pickup_date__lte=dropoff_date, dropof_date__gte=pickup_date).values_list(
        'car_id', flat=True)
    # booked_cars = CarImgModel.objects.exclude(car__car_id__in=car_id)
    # print(booked_cars)
    cars = CarImgModel.objects.all()

    # Convert the date strings to datetime objects
    pdate = datetime.strptime(pickup_date, '%Y-%m-%d')
    ddate = datetime.strptime(dropoff_date, '%Y-%m-%d')
    time_difference = ddate - pdate
    total_hours = time_difference.total_seconds() / 3600
    request.session['hour'] = total_hours

    if request.method == 'POST':
        # Filters
        if request.POST.get('filter-btn'):
            if request.POST.get('manual'):
                cars = cars.filter(car__car_type='Manual')
            if request.POST.get('automatic'):
                cars = cars.filter(car__car_type='Automatic')
            if request.POST.get('petrol'):
                cars = cars.filter(car__car_fuel='Petrol')
            if request.POST.get('diesel'):
                cars = cars.filter(car__car_fuel='Diesel')
            if request.POST.get('maruti'):
                cars = cars.filter(car__car_company='Maruti')
            if request.POST.get('toyota'):
                cars = cars.filter(car__car_company='Toyota')
            if request.POST.get('price') == '1':
                cars = cars.order_by('car__car_price')
            if request.POST.get('price') == '2':
                cars = cars.order_by('-car__car_price')

        # car-selection
        if request.POST.get('select-btn'):
            carid = request.POST.get('carid')
            request.session['carid'] = carid
            return redirect('car')
    return render(request, 'booking.html',
                  {'booked_cars': car_id, 'cars': cars, 'user': user_authenticated, 'name': username,
                   'pickup': pickup, 'pickup_date': pdate.date(), 'dropoff': dropoff, 'dropoff_date': ddate.date()})


def blogs(request):
    user_authenticated = 'user' in request.session
    username = request.session.get('user', None)
    return render(request, 'blogs.html', {'user': user_authenticated, 'name': username})


def kochiblog(request):
    user_authenticated = 'user' in request.session
    username = request.session.get('user', None)
    return render(request, 'kochiblog.html', {'user': user_authenticated, 'name': username})


def tvmblog(request):
    user_authenticated = 'user' in request.session
    username = request.session.get('user', None)
    return render(request, 'tvmblog.html', {'user': user_authenticated, 'name': username})


def contact(request):
    user_authenticated = 'user' in request.session
    username = request.session.get('user', None)
    return render(request, 'contact.html', {'user': user_authenticated, 'name': username})


def about(request):
    user_authenticated = 'user' in request.session
    username = request.session.get('user', None)
    return render(request, 'about.html', {'user': user_authenticated, 'name': username})


def car(request):
    pickup_loc = request.session.get('pickup_location')
    pickup_date = request.session.get('pickup_date')
    dropoff_loc = request.session.get('dropoff_location')
    dropoff_date = request.session.get('dropoff_date')
    hours = request.session.get('hour')

    pdate = datetime.strptime(pickup_date, '%Y-%m-%d')
    ddate = datetime.strptime(dropoff_date, '%Y-%m-%d')

    pickup = PlacesModel.objects.filter(places_id=pickup_loc)
    dropoff = PlacesModel.objects.filter(places_id=dropoff_loc)

    carid = request.session.get('carid')
    cars = CarImgModel.objects.filter(car_id=carid)
    car_interiors = CarInteriorsModel.objects.filter(car__car_id=carid)
    review = CommentModel.objects.filter(car__car_id=carid)
    user_authenticated = 'user' in request.session
    username = request.session.get('user', None)

    if request.POST.get('confirm-btn'):
        car_id = request.session.get('carid')
        print(car_id)
        new_booking = BookingModel()
        new_booking.car = CarModel.objects.get(car_id = car_id)
        new_booking.user = UserRegModel.objects.get(user_name = username)
        new_booking.pickup = get_object_or_404(PlacesModel, places_id=pickup_loc).places
        new_booking.pickup_date = request.session.get('pickup_date')
        new_booking.dropof = get_object_or_404(PlacesModel, places_id=dropoff_loc).places
        new_booking.dropof_date = request.session.get('dropoff_date')
        new_booking.save()
        booking_id = new_booking.booking_id
        request.session['booking_id'] = booking_id
        print(booking_id)
        return redirect('/payment')
    return render(request, 'car.html',
                  {'car_interiors': car_interiors, 'cars': cars, 'user': user_authenticated, 'name': username,
                   'pickup': pickup, 'pickup_date': pdate.date(), 'dropoff': dropoff,
                   'dropoff_date': ddate.date(), 'hours': hours, 'reviews': review})


def account(request):
    username = request.session.get('user')
    users = UserRegModel.objects.filter(user_name=username)
    current_date = datetime.now().date()
    completed_bookings = BookingModel.objects.filter(user__user_name=username, dropof_date__lt=current_date)
    upcoming_bookings = BookingModel.objects.filter(user__user_name=username, pickup_date__gte=current_date)
    if request.POST.get('save-btn'):
        user = UserRegModel.objects.get(user_name=username)
        user.user_name = request.POST.get('username')
        user.user_mail = request.POST.get('usermail')
        user.user_pno = request.POST.get('userpno')
        user.license_no = request.POST.get('license')
        user.save()
        return render(request, 'account.html',
                      {'name': username, 'user': users, 'completed_bookings': completed_bookings,
                       'upcoming_bookings': upcoming_bookings})
    return render(request, 'account.html', {'name': username, 'user': users, 'completed_bookings': completed_bookings,
                                            'upcoming_bookings': upcoming_bookings})


def faq_section(request):
    return render(request, 'faq.html')


def payment(request):
    pickup_loc = request.session.get('pickup_location')
    pickup_date = request.session.get('pickup_date')
    dropoff_loc = request.session.get('dropoff_location')
    dropoff_date = request.session.get('dropoff_date')
    hours = request.session.get('hour')

    pdate = datetime.strptime(pickup_date, '%Y-%m-%d')
    ddate = datetime.strptime(dropoff_date, '%Y-%m-%d')

    pickup = PlacesModel.objects.filter(places_id=pickup_loc)
    dropoff = PlacesModel.objects.filter(places_id=dropoff_loc)

    carid = request.session.get('carid')
    cars = CarImgModel.objects.filter(car_id=carid)

    user_authenticated = 'user' in request.session
    username = request.session.get('user', None)
    print(request.POST.get('amount'))
    if request.method == 'POST':
        amount = int(request.POST.get('amount')) * 100

        # Create razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        # create order
        payment_data = {
            'amount': amount,
            'currency': 'INR',
            'payment_capture': 1
        }
        response_payment = client.order.create(data = payment_data)
        print(response_payment)
        order_id = response_payment['id']
        order_status = response_payment['status']

        # if order_status == 'created':
        #     payment = PaymentModel()
        #     payment.user = UserRegModel.objects.get(user_name=username)
        #     payment.amount = amount
        #     payment.order_id = order_id
        #     payment.save()
        response_payment['name'] = username

        return render(request, 'payment.html', {'cars': cars, 'user': user_authenticated, 'name': username,
                                            'pickup': pickup, 'pickup_date': pdate.date(), 'dropoff': dropoff,
                                            'dropoff_date': ddate.date(), 'payment': response_payment})
    return render(request, 'payment.html', {'cars': cars, 'user': user_authenticated, 'name': username,
                                            'pickup': pickup, 'pickup_date': pdate.date(), 'dropoff': dropoff,
                                            'dropoff_date': ddate.date()})


def payment_status(request):
    booking = request.session.get('booking_id')
    user_authenticated = 'user' in request.session
    username = request.session.get('user', None)
    razorpay_payment_id = request.GET.get('razorpay_payment_id')
    razorpay_order_id = request.GET.get('razorpay_order_id')
    razorpay_signature = request.GET.get('razorpay_signature')
    price = request.GET.get('price')

    payment = PaymentModel()
    payment.user = UserRegModel.objects.get(user_name = username)
    payment.amount = price
    payment.order_id = razorpay_order_id
    payment.razorpay_id = razorpay_payment_id
    payment.razorpay_payment_signature = razorpay_signature
    payment.booking = BookingModel.objects.get(booking_id = booking)
    payment.paid = True
    payment.save()
    return render(request, 'payment_status.html', {'user': user_authenticated, 'name': username})
