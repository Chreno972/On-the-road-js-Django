<!-- forms > views > templates (gabarit) > main urls.py
models (migr) > views > templates > templates > main urls.py -->

**Configuration du projet**

`mkdir fotoblog && cd fotoblog` très pratique

Maintenant, créez un environnement virtuel Python, activez-le, et installez Django. Créez aussi un fichier  requirements.txt  avec  pip freeze  pour pouvoir recréer l’environnement ailleurs.


```shell
~/fotoblog  → python -m venv  env
~/fotoblog  → env\Scripts\activate
(ENV) ~/fotoblog  → pip install django
(ENV) ~/fotoblog → pip freeze > requirements.txt
```

Notre projet contiendra deux applications : l’une, nommée  authentication, qui gèrera l’authentification et les comptes, et l’autre,  blog  , qui hébergera notre logique de partage de billets de  blog  et de photos.

```shell
# Ne pas oublier le . qui positionne manage.py à l'extérieur de fotoblog, 
# Cela évite de créer un autre 3ème dossier fotoblog, comme ça nos apps
# peuvent être construits à l'extérieur du dossier de projet
(ENV) ~/fotoblog  → django-admin startproject fotoblog . 
(ENV) ~/fotoblog  → python manage.py startapp authentication
(ENV) ~/fotoblog  → python manage.py startapp blog
```

Ajoutez ces applications aux  INSTALLED_APPS  dans les paramètres.

```python
# fotoblog/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
    'blog',
]

LANGUAGE_CODE = 'fr-fr'
```

Configurez le projet en tant que dépôt Git, et effectuez le commit initial.

```bash
(ENV) ~/fotoblog  → git init
(ENV) ~/fotoblog  → echo env > .gitignore # écrit env dans gitignore en le créant
(ENV) ~/fotoblog  → echo __pycache__ >> .gitignore # ajoute ensuite pycache dedans
(ENV) ~/fotoblog  → echo db.sqlite3 >> .gitignore
(ENV) ~/fotoblog  → # Vous pouvez ajouter d’autres fichiers et répertoires dans le .gitignore ici
(ENV) ~/fotoblog  → git add .
(ENV) ~/fotoblog  → git status
(ENV) ~/fotoblog  → git commit -m “initial commit”

git branch -M main
git remote add origin https://github.com/Chreno972/the_big_thing.git
git push -u origin main
```

**mise en place d’un modèle de données pour les utilisateurs**

Par convention, les données concernant un utilisateur individuel sont stockées dans un modèle nommé User(Utilisateur). Django fournit un modèle `User` par défaut. Ce modèle possède de nombreuses méthodes et fonctionnalités spéciales, en particulier en ce qui concerne l’authentification et les permissions, qui lui permettent de s’intégrer automatiquement au framework Django. Heureusement, vous n’avez pas à vous limiter au modèle par défaut. Voyons comment personnaliser  User.

Même si vous trouvez que le modèle  User  par défaut est tout à fait convenable, je vous conseille de toujours implémenter un modèle  User  personnalisé dans votre projet. Et ce, même s’il est identique au modèle par défaut !
Pourquoi ? Parce qu’il est difficile et compliqué de migrer vers un modèle  User   personnalisé après la configuration de votre site Django et l’exécution de vos migrations initiales. Cela demande beaucoup de migrations délicates et une compréhension en profondeur de SQL. Les projets changent, et les clients modifient les spécifications. Épargnez-vous une migraine et configurez un modèle  User  personnalisé dès le début de votre projet. `AbstractUser et AbstractBaseUser`

`La classeAbstractUser` contient tous les champs et les méthodes du  User  par défaut.
Si vous pensez que les fonctionnalités de la classe  User  par défaut répondront à vos besoins à elles seules, alors il vous sera vraiment facile de l’utiliser comme modèle  User  personnalisé :

```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

"""
Ceci fournit tous les champs et fonctionnalités du modèle  User  par défaut, avec la souplesse supplémentaire 
de pouvoir y ajouter des champs et des méthodes par la suite.
Imaginons, par exemple, que vous vouliez stocker un numéro de compte unique à 10 chiffres pour chaque utilisateur.
Pour ce faire, spécifiez-le simplement comme vous le feriez pour un champ de n’importe quel modèle.
Si vous voulez ajouter davantage de champs à la classe  User, vous pouvez les spécifier de la même façon.
"""

class User(AbstractUser):
    account_number =  CharField(max_length=10, unique=True)
```

Si on ne souhaite pas utiliser tous les champs fournis dans la classe  `User`  par défaut ?
Dans ce cas, étendre la classe  `AbstractBaseUser`

La classe `AbstractBaseUser` ne contient aucun champ, excepté  password  (mot de passe). Elle possède aussi une suite de méthodes pour gérer l’authentification (tout comme  `AbstractUser`).
Lorsque vous étendez `AbstractBaseUser`, vous devez spécifier tous les champs que vous voulez inclure (sauf  password). Il faut aussi un peu de configuration supplémentaire pour qu’elle s’intègre bien au système d’authentification de Django.
Les configurations clés à implémenter avec le modèle  AbstractBaseUser  sont les suivantes :

`USERNAME_FIELD`  — indique le nom du champ devant être utilisé comme identifiant de connexion.

`EMAIL_FIELD`  — indique le nom du champ contenant l’adresse e-mail principale d’un utilisateur ('email' par défaut).

`REQUIRED_FIELDS`  — liste des champs à spécifier obligatoirement lors de l’utilisation de la commande  `python manage.py createsuperuser`.

`is_active`  — vaut  True  par défaut dans   `AbstractBaseUser`, mais vous pouvez ajouter votre propre champ si vous voulez gérer les utilisateurs actifs et inactifs. 

Et si je veux utiliser une adresse e-mail pour m’identifier ?
C’est facile ! Configurez simplement la constante  `USERNAME_FIELD`  sur le champ email. Django exige qu’il soit unique. Si votre classe  User  hérite de `AbstractUser`,  vous pouvez aussi supprimer le champ  username  en le réglant sur  None.

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = None

    USERNAME_FIELD = 'email'
```

Très bien, maintenant que nous avons vu différentes façons d’implémenter un modèle  User  avec Django, faisons-le dans notre application !

En général, il est préférable de construire son modèle à partir du modèle AbstractUser, car il s’intégrera automatiquement avec le reste du framework Django et aura la meilleure compatibilité avec des applications tierces.

Pour notre site, nous voulons inclure toutes les fonctionnalités de la classe  `User`  par défaut. Nous allons donc étendre  `AbstractUser`. Nous allons aussi ajouter deux champs supplémentaires :

`ImageField`  contenant une photo de profil,

et `role`, un `CharField`, qui différenciera les deux types d’utilisateurs sur notre site, les créateurs et les abonnés.

**Ajoutez un modèle  User  dans  authentication**
Le fait de désigner le  CREATOR  (créateur) et leSUBSCRIBER  (abonné) comme des constantes vous permet de vérifier la valeur du champ  role  (rôle) sans écrire la valeur en dur. Par exemple, si user.role == user.CREATOR.



```python
""" Étape 1 : Créez le modèle User   """

class User(AbstractUser):
    CREATOR = "CREATOR"
    SUBSCRIBER = "SUBSCRIBER"

    ROLE_CHOICES = (
        (CREATOR, "Créateur"),
        (SUBSCRIBER, "Abonné"),
    )

    profile_photo = models.ImageField()
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)

# dans le modèle hours, peut-on tenir compte de la date à laquelle les heures ont été communiquées afin de les additionner et les classer par date, afin de faire des statistiques

"""
Étape 2 : Configurez Django pour utiliser un modèle User personnalisé
Tel quel, Django utilise le modèle  User  par défaut pour l’authentification.
Vous devez donc dire à Django que vous voulez plutôt utiliser votre propre
modèle  User. Pour cela, configurez  AUTH_USER_MODEL  avec votre propre modèle
dans les paramètres. Lorsque vous configurez  AUTH_USER_MODEL  , utilisez la
notation  '<nom-de-l’app>.<nom-du-modèle>'
"""

AUTH_USER_MODEL = 'authentication.User' #l'app authentication . le modèle User

"""
Par rapport au champ ImageField, on est obligé d'intaller Pillow
pour cela on tape py -m pip install Pillow
Puis on makemigrations et migrate
Bravo, vous avez créé un modèle utilisateur personnalisé, généré et exécuté
les migrations !
"""
```

**Résumé**

Django utilise le modèle `User` pour gérer l’authentification. 

C’est toujours une bonne idée d’utiliser un modèle `User` personnalisé dans un projet, même si vous n’avez pas besoin de fonctionnalités supplémentaires, car cela permet de faciliter grandement la personnalisation par la suite. 

Vous pouvez étendre `AbstractUser` pour enrichir le modèle `User` par défaut. 

Vous pouvez étendre `AbstractBaseUser` si vous voulez encore plus de flexibilité, et définir tous les champs vous-même.

Maintenant que vous pouvez stocker des utilisateurs dans la base de données, essayons de les authentifier sur notre site.

---

**Programmez la vue pour que les utilisateurs se connectent**

Parfait ! Nous avons maintenant un moyen de stocker différents utilisateurs dans notre base de données. Néanmoins, pour savoir qui sont ces utilisateurs, nous devons leur donner un moyen de se connecter au site.

**Étape 1 : Créez le LoginForm(formulaire de connexion)**
Tout d’abord, créez un fichier  forms.py  qui contiendra le formulaire de connexion

```python
# authentication/forms.py
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')
```
Vous remarquerez aussi que nous paramétrons le champ Mot de passe (« password ») pour qu’il utilise le widget  forms.PasswordInput. Un widget détermine la façon dont vous affichez le champ. Comme vous l’avez peut-être deviné, le widget  PasswordInput  cache automatiquement la saisie en utilisant un  <input>  HTML avec l’attribut  type="password"  .


**Étape 2 : Créez la vue de la page de connexion**

```python
# authentication/views.py
from django.shortcuts import render

from . import forms

def login_page(request):
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            pass
    return render(request, 'authentication/login.html', context={'form': form})

