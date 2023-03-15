from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, name, phone_number):
        if not name:
            raise ValueError("Users must have a name.")
        if not phone_number:
            raise ValueError("Users must have a phone number.")

        user = self.model(
            name=name,
            phone_number=phone_number,
        )

        user.save(using=self._db)
        return user

    def create_superuser(self, name, phone_number, password):
        raise ValueError("Cannot create a superuser without a password.")


class CustomUser(AbstractBaseUser):
    name = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
