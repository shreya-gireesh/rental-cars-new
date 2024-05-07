from django.db import models


# Create your models here.
class AdminModel(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=200)
    admin_mail = models.CharField(max_length=200)
    admin_password = models.CharField(max_length=200)

    class Meta:
        db_table = 'Admin'


class CarModel(models.Model):
    CAR_TYPE_CHOICES = [
        ('Manual', 'Manual'),
        ('Automatic', 'Automatic'),
    ]

    CAR_FUEL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
    ]

    car_id = models.AutoField(primary_key=True)
    car_name = models.CharField(max_length=200)
    car_company = models.CharField(max_length=200)
    car_type = models.CharField(max_length=100, choices=CAR_TYPE_CHOICES, null=True)
    car_fuel = models.CharField(max_length=100, choices=CAR_FUEL_CHOICES, null=True)
    car_seats = models.IntegerField(null=True)
    car_price = models.IntegerField()
    status = models.CharField(max_length=100, default='Active')

    def __str__(self):
        return self.car_name

    class Meta:
        db_table = 'Car'


class CarImgModel(models.Model):
    carimg_id = models.AutoField(primary_key=True)
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE, null=True)
    car_img = models.ImageField(upload_to='images/')

    class Meta:
        db_table = 'CarImage'


class CarInteriorsModel(models.Model):
    car_interior_id = models.AutoField(primary_key=True)
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE, null=True)
    car_interior = models.ImageField(upload_to='car_interiors/')

    class Meta:
        db_table = 'Car_Interior_Images'


# class LocationModel(models.Model):
#     location_id = models.AutoField(primary_key=True)
#     location = models.CharField(max_length=200)
#
#     def __str__(self):
#         return self.location
#
#     class Meta:
#         db_table = 'Location'


class PlacesModel(models.Model):
    places_id = models.AutoField(primary_key=True)
    places = models.CharField(max_length=200)

    def __str__(self):
        return self.places

    class Meta:
        db_table = 'Places'

#
#
# class BlogModel(models.Model):
#     blog_id = models.AutoField(primary_key=True)
#     blog_name = models.CharField(max_length=200)
#     details = models.TextField()
#     status = models.CharField(max_length=100, default='Active')
#
#     class Meta:
#         db_table = 'Blog'
#
#
# class BlogImgModel(models.Model):
#     blogimg_id = models.AutoField(primary_key=True)
#     blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE, null=True)
#     blog_img = models.ImageField()
#
#     class Meta:
#         db_table = 'BlogImage'
