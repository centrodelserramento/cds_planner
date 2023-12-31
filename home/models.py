from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.db.models.signals import post_save
from django.dispatch import receiver


class Order(models.Model):
    id = ShortUUIDField(
        length=8,
        prefix="id_",
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


class Posa(models.Model):
    order = models.OneToOneField(
        "Order", null=False, primary_key=True, on_delete=models.CASCADE
    )
    descrizione = models.CharField(max_length=100, null=True)
    tipo = models.ForeignKey("TipoPosa", null=True)


class TipoPosa(models.Model):
    descrizione = models.CharField(max_length=20)


@receiver(post_save, sender=Order)
def create_posa(sender, instance, created, **kwargs):
    if created:
        Posa.objects.create(order=instance)


@receiver(post_save, sender=Order)
def save_posa(sender, instance, **kwargs):
    instance.posa.save()
