from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()


class AbstractUserCreationForm(forms.ModelForm):
    """A form that creates a user, with no privileges, from the given username and password."""

    error_messages = {
        "duplicate_username": "A user with that username already exists.",
        "password_mismatch": "The two password fields didn't match.",
    }

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        help_text="Enter the same password as above, for verification.",
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        self.instance.username = self.cleaned_data.get("username")
        password_validation.validate_password(
            self.cleaned_data.get("password2"), self.instance
        )
        return password2

    def save(self, commit=True):
        user = super(AbstractUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserCreationForm(AbstractUserCreationForm):
    """An implementation of `AbstractUserCreationForm` that uses an email as an identifier."""

    error_messages = {
        "duplicate_email": "A user with that email already exists.",
        "password_mismatch": "The two password fields didn't match.",
    }

    class Meta:
        model = User
        fields = (
            "email",
            "full_name",
        )

    def clean_email(self):
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages["duplicate_email"],
            code="duplicate_email",
        )


class AbstractUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text="Raw passwords are not stored, so there is no way to see "
        "this user's password, but you can change the password "
        'using <a href="password/">this form</a>.',
    )

    def __init__(self, *args, **kwargs):
        super(AbstractUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get("user_permissions", None)
        if f is not None:
            f.queryset = f.queryset.select_related("content_type")

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserChangeForm(AbstractUserChangeForm):
    class Meta:
        model = User
        fields = "__all__"
