from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, Q

from post_order.models import PostOrder


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Пользовтеля не существует')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неверный пароль')

    context = {'page': page}
    return render(request, 'frontend/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            errors = form.errors.as_data()
            for error_list in errors.values():
                for error in error_list:
                    messages.error(request, error.message)
    
    return render(request, 'frontend/login_register.html', {'form': form})


@login_required(login_url='login')
def home(request):
    queryset = PostOrder.objects.annotate(
        messages_sent=Count(
            'MESSAGE_POSTORDER__id',
            filter=Q(MESSAGE_POSTORDER__status='sent')
        ),
        messages_error=Count(
            'MESSAGE_POSTORDER__id',
            filter=Q(MESSAGE_POSTORDER__status='error')
        ),
        messages_processing=Count(
            'MESSAGE_POSTORDER__id',
            filter=Q(MESSAGE_POSTORDER__status='processing')
        ),
        messages_expired=Count(
            'MESSAGE_POSTORDER__id',
            filter=Q(MESSAGE_POSTORDER__status='expired')
        ),
    ).all().order_by('id')
    return render(request, 'frontend/home.html', {'orders': queryset})
