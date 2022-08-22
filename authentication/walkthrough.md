# Walkthrough

## User Model
```python
class User(AbstractUser):
    """_summary_

    Args:
        AbstractUser (_type_): _description_
    """
    LEARNER = "LEARNER"
    JURY = "JURY"
    MENTOR = "MENTOR"
    ADMINISTRATEUR = "ADMINISTRATEUR"

    ROLE_CHOICES = (
        (LEARNER, "Learner"),
        (JURY, "Jury"),
        (MENTOR, "Mentor"),
        (ADMINISTRATEUR, "Administrateur"),
    )

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        default='profile_photos/photoretouches.jpeg', blank=True, null=True
    )
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='LEARNER'
    )
```

## User settings
```python
ROOT_URLCONF = "on_the_road_main.urls"
AUTH_USER_MODEL = 'authentication.User
```

## Login Form
```python
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
```

## Login view
```python
from .forms import LoginForm, SignupForm, UploadProfilePhotoForm

def login_page(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Identifiants invalides.'
    return render(
        request,
        'authentication/login.html',
        context={'form': form, 'message': message}
    )
```

## authentication urls
```python
from django.urls import path
from authentication import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('logout/', views.logout_user, name='logout'),
]
```

## Login template
```html
<!DOCTYPE html>
<html>
    {% load static %}
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
        <link rel="stylesheet" href="{% static 'the_main_space/css/style.css' %}" type="text/css">
        <title>LOGIN OR SUBSCRIBE</title>
    </head>
    <body>
        <header id="header">
            <img src="{% static 'the_main_space/images/LogoMakr-05nrqV.png' %}" alt="">
            <div class="ontheroad">
                {% block title %}<h1>ON THE ROAD JS</h1>{% endblock title %}
            </div>
            <div id="connection_submit">
                <form method="post">
                    {{ form.as_p }}
                    {% csrf_token %}
                    <button type="submit" >Se connecter</button>
                </form>
                <p>Pas encore membre ? <a href="{% url 'signup' %}">Inscrivez-vous maintenant !</a></p>
            </div>
            {% if user.is_authenticated %}
                <p> 
                    Vous êtes connecté en tant que {{ user }}. 
                    <a href="{% url 'logout' %}" class="deconnexion_retour">
                        Se déconnecter
                    </a>
                </p>
            {% endif %}
        </header>
    </body>
</html>
```

## Login settings
```python
LOGIN_URL = 'login'
```

## Signup form
```python
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

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
        ),
        label=''
    )
    password1 = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password'}
        ),
        label=''
    )
    password2 = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirm Password'}
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
        )
```

## Signup view
```python
def signup_page(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect('home')
    return render(
        request,
        'authentication/signup.html',
        context={'form': form},
    )
```