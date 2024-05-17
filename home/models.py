from typing import Any
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from colorfield.fields import ColorField
from django.urls import reverse
from django.conf import settings
from datetime import timedelta

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from datetime import datetime

SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = './calendario-centrodelserramento-09627e115b67.json'
credential = ServiceAccountCredentials.from_json_keyfile_name(
    SERVICE_ACCOUNT_FILE, SCOPES)
delegated_credentials = credential.create_delegated("andrea@andreazonca.com")
calendar_service = build("calendar", "v3", credentials=delegated_credentials)

class TrackModifyDate(models.Model):
    data_modificato = models.DateTimeField(auto_now=True)
    data_creato = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Order(TrackModifyDate):

    def __str__(self):
        return "Ordine " + str(self.InternalOrdNo) + " Linea " + str(self.RgLine)

    def pose(self):
        return Posa.objects.filter(ordine=self.InternalOrdNo, nel_cestino=False).order_by("data")
    def ordine_url(self):
        return self.InternalOrdNo.replace("/", "-")
    SaleOrdId = models.BigIntegerField(blank=True, null=True)
    InternalOrdNo = models.TextField(blank=True, null=True)
    ExternalOrdNo = models.TextField(blank=True, null=True)
    OrderDate = models.TextField(blank=True, null=True)
    ExpectedDeliveryDate = models.TextField(blank=True, null=True)
    ConfirmedDeliveryDate = models.TextField(blank=True, null=True)
    Customer = models.TextField(blank=True, null=True)
    CompanyName = models.TextField(blank=True, null=True)
    TaxIdNumber = models.TextField(blank=True, null=True)  # This field type is a guess.
    FiscalCode = models.TextField(blank=True, null=True)
    Address = models.TextField(blank=True, null=True)
    ZIPCode = models.TextField(blank=True, null=True)  # This field type is a guess.
    City = models.TextField(blank=True, null=True)
    County = models.TextField(blank=True, null=True)
    Country = models.TextField(blank=True, null=True)
    OurReference = models.TextField(blank=True, null=True)
    YourReference = models.TextField(blank=True, null=True)
    Payment = models.TextField(blank=True, null=True)
    PayDescription = models.TextField(blank=True, null=True)
    Notes = models.TextField(blank=True, null=True)
    Delivered = models.BigIntegerField(blank=True, null=True)
    Invoiced = models.TextField(blank=True, null=True)  # This field type is a guess.
    Cancelled = models.BigIntegerField(blank=True, null=True)
    Priority = models.BigIntegerField(blank=True, null=True)
    ShipToAddress = models.TextField(blank=True, null=True)
    ShaCompanyName = models.TextField(blank=True, null=True)
    ShaAddress = models.TextField(blank=True, null=True)
    ShaZIPCode = models.TextField(blank=True, null=True)  # This field type is a guess.
    ShaCity = models.TextField(blank=True, null=True)
    ShaCounty = models.TextField(blank=True, null=True)
    ShaCountry = models.TextField(blank=True, null=True)
    RgLine = models.TextField(blank=True, null=True)  # This field type is a guess.
    RgPosition = models.TextField(blank=True, null=True)  # This field type is a guess.
    RgLineType = models.TextField(blank=True, null=True)  # This field type is a guess.
    RgDescription = models.TextField(blank=True, null=True)
    RgItem = models.TextField(blank=True, null=True)
    RgUoM = models.TextField(blank=True, null=True)
    RgQty = models.TextField(blank=True, null=True)  # This field type is a guess.
    RgExpectedDeliveryDate = models.TextField(blank=True, null=True)
    RgConfirmedDeliveryDate = models.TextField(blank=True, null=True)
    RgDeliveredQty = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    RgInvoicedQty = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    RgDelivered = models.TextField(blank=True, null=True)  # This field type is a guess.
    RgInvoiced = models.TextField(blank=True, null=True)  # This field type is a guess.
    RgNotes = models.TextField(blank=True, null=True)  # This field type is a guess.
    RgCancelled = models.TextField(blank=True, null=True)  # This field type is a guess.

    def righe_ordine(self):
        return Order.objects.filter(InternalOrdNo=self.InternalOrdNo).order_by("RgLine")

    # Only in the planner
    tipo = models.ForeignKey("TipoPosa", null=True, blank=True, on_delete=models.PROTECT)

    def ha_servizi(self):
        return Order.objects.filter(SaleOrdId=self.SaleOrdId, RgLineType=3538946).exclude(RgItem__startswith="CDS").exists()

    def lista_servizi(self):
        linee_installazione = Order.objects.filter(SaleOrdId=self.SaleOrdId, RgLineType=3538946).exclude(RgItem__startswith="CDS")
        return linee_installazione.values_list("RgDescription", flat=True)

    def lista_materiali(self):
        linee_materiali = Order.objects.filter(SaleOrdId=self.SaleOrdId, RgLineType=3538947)
        return linee_materiali.values("RgDescription", "RgItem", "RgQty", "RgUoM")

