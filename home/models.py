from django.db import models

# Create your models here.


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    info = models.CharField(max_length=100, default="")
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
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