"""
Django est fourni avec une série de méthodes qui peuvent aider les développeurs à
gagner du temps. Vous pouvez utiliser les fonctions  login et authenticate  du
module  django.contrib.auth  pour l’authentification.
"""

from django.contrib.auth import login, authenticate  
# import des fonctions login et authenticate

def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Bonjour, {user.username}! Vous êtes connecté.'
            else:
                message = 'Identifiants invalides.'
    return render(
        request, 'authentication/login.html', context={'form': form, 'message': message})
```

la fonction  `authenticate`. Cette fonction prend deux arguments : le nom d’utilisateur et le mot de passe.
Si les identifiants sont corrects, elle retourne l’utilisateur correspondant aux identifiants. Sinon, elle retourne None.
La fonction `authenticate` seule ne gère pas la connexion de l’utilisateur. Pour cela, utilisez la fonction `login`. Elle prend deux arguments : l’objet `request` et l’objet `user`  correspondant à l’utilisateur qui doit être connecté.
Vous avez maintenant une vue qui permet à un utilisateur de se connecter au site.

**Étape 3 : Ajoutez un gabarit, ou template**
Nous avons spécifié que nous utilisons le gabaritauthentication/login.html  dans la vue  login_page
Ensuite, créez les gabarits : commencez par un gabarit de base qui sera utilisé pour l’ensemble du projet, puis celui de la page de connexion.

```
(ENV) ~/fotoblog (master)
→ mkdir -p  authentication/templates/authentication
(ENV) ~/fotoblog (master)
→ mkdir -p blog/templates/blog/
(ENV) ~/fotoblog (master)
→ mkdir templates
```

```html
# templates/base.html
<html>
    <head>
        <title>FotoBlog</title>
    </head>
    <body>
        <h1>FotoBlog</h1>
        {% block content %}{% endblock content %}
    </body>
</html>

<!--  -->

# authentication/templates/authentication/login.html
{% extends 'base.html' %}
{% block content %}
    <p>{{ message }}</p>
    <form method="post">
        {{ form.as_p }}
        {% csrf_token %}
        <button type="submit" >Se connecter</button>
    </form>
{% endblock content %}
```

Lorsque  APP_DIRS  est réglé sur  True, Django trouve automatiquement le répertoire  templates/  quand il est situé dans une application. Néanmoins, comme nous plaçons le gabarit de base à la racine du projet, nous devons le spécifier danssettings.py  pour que Django puisse trouver ce répertoire.
Ce code dit à Django qu’il y a des gabarits dans le répertoire  templates/  à la racine du projet. Un chemin absolu, c’est-à-dire depuis le répertoire racine, est nécessaire. Utilisez la constante  BASE_DIR  pour permettre cela.

```shell
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.joinpath('templates'),  # <--- ajoutez cette ligne
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

**Étape 4 : Ajoutez l’URL à urlpatterns**

Le  `LoginForm`  est construit et incorporé à la vuelogin_page. Vous avez maintenant un gabarit que vous pouvez utiliser pour générer la page HTML.
Vous n’avez plus qu’à inclure le modèle, ou pattern, d’URL dans `urls.py` 

```python
from django.contrib import admin
from django.urls import path

import authentication.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='login'),
]
```

**Étape 5 : Affichez la page de connexion**
Parfait ! Démarrons le serveur de développement pour voir la nouvelle page de connexion.

Testez la fonctionnalité de connexion et ajoutez la déconnexion
Plus tard, nous construirons une page d’inscription pour permettre aux utilisateurs de rejoindre le site. Mais pour l’instant, commençons par créer un utilisateur dans le shell Django et utilisons-le pour tester la fonctionnalité de connexion. Voici la technique en vidéo
Pour ouvrir le shell Django, exécutez  `python manage.py shell`

```shell
>>> from authentication.models import User
>>> User.objects.create_user(username='toto', password='S3cret!', role='CREATOR')
<User: toto>
```
Maintenant que nous avons un utilisateur stocké dans la base de données, retournons à la page de connexion et essayons de nous connecter.
Ajoutons une vue de déconnexion avec `logout` de  `django.contrib.auth.`
La vue dit à Django de déconnecter l’utilisateur. Vous utilisez ensuite la fonction `redirect`  pour rediriger l’utilisateur vers la page de connexion. La fonction  `redirect`  peut prendre un nom de vue, comme spécifié dans  `urls.py` 

```python
# authentication/views.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from . import forms

def logout_user(request):
    
    logout(request)
    return redirect('login')

def login_page(request):

# authentication/urls.py
urlpatterns = [
    path('logout/', authentication.views.logout_user, name='logout'),
]
```

Pour finir, ajoutez un lien vers la page de déconnexion dans  base.html. Ainsi, il est visible dès qu’un utilisateur est connecté, du moment que vous étendez  base.html

```html
<html>
    <head>
        <title>FotoBlog</title>
    </head>
    <body>
        <h1>FotoBlog</h1>
        {% block content %}{% endblock content %}
        {%  if user.is_authenticated %}
            <p> 
                Vous êtes connecté en tant que {{ request.user }}. 
                <a href="{% url 'logout' %}">
                    Se déconnecter
                </a>
            </p>
        {% endif %}
    </body>
</html>
```

Vous pouvez toujours accéder à l’objet  `user`  dans le gabarit. Il correspond à l’utilisateur  qui est en train de naviguer sur le site. Il est important de noter que Django représente un utilisateur anonyme avec un objet de type  `AnonymousUser`.  Par conséquent, la seule présence d’un objet  `user`  ne suffit pas à nous indiquer si l’utilisateur est authentifié.

Pour le vérifier, vous devez utiliser la méthode  `user.is_authenticated`. Elle renvoie `True` si l’utilisateur est authentifié, ou `False` dans le cas contraire.
Maintenant que vous pouvez connecter et déconnecter des utilisateurs, créons une page d’accueil vers laquelle rediriger les utilisateurs une fois connectés. Comme cette page ne s’occupe pas de l’authentification, vous allez la créer dans l’application `blog`.

```python
# blog/views.py
def home(request):
    return render(request, 'blog/home.html')

# fotoblog/urls.py
import blog.views

urlpatterns = [
    ...
    path('home/', blog.views.home, name='home'),
]
```

```html
# blog/templates/blog/home.html
{% extends 'authentication/base.html' %}
{% block content %}
    <p>Vous êtes connecté !</p>
{% endblock content %}
```

**Configurez une redirection après connexion**

```python
# views.py
def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Identifiants invalides.'
    return render(request, 'authentication/login.html', context={'form': form, 'message': message})
```

**Restreignez l’accès à la page d’accueil**
Utilisons le décorateur  login_required   sur la vue  home  en ajoutant les lignes suivantes au fichier  blog/views.html.

```python
# blog/views.py
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, blog/home.html')

"""
Pour que ça fonctionne, vous devez dire à Django vers quelle page rediriger si l’utilisateur n’est pas connecté. Faites-le en configurant LOGIN_URL avec l’URL de la page de connexion ou, encore mieux, avec le nom du modèle d’URL de la page de connexion (login) dans  settings.py
"""

# fotoblog/settings.py
LOGIN_URL = 'login'
```
Si vous regardez attentivement l’URL, vous allez voir qu’on y a ajouté  ?next=/home/. Cela se fait automatiquement et signifie qu’une fois l’utilisateur connecté, il sera redirigé vers la page à laquelle il essayait initialement d’accéder.

**Résumé**
Vous pouvez utiliser la fonction  authenticate   pour vérifier les identifiants d’un utilisateur, et la méthode  login  pour le connecter. Utilisez la méthode  logout   pour le déconnecter.

La méthodeuser.is_authenticatedvérifie si l’utilisateur actuel est connecté.

Vous pouvez utiliser le décorateur login_required  sur une vue pour restreindre l’accès à certaines parties du site aux utilisateurs connectés uniquement.

Maintenant que nous avons construit un système de connexion qui utilise des vues basées sur des fonctions, voyons comment nous servir du pouvoir des vues basées sur des classes pour rendre les choses encore plus faciles.

---

**Ajoutez une page d’inscription**

Tous les formulaires utilisés dans les vues d’authentification basées sur des classes sont également disponibles seuls. Cela vous permet de les utiliser lorsque vous implémentez vos propres vues de connexion. Bien que Django ne donne pas de vue basée sur une classe pour l’inscription, il fournit un formulaire de création d’utilisateur,UserCreationForm  .

Vous pouvez importer tous les formulaires du packageauth  depuisdjango.contrib.auth.forms 

**Étape 1 : Spécialisez UserCreationForm**
UserCreationForm  est un   ModelForm   qui possède trois champs :username,password1,et password2. Comme nous demandons également d’autres champs à l’utilisateur, nous allons devoir spécialiser ce formulaire.

Premièrement, héritez du formulaire et ajoutez vos champs.

```python
# authentication/forms.py
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'role')
```
Étant donné que nous héritons d’unModelForm, la meilleure pratique est d’hériter également de sa classe interneMeta.

Vous voudrez peut-être surcharger complètement la classe  Meta   dans certains cas. Pas de problème ! Vous vous apercevrez également que souvent, vous n’avez aucun élément de la classe  Meta  à surcharger. Dans ce cas, vous pouvez simplement la laisser de côté. Elle sera toujours là, car elle hérite de la superclasse.

Nous utilisons également la méthode utilitaire  get_user_model, qui vous permet d’obtenir le modèle  Usersans l’importer directement. C’est particulièrement important si vous construisez une application conçue pour être réutilisée dans différents projets.

**Étape 2 : Ajoutez une vue d’inscription**
Maintenant que nous avons le formulaire, il nous faut simplement nous occuper de l’ajout de la vue, de l’écriture du gabarit, et de son inclusion dans les modèles d’URL !

```python
# authentication/views.py
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render

from . import forms


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
return render(request, 'authentication/signup.html', context={'form': form})
```

