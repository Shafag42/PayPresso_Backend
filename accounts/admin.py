from django.contrib import admin
from .models import PersonalUser, BusinessUser,Profile

admin.site.register(PersonalUser)
admin.site.register(BusinessUser)
admin.site.register(Profile)
