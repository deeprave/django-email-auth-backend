"""
Custom login/logout views
Unlike the standard Login/logout views these are suitable
to be called via ajax
"""
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, resolve_url
from django.utils.translation import gettext_lazy as _
from django.views import View


class CustomLoginView(View):
    http_method_names = ["post",]

    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request. This class only handles the POST request

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponseRedirect: Redirects to the specified URL.
        """
        redirect_to = "/"
        credentials = {}
        for name in ("username", "password", "topt", "next"):
            value = request.POST.get(name, None)
            if name == "next":
                redirect_to = value
                continue
            credentials[name] = value
        user = authenticate(request, **credentials)

        if user is not None:
            login(request, user)
            messages.success(request, _("You have been successfully logged in"))
        else:
            messages.error(request, _("Failed logging in"))
        return redirect(redirect_to)


class CustomLogoutView(LogoutView):
    http_method_names = ["post",]
    custom_redirect = resolve_url("home")

    def get_success_url(self):
        messages.success(self.request, _("You have been logged out"))
        return getattr(settings, "LOGOUT_REDIRECT_URL", self.custom_redirect)

    def post(self, request, *args, **kwargs):
        """Logout may be done via POST."""
        logout(request)
        return HttpResponseRedirect(self.get_success_url())


class CustomPasswordChangeView(PasswordChangeView):
    http_method_names = ["post",]
    form_class = PasswordChangeForm
    title = _("Password change")
    custom_redirect = resolve_url("home")

    def get_success_url(self):
        messages.success(self.request, _("Your password has been changed"))
        return self.custom_redirect

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)
