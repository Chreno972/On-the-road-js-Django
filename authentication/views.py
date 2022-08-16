from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, SignupForm, UploadProfilePhotoForm


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
        context={'form': form}
    )


def logout_user(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    logout(request)
    return redirect('login')


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

def upload_profile_photo(request):
    form = UploadProfilePhotoForm(instance=request.user)
    if request.method == 'POST':
        form = UploadProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'authentication/upload_profile_photo.html', context={'form': form})

