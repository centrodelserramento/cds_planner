from django.shortcuts import render, redirect
from admin_datta.forms import (
    RegistrationForm,
    LoginForm,
    UserPasswordChangeForm,
    UserPasswordResetForm,
    UserSetPasswordForm,
)
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin

from .models import *


def index(request):
    context = {
        "segment": "index",
        #'products' : Product.objects.all()
    }
    return render(request, "pages/index.html", context)


def tables(request):
    context = {"segment": "tables"}
    return render(request, "pages/dynamic-tables.html", context)


class PosaUpdateView(SuccessMessageMixin, UpdateView):
    model = Posa
    template_name = "pages/posa-update.html"
    context_object_name = "posa"
    fields = ["data","ora","durata_ore","durata_minuti","tipo","telefono1","telefono2","descrizione"]
    success_message = "L'evento di posa e' stato aggiornato con successo"


