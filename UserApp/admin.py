from django.contrib import admin
from UserApp.models import *

# Register your models here.
admin.site.register(UserRegModel)
admin.site.register(LicenseImgModel)
admin.site.register(UserProfilePic)
admin.site.register(BookingModel)
admin.site.register(CommentModel)
admin.site.register(PaymentModel)