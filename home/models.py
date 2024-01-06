from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from colorfield.fields import ColorField
from django.urls import reverse


class TrackModifyDate(models.Model):
    data_modificato = models.DateTimeField(auto_now=True)
    data_creato = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Order(TrackModifyDate):
    id = ShortUUIDField(
        length=8,
        alphabet="abcdefghijkmnpqrstuvwxyz23456789",
        primary_key=True,
    )
    index = models.BigIntegerField(blank=True, null=True)
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


class Posa(TrackModifyDate):
    order = models.OneToOneField(
        "Order", null=False, primary_key=True, on_delete=models.CASCADE
    )
    descrizione = models.TextField(max_length=500, null=True)
    data = models.DateField(null=True, blank=True)
    ora = models.TimeField(
        null=True, blank=True, help_text="Ora di inizio posa, esempio 14:30"
    )
    durata_ore = models.PositiveSmallIntegerField(null=True, blank=True)
    durata_minuti = models.PositiveSmallIntegerField(null=True, default=0)
    tipo = models.ForeignKey("TipoPosa", null=True, on_delete=models.PROTECT)
    stato = models.ForeignKey("StatoPosa", null=True, on_delete=models.PROTECT)
    telefono1 = PhoneNumberField(null=False, blank=True, unique=False)
    telefono2 = PhoneNumberField(null=False, blank=True, unique=False)
    utente_modificato_per_ultimo = models.ForeignKey(
        "auth.User",
        null=True,
        on_delete=models.PROTECT,
    )
    posatori = models.ManyToManyField("auth.User", related_name="pose")

    def get_absolute_url(self):
        return reverse("posa-update", kwargs={"pk": self.pk})


class StatoPosa(models.Model):
    descrizione = models.CharField(max_length=20, null=False)
    colore = ColorField(default="#FF0000", null=False)

    def __str__(self) -> str:
        return self.descrizione


class TipoPosa(models.Model):
    descrizione = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.descrizione


@receiver(post_save, sender=Order)
def create_posa(sender, instance, created, **kwargs):
    if created:
        Posa.objects.create(order=instance)


@receiver(post_save, sender=Order)
def save_posa(sender, instance, **kwargs):
    instance.posa.save()