La meilleure façon d’accéder aux paramètres généraux est d’importerdjango.conf.settings. Cela vous permet d’accéder à  LOGIN_REDIRECT_URL, que vous utiliserez pour la redirection après une inscription réussie. Vous avez aussi utilisé la fonction  login  pour connecter l’utilisateur automatiquement.

**Étape 3 : Configurez les gabarits**

```html
# authentication/templates/authentication/signup.html
{% extends 'base.html' %}
{% block content %}
    <h2>Inscription</h2>
    {% if form.errors %}
        {{ form.errors }}
    {% endif %}
    <form method="post">
        {{ form.as_p }}
        {% csrf_token %}
        <button type="submit" >S’inscrire</button>
    </form>
{% endblock content %}

<!-- Ajoutons également un lien d’inscription sur la page de connexion -->

# authentication/templates/authentication/login.html
{% extends 'authentication/base.html' %}
{% block content %}
    <form method="post">
        {{ form.as_p }}
        {% csrf_token %}
        <button type="submit" >Se connecter</button>
    </form>
    <p>Pas encore membre ? <a href="{% url 'signup' %}">Inscrivez-vous maintenant !</a></p>
{% endblock content %}
```

**Étape 4 : Ajoutez le modèle d’URL**

```python
# fotoblog/urls.py
urlpatterns = [
    ...
    path('signup/', authentication.views.signup_page, name='signup'),
]
```

Vous verrez toutes les restrictions sur le mot de passe. Il s’agit des validateurs de mot de passe par défaut de Django, mais vous pouvez les configurer pour qu’ils soient aussi forts ou aussi faibles que vous le souhaitez

**Personnalisez la validation de mot de passe**

Vous devez utiliser des validateurs pour personnaliser la validation de mot de passe. Les validateurs sont des classes utilisées pour valider les données entrantes d’un champ. Le module  auth  fournit quatre validateurs de mots de passe différents, qui se trouvent dans  django.contrib.auth.password_validation

Les validateurs par défaut sont les suivants :

> UserAttributeSimilarityValidator  : invalide le mot de passe s’il est trop similaire aux informations utilisateur.

> MinimumLengthValidator  : invalide le mot de passe en dessous d’une longueur minimale.

> CommonPasswordValidator  : invalide le mot de passe s’il se trouve dans une liste de mots de passe courants.

> NumericPasswordValidator   : invalide le mot de passe s’il est entièrement numérique.

Tous ces validateurs sont activés par défaut, mais vous pouvez les configurer avec  AUTH_PASSWORD_VALIDATORS   dans les paramètres.

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```
Imaginons que les restrictions de mot de passe par défaut soient trop strictes. Vous voulez imposer les obligations suivantes pour le mot de passe :

> Il doit faire au moins huit caractères de long ;

> Il doit contenir des lettres ;

> Il doit contenir des chiffres.

Pour mettre ces conditions en œuvre, il vous faudra créer des validateurs sur mesure.

**Étape 1 : Créez les validateurs**

Tout d’abord, créez un nouveau fichier nommé   `validators.py`   qui contiendra vos validateurs.
Un validateur est une classe qui n’a besoin que de deux méthodes : une méthode  `validate`  et une méthode  `get_help_text`.
Construisons un validateur vérifiant que le mot de passe contient une lettre.

```python
# authentication/validators.py
from django.core.exceptions import ValidationError


class ContainsLetterValidator:
    # vérifier si le mot de passe contient au moins une lettre
    def validate(self, password, user=None):
        if not any(char.isalpha() for char in password):
            # sinon, on lève une exception
            raise ValidationError(
                'Le mot de passe doit contenir une lettre', code='password_no_letters')

    # retourne une chaine de caractère qui guide l'utilisateur          
    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins une lettre majuscule ou minuscule.'
```

La méthode  validate  vérifie le mot de passe et provoque une  ValidationError  si le mot de passe ne remplit pas le critère. La méthode  get_help_text  guide l’utilisateur final pour qu’il sache comment passer la validation.

**Étape 2 : Configurez les paramètres pour utiliser le validateur personnalisé**

Maintenant que le validateur est construit, ajoutons-le aux paramètres. Nous utiliserons également le  MinimumLengthValidator, que nous pouvons configurer à l’aide de la clé  OPTIONS.

```python
# fotoblog/settings.py  
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'authentication.validators.ContainsLetterValidator',
    },
]

"""
Ces validateurs fonctionnent très bien pour les mots de passe, mais vous pouvez aussi les utiliser pour d’autres champs.

Si vous voulez vérifier par exemple qu’un code postal est valide, vous pouvez définir un  PostCodeValidator  dans votre fichier de validateurs, puis le spécifier dans le formulaire
"""

from . import validators


class PostCodeForm(forms.Form):
    post_code = forms.CharField(max_length=10, validators=[validators.PostCodeValidator])
```

Essayez de créer un validateur qui vérifiera le mot de passe pour voir s’il contient un chiffre en utilisant  if not  any(character.is_digit() for character in password).
Vous devrez :

> Créer le   ContainsNumberValidator  dans   authentication/validators.py.

> Configurer   AUTH_PASSWORD_VALIDATORS  dans les paramètres pour utiliser le validateur.

```python
# validators
class ContainsNumberValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir un chiffre', code='password_no_number')

    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins un chiffre.'
```

Vous avez construit une application d’ authentication   (authentification)  qui peut gérer l’inscription et la connexion d’utilisateurs. Néanmoins, nous pourrions ajouter beaucoup plus de fonctionnalités d’authentification. Par exemple :

> La vérification par email.

> L’intégration de la connexion unique avec les comptes sur les réseaux sociaux.

> Des emails de réinitialisation de mot de passe.

La construction de toutes ces fonctionnalités serait un gros travail. Et pourtant, ces tâches sont communes à un grand nombre de sites.
Est-ce que je dois les recréer pour chaque projet ?
Non, ce n’est pas nécessaire.

Il y a plusieurs considérations à prendre en compte lorsqu’on choisit un package :
>
> Il est activement maintenu. Un projet non maintenu ne recevra pas de mises à jour pour être compatible avec les nouvelles versions de Django, et les bugs ne seront pas corrigés. Vous pouvez regarder la date de la dernière mise à jour du dépôt sur GitHub. 
>
> Il est populaire. Les projets à forte popularité sont moins susceptibles de contenir des bugs, mais aussi plus susceptibles d’avoir une communauté de développeurs qui ouvriront activement des pull requests pour réparer les bugs. Une bonne manière d’évaluer la popularité d’un dépôt est de voir son nombre d’étoiles sur GitHub.
>
> Il est compatible avec votre version de Python.
>
> Il est compatible avec votre version de Django.
>
> Beta ou Production. En règle générale, préférez un package en Production. Il existe tout de même des packages Django robustes en phase Beta. Si tous les autres critères sont remplis et que le package est en Beta, vous pouvez probablement l’utiliser sans problèmes.
>
> Si vous travaillez avec un package et que vous trouvez un bug, signalez-le sur GitHub avec une issue. Si vous vous en sentez le courage, dupliquez le dépôt (créez un fork), corrigez-le vous-même, puis ouvrez une pull request. Félicitations, vous êtes maintenant un contributeur open-source !
>
> Une dernière chose à garder en tête : de nombreux packages sont faits par amour de l’art. Ils sont maintenus par des personnes qui prennent sur leur temps libre, de façon complètement bénévole. Les questions et les propositions d’aide seront souvent bien reçues, mais les demandes trop pressantes risquent de ne pas être accueillies chaleureusement !

**Résumé**
Vous pouvez utiliser des formulaires d’authentification Django génériques dans votre projet pour gagner du temps.

Vous pouvez spécifier des validateurs de mot de passe avec le paramètre   AUTH_PASSWORD_VALIDATORS.

Utilisez Django Packages pour trouver des packages tiers à intégrer à votre site.

**Ajoutez les modèles du blog et des photos**

Notre but ultime est de construire un flux qui contiendra des billets de blog et des photos partagés par les créateurs auxquels un utilisateur s’est abonné.

Néanmoins, avant de pouvoir faire cela, nous devons ajouter les modèles qui représenteront ces billets de blog et ces photos, puis nous devons donner aux utilisateurs les moyens de les créer. Découvrez dans la vidéo ci-dessous comment ajouter une page qui permettra aux utilisateurs de mettre en ligne des fichiers.

Commençons par les modèles. Tous nos changements concernent désormais l’application  blog, donc ajoutons ce qui suit à  blog/models.py

```python
# blog/models.py
from django.conf import settings
from django.db import models


class Photo(models.Model):
    image = models.ImageField()
    caption = models.CharField(max_length=128, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


class Blog(models.Model):
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=5000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    starred = models.BooleanField(default=False)
```

Comme vous pouvez le constater, les billets de blog peuvent, de façon optionnelle, être liés à une  photopar la relationForeignKey. Le modèlePhotocontient une image stockée dans le  ImageField.
Générons et exécutons les migrations.

**Mettez en ligne des images avec un formulaire**

Avant de mettre en ligne des images dans Django, vous devez configurer l’emplacement où stocker le contenu média. Dans ce cas, le contenu média correspond aux fichiers et images qui sont mises par les utilisateurs. Configurons maintenant notre application afin de gérer les fichiers mis en ligne par les utilisateurs sur notre site.

**Configurezsettings.py**

Pour ce faire, vous devez configurer deux valeurs danssettings.py.
Premièrement,  MEDIA_URL  , qui est l’URL depuis laquelle Django va essayer de servir des médias. Dans certains cas, ce peut être une URL complète vers un autre hôte, si vous utilisez un service tiers pour servir vos médias.
Pour cette classe, vous allez servir les images en local. Vous pouvez donc fournir un chemin qui pointe vers votre serveur local.
Le deuxième paramètre à configurer est  MEDIA_ROOT. Il indique le répertoire local dans lequel Django doit sauvegarder les images téléversées.

```python
# fotoblog/settings.py
MEDIA_URL = "/media/"
MEDIA_ROOT = "media/"
```

**Étape 2 : Ajoutez les médias aux modèles d’URL**

Vous devez maintenant mettre à jour vos modèles d’URL, de sorte que le média mis en ligne soit accessible par le biais d’une URL

```python
# fotoblog/urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ...
    ]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Désormais, les images stockées dans le répertoireMEDIA_ROOTseront servies au chemin donné parMEDIA_URL.

