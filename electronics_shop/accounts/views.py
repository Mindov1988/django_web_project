from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from electronics_shop.accounts.forms import RegisterForm, LoginForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': RegisterForm})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')

    return render(request, 'accounts/login.html', {'form': LoginForm})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('index')