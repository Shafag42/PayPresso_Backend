from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone

# Create your models here.

''' Baseuser manager which creates new user and create_superuser '''
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have an Email address")
        user = self.model( email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
    def create_personaluser(self,email,password):
        if password is None:
             raise TypeError('Paitent must have a password')
        user = self.create_user(email,password)
        user.is_personal = True
        user.save()
        return user


    def create_businessuser(self,email,password):
        if password is None:
            raise TypeError('Doctors must have a password')
        user = self.create_user(email,password)
        user.is_business = True
        user.save()
        return user

""" Custom User which supports both email and username """
class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name="Email Address")
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_business = models.BooleanField(default=False)
    is_personal = models.BooleanField(default=False)
    is_active = models.BooleanField(_('active'), default=True, help_text=_(
        'Designates whether this user should be treated as active. Unselect this instead of deleting account')
    )
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_trusty = models.BooleanField(_('trusty'), default=False, help_text=_(
        'Designates whether this user has confirmed his account.')
    )

    objects = UserManager()

    USERNAME_FIELD = 'email' # Set email as a default login field
    REQUIRED_FIELDS = []  # <- email and password are required by default


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        """Does the user has permission to view a specific app"""


    @property
    def is_staff(self):
        """Is the user a staff member"""
        return self.is_staff

    @property
    def is_admin(self):
        """Is the user a admin member"""
        return self.is_admin

    @property
    def is_active(self):
        """Is the user active"""
        return self.is_active
    
    class Meta:
        verbose_name = _('MyUser')
        verbose_name_plural = _('MyUsers')
        db_table = 'user'


    def __str__(self):
        return self.email
    

    class BusinessProfile(models.Model):
        user = models.OneToOneField("MyUser", on_delete=models.CASCADE)
        company_name=models.CharField(max_length=255)
        phone_number =models.CharField(max_length=25)

        def __str__ (self):
            return self.company_name


    class PersonalProfile(models.Model):
        user = models.OneToOneField("MyUser", on_delete=models.CASCADE)
        date_of_birth=models.DateField(null=True, blank=True)
        phone_number =models.CharField(max_length=25)

        def __str__ (self):
            return self.phone_number

        

        
