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


@login_required
def user_profile_edit(request):
    """user_profile_edit view
    validates form
    :decorator: - login_required
    :input: - request
    :return: - HttpResponseRedirect('/accounts/profile/view/')
             - render template accounts/user_profile_edit.html with form dict
    """
    try:
        profile = models.UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        profile = None
    form = forms.UserProfileForm(instance=profile)
    if request.method == 'POST':
        form = forms.UserProfileForm(
            request.POST,
            request.FILES,
            instance=profile)
        if not form:
            return HttpResponseRedirect('/accounts/profile/view/')
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return HttpResponseRedirect('/accounts/profile/view/')
        else:
            messages.error(request, form.non_field_errors()[0])
    return render(request, 'accounts/user_profile_edit.html', {'form': form})


@login_required
def user_profile_detail(request):
    """user_profile_detail view
    sets the user_profile
    :decorator: - login_required
    :input: - request
    :return: - render template accounts/user_profile_detail.html with user_profile dict
    """
    try:
        user_profile = models.UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        user_profile = None
    return render(request,
                  'accounts/user_profile_detail.html',
                  {'user_profile': user_profile})


@login_required
def change_password(request):
    """change_password view
    validates form
    :decorator: - login_required
    :input: - request
    :return: - HttpResponseRedirect('accounts/profile/view/')
             - render template accounts/change_password_form.html with form dict
    """

    if request.method == 'POST':
        form = forms.ChangePasswordForm(data=request.POST, request=request)
        if form.is_valid():
            user = request.user
            if user.check_password(form.cleaned_data['old_password']):
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password successfully updated.")
                return HttpResponseRedirect('accounts/profile/view/')
            else:
                messages.error(request, "Old password incorrect.")
        else:
            messages.error(request, form.non_field_errors()[0])
    form = forms.ChangePasswordForm(request=request)
    return render(
        request,
        'accounts/change_password_form.html',
        {'form': form})


@login_required
def user_avatar_edit(request):
    pass