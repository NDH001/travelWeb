from typing import Any, Callable, Dict, Optional
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse

from .forms import UserLoginForm, UserRegForm, UserUpdateForm, ProfileUpdateForm
from .models import Connection

# Create your views here.


class UserLoginView(FormView):
    template_name = "userdata/login.html"
    form_class = UserLoginForm
    success_url = "/index"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form = self.form_class()
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return self.form_valid(form)

        messages.error(request, "Username and password does not match")

        return self.form_invalid(form)


class UserRegisterView(FormView):
    template_name = "userdata/register.html"
    form_class = UserRegForm
    success_url = "/index"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form = self.form_class(request.POST)

        if not form.is_valid():
            return self.form_invalid(form)

        return self.form_valid(form)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class ProfileView(UserPassesTestMixin, DetailView):
    template_name = "userdata/profile.html"
    context_object_name = "user"
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    def test_func(self):
        return self.request.user == get_object_or_404(
            self.model, username=self.kwargs.get("username")
        )


def user_logout(request):
    logout(request)
    return redirect("journing:index")


class EditProfileView(FormView):
    template_name = "userdata/edit_profile.html"
    user_form_class = UserUpdateForm
    profile_form_class = ProfileUpdateForm
    success_url = "/index"

    def get(self, request, *args, **kwargs):
        u_form = self.user_form_class(instance=request.user)
        p_form = self.profile_form_class(instance=request.user.profile)
        return render(
            request, self.template_name, context={"u_form": u_form, "p_form": p_form}
        )

    def post(self, request, *args, **kwargs):
        u_form = self.user_form_class(request.POST, instance=request.user)
        p_form = self.profile_form_class(
            request.POST, request.FILES, instance=request.user.profile
        )

        if not (u_form.is_valid() and p_form.is_valid()):
            return self.form_invalid(u_form, p_form)

        return self.form_valid(u_form, p_form)

    def form_valid(self, u_form, p_form):
        u_form.save()
        p_form.save()
        return super().form_valid(u_form)

    def form_invalid(self, u_form, p_form):
        return render(
            self.request,
            self.template_name,
            {
                "u_form": u_form,
                "p_form": p_form,
                "u_errors": u_form.errors.values(),
                "p_errors": p_form.errors.values(),
            },
        )


class PeekView(DetailView):
    template_name = "userdata/peek.html"
    context_object_name = "target_user"

    def get_object(self, queryset=None):
        self.target_user = User.objects.select_related("profile").get(
            pk=self.kwargs.get("pk")
        )
        return self.target_user

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        try:
            following = Connection.objects.get(
                user=self.target_user, follower=self.request.user
            )
        except:
            following = None

        context["following"] = following
        return context


class Connect(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return JsonResponse(
                {"message": "login", "redirect_url": "/accounts/login/"}
            )

        self.target_user = User.objects.get(username=request.POST.get("target_user"))
        try:
            self.connection = Connection.objects.get(
                user=self.target_user.pk, follower=request.user.pk
            )
        except:
            self.connection = None

    def count(self, request, follow=True):
        if follow:
            self.target_user.profile.followers += 1
            request.user.profile.following += 1
        else:
            self.target_user.profile.followers -= 1
            request.user.profile.following -= 1

        self.target_user.save()
        request.user.save()


class Follow(Connect):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response:
            return response

        if self.connection:
            return JsonResponse({"message": "Already Followed!"})

        connection = Connection.objects.create(
            user=self.target_user, follower=request.user
        )
        connection.save()
        self.count(request, follow=True)
        return JsonResponse({"message": "Followed!"})


class Unfollow(Connect):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response:
            return response

        if not self.connection:
            return JsonResponse({"message": "Already unfollowed"})

        self.connection.delete()

        self.count(request, follow=False)
        return JsonResponse({"message": "Unfollowed!"})
