from django.contrib import messages
from django.contrib.auth import (
    authenticate, login, logout, update_session_auth_hash
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm
)
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import forms
from . import models


def sign_in(request):
    """sign_in view
    validates form and login
    :input: - request
    :return: - HttpResponseRedirect(reverse('home'))
             - render template(accounts/sign_in.html) with form dict
    """
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    """sign_up view
    validates form and login
    :input: - request
    :return: - HttpResponseRedirect(reverse('home'))
             - render template(accounts/sign_up.html) with form dict
    """
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'accounts/sign_up.html', {'form': form})


@login_required
def sign_out(request):
    """sign_out view
    logout user
    :decorator: - login_required
    :input: - request
    :return: - HttpResponseRedirect(reverse('home'))
    """
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))