Cette méthode n’est adaptée que dans un environnement de développement. Sur un site en production, paramétrez  settings.DEBUGsurFalseet implémentez un processus de stockage des médias plus sophistiqué. Habituellement, cela implique de configurer le serveur web pour qu’il serve le média directement, ou qu’il mette en ligne le média à un fournisseur de stockage tiers.

**Étape 3 : Créez un formulaire capable de gérer les mises en ligne d’images**

Maintenant que les paramètres sont configurés, ajoutons un formulaire pour mettre en ligne les photos.
C’est très facile à faire. Vous pouvez utiliser un ModelForm , et Django gérera le transfert du fichier et l’enregistrera dans le système de fichiers pour vous.
Créons un fichierforms.pydansblog/ et ajoutons les lignes suivantes

```python
# blog/forms.py
from django import forms

from . import models

class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image', 'caption']
```

**Étape 4 : Construisez la vue pour qu’elle gère les téléversements d’images**

Et maintenant, ajoutons la vue. D’habitude, on remplit un formulaire uniquement avec l’objet  request.POST. Ici, vu que vous transférez une image, vous devez aussi lui donner tout fichier envoyé avec la requête. Faites-le en passant égalementrequest.FILESen argument.
Nous voulons assigner au champ  uploader  de la  Photo  l’utilisateur connecté à ce moment-là. Vous pouvez créer l’objet  Photo  sans le sauvegarder dans la base de données, en enregistrant le formulaire avec l’argumentcommit=False. Ensuite, assignez la valeur correcte à  uploader, et enfin, sauvegardez le modèle pour le stocker dans la base de données.

```python
# blog/views.py
from django.shortcuts import redirect, render

from . import forms

@login_required
def photo_upload(request):
    form = forms.PhotoForm()
    if request.method == 'POST':
        form = forms.PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            # set the uploader to the user before saving the model
            photo.uploader = request.user
            # now we can save
            photo.save()
            return redirect('home')
    return render(request, 'blog/photo_upload.html', context={'form': form})

"""
Mettre l’image en ligne est facile, car c’est le  ModelForm  qui fait le gros du travail !
"""
```

**Étape 5 : Ajoutez le gabarit**

```html
# blog/templates/blog/photo_upload.html
{% extends 'base.html' %}
{% block content %}
    <h2>Télécharger une photo</h2>
    <form method="post" enctype="multipart/form-data">
        {{ form.as_p }}
        {% csrf_token %}
        <button type="submit" >Publier</button>
    </form>
{% endblock content %}
```

Notez l’ajout de l’attribut  enctype="multipart/form-data" à la balise <form>.C’est obligatoire pour que le formulaire puisse gérer l’envoi de fichiers.

**Étape 6 : Mettez à jour les modèles d’URL**

```python
# fotoblog/urls.py
import blog.views

urlpatterns = [
    ...
    path('photo/upload/', blog.views.photo_upload, name='photo_upload')
]
```

**Étape 7 : Créez un flux, ou « feed »**

```python
# blog/views.py
from . import models

@login_required
def home(request):
    photos = models.Photo.objects.all()
    return render(request, 'blog/home.html', context={'photos': photos})
```

Ensuite, mettez à jour le gabarit. Vous pouvez obtenir le chemin de la photo depuis la propriété  urldu champ  image. La propriété  url  est construite à partir du paramètre  MEDIA_URLque nous avons configuré précédemment.

```html
# blog/templates/blog/home.html
{% extends 'base.html' %}
{% block content %}
    <h2>Photos</h2>
    {% for photo in photos %}
        <img src="{{ photo.image.url }}">
        <p>{{ photo.caption }}</p>
    {% endfor %}
{% endblock content %}
```

C’est gagné ! Les utilisateurs peuvent désormais mettre en ligne leurs photos et les voir dans le flux.
Ensuite, vous allez ajouter une fonctionnalité permettant à un utilisateur de mettre à jour sa photo de profil.
Vous voulez permettre aux utilisateurs de mettre en ligne et d’afficher des photos de profil.
À ces fins, vous allez construire un service de mise en ligne de photo de profil.
Nous avons construit une version mise à jour du site, en soignant le design. Voyons à quoi elle ressemble.

Vous verrez que votre profil utilisateur s’affiche maintenant à gauche de la page, avec le lien         « Changer la photo de profil » en dessous.
Pour le moment, ce lien ne fait rien. Pour le faire fonctionner, vous allez devoir :
Créer un formulaire   UploadProfilePhotoForm  dansauthentication/forms.py  — ça peut être unModelFormpourUser.
Créer une vueupload_profile_photodans l’applicationauthentication  et configurer la vue pour mettre à jour la photo de profil de l’utilisateur.
Créer un gabarit pour cette vue et ajouter la vue aux modèles d’URL.
Envoyer vers la page avec le lienChange Profile Photo.
Afficher la photo de profil de l’utilisateur dans le profil utilisateur s’il a chargé une photo de profil. Sinon, afficher la photo de profil par défaut. Vous pouvez vérifier ceci avec   {% if user.profile_photo %}.

Si vous bloquez :
Vérifiez que vous passezinstance=request.user  à votreUploadProfilePhotoForm  pour mettre à jour l’utilisateur connecté.
Incluez enctype="multipart/form-data">  dans votre balise<form>  .
N’oubliez pas de passerrequest.FILES  à  UploadProfilePhotoForm  lorsque vous gérez les donnéesPOST.

```python
#authentication/forms
class UploadProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('profile_photo', )

#authentication/views
def upload_profile_photo(request):
    form = forms.UploadProfilePhotoForm(instance=request.user)
    if request.method == 'POST':
        form = forms.UploadProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'authentication/upload_profile_photo.html', context={'form': form})
```

**Résumé**
Vous pouvez définir les constantes MEDIA_x dans les paramètres, pour configurer l’emplacement où Django stockera les fichiers chargés par les utilisateurs.
L’ ImageField  vous permet de mettre en ligne des images sur le serveur avec un ModelForm  
Maintenant que vous savez permettre à des utilisateurs de mettre en ligne leurs propres médias dans une vue, le moment est venu de gérer des formulaires multiples sur une seule page !


**Créez plusieurs modèles avec un seul formulaire**

Maintenant que nous avons donné un moyen aux utilisateurs de téléverser des photos, donnons-leur la possibilité de créer aussi des billets de blog.
Parfois, en créant un formulaire, vous voudrez instancier plus d’un modèle à la fois. Dans notre cas, il faut que les utilisateurs puissent créer et une  Photo, et un post de  Blog  en même temps. Découvrez comment en vidéo ci-dessous.

**Étape 1 : Créez les formulaires**

Pour permettre aux utilisateurs d’instancier plusieurs modèles simultanément, il vous faut un formulaire pour chacun des modèles  Photo  et  Blog  .
Vous avez créé un  ModelForm  pour la  Photo  au chapitre précédent. Réutilisons-le ! Et maintenant, créons-en un pour le modèle  Blog  .

```python
# blog/forms.py
from django import forms

from . import models


class PhotoForm(forms.ModelForm):
    ...

class BlogForm(forms.ModelForm):
    class Meta:
        model = models.Blog
        fields = ['title', 'content']
```

**Étape 2 : Incluez les formulaires dans le gabarit**

Voyons à présent comment inclure ces deux formulaires dans le gabarit. La vue n’a pas encore été créée, mais nommons déjà les formulaires  photo_form  et  blog_form  .
Nous voulons que les deux formulaires puissent être envoyés avec un clic unique sur un bouton, pour instancier les deux modèles simultanément. Pour ce faire, incluez ces deux formulaires individuellement sous la même balise  <form>

```html
# blog/templates/blog/create_blog_post.html
{% extends 'base.html' %}
{% block content %}
    <h2>Écrire un billet</h2>
    <form method="post" enctype="multipart/form-data">
        {{ blog_form.as_p }}
        {{ photo_form.as_p }}
        {% csrf_token %}
        <button type="submit" >Publier</button>
    </form>
{% endblock content %}
```

Maintenant que les deux formulaires sont sous la même balise  <form>  , un clic sur le bouton «envoyer» enverra les données  POST  des deux formulaires en même temps. Voyons comment gérer cela dans la vue.

**Étape 3 : Écrivez la vue**

Avant d’apprendre à gérer l’aspect  POST  de la requête, définissons la vue pour inclure à la fois le  photo_form  et le  blog_form  dans le  context  et retourner le rendu du gabarit dans la réponse HTTP.

```python
# blog/views.py
@login_required
    def blog_and_photo_upload(request):
    blog_form = forms.BlogForm()
    photo_form = forms.PhotoForm()
    if request.method == 'POST':
        # handle the POST request here
    context = {
        'blog_form': blog_form,
        'photo_form': photo_form,
}
return render(request, 'blog/create_blog_post.html', context=context)

"""
Désormais, vous pouvez fournir les données  POST  aux formulaires, puis utiliser
la méthode  save()  pour instancier les modèles.
"""

# blog/forms.py
@login_required
def blog_and_photo_upload(request):
    blog_form = forms.BlogForm()
    photo_form = forms.PhotoForm()
    if request.method == 'POST':
        blog_form = forms.BlogForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if all([blog_form.is_valid(), photo_form.is_valid()]):
            blog_form.save()
            photo_form.save()
    context = {
        'blog_form': blog form,
        'photo_form': photo_form,
}
return render(request, 'blog/create_blog_post.html', context=context)
```

