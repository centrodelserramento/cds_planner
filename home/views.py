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


from django import forms
from django.contrib.auth.models import Group, User
from .models import Posa  # replace with your actual model name


class PosaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        posatori_group = Group.objects.get(name="Posatori")
        self.fields["posatori"].queryset = User.objects.filter(groups=posatori_group)

    class Meta:
        model = Posa
        fields = [
            "data",
            "ora",
            "durata_ore",
            "durata_minuti",
            "tipo",
            "telefono1",
            "telefono2",
            "descrizione",
            "posatori",
        ]


class PosaUpdateView(SuccessMessageMixin, UpdateView):
    model = Posa
    form_class = PosaForm
    template_name = "pages/posa-update.html"
    context_object_name = "posa"
    success_message = "L'evento di posa e' stato aggiornato con successo"

    def form_valid(self, form):
        form.instance.utente_modificato_per_ultimo = self.request.user
        return super().form_valid(form)
