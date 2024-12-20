from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic as views
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from asgiref.sync import async_to_sync
import asyncio

from electronics_shop.accounts.forms import RegisterForm, EditProfileForm, LoginForm
from electronics_shop.accounts.models import Profile
from electronics_shop.core.utils import get_account


async def send_registration_email(user_email):
    subject = "Welcome to our platform!"
    message = (
        "Thank you for registering on our platform. "
        "We are excited to have you on board!"
    )
    from_email = "no-reply@electronicsshop.com"
    recipient_list = [user_email]

    await asyncio.to_thread(
        send_mail, subject, message, from_email, recipient_list
    )


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            async_to_sync(send_registration_email)(user.email)
            messages.success(request, "Registration successful! Check your email.")
            return redirect('index')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Wrong username or password.")
        else:
            messages.error(request, "Fill all required fields.")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('index')


class DetailsProfileView(views.DetailView):
    queryset = Profile.objects.all()
    template_name = 'accounts/profile_details.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return get_account()


class EditProfileView(views.UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('details profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        return self.request.user.profile


@login_required
def delete_profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        user = profile.user
        profile.delete()
        user.delete()
        messages.success(request, "Your profile has been successfully deleted.")
        return redirect('index')

    return render(request, 'accounts/delete_profile.html', {'profile': profile})
