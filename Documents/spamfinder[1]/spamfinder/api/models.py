from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class ClientUserManager(BaseUserManager):
    def create_user(self, phone, name, email=None, password=None):
        if not phone:
            raise ValueError("Users must have a phone number")
        
        user = self.model(
            phone=phone,
            name=name,
            email=email,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, email=None, password=None):
        user = self.create_user(
            phone=phone,
            name=name,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class ClientUser(AbstractBaseUser):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = ClientUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class PhoneNumber(models.Model):
    number = models.CharField(max_length=15, unique=True, null=False)
    report_count = models.IntegerField(default=0)

    def __str__(self):
        return self.number


class Contact(models.Model):
    user = models.ForeignKey('ClientUser', on_delete=models.CASCADE, related_name='contacts')
    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=255)
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.phone_number})"