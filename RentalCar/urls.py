"""
URL configuration for RentalCar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from UserApp import views as view_users
from AdminApp import views as view_admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    #users
    path('', view_users.home, name='home'),
    path('logout', view_users.logout, name='logout'),
    path('booking', view_users.booking, name='booking'),
    path('blogs', view_users.blogs, name='blogs'),
    path('kochi', view_users.kochiblog, name='kochi'),
    path('tvm', view_users.tvmblog, name='tvm'),
    path('contact', view_users.contact, name='contact'),
    path('about', view_users.about, name='about'),
    path('car', view_users.car, name='car'),
    path('payment', view_users.payment, name='payment'),
    path('payment_success/', view_users.payment_status, name='payment_success'),
    path('account', view_users.account, name='account'),
    path('faq', view_users.faq_section, name= 'faq'),

    #admin
    # path('car_admin', view_admin.show, name='show'),
    # path('car_reg', view_admin.car_reg, name='car_reg'),
    # path('carimg_reg', view_admin.carimg_reg, name='carimg_reg'),
    # path('carinterior_reg', view_admin.carinterior_reg, name='car_interiors'),
    # path('location_reg', view_admin.location_reg, name='location'),
    # path('places_reg', view_admin.places_reg, name='places'),


    #customadmin
    path('admin_home', view_admin.admin_home, name='admin_home'),
    path('admin_car', view_admin.admin_car, name='admin_car'),
    path('admin_car_reg', view_admin.admin_car_reg, name='admin_car_reg'),
    path('admin_car_images', view_admin.admin_car_images, name='admin_car_images'),
    path('admin_car_images_reg', view_admin.carimg_reg, name='admin_carimg_reg'),
    path('admin_car_interiors', view_admin.admin_car_interiors, name='admin_car_interiors'),
    path('admin_car_interiors_reg', view_admin.carinterior_reg, name='admin_interior_reg'),
    path('admin_bookings', view_admin.admin_bookings, name='admin_bookings'),
    path('admin_payment', view_admin.admin_payment, name='admin_payment'),

    path('reset_password', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
