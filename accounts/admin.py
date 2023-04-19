from django.contrib import admin
from .models import PersonalUser, BusinessUser,PersonalProfile,BusinessProfile
from django.contrib.auth.admin import UserAdmin


class PersonalUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone_number','birthday','date_joined', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number','birthday')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        # ('Important dates', {'fields': ( 'date_joined')}),
        ('Groups & Permissions', {'fields': ('groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','first_name', 'last_name', 'phone_number','birthday', 'password1', 'password2','date_joined',  'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)

class BusinessUserAdmin(UserAdmin):
    list_display = ('email', 'company_name', 'voen', 'phone_number','date_joined', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Company Info', {'fields': ('company_name', 'voen', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        # ('Important dates', {'fields': ('date_joined')}),
        ('Groups & Permissions', {'fields': ('groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'company_name', 'voen', 'phone_number', 'password1', 'password2','date_joined','is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'company_name', 'voen', 'phone_number')
    ordering = ('email',)

   
class PersonalProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone_number', 'birthday')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    fields = ('first_name', 'last_name', 'phone_number', 'birthday','date_joined')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user__isnull=False)
    
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ('business_user', 'company_name', 'phone_number', 'voen')
    search_fields = ('business_user__email', 'company_name')
    fields = ('company_name', 'phone_number', 'voen', 'business_user','date_joined')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(business_user__isnull=False)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.business_user = request.user
        obj.save()


admin.site.register(PersonalUser, PersonalUserAdmin)
admin.site.register(BusinessUser, BusinessUserAdmin)
admin.site.register(PersonalProfile, PersonalProfileAdmin)
admin.site.register(BusinessProfile, BusinessProfileAdmin)