La vue va maintenant recevoir la requête  POST  et créer une instance des modèles  Blog  et  Photo  , si les deux formulaires sont valides.
Pourquoi ne pas simplement utiliser  if  blog_form.is_valid() and photo_form.is_valid()   ?
L’exécution de la méthode  is_valid()  sur un formulaire ne se contente pas de vérifier sa validité. Elle génère aussi des messages d’erreur pour tous les champs qui auraient des entrées non valides. Ces messages sont affichés en tant que feedback sur le front-end.
Lorsque vous exécutez une instruction  if  condition_a and condition_b  , Python exige que les deux conditions soient « Truthy » (évaluées à True). Si l’instruction conclut que   condition_a  est « Falsy » (évaluée à False), elle cessera immédiatement d’exécuter la ligne et sautera directement au prochain bloc de code.
Cela signifie que si vous avez l’instruction   if blog_form.is_valid() and photo_form.is_valid()  , et que  blog_form.is_valid()  renvoie  False  , alors  photo_form.is_valid()  ne sera jamais exécuté, et ne générera pas de message d’erreur.
L’approche actuelle marche très bien si vous voulez uniquement instancier ces modèles. Néanmoins, nous devrons lier les deux objets à l’utilisateur qui les a créés, et remplir le champ  photo   pour l’objet  Blog  . Ajustons la vue pour prendre ces éléments en compte.

```python
@login_required
def blog_and_photo_upload(request):
    blog_form = forms.BlogForm()
    photo_form = forms.PhotoForm()
    if request.method == 'POST':
        blog_form = forms.BlogForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if all([blog_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            blog = blog_form.save(commit=False)
            blog.author = request.user
            blog.photo = photo
            blog.save()
            return redirect('home')
    context = {
        'blog_form': blog_form,
        'photo_form': photo_form,
}
return render(request, 'blog/create_blog_post.html', context=context)
```
La vue met désormais correctement à jour tous les champs avant de les enregistrer effectivement dans la base de données. La  photo  et le  blog  seront liés l’un à l’autre, ainsi qu’à l’utilisateur qui les a créés.

**Étape 4 : Ajoutez le modèle d’URL**

```python
# fotoblog/urls.py
urlpatterns = [
    …
    path('blog/create', blog.views.blog_and_photo_upload, name='blog_create'),
]
```

**Étape 5 : Ajoutez « Écrire un billet » à la barre latérale**

```html
# templates/base.html
...
<p><a href="{% url 'home' %}">Accueil</a></p>
<p><a href="{% url 'blog_create' %}">Écrire un billet</a></p>
<p><a href="{% url 'photo_upload' %}">Télécharger une photo</a></p>
...
```
**Ajoutez une page de visualisation d’un billet de blog**

Nous allons inclure des posts de blog sur la page d’accueil, mais nous ne voulons tout de même pas voir tout le texte de chaque billet du blog. Ajoutons donc une autre page, où l’utilisateur peut voir un billet complet.

**Étape 1 : Ajoutez la vue pour la page de visualisation d’un billet**

```python
# blog/views.py

from django.shortcuts import get_object_or_404
@login_required
def view_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    return render(request, 'blog/view_blog.html', {'blog': blog})
```

**Étape 2 : Ajoutez le gabarit pour la page de visualisation d’un billet**

```html
# blog/templates/blog/view_blog.html
{% extends 'base.html' %}
{% block content %}
    <h2>{{ blog.title }}</h2>
    <img src="{{ blog.photo.image.url }}">
    <p>{{ blog.photo.caption }}</p>
    <p>{{ blog.content }}</p>
{% endblock content %}
```

**Étape 3 : Ajoutez le modèle d’URL pour la page de visualisation d’un billet**

```python
# fotoblog/urls.py
urlpatterns = [
    …
    path('blog/<int:blog_id>', blog.views.view_blog, name='view_blog'),
]
```

**Étape 4 : Récupérez les instances de Blogdans la vue home**

Maintenant que la page de visualisation d’un billet est construite, récupérons les instances de  Blog  pour la page d’accueil.

```python
# blog/views.py
@login_required
def home(request):
    photos = models.Photo.objects.all()
    blogs = models.Blog.objects.all()
    return render(request, 'blog/home.html', context={'photos': photos, 'blogs': blogs})
```

**Étape 5 : Mettez à jour le gabarit home.html**

```html
# blog/templates/blog/home.html
{% extends 'base.html' %}
{% block content %}
    ...
    <h2>Blog</h2>
    <div class="grid-container">
        {% for blog in blogs %}
            <div class="post">
                <a href="{% url 'view_blog' blog.id %}">
                    <h4>Billet : {{ blog.title }}</h4>
                    <img src="{{ blog.photo.image.url }}">
                </a>
            </div>
        {% endfor %}
    </div>
{% endblock content %}
```

**Étape 6 : Testez le service vous-même**

Bravo ! Vous avez ajouté beaucoup de fonctionnalités ! Prenez le temps de créer quelques billets sur le blog, visualisez-les depuis la page d’accueil, puis cliquez dedans pour voir leur contenu.
Une fois que vos changements vous conviendront, vous serez prêt à passer à l'étape suivante.

**Résumé**

Vous pouvez inclure plusieurs formulaires dans une vue, pour instancier plusieurs modèles simultanément.
Si vous faites le rendu de ces formulaires au sein des mêmes balises   <form>  dans le gabarit, ils seront soumis dans la même requête  POST  .
Vous pouvez remplir ces deux formulaires avec l’objet   request.POST  dans la vue, et instancier plusieurs modèles depuis la même requête.
Maintenant que vous pouvez instancier plusieurs modèles en envoyant un seul formulaire, vous pouvez vous plonger dans le prochain chapitre. Vous allez y apprendre à gérer plusieurs formulaires sur une seule page.

**Incluez plusieurs formulaires sur une page**

Maintenant que nous avons vu comment créer plusieurs instances de modèles en envoyant un seul formulaire, voyons comment inclure différents formulaires, par le biais d’envois séparés, sur la même page.
Pour démontrer ceci, nous allons construire une page depuis laquelle nous modifierons et supprimerons un billet de blog.

**Étape 1 : Créez les formulaires**

Pour supprimer l’instance de `Blog`, créez un nouveau formulaire,  `DeleteBlogForm`. Pour modifier l’instance de `Blog`, utilisez le `BlogForm` déjà créé.
Néanmoins, il nous faut un moyen de distinguer ces deux formulaires lorsque nous récupérons les données de la requête  POST  dans la vue.
Pour atteindre ce but, attachez un champ caché à chaque formulaire.

```python
# blog/forms.py
class BlogForm(forms.ModelForm):
    edit_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    
    class Meta:
        model = models.Blog
        fields = ['title', 'content']
        
class DeleteBlogForm(forms.Form):
    delete_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)
```

Vous avez attaché un champ `edit_blog` et un champ `delete_blog` aux formulaires  `BlogForm` et `DeleteBlogForm`, respectivement. Ces champs utilisent le widget `HiddenInput`, et ne seront pas vus par l’utilisateur sur le front-end. Le choix du type de champ et de la valeur initiale est quelque peu arbitraire, vu que nous allons simplement vérifier la présence du champ dans la vue.

**Étape 2 : Incluez les formulaires dans une vue**

Maintenant que nous avons les formulaires, gérons-les dans une vue.
Premièrement, créez une vue edit_blog  sans gestion de requête `POST`

```python
# blog/views.py
@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    edit_form = forms.BlogForm(instance=blog)
    delete_form = forms.DeleteBlogForm()
    if request.method == 'POST':
        pass
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'blog/edit_blog.html', context=context)
```

Depuis que vous avez ajouté les champs cachés aux formulaires, vous pouvez vérifier quel formulaire est envoyé en vérifiant la présence de ce champ dans les données  POST  . Puis, vous pouvez simplement gérer le formulaire comme d’habitude.

```python
@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    edit_form = forms.BlogForm(instance=blog)
    delete_form = forms.DeleteBlogForm()
    if request.method == 'POST':
        if 'edit_blog' in request.POST:
            edit_form = forms.BlogForm(request.POST, instance=blog)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
            if 'delete_blog' in request.POST:
                delete_form = forms.DeleteBlogForm(request.POST)
                if delete_form.is_valid():
                    blog.delete()
                    return redirect('home')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
}
return render(request, 'blog/edit_blog.html', context=context)
```

**Étape 3 : Ajoutez le gabarit**

```html
# blog/templates/blog/edit_blog.html
{% extends 'base.html' %}
{% block content %}
    <h2>Modifier le billet</h2>
    <form method="post">
        {{ edit_form.as_p }}
        {% csrf_token %}
        <button type="submit" >Sauvegarder</button>
    </form>
    <hr>
    <h3>Supprimer le billet ?</h3>
    <form method="post">
        {{ delete_form }}
        {% csrf_token %}
        <button type="submit" >Supprimer</button>
    </form>
{% endblock content %}
```

L’inclusion des champs cachés garantit que chaque formulaire n’est géré que lorsque vous avez l’intention de l’envoyer. Vous pouvez désormais inclure n’importe quelle quantité de formulaires sur la même page.

**Étape 4 : Ajoutez le modèle d’URL**

```python
# fotoblog/urls.py
urlpatterns = [
    …
    path('blog/<int:blog_id>/edit', blog.views.edit_blog, name='edit_blog'),
]
```

**Étape 5 : Ajoutez un lien vers la page de modification du billet**

Et pour finir, ajoutez un lien vers la page de modification du billet depuis la page de visualisation du billet.

```html
# blog/templates/blog/view_blog.html
{% extends 'authentication/base.html' %}
{% block content %}
    <h2>{{ blog.title }}</h2>
    <p><a href="{% url 'edit_blog' blog.id %}">Modifier le billet</a></p>
    <img src="{{ blog.photo.image.url }}">
    <p>{{ blog.photo.caption }}</p>
    <p>{{ blog.content }}</p>
{% endblock content %}
```

**Incluez plusieurs instances du même formulaire avec des ensembles de formulaires, ou formsets**

Vous possédez maintenant deux techniques pour inclure différents formulaires sur la même page. Vous pouvez les envoyer simultanément ou séparément. Mais que se passerait-il si vous vouliez inclure le même formulaire plusieurs fois sur une même page ?
Vous pouvez utiliser des ensembles de formulaires, ou formsets. Découvrez dans la vidéo ci-dessous comment créer une page qui permettra à un utilisateur de charger plusieurs photos en même temps.

