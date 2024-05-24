from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class UserDetails(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=100)
    Address = models.TextField()
    @property
    def email(self):
        return self.user.email
    
    @property
    def username(self):
        return self.user.username
    
class PartyModel(models.Model):
    user = models.CharField(max_length=100,null=True, blank=True)
    PartyName = models.CharField(max_length=100)
    Number = models.CharField(max_length=100, null=True, blank=True)
    Address = models.TextField() 
    GSTNo = models.CharField(max_length=100)
    Email = models.CharField(max_length=100, null=True, blank=True)
    City = models.CharField(max_length=100, null=True, blank=True)
    Type = models.CharField(max_length=100,null=True, blank=True)

class ProductModel(models.Model):
    user = models.CharField(max_length=100,null=True, blank=True)
    ProductName = models.CharField(max_length=100)
    Category = models.CharField(max_length=100,null=True, blank=True)
    Tax = models.CharField(max_length=100)
    Unit = models.CharField(max_length=100)
    MinQty = models.CharField(max_length=100,blank=True)
    MaxQty = models.CharField(max_length=100,blank=True)
    BarcodeNo = models.CharField(max_length=100,blank=True)
    HSNCode = models.CharField(max_length=100,blank=True)
    MRP = models.CharField(max_length=100,blank=True)
    MFGDate = models.DateField(null=True, blank=True)
    ExpiryDate = models.DateField(null=True, blank=True)


