from django.contrib import admin

from users import models as user_models


# Register your models here.
admin.site.register(user_models.CustomUser)