**Étape 1 : Créez un formset dans une vue avec  formset_factory**

Vous avez déjà  PhotoForm  qui peut instancier le modèle  Photo. Vous pouvez réutiliser ce formulaire plutôt que d’en créer un nouveau.
Pour générer un formset avec ce formulaire, utilisez la méthodeformset_factoryque vous trouverez dans   django.forms. Cette méthode prend la classe formulaire (« form ») comme premier argument, puis un autre argument,extra, qui définit combien d’instances du formulaire vous voulez faire générer. Cette fonction « factory » (usine) renvoie une  classe, que vous devrez ensuite instancier dans la vue.

```python
# blog/views.py
from django.forms import formset_factory

@login_required
def create_multiple_photos(request):
    PhotoFormSet = formset_factory(forms.PhotoForm, extra=5)
    formset = PhotoFormSet()
    if request.method == 'POST':
        pass
    return render(request, 'blog/create_multiple_photos.html', {'formset': formset})
```

Pour traiter les données  POST , vous pouvez exécuter la méthode  is_valid()   sur le  formset  , exactement comme vous pouvez le faire sur un formulaire. Puis, vous pouvez itérer à travers les formulaires dans le  formset  en utilisant une boucle. Vous pouvez les gérer comme vous le feriez habituellement. Leformset  ne sera pas invalidé si des formulaires individuels sont vides, alors vérifions si un formulaire contient des données avant de le sauvegarder, comme ceci :

```python
# blog/views.py
@login_required
def create_multiple_photos(request):
    PhotoFormSet = formset_factory(forms.PhotoForm, extra=5)
    formset = PhotoFormSet()
    if request.method == 'POST':
        formset = PhotoFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    photo = form.save(commit=False)
                    photo.uploader = request.user
                    photo.save()
            return redirect('home')
    return render(request, 'blog/create_multiple_photos.html', {'formset': formset})
```

Ceci sauvegardera tous les formulaires, avant de nous rediriger vers la page d’accueil. Et maintenant, ajoutons un gabarit.

**Étape 2 : Créez le gabarit**

```html
# blog/templates/blog/create_multiple_photos.html
{% extends 'base.html' %}
{% block content %}
    <h2>Télécharger plusieurs photos</h2>
    <form method="post" enctype="multipart/form-data">
        {{ formset.as_p }}
        {% csrf_token %}
        <button type="submit" >Publier</button>
    </form>
{% endblock content %}
```

Vous voudrez peut-être présenter chaque formulaire du formset individuellement. Pour ce faire, n’oubliez pas d’inclure  {{ formset.management_form }}  dans les balises  <form>. Le  management_form   n’inclut rien qui sera vu par l’utilisateur sur le front-end, mais il comprend certaines métadonnées dont Django a besoin pour traiter le formset, par exemple le nombre de formulaires dans le formset. Pour inclure un formset dans une page tout en gérant l’affichage de chaque formulaire.

```html
# blog/templates/blog/create_multiple_photos.html
{% extends 'base.html' %}
{% block content %}
    <h2>Télécharger des photos</h2>
    <form method="post" enctype="multipart/form-data">
        {{ formset.managment_form }}
        {% csrf_token %}
        {% for form in formset %}
            {{ form.as_p }}
        {% endfor %}
        <button type="submit" >Publier</button>
    </form>
{% endblock content %}
```

**Étape 3 : Ajoutez le modèle d’URL**

```python
# fotoblog/urls.py
urlpatterns = [
    …
    path('photo/upload-multiple/', blog.views.create_multiple_photos,
    name='create_multiple_photos'),
]
```

**Étape 4 : Ajoutez un lien dans la barre latérale**

```html
# templates/base.html
...
<p><a href="{% url 'photo_upload' %}">Télécharger une photo</a></p>
<p><a href="{% url 'create_multiple_photos' %}">Télécharger plusieurs photos</a></p>
<p><a href="{% url 'upload_profile_photo' %}">Changer la photo de profil</a></p>
...
```

**Résumé**

Vous pouvez gérer plusieurs formulaires séparés sur une seule page, en incluant un champ caché qui identifie le formulaire envoyé.
Vous pouvez utiliser des ensembles de formulaires, dits formsets, pour créer plusieurs instances différentes du même formulaire sur une seule page.
Maintenant que vous savez gérer plusieurs formulaires dans une seule vue, vous pouvez apprendre à étendre des modèles avec des méthodes personnalisées !

---

**Écrivez vos propres méthodes de modèle pour redimensionner des photos**

L’un des patrons de conception, ou design patterns, couramment utilisé dans les applications Django s’appelle « fat models — skinny views » (littéralement : gros modèles — vues maigres). Sa philosophie : la logique de vos vues doit être aussi simple que possible, et le gros du travail doit être effectué par les modèles.
Vous pouvez y parvenir en écrivant des méthodes personnalisées pour vos modèles. Elles rendent vos vues plus simples et plus lisibles. Vous pouvez donc facilement réutiliser la logique de votre méthode pour différentes vues ou tâches.
Si le code que vous écrivez implique de manipuler un modèle ou de récupérer des informations depuis un modèle, il constitue probablement une méthode de modèle.
Pour notre projet, nous voulons redimensionner les photos avant de les sauvegarder. Cela nous aidera à éviter des coûts de stockage élevés lorsque nous aurons davantage de photos.
Comme cette méthode manipule le modèle  Photo  , c’est une candidate parfaite pour être une méthode de modèle. Si nous mettions cette logique uniquement dans une vue, nous ne pourrions la réutiliser nulle part ailleurs, et cela compliquerait également la logique de la vue. On utilise pillow (PIL) pour manipuler des images.
Utilisons la bibliothèque  Pillow  pour redimensionner les photos. Vous avez installé cette librairie tout à l’heure, car elle est nécessaire lorsqu’on utilise  ImageField  . Vous pouvez aussi l’utiliser pour manipuler des images.
Pour redimensionner l’image tout en conservant ses proportions d’origine, utilisez la fonction  thumbnail  . Elle ne redimensionnera l’image que si celle-ci est supérieure à la taille maximale.
Nous allons créer une nouvelle méthode dans notre modèle   Photo  ,   resize_image

```python
# blog/models.py
from PIL import Image


class Photo(models.Model):
    ...
    IMAGE_MAX_SIZE = (800, 800)
    
    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        # sauvegarde de l’image redimensionnée dans le système de fichiers
        # ce n’est pas la méthode save() du modèle !
        image.save(self.image.path)
```
Testons-la maintenant dans le shell Python. Nous prenons une image que nous avons déjà mise en ligne, donc pour votre test, vous devrez tout d’abord charger une image via le site.

```shell
>>> from blog.models import Photo
>>> photo = Photo.objects.first()
>>> print(f'taille : {photo.image.size // 1000} ko')
taille : 683 ko
>>> photo.resize_image()
>>> print(f'taille : {photo.image.size // 1000} ko')
taille : 44 ko
```
On dirait que nous avons réduit la taille de la photo plus de 15 fois ! Maintenant que vous avez la capacité de redimensionner les photos, voyons comment faire en sorte que ce soit fait automatiquement, dès qu’une photo est enregistrée.

**Surchargez la méthode save()  sur un modèle**

Vous avez maintenant une méthode bien pratique,   resize_image  , sur le modèle   Photo  . Mais vous ne voulez pas avoir à appeler cette méthode manuellement à chaque fois qu’une nouvelle photo est mise en ligne !
Vous vous souvenez avoir utilisé la méthode  save()  pour enregistrer des instances de modèle dans la base de données ? Eh bien, vous pouvez surcharger cette méthode. En réalité, vous pouvez surcharger toutes les méthodes des modèles pour les personnaliser selon vos besoins.
Surchargeons la méthode  save()  de la classe  Photo  pour nous assurer que toutes les photos mises en ligne sur le site soient redimensionnées selon vos spécifications.

```python
"""
Voyons de quoi ça a l’air. Premièrement, utilisez la méthode  super()  pour vous assurer que la sauvegarde de l’objet en base de données fonctionne toujours.
"""

class Photo(models.Model):
    ...
    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
```
Lorsque vous surchargez les modèles intégrés de Django, c’est toujours une bonne idée de récupérer les arguments  *args    et   **kwargs    passés à votre méthode et de les fournir à la méthode  super(), même si les spécifications actuelles ne les exigent pas.
Car si les spécifications changent, et que la méthode de modèle commence à prendre des arguments nouveaux et différents, votre méthode personnalisée pourra les gérer, grâce aux *args et **kwargs  génériques.
Et maintenant, ajoutez simplement la méthode  resize_image()

```python
class Photo(models.Model):
    ...
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()
```
C’est aussi simple que ça ! Vos images seront désormais automatiquement redimensionnées dès que la méthode  Photo.save()  sera appelée.


Nous voulons maintenant afficher le nombre de mots du post de  Blog  sur le front-end. Pour ce faire, calculez-le à partir du champ  content  de  Blog.
Imaginons qu’un développeur senior ait décidé que le fait de calculer le nombre de mots pour chaque billet individuel au fil de l’eau était trop intensif d’un point de vue informatique. Il estime que ces informations devraient être stockées en tant que champ dans le modèle  Blog  . Ce champ devrait alors se mettre à jour automatiquement, dès que l’on apporte des changements à l’instance de  Blog.
Si vous mettez à jour plusieurs instances d’un modèle en même temps avec  QuerySet.update(  ), la méthode de modèle  save()ne sera pas appelée. C’est vrai aussi si vous appelez la méthode  update_fields  sur le modèle, car elles conduisent toutes deux leurs changements en SQL brut.


**Écrivez des méthodes personnalisées pour le modèle Blog**

Vous allez devoir:
> Créer un nouveau `champword_count`   sur le `modèleBlog`  . Vous pouvez paramétrer `null=True`   pour ne pas avoir à fournir une valeur par défaut.

> Générer et exécuter les migrations afin de mettre en œuvre ce changement.

