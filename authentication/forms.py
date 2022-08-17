from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    """_summary_

    Args:
        forms (_type_): _description_
    """
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Ton pseudo"}),
        label=''
    )
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={"placeholder": 'Mot de passe'}),
        label=''
    )


class SignupForm(UserCreationForm):
    """_summary_

    Args:
        UserCreationForm (_type_): _description_
    """
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"placeholder": "Ton pseudo", "autocomplete": 0}
        ),
        label=''
    )
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"placeholder": "Prénom", "autocomplete": 0}
        ),
        label=''
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"placeholder": "Nom", "autocomplete": 0}
        ),
        label=''
    )
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email'}
        )
    )
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Mot de passe"}
        ),
        label=''
    )

    class Meta(UserCreationForm.Meta):
        """_summary_

        Args:
            UserCreationForm (_type_): _description_
        """
        model = get_user_model()
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'profile_photo'
        )


class UploadProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('profile_photo', )
