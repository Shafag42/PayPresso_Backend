from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class PersonalUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, birthday, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            birthday=birthday,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone_number, birthday, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, first_name, last_name, phone_number, birthday, password, **extra_fields)


class PersonalUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    birthday = models.DateField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'birthday']

    objects = PersonalUserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='personal_usersrrr',
        related_query_name='personal_userrrr'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='personal_usersrr',
        related_query_name='personal_userrrr'
    )

    class Meta:
        verbose_name = 'Personal User'
        verbose_name_plural = 'Personal Users'

    def __str__(self):
        return self.email


class BusinessUserManager(BaseUserManager):
    def create_user(self, email, company_name, voen, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        user = self.model(
            email=self.normalize_email(email),
            company_name=company_name,
            voen=voen,
            phone_number=phone_number,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, company_name, voen, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, company_name, voen, phone_number, password, **extra_fields)
    
    

class BusinessUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    company_name = models.CharField(max_length=255)
    voen = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company_name', 'voen', 'phone_number']

    objects = BusinessUserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='business_users',
        related_query_name='business_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='business_users',
        related_query_name='business_user'
    )

    class Meta:
        verbose_name = 'Business User'
        verbose_name_plural = 'Business Users'

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(PersonalUser, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    business_user = models.OneToOneField(BusinessUser, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    voen = models.CharField(max_length=20, blank=True)
    # address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Profile for {self.user} / {self.business}"