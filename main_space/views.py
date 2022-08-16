from django.shortcuts import render, redirect
from authentication.models import User
from main_space.forms import StatisticsForm


def see_user(request, user_id):
    """_summary_

    Args:
        request (_type_): _description_
        user_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    user = User.objects.get(id=user_id)
    return render(request, 'main_space/user_profile.html', {'user': user})


def home(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    return render(request, 'main_space/home.html')


def statistics_page(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    form = StatisticsForm()
    if request.method == 'POST':
        form = StatisticsForm(request.POST)
        if form.is_valid():
            form.save()
    return render(
        request,
        'main_space/statistics.html',
        context={'form': form}
    )