class Posa(TrackModifyDate):
    def __str__(self) -> str:
        return "Posa " + self.id + " Ordine " + str(self.ordine) + " " + str(self.data)
    def ordini(self):
        return Order.objects.filter(InternalOrdNo=self.ordine)
    id = ShortUUIDField(
        length=8,
        alphabet="abcdefghijkmnpqrstuvwxyz23456789",
        primary_key=True,
    )
    ordine = models.CharField(max_length=20, blank=True)
    def ordine_url(self):
        return self.ordine.replace("/", "-")
    descrizione = models.TextField(max_length=500, null=True)
    data = models.DateField(null=True, blank=True)
    ora = models.TimeField(
        null=True, blank=True, help_text="Ora di inizio posa, esempio 14:30"
    )
    durata_ore = models.PositiveSmallIntegerField(null=True, blank=True)
    durata_minuti = models.PositiveSmallIntegerField(null=True, default=0)

    def calcola_ora_fine(self):
        data_ora = datetime.combine(self.data, self.ora)
        ora_fine = data_ora + timedelta(minutes=self.durata_minuti, hours=self.durata_ore)
        return ora_fine
    stato = models.ForeignKey("StatoPosa", null=True, on_delete=models.PROTECT)
    telefono1 = PhoneNumberField(null=False, blank=True, unique=False)
    telefono2 = PhoneNumberField(null=False, blank=True, unique=False)
    event_id = models.CharField(max_length=200, blank=True)
    calendar_id = models.CharField(max_length=200, blank=True)
    nota_posatore = models.TextField(max_length=500, blank=True)
    nota_cliente = models.TextField(max_length=500, blank=True)
    utente_modificato_per_ultimo = models.ForeignKey(
        "auth.User",
        null=True,
        on_delete=models.PROTECT,
    )
    posatori = models.ManyToManyField("auth.User", related_name="pose", blank=True)
    lista_materiali_visibile_posatori = models.BooleanField(default=True)
    nel_cestino = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("posa-update", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if self.nel_cestino:
            self.delete_calendar_event()
        elif self.posatori.count() > 0 and self.data is not None and self.ora is not None and self.durata_ore is not None and self.durata_minuti is not None:
            description = "<b><a href=\"" + self.get_absolute_url() + "\">Link al sistema di gestione pose</a></b><br><br>Ordine: " + \
                str(self.ordine) + "<br>Cliente: " + self.ordini()[0].CompanyName + \
                "<br>Posatori: " + ", ".join([posatore.username for posatore in self.posatori.all()]) + \
                "<br>Telefono1: " + str(self.telefono1)
            if self.telefono2:
                description += "<br>Telefono2: " + str(self.telefono2)
            description += "<br><br>" + self.descrizione 
            attendees = [{'email': 'clientxxxxxxx@gmail.com'},]
            event = {
                'summary': 'Appuntamento di posa - ' + self.ordini()[0].CompanyName,
                'location': self.ordini()[0].Address + ", " + self.ordini()[0].City + ", " + self.ordini()[0].Country,
                'description' : description,
                'start': {
                    'dateTime': str(self.data) + "T" + str(self.ora),
                    'timeZone': 'Europe/Rome',
                },
                'end': {
                    'dateTime': "T".join(str(self.calcola_ora_fine()).split()),
                    'timeZone': 'Europe/Rome',
                },
                'attendees': [
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                    ],
                },
                }
            if self.event_id == "":
                calendar_event = calendar_service.events().insert(calendarId=self.posatori.first().calendario.id, body=event).execute()
                self.event_id = calendar_event['id']
                self.calendar_id = self.posatori.first().calendario.id
            else:
                new_calendar_id = self.posatori.first().calendario.id
                if new_calendar_id == self.calendar_id:
                    calendar_event = calendar_service.events().update(calendarId=self.calendar_id, eventId=self.event_id, body=event).execute()
                else:
                    self.delete_calendar_event()
                    calendar_event = calendar_service.events().insert(calendarId=new_calendar_id, body=event).execute()
                    self.event_id = calendar_event['id']
                    self.calendar_id = new_calendar_id
        super().save(*args, **kwargs)

    def delete_calendar_event(self):
        if len(self.calendar_id) > 0 and len(self.event_id) > 0:
            calendar_service.events().delete(calendarId=self.calendar_id, eventId=self.event_id).execute()
    

class StatoPosa(models.Model):
    descrizione = models.CharField(max_length=20, null=False)
    colore = ColorField(default="#FF0000", null=False)

    def __str__(self) -> str:
        return self.descrizione


class TipoPosa(models.Model):
    descrizione = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.descrizione

class Calendario(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    utente = models.OneToOneField("auth.User", null=False, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return "Calendario of " + self.utente.username