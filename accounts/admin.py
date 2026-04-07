## import admin avails all inbuilt operations to manage the admin interface of our app
from django.contrib import admin
# import the exsisting configs for an admin user
from django.contrib.auth.admin import UserAdmin
# import the custom user model/ custom users table to be registered in the admin interface
from .models import User
# Register your models here.
# step1: utilize the admin decorator to register our custom user model
@admin.register(User)
# step2: create a custom admin class to specify the display and field options for our custom user model
class CustomUserAdmin(UserAdmin):
    # override the default list display to show specific fields in the admin interface
    list_display = ('username', 'email', 'user_type', 'is_staff', 'date_joined')
    #override the filtering of above list
    list_filter = ('user_type', 'is_staff', 'is_superuser')
    # override what credentials the admin can create
    # add our own custom fields
    # UserAdmin fieldsets point to existing django user model fields and we are adding our custom fields to it
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', 
         {'fields': ('user_type', 'profile_image', 'bio')
          }),
    )
    #We are adding above fields  to djangos inbuilt admin system
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', 
         {'fields': ('user_type',)
          }),
    )
    