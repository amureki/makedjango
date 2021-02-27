from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.mail import send_mail
from django.db import models, transaction
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """Create and save a `User` with the given email and password."""
        now = timezone.now()
        if not email:
            raise ValueError("An email address must be provided.")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
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

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class SimpleIdentityMixin(models.Model):
    """A mixin class that provides a first name/last name representation of user identity."""

    full_name = models.CharField("Full name", max_length=200, blank=True)
    is_staff = models.BooleanField(
        "Staff status",
        default=False,
        help_text="Designates whether the user can log into the admin site.",
    )
    is_active = models.BooleanField(
        "Active",
        default=True,
        help_text="Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts.",
    )
    date_joined = models.DateTimeField("Date joined", default=timezone.now)

    class Meta:
        abstract = True

    def get_full_name(self):
        """Return the full name of the user."""
        return self.full_name


class AbstractUser(SimpleIdentityMixin, PermissionsMixin, AbstractBaseUser):
    """
    An abstract base class implementing a fully featured User model.
    This model includes admin-compliant permissions and uses email as a username.
    All fields other than email and password are optional.
    """

    email = models.EmailField("Email address", max_length=254, unique=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        abstract = True
        verbose_name = "User"
        verbose_name_plural = "Users"

    def email_user(self, subject, message, from_email=None, to_emails=None, **kwargs):
        """Send an email to this user."""
        if to_emails is None:
            to_emails = [self.email]

        send_mail(subject, message, from_email, to_emails, **kwargs)


class User(AbstractUser):
    """Final user class that should be instantiated."""
    pass