> Ajouter une nouvelle méthode _get_word_count()au modèleBlog, qui calcule le nombre de mots du champcontent. Le tiret bas (ou underscore) du début indique qu’il s’agit d’une méthode interne, et que l’attributword_countconstitue la bonne façon d’accéder au nombre de mots.

> Créer une méthode `save(self, *args, **kwargs)` pour assigner à `word_count` le résultat de   _get_word_count(). 

```python
def _get_word_count(self):
        return len(self.content.split(" "))

    def save(self, *args, **kwargs):
        self.word_count = self._get_word_count()
        super().save(*args, **kwargs)
```

**Résumé**

Écrivez les blocs de code qui manipulent ou récupèrent des données depuis des modèles en tant que méthodes de modèle.
Lorsque c’est approprié, conservez la logique dans les modèles (fat models) et non dans les vues (skinny views).
Vous pouvez surcharger les méthodes de base d’un modèle, telles que les méthodes  save() etdelete().
Maintenant que vous savez manipuler des modèles grâce aux méthodes, assurons-nous qu’il n’y a pas de perte de données lors des migrations vers de nouveaux schémas de base de données.

**Restreignez des aspects de la fonctionnalité du site avec les permissions**

Lorsque vous développez un site, vous serez souvent dans le cas où différents utilisateurs ont besoin d’interagir de façon différente avec certaines parties du site. Vous devrez peut-être restreindre certaines fonctionnalités à des utilisateurs spécifiques. Pour cela, utilisez des permissions.
Pour notre site web, nous allons restreindre l’accès à la création, la modification, et la suppression des modèles  Photo  et   Blog  aux utilisateurs de type   CREATOR.
Chaque modèle créé en Django a quatre permissions qui sont générées en parallèle. Pour le modèle  Photo  , ce sont les suivantes :

> blog.add_photo  — ou, plus généralement   <app>.add_<model>

> blog.change_photo  — ou   <app>.change_<model>

> blog.delete_photo  — ou   <app>.delete_<model>

> blog.view_photo  — ou   <app>.view_<model>

Django utilise ces permissions en interne pour gérer l’accès au site administrateur, mais vous pouvez également les utiliser dans votre code. Découvrez en vidéo comment restreindre les fonctionnalités du site selon les permissions de l'utilisateur.

**Étape 1 : Restreignez l’accès dans la vue**

Tout d’abord, voyons comment restreindre l’accès à la vue en utilisant les permissions.
Tout comme vous utilisez le décorateur  @login_required  pour restreindre l’accès aux utilisateurs en fonction de s’ils sont ou non connectés, vous pouvez utiliser le décorateur  @permission_required  pour limiter l’accès en fonction de la permission. Dans ce cas, la seule différence est que vous spécifiez la permission requise comme argument au décorateur.
Restreignons l’accès à la vue  photo_upload  aux seuls utilisateurs qui ont la permission  blog.add_photo.

```python
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('blog.add_photo', raise_exception=True)
def photo_upload(request):
    ...
```
Maintenant, essayez d’accéder à http://localhost:8000/photo/upload en étant connecté. Vous verrez que vous allez recevoir une réponse 403 forbidden (interdit).

**Étape 2 : Restreignez l’accès dans le gabarit**

Vous pouvez aussi vérifier si un utilisateur a des permissions dans un gabarit. Cela peut vous servir pour montrer ou cacher du contenu en fonction de ses droits d’accès.
Ne montrons le lien   Télécharger une photo  que si l’utilisateur a la permission   blog.add_photo . Pour cela, utilisez l’attribut   perms  , qui est automatiquement chargé dans le contexte du gabarit.

```html
# blog/templates/blog/base.html
…
{% if perms.blog.add_photo %}
    <a href="{% url 'photo_upload' %}">Upload a Photo</a>
{% endif %}
```
Et maintenant, si vous naviguez jusqu’à la page d’accueil. L’accès à cette page est maintenant restreint en fonction des permissions.
Comment est-ce que je peux donner ces permissions aux utilisateurs ?
Avec du code, dans le shell Django.

**Étape 3 : Donnez des permissions à un utilisateur**

Vous pouvez utiliser la méthode  user_permissions.add()  pour ajouter des permissions.

```shell
>>> from authentication.models import User
>>> user = User.objects.get(username='toto')
>>> from django.contrib.auth.models import Permission
>>> permission = Permission.objects.get(codename='add_photo')
>>> user.user_permissions.add(permission)
```
 Si vous retournez au site, vous devriez voir réapparaître le lien  Télécharger une photo  , et pouvoir accéder à la page de mise en ligne de photos.
 Ça fonctionne ! Un utilisateur a maintenant l’autorisation. Néanmoins, cette approche ne peut pas être mise à l’échelle si vous voulez l’appliquer à de nombreux utilisateurs. L’utilisation des groupes permet de résoudre ce problème.

 **Attribuez des permissions à plusieurs utilisateurs grâce aux groupes**

