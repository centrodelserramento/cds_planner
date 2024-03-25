from django.shortcuts import render, redirect
import datetime
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
    from django.contrib.auth.forms import AuthenticationForm
    form = AuthenticationForm()
    context = {
        "segment": "index",
        #'products' : Product.objects.all()
        'form': form
    }
    # if user is in group "Posatori"
    if request.user.groups.filter(name="Posatori").exists():
        context["pose_posatori"] = {
            "Pose future":Posa.objects.filter(posatori=request.user, data__gte=datetime.date.today()).order_by("data"),
         "Pose passate":Posa.objects.filter(posatori=request.user, data__lt=datetime.date.today()).order_by("-data")[:10]
        }
    return render(request, "pages/myindex.html", context)


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

def ordine(request, numero_ordine):
    # get orders which have saleordid = numero_ordine
    # sort by RgLine

    righe_ordine = Order.objects.filter(SaleOrdId=numero_ordine).order_by('RgLine')
    pose = Posa.objects.filter(ordine=numero_ordine)
    context = {
        "righe_ordine": righe_ordine,
        "pose": pose,
    }
    return render(request, "pages/ordine.html", context)

def crea_posa(request, numero_ordine):
    posa = Posa.objects.create(ordine=numero_ordine)
    return redirect("posa-update", pk=posa.pk)