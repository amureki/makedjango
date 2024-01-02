from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from users import validators


class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, is_staff, is_superuser, **extra_fields):
        """Create and save a `User` with the given email and password."""
        now = timezone.now()
        if not email:
            raise ValueError("An email address must be provided.")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, username=None, password=None, **extra_fields):
        return self._create_user(email, username, password, False, False, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        return self._create_user(email, username, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    email = models.EmailField(
        "email address",
        max_length=254,
        unique=True,
        db_collation="case_insensitive",
        validators=[validators.EmailValidator()],
    )
    username = models.CharField(
        "username",
        max_length=20,
        unique=True,
        db_collation="case_insensitive",
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        validators=[validators.UsernameValidator()],
    )
    name = models.CharField("name", max_length=70, blank=True)

    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into the admin site.",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text="Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts.",
    )
    date_joined = models.DateTimeField("date joined", default=timezone.now)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def anonymize(self):
        self.email = self.name = ""
        self.is_active = False
        self.save(update_fields=["email", "name", "is_active"])