À présent que le site a des parties restreintes en fonction des permissions, vous allez devoir en permettre l’accès à différents utilisateurs selon des spécifications.
Pour cela, répartissez les utilisateurs en groupes. Cela permet de regrouper un sous-ensemble d’utilisateurs. Ce groupement existe sous forme de tableau dans la base de données.
Pour notre site, nous aurons deux groupes :Creator (CréateuretSubscriber (Abonné). Nous voulons que ces groupes soient créés automatiquement. Ainsi, si quelqu’un récupérait une copie du projet et le paramétrait sur son ordinateur, il n’aurait pas besoin de créer ces groupes et de leur attribuer les permissions appropriées manuellement.
Pour ce faire, nous devons écrire une migration personnalisée.

> migrations personnalisées (def)
> Les migrations que vous avez rencontrées jusqu’à présent étaient liées à des changements du schéma dans la base de données, et étaient automatiquement générées par Django.
Les migrations personnalisées vous permettent de manipuler des données déjà contenues dans la base de données, ou même de créer de nouvelles instances de modèle fondées sur des critères spécifiques. Elles sont utiles si vous devez migrer des données vers un nouveau type de données, sans perdre aucune information.
Comme ce sont des migrations, elles peuvent être stockées dans votre historique de contrôle de version. Elles peuvent être récupérées et exécutées par toute personne ayant accès au projet. Cela permet à l’application d’être reproductible dans différents environnements. Elles seront également exécutées dès que quelqu’un configure le projet initialement.

Tout d’abord, nous allons écrire une migration personnalisée pour créer les groupes  creators  et   subscribers. Nous ajouterons ensuite les utilisateurs dans leur groupe approprié, en fonction de leur attribut  role
Pour créer une migration personnalisée, vous devez générer une migration vide grâce au drapeau  --empty   . Ensuite, spécifiez l’application où la migration sera générée. Dans notre cas, c’est  authentication.

`python manage.py makemigrations --empty authentication`

Et maintenant, si vous regardez le répertoiremigrationsde l’application  authentication, vous verrez qu’une nouvelle migration a été générée. Voyons ce qu’elle contient :

```python
# Generated by Django 3.2.1 on 2021-04-06 01:35

from django.db import migrations


class Migration(migrations.Migration):
    
    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
    ]
```
La propriété  dependencies   liste les migrations qui doivent être exécutées avant celle-ci, tandis qu’  operations  constitue une liste des opérations que la migration va effectuer.

Pour écrire le code sur mesure à exécuter dans la migration, vous devez l’écrire en tant que fonction prenant deux arguments,  apps  et   schema_editor  . Vous ne pouvez pas accéder aux modèles directement depuis les imports, vous devez donc utiliser la fonction  apps.get_model()  pour les récupérer.

Écrivons une fonction  create_groups  , qui va créer les groupes  creators  et   subscribers  , puis leur attribuer correctement les utilisateurs existants dans la base de données avec la fonction  Group.user_set.add()

```python
def create_groups(apps, schema_migration):
    User = apps.get_model('authentication', 'User')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    add_photo = Permission.objects.get(codename='add_photo')
    change_photo = Permission.objects.get(codename='change_photo')
    delete_photo = Permission.objects.get(codename='delete_photo')
    view_photo = Permission.objects.get(codename='view_photo')
    
    creator_permissions = [
        add_photo,
        change_photo,
        delete_photo,
        view_photo,
    ]
    
    # 1. la fonction crée 2 groupes creators et subscribers
    creators = Group(name='creators')
    creators.save()
    # 2. Elle associe un certain nombre de permissions
    # qui permettront aux utilisateurs (ajouter, modifier ...)
    # ces commandes native des migrations Django sont stockées
    # dans la liste creator_permissions et appelées afin de
    # toutes les assigner à creators.
    creators.permissions.set(creator_permissions)

    subscribers = Group(name='subscribers')
    subscribers.save()
    # 2. Elle permet uniquement aux subscribers de 
    # voir leurs photos (view_photo)
    # la commande view_photos est native pour les migrations
    subscribers.permissions.add(view_photo)
    
    # 3. Elle parcourt l'ensemble des utilisateurs et en fonction
    # de leur rôle, les assigne au groupe adéquat.
    for user in User.objects.all():
        if user.role == 'CREATOR':
            creators.user_set.add(user)
        if user.role == 'SUBSCRIBER':
            subscribers.user_set.add(user)

"""
Ensuite, ajoutez la migration aux  operations  en spécifiant la fonction  create_groups   comme argument de la classe  migrations.RunPython
"""

class Migration(migrations.Migration):
    
        dependencies = [
    ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups)
    ]
```
Et maintenant, exécutez la migration :

Maintenant que vous savez comment configurer les permissions pour la fonctionnalité  Photo Upload  , il est temps de construire les permissions restantes.

Quatre tâches vous attendent :

> Utilisez le décorateur   permission_required  pour restreindre l’accès aux vues    create_multiple_photos   ,   edit_blog  et   blog_and_photo_upload  .

> Utilisez l’attribut   perms  dans un gabarit pour afficher de façon optionnelle les liens   Télécharger plusieurs photos  ,  Écrire un billet  , et  Modifier un billet  .

> Mettez à jour la méthode   save()  de   User  pour ajouter l’utilisateur au bon groupe.

> Créez une migration personnalisée pour attribuer les bonnes permissions aux groupes pour le modèle  Blog  . Ce seront les mêmes permissions que pour   Photo  . 

**Configurez des accès à granularité fine avec les permissions personnalisées**

Les quatre autorisations par défaut créées par Django sont utiles, mais que faire si vous avez besoin de permissions à granularité plus fine ? Vous pourriez vouloir, par exemple, qu’un type d’utilisateur soit uniquement capable de modifier un champ particulier dans un modèle, comme le champ  title  de  Blog  .
Comment faire ? En créant des permissions personnalisées ! La façon la plus simple de les créer est de les définir comme faisant partie du modèle.
Spécifiez des permissions personnalisées en configurant l’attribut  permissions  dans une classe  Meta  d’un modèle, comme ceci:

```python
class Blog(models.Model):
    ...
    
    class Meta:
        permissions = [
            ('change_blog_title', 'Peut changer le titre d’un billet de blog')
        ]
```
Vous pouvez ensuite attribuer cette permission à des groupes ou des utilisateurs, exactement comme pour les permissions de base.
Vous ne pouvez appliquer ces permissions qu’à l’échelle du modèle. Cela signifie que vous ne pouvez pas utiliser ces permissions à une échelle spécifique à l’objet : par exemple, ne laisser un utilisateur modifier une publication que s’il en est l’auteur.

Les permissions par objet ne sont pas bien gérées par Django tel qu’il est conçu. Si vous avez besoin d’utiliser des permissions de cette façon, certaines bibliothèques tierces bien faites peuvent vous aider. Django Guardian et Rules sont deux solutions populaires à ce problème, et vous pouvez toujours aller voir la section sur les permissions de Django Packages pour d’autres propositions (les trois sont des ressources en anglais).

**Résumé**

Django fournit quatre permissions par défaut pour chaque modèle, qui correspondent aux quatre opérations CRUD.

> Vous pouvez utiliser le décorateur   permission_required  pour restreindre l’accès à une vue en fonction d’une permission.

> Vous pouvez attribuer des permissions à des utilisateurs individuels, ou à plusieurs utilisateurs en utilisant les groupes.

> Les migrations personnalisées vous permettent d’apporter des changements sur mesure à la base de données, qu’on peut répéter sur différents environnements..

> Les permissions personnalisées peuvent être spécifiées dans une classe de modèle   Meta  .

> Il vaut mieux utiliser un package tiers pour les permissions au niveau de l’objet.

Maintenant que vous savez restreindre l’accès en fonction des permissions et écrire des migrations personnalisées, vous pouvez aller découvrir les champs plusieurs-à-plusieurs (many-to-many en anglais).

---

**Liez des utilisateurs avec des champs plusieurs-à-plusieurs**

Jusqu’à présent, nous avons utilisé des relationsForeignKey  pour lier différents types de modèles les uns aux autres, ce qui crée des relations un-à-plusieurs (ou one-to-many). Par exemple, le modèlePhoto  a une relationForeignKey à User  par le champuploader. Vous ne pouvez lier chaque instance de Photo  qu’à une instance de User, mais vous pouvez lier une instance de User  à de nombreuses instances différentes de   Photo. 

<img src="https://user.oc-static.com/upload/2021/09/08/16311173779731_FR_7192426_P3C5-3_P3C5-3.png">

Vous pouvez également utiliser le  OneToOneField  pour créer des relations un-à-un (one-to-one). Dans ce cas, vous ne pouvez lier chaque instance du modèle A qu’à une instance du modèle B, et vice-versa.

Un cas d’usage courant pour les relations un-à-un : l’utilisation des modèles de profil pour étendre le modèle  User  . Dans notre cas, comme nous avons deux types d’utilisateurs — les créateurs et les abonnés — nous voudrions peut-être créer un modèle  Creator   et un modèle  Subscriber  , chacun ayant un  OneToOneField  relatif au  User  . Ceux-ci contiendront les informations nécessaires pour chaque utilisateur, mais qui ne sont significatives que pour les types créateur et abonné.

<img src="https://user.oc-static.com/upload/2021/09/08/16311174935211_FR_7192426_P3C5-2.png">

Enfin, vous avez également l’option du  ManyToManyField  , que vous pouvez utiliser pour créer des relations plusieurs-à-plusieurs. Imaginons que le modèle A a un  ManyToManyField  qui le lie au modèle B. Cela signifie qu’il peut être lié à plusieurs instances différentes du modèle B, et aussi qu’une instance du modèle B peut être liée à plusieurs instances différentes du modèle A.

Sur notre site, nous allons utiliser des relations plusieurs-à-plusieurs pour permettre aux utilisateurs de suivre d’autres utilisateurs. Nous voulons qu’un utilisateur puisse s’abonner à de nombreux créateurs différents, et que de nombreux autres utilisateurs puissent aussi s’abonner à lui. La relation plusieurs-à-plusieurs est donc parfaitement adaptée. Implémentons maintenant ce schéma dans nos modèles. 

<img src="https://user.oc-static.com/upload/2021/09/08/16311175260451_FR_7192426_P3C5-3.png">

**Étape 1 : Mettez à jour les modèles**

Pour établir une relation plusieurs-à-plusieurs entre les utilisateurs, vous devez spécifier un  ManyToManyField  sur le modèle  User, qui lie à un autre  User. Appelons le nôtre  follows (suit).

```python
# authentication/models.py
class User(AbstractUser):
...
follows = models.ManyToManyField(
    'self',
    limit_choices_to={'role': CREATOR},
    symmetrical=False,
    verbose_name='suit',
)
```

Le premier argument dans le  ManyToManyField  est le modèle avec lequel vous nouez une relation. Dans notre cas, il s’agit du même modèleUser, auquel nous référons avec'self'.

Vous pouvez limiter quels utilisateurs peuvent être suivis en utilisant le mot-clé optionnel limit_choices_to. Nous voulons que seuls les utilisateurs avec le rôle  CREATOR  puissent être suivis.

Dans ce cas particulier, où les deux modèles dans la relation plusieurs-à-plusieurs sont les mêmes, vous devez également préciser si la relation est symétrique. Les relations symétriques sont celles où il n’y a aucune différence entre les deux acteurs de la relation, comme quand on lie deux amis. Un utilisateur en suit un autre, donc vous précisez  symmetrical=False  . L’argument  symmetrical  n’est pas  requis si vous liez à un autre modèle que celui dans lequel le  ManyToManyField  est déclaré.

Maintenant, générez et exécutez les migrations :

Ensuite, voyons comment utiliser des formulaires pour créer des relations plusieurs-à-plusieurs au sein d’une vue.

**Étape 2 : Créez des relations plusieurs-à-plusieurs dans un formulaire**

Pour créer la relation plusieurs-à-plusieurs dans la vue, vous devez d’abord définir le formulaire approprié. Comme les champs sont dans le modèleUser, vous pouvez utiliser unmodelForm.
Créez un formulaire qui permette à l’utilisateur de choisir d’autres utilisateurs qu’il veut suivre.
```python
# blog/forms.py
from django.contrib.auth import get_user_model

User = get_user_model()


class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['follows']
```

**Étape 3 : Créez la vue**

```python
# blog/views.py

@login_required
def follow_users(request):
    form = forms.FollowUsersForm(instance=request.user)
    if request.method == 'POST':
        form = forms.FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'blog/follow_users_form.html', context={'form': form})
```
Avec le  ManyToManyField  , vous pouvez utiliser la fonction   ModelForm.save()  pour créer la relation plusieurs-à-plusieurs.

> Si vous utilisez la méthode   ModelForm.save()  avec l’argument   commit=False  , les relations plusieurs-à-plusieurs ne seront pas sauvegardées, car elles nécessitent d’abord la sauvegarde de l’instance initiale dans la base de données. Vous devrez appeler la méthode  ModelForm.save_m2m()  après avoir sauvegardé l’instance du modèle dans la base de données.

**Étape 4 : Créez le gabarit**

```html
# blog/templates/blog/follow_users_form.html
{% extends 'base.html' %}
{% block content %}
    <h2>Suivre des utilisateurs</h2>
    <form method="post">
        {{ form.as_p }}
        {% csrf_token %}
        <button type="submit" >Confirmer</button>
    </form>
{% endblock content %}
```

**Étape 5 : Ajoutez le modèle d’URL**

```python
# fotoblog/urls.py
urlpatterns = [
    …
    path('follow-users/', blog.views.follow_users, name='follow_users')
    
]
```

**Étape 6 : Ajoutez un lien vers la nouvelle page**

```html
# templates/base.html
…
{% if perms.blog.add_photo %}
    <p><a href="{% url 'photo_upload' %}">Télécharger une photo</a></p>
    <p><a href="{% url 'create_multiple_photos' %}">Télécharger plusieurs photos</a></p>
{% endif %}
<p><a href="{% url 'follow_users' %}">Suivre des utilisateurs</a></p>
<p><a href="{% url 'upload_profile_photo' %}">Changer la photo de profil</a></p>
...
```

Le formulaire contient tous les créateurs, et permet à l’utilisateur de les sélectionner et de les suivre. Il vous permet aussi de sélectionner plusieurs utilisateurs en maintenant le bouton CTRL/Commande appuyé. Le formulaire les stocke alors dans un champ plusieurs-à-plusieurs. Voyons ensuite comment stocker des informations sur les relations plusieurs-à-plusieurs.

**Stockez des données supplémentaires sur les relations plusieurs-à-plusieurs avec des tables intermédiaires**

Vous aurez parfois besoin de stocker des données supplémentaires sur la relation entre deux instances du modèle liées par une relation plusieurs-à-plusieurs.
Disons que vous voulez autoriser un modèle  Blog  à avoir plusieurs contributeurs, et stocker un log de ce que chaque auteur a ajouté.
Pour cela, créez une table intermédiaire afin de stocker des données sur la relation. Lorsque vous utilisez un  ManyToManyField, Django produit lui-même cette table. Ici, vous  la créez simplement manuellement à la place.

**Étape 1 : Créez la table intermédiaire**