class DeliveryBoyModel(models.Model):
    user = models.CharField(max_length=100,null=True, blank=True)
    Name = models.CharField(max_length=100)
    Number = models.CharField(max_length=100, null=True, blank=True)
    Address = models.TextField()
    Licence = models.FileField(upload_to='DeliveryBoy',null=True, blank=True)
    AdharCard = models.FileField(upload_to='DeliveryBoy',null=True, blank=True)
    PanCard = models.FileField(upload_to='DeliveryBoy',null=True, blank=True)
    Email = models.CharField(max_length=100, null=True, blank=True)
    PassWord = models.CharField(max_length=100, null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.Licence.delete()
        self.AdharCard.delete()
        self.PanCard.delete()
        super().delete(*args, **kwargs)

class CategoryModel(models.Model):
    user = models.CharField(max_length=100,null=True, blank=True)
    Category = models.CharField(max_length=100)

class ExpanseModel(models.Model):
    user = models.CharField(max_length=100,null=True, blank=True)
    Expanse = models.CharField(max_length=100,null=True,blank=True)
    Type = models.CharField(max_length=100,null=True, blank=True)

class NMModel(models.Model):
    ProductId = models.CharField(max_length=100,null=True,blank=True)
    user = models.CharField(max_length=100,null=True, blank=True)
    type = models.CharField(max_length=100,null=True, blank=True)

class BiilNoModel(models.Model):
    BillNo = models.CharField(max_length=100,null=True,blank=True)
    user = models.CharField(max_length=100,null=True, blank=True)
    type = models.CharField(max_length=100,null=True, blank=True)

class StockModel(models.Model):
    ProductId = models.CharField(max_length=100,null=True,blank=True)
    user = models.CharField(max_length=100,null=True, blank=True)
    type = models.CharField(max_length=100,null=True, blank=True)
    ProductName = models.CharField(max_length=100,null=True, blank=True)
    Category = models.CharField(max_length=100,null=True, blank=True)
    Tax = models.CharField(max_length=100,null=True, blank=True)
    Unit = models.CharField(max_length=100,null=True, blank=True)
    PurchasePrice = models.CharField(max_length=100,null=True, blank=True)
    PurchaseIncTax = models.CharField(max_length=100,null=True, blank=True)
    MinQty = models.CharField(max_length=100,blank=True)
    MaxQty = models.CharField(max_length=100,blank=True)
    BarcodeNo = models.CharField(max_length=100,blank=True)
    Quantity = models.CharField(max_length=100,blank=True)
    Amount = models.CharField(max_length=100,null=True, blank=True)
    sid = models.CharField(max_length=100,null=True, blank=True)

class PurchaseEntryModel(models.Model):
    user = models.CharField(max_length=100,null=True, blank=True)
    TypeofPurchase = models.CharField(max_length=100)
    BillNo = models.CharField(max_length=100)
    InvoiceNo = models.CharField(max_length=100)
    DateTime = models.DateTimeField(default=datetime.now())
    TypeofPayment = models.CharField(max_length=100)
    PartyName = models.CharField(max_length=100)
    ProductId = models.CharField(max_length=100)
    Type = models.CharField(max_length=100)
    Amount = models.CharField(max_length=100)
    DueDate = models.DateField(null=True, blank=True)
    Date = models.DateField(null=True, blank=True)
    TQuantity = models.CharField(max_length=100,null=True, blank=True)
    TPurchasePrice = models.CharField(max_length=100,null=True, blank=True)
    TPurchaseIncTax = models.CharField(max_length=100,null=True, blank=True)
    TChargesAmount = models.CharField(max_length=100,null=True, blank=True)
    Terms = models.CharField(max_length=100,null=True, blank=True)

    def DDate(self):
        return self.Date.strftime('%Y-%m-%d')

    def DueDate2(self):
        return self.DueDate.strftime('%Y-%m-%d')
    
    def date(self):
        return self.DateTime.strftime('%B %d %Y')
    
class MainStockModel(models.Model):
    OldProductId = models.CharField(max_length=100,null=True,blank=True)
    ProductId = models.CharField(max_length=100,null=True,blank=True)
    user = models.CharField(max_length=100,null=True, blank=True)
    type = models.CharField(max_length=100,null=True, blank=True)
    ProductName = models.CharField(max_length=100,null=True, blank=True)
    Category = models.CharField(max_length=100,null=True, blank=True)
    Tax = models.CharField(max_length=100,null=True, blank=True)
    Unit = models.CharField(max_length=100,null=True, blank=True)
    PurchasePrice = models.CharField(max_length=100,null=True, blank=True)
    PurchaseIncTax = models.CharField(max_length=100,null=True, blank=True)
    MinQty = models.CharField(max_length=100,blank=True)
    MaxQty = models.CharField(max_length=100,blank=True)
    BarcodeNo = models.CharField(max_length=100,blank=True)
    Quantity = models.CharField(max_length=100,blank=True)
    Amount = models.CharField(max_length=100,null=True, blank=True)
    out = models.IntegerField(default=0)

class SalesStockModel(models.Model):
    ProductId = models.CharField(max_length=100,null=True,blank=True)
    user = models.CharField(max_length=100,null=True, blank=True)
    type = models.CharField(max_length=100,null=True, blank=True)
    ProductName = models.CharField(max_length=100,null=True, blank=True)
    Category = models.CharField(max_length=100,null=True, blank=True)
    Tax = models.CharField(max_length=100,null=True, blank=True)
    Unit = models.CharField(max_length=100,null=True, blank=True)
    PurchaseIncTax = models.CharField(max_length=100,null=True, blank=True)
    BarcodeNo = models.CharField(max_length=100,blank=True)
    Quantity = models.CharField(max_length=100,blank=True)
    Amount = models.CharField(max_length=100,null=True, blank=True)
    sid = models.CharField(max_length=100,null=True, blank=True)
    ProfitMargin = models.CharField(max_length=100,null=True, blank=True)
    BasicSalesPrice = models.CharField(max_length=100,null=True, blank=True)
    Discount = models.CharField(max_length=100,null=True, blank=True)
    SalesPriceAfterDiscount = models.CharField(max_length=100,null=True, blank=True)
    IncSalesPrice = models.CharField(max_length=100,null=True, blank=True)
    TotalSales = models.CharField(max_length=100,null=True, blank=True)

class EditSalesStockModel(models.Model):
    ProductId = models.CharField(max_length=100,null=True,blank=True)
    user = models.CharField(max_length=100,null=True, blank=True)
    type = models.CharField(max_length=100,null=True, blank=True)
    ProductName = models.CharField(max_length=100,null=True, blank=True)
    Category = models.CharField(max_length=100,null=True, blank=True)
    Tax = models.CharField(max_length=100,null=True, blank=True)
    Unit = models.CharField(max_length=100,null=True, blank=True)
    PurchaseIncTax = models.CharField(max_length=100,null=True, blank=True)
    BarcodeNo = models.CharField(max_length=100,blank=True)
    Quantity = models.CharField(max_length=100,blank=True)
    Amount = models.CharField(max_length=100,null=True, blank=True)
    sid = models.CharField(max_length=100,null=True, blank=True)
    ProfitMargin = models.CharField(max_length=100,null=True, blank=True)
    BasicSalesPrice = models.CharField(max_length=100,null=True, blank=True)
    Discount = models.CharField(max_length=100,null=True, blank=True)
    SalesPriceAfterDiscount = models.CharField(max_length=100,null=True, blank=True)
    IncSalesPrice = models.CharField(max_length=100,null=True, blank=True)
    TotalSales = models.CharField(max_length=100,null=True, blank=True)

class SalesEntryModel(models.Model):
    user = models.CharField(max_length=100,null=True, blank=True)
    DeliveryBoyName = models.CharField(max_length=100,null=True, blank=True)
    TypeOfBusiness = models.CharField(max_length=100,null=True, blank=True)
    DeliveryTime = models.TimeField()
    InvoiceNo = models.CharField(max_length=100,null=True, blank=True)
    DateTime = models.DateTimeField(default=datetime.now())
    PartyName = models.CharField(max_length=100,null=True, blank=True)
    ProductId = models.CharField(max_length=100,null=True, blank=True)
    Type = models.CharField(max_length=100,null=True, blank=True)
    Amount = models.CharField(max_length=100,null=True, blank=True)
    Date = models.DateField(null=True, blank=True)
    Terms = models.CharField(max_length=100,null=True, blank=True)
    TypeofPayment = models.CharField(max_length=100,null=True, blank=True)
    TChargesAmount = models.CharField(max_length=100,null=True, blank=True)
    def DDate(self):
        return self.Date.strftime('%Y-%m-%d')

    def date(self):
        return self.DateTime.strftime('%B %d %Y')
    
    def time(self):
        return self.DeliveryTime.strftime("%H:%M")
        
    
class ExpanseListModel(models.Model):
    ProductId = models.CharField(max_length=100,null=True, blank=True)
    user = models.CharField(max_length=100,null=True, blank=True)
    Expanse = models.CharField(max_length=100,null=True,blank=True)
    Amount = models.CharField(max_length=100,null=True, blank=True)

class ExpanseEntryModel(models.Model):
    user = models.CharField(max_length=100,null=True, blank=True)
    Terms = models.CharField(max_length=100,null=True, blank=True)
    TypeofPayment = models.CharField(max_length=100,null=True, blank=True)
    DateTime = models.DateTimeField(default=datetime.now())
    PartyName = models.CharField(max_length=100,null=True, blank=True)
    ProductId = models.CharField(max_length=100,null=True, blank=True)
    Amount = models.CharField(max_length=100,null=True, blank=True)
    Date = models.DateField(null=True, blank=True)

    def date(self):
        return self.DateTime.strftime('%B %d %Y')
    
class ChargesModel(models.Model):
    user = models.CharField(max_length=100,null=True, blank=True)
    Charges = models.CharField(max_length=100,null=True,blank=True)

class ChargesListModel(models.Model):
    user = models.CharField(max_length=100,null=True, blank=True)
    Charges = models.CharField(max_length=100,null=True,blank=True)
    ProductId = models.CharField(max_length=100,null=True, blank=True)
    Amount = models.CharField(max_length=100,null=True, blank=True)
    Tax = models.CharField(max_length=100,null=True, blank=True)
    TotalAmount = models.CharField(max_length=100,null=True, blank=True)
    type = models.CharField(max_length=100,null=True, blank=True)

class InvoiceNoModel(models.Model):
    InvoiceNo = models.CharField(max_length=100,null=True,blank=True)
    user = models.CharField(max_length=100,null=True, blank=True)
    type = models.CharField(max_length=100,null=True, blank=True)