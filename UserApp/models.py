from django.db import models
from AdminApp.models import CarModel

# Create your models here.
class UserRegModel(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=200)
    user_mail = models.CharField(max_length=200)
    user_pasw = models.CharField(max_length=100)
    user_pno = models.CharField(max_length=100)
    license_no = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='Active')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        db_table = 'User'


class LicenseImgModel(models.Model):
    img_id = models.AutoField(primary_key = True)
    user = models.ForeignKey(UserRegModel, on_delete=models.CASCADE, null=True)
    license_img = models.ImageField()
    class Meta:
        db_table = 'User_License'
#
#
class UserProfilePic(models.Model):
    img_id = models.AutoField(primary_key = True)
    user = models.ForeignKey(UserRegModel, on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField()
    class Meta:
        db_table = 'Profile_Pic'
#
#
class BookingModel(models.Model):
    booking_id = models.AutoField(primary_key = True)
    user = models.ForeignKey(UserRegModel, on_delete=models.CASCADE, null=True)
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE, null=True)
    pickup = models.CharField(max_length=200)
    pickup_date = models.DateField()
    dropof = models.CharField(max_length=200)
    dropof_date = models.DateField()
    action = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        db_table = 'Booking'
#
#
class CommentModel(models.Model):
    cmt_id = models.AutoField(primary_key = True)
    user = models.ForeignKey(UserRegModel, on_delete=models.CASCADE, null=True)
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE, null=True)
    # booking = models.ForeignKey(BookingModel, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField()
    comment = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='Active')

    def __str__(self):
        return f"Review by {self.user.user_name}"

    class Meta:
        db_table = 'Comments'
#
#
# class ComplaintsModel(models.Model):
#     complaint_id = models.AutoField(primary_key = True)
#     user = models.ForeignKey(UserRegModel, on_delete=models.CASCADE, null=True)
#     booking = models.ForeignKey(BookingModel, on_delete=models.CASCADE, null=True)
#     complaint = models.CharField(max_length=200)
#     class Meta:
#         db_table = 'Complaints'
#
#
class PaymentModel(models.Model):
    user = models.ForeignKey(UserRegModel, on_delete=models.CASCADE, null=True)
    booking = models.ForeignKey(BookingModel, on_delete=models.CASCADE, null=True)
    amount = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_signature = models.CharField(max_length=100, blank=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        db_table = 'Payment'