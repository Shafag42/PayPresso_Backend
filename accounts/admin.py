from django.contrib import admin
from accounts.models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):

    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'birthday', 'company_name', 'voen', 'is_staff', 'is_personal', 'is_business','password')
    fieldsets_personal = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'phone_number', 'birthday')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_personal','is_business')}),
        (_('Important dates'), {'fields': ('date_joined',)}),
    )
    fieldsets_business = (
        (None, {'fields': ('email', 'password')}),
        (_('Company Info'), {'fields': ('company_name', 'voen', 'phone_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_business')}),
        (_('Important dates'), {'fields': ('date_joined',)}),
    )
    add_fieldsets_personal = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'birthday', 'password','is_business'),
        }),
    )
    add_fieldsets_business = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'company_name', 'voen', 'phone_number', 'password'),
        }),
    )
    

    def get_fieldsets(self, request, obj=None):
        if obj and obj.is_business:
            return self.fieldsets_business
        elif obj and obj.is_personal:
            return self.fieldsets_personal
        elif request.POST.get('is_business'):
            return self.fieldsets_business
        else:
            return self.fieldsets_personal

    def get_add_fieldsets(self, request):
        if request.POST.get('is_business'):
            return self.add_fieldsets_business
        else:
            return self.add_fieldsets_personal

    list_display_personal = ('email', 'first_name', 'last_name', 'phone_number', 'birthday', 'is_staff', 'is_personal', 'is_business')
    list_display_business = ('email', 'is_staff', 'is_personal', 'is_business')

    def get_list_display(self, request):
        if request.POST.get('is_business'):
            return self.list_display_business
        else:
            return self.list_display_personal
    
    def get_list_display(self, request):
        if request.POST.get('is_business'):
            return self.list_display_business
        else:
            return self.list_display_personal
        
    # def add_view(self, request, extra_context=None):
    #     request.POST._mutable = True
    #     is_business = request.POST.get('is_business')
    #     if is_business:
    #        self.fieldsets = self.add_fieldsets_business
    #     else:
    #        self.fieldsets = self.add_fieldsets_personal
    #     return super().add_view(request, extra_context=extra_context)
    

    def add_view(self, request, extra_context=None):
        if 'is_business' in request.POST:
            self.fieldsets = self.add_fieldsets_business
        else:
            self.fieldsets = self.add_fieldsets_personal
        return super().add_view(request, extra_context=extra_context)

   


    def save_model(self, request, obj, form, change):
        if request.POST.get('is_business'):
            obj.is_personal = False
            obj.is_business = True
        else:
            obj.is_personal = True
            obj.is_business = False
        super().save_model(request, obj, form, change)

admin.site.register(CustomUser, CustomUserAdmin)

