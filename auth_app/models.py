from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    """
    Custom user model that uses email as the username field.
    Includes first and last name, and standard user flags.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email ist erforderlich")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    CustomUser model that extends AbstractBaseUser and PermissionsMixin.
    Attributes:
        email (EmailField): The unique email address used for authentication.
        first_name (CharField): Optional first name of the user.
        last_name (CharField): Optional last name of the user.
        is_active (BooleanField): Indicates whether the user account is active.
        is_staff (BooleanField): Indicates whether the user has staff privileges.
        date_joined (DateTimeField): Timestamp of when the user account was created.
    Meta:
        USERNAME_FIELD (str): Field used as the unique identifier for authentication.
        REQUIRED_FIELDS (list): Additional fields required for user creation.
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
