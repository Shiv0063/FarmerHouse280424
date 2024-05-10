from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User,Group
from django.http import HttpResponse,JsonResponse
from .models import PartyModel,CategoryModel,DeliveryBoyModel,ProductModel,UserDetails,ExpanseModel,NMModel,BiilNoModel,StockModel,PurchaseEntryModel,MainStockModel,SalesStockModel,SalesEntryModel,ExpanseListModel,ExpanseEntryModel,ChargesModel,ChargesListModel,InvoiceNoModel
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import os

def Login(request):
    if request.method=="POST":
        username=request.POST.get('Username')
        password=request.POST.get('Password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
    return render(request,"login.html")

def Logout(request):
    logout(request)
    return redirect('/')

def is_user(user):
    return User.objects.filter(username=user).exists()

def useremail(email):
    return User.objects.filter(email=email).exists()

def is_admin(user):
    data=User.objects.filter(is_superuser=True)
    for i in data:
        if str(i.username) == str(user):
            return True

@login_required(login_url='Login')
def dashboard(request):
    if is_admin(request.user):
        return render(request,'admin/dashboard.html')
    if is_user(request.user):
        return render(request,'dashboard.html')

@login_required(login_url='Login')
def Party(request):
    if is_admin(request.user):
        data=PartyModel.objects.filter(user=request.user)
        return render(request,'admin/party.html',{'data':data})
    if is_user(request.user):
        data=PartyModel.objects.filter(user=request.user)
        return render(request,'party.html',{'data':data})

@login_required(login_url='Login')
def AddParty(request):
    if request.method=="POST":    
        user=str(request.user)
        Type=request.POST.get('Type')
        PartyName=request.POST.get('PartyName')
        Number=request.POST.get('Number')
        Address=request.POST.get('Address')
        GSTNo=request.POST.get('GSTNo')
        Email=request.POST.get('Email')
        City=request.POST.get('City')
        try:
            d=PartyModel.objects.filter(user=request.user.username)
            if d:
                for i in d:
                    if i.Number == Number:
                        messages.success(request,'This Number is Allready Available.')
                        return redirect('/AddParty')
                    elif i.Email == Email:
                        messages.success(request,'This Email is Allready Available.')
                        return redirect('/AddParty')
                    else:
                        dt=PartyModel.objects.create(user=user,Type=Type,PartyName=PartyName,Number=Number,Address=Address,GSTNo=GSTNo,Email=Email,City=City)
                        dt.save()
                        messages.success(request,'Add Party Successfully.')
                        return redirect('/AddParty')
            else:
                dt=PartyModel.objects.create(user=user,Type=Type,PartyName=PartyName,Number=Number,Address=Address,GSTNo=GSTNo,Email=Email,City=City)
                dt.save()
                messages.success(request,'Add Party Successfully.')
                return redirect('/AddParty')    
        except:
            dt=PartyModel.objects.create(user=user,Type=Type,PartyName=PartyName,Number=Number,Address=Address,GSTNo=GSTNo,Email=Email,City=City)
            dt.save()
            messages.success(request,'Add Party Successfully.')
            return redirect('/AddParty')
    if is_admin(request.user):
        return render(request,'admin/addparty.html')
    if is_user(request.user):
        return render(request,'addparty.html')
    

@login_required(login_url='Login')
def PartyDetails(request,id):
    data=PartyModel.objects.get(id=id)
    return render(request,'admin/partydetails.html',{'data':data})

@login_required(login_url='Login')
def EditParty(request,id):
    data=PartyModel.objects.get(id=id)
    if request.method=="POST":    
        data.user=str(request.user)
        data.Type=request.POST.get('Type')
        data.PartyName=request.POST.get('PartyName')
        data.Number=request.POST.get('Number')
        data.Address=request.POST.get('Address')
        data.GSTNo=request.POST.get('GSTNo')
        data.Email=request.POST.get('Email')
        data.City=request.POST.get('City')
        data.save()
        messages.success(request,'Party Edit Successfully.')
        return redirect('/Party')
    return render(request,'admin/editparty.html',{'data':data})

@login_required(login_url='Login')
def DeleteParty(request,id):
    data=PartyModel.objects.get(id=id)
    data.delete()
    messages.success(request,'Party Delete Successfully.')
    return redirect('/Party')

@login_required(login_url='Login')
def UserAccount(request):
    if is_admin(request.user):
        data=UserDetails.objects.all()
        return render(request,'admin/useraccount.html',{'data':data})
    return redirect('/')

@login_required(login_url='Login')
def AddUserAccount(request):
    if is_admin(request.user):
        if request.method=="POST":
            username=request.POST.get('Username')
            emailaddress=request.POST.get('emailaddress')
            password=request.POST.get('Password')
            phone=request.POST.get('Number')
            Address=request.POST.get('Address')
            if is_user(username):
                return redirect('/AddUserAccount')
            if useremail(emailaddress):
                return redirect('/AddUserAccount')
            new_user= User.objects.create_user(username,emailaddress,password)
            new_user.save()
            dg=User.objects.get(username=username)
            userd=UserDetails.objects.create(user_id=dg.id,phone=phone,Address=Address)
            userd.save()
            my_customer_group = Group.objects.get_or_create(name='USER')
            my_customer_group[0].user_set.add(new_user)
            messages.success(request,'New User Create Successfully.')
            return redirect('/AddUserAccount')
        return render(request,'admin/adduseraccount.html')
    return redirect('/')

@login_required(login_url='Login')
def EditUserAccount(request,id):
    if is_admin(request.user):
        data=UserDetails.objects.get(user_id=id)
        if request.method=="POST":
            username=request.POST.get('Username')
            emailaddress=request.POST.get('emailaddress')
            phone=request.POST.get('Number')
            Address=request.POST.get('Address')
            new_user= User.objects.get(username=data.username)
            new_user.username=username
            new_user.email=emailaddress
            dg=User.objects.get(username=data.username)
            userd=UserDetails.objects.get(user_id=dg.id)
            userd.phone=phone
            userd.Address=Address
            new_user.save()
            userd.save()
            messages.success(request,'User Details Edit Successfully.')
            return redirect('/UserAccount')
        return render(request,'admin/edituseraccount.html',{'data':data})
    return redirect('/')

@login_required(login_url='Login')
def DeleteUserAccount(request,id):
    if is_admin(request.user):
        data=User.objects.get(id=id)
        data.delete()
        messages.success(request,'Delete User Account Successfully.')
        return redirect('/UserAccount')
    return redirect('/')

@login_required(login_url='Login')
def Product(request):
    if is_admin(request.user):
        data=ProductModel.objects.filter(user=request.user)
        return render(request,'admin/product.html',{'data':data})
    if is_user(request.user):
        data=ProductModel.objects.filter(user=request.user)
        return render(request,'product.html',{'data':data})
    
@login_required(login_url='Login')
def AddProduct(request):
    Category = CategoryModel.objects.filter(user=request.user)
    data={"Category":Category}
    if request.method=="POST":    
        user=str(request.user)
        ProductName=request.POST.get('ProductName')
        Tax=request.POST.get('Tax')
        Category=request.POST.get('Category')
        Unit=request.POST.get('Unit')
        MinQty=request.POST.get('MinQty')
        MaxQty=request.POST.get('MaxQty')
        BarcodeNo=request.POST.get('Barcode')
        HSNCode=request.POST.get('HSNCode')
        MRP=request.POST.get('MRP')
        MFGDate=request.POST.get('MFGDate')
        ExpiryDate=request.POST.get('ExpiryDate')
        dt=ProductModel.objects.create(user=user,ProductName=ProductName,Tax=Tax,Category=Category,Unit=Unit,MinQty=MinQty,MaxQty=MaxQty,BarcodeNo=BarcodeNo,HSNCode=HSNCode,MRP=MRP,MFGDate=MFGDate,ExpiryDate=ExpiryDate)
        dt.save()
        messages.success(request,'Product Add Successfully.')
        return redirect('/AddProduct')
    if is_admin(request.user):
        return render(request,'admin/addproduct.html',data)
    if is_user(request.user):
        return render(request,'addproduct.html',data)

@login_required(login_url='Login')
def EditProduct(request,id):
    if is_admin(request.user):
        Category = CategoryModel.objects.filter(user=request.user)
        data=ProductModel.objects.get(id=id)
        if request.method=="POST":    
            data=ProductModel.objects.get(id=id)
            data.user=str(request.user)
            data.ProductName=request.POST.get('ProductName')
            data.Tax=request.POST.get('Tax')
            data.Category=request.POST.get('Category')
            data.Unit=request.POST.get('Unit')
            data.MinQty=request.POST.get('MinQty')
            data.MaxQty=request.POST.get('MaxQty')
            data.BarcodeNo=request.POST.get('Barcode')
            data.HSNCode=request.POST.get('HSNCode')
            data.MRP=request.POST.get('MRP')
            data.MFGDate=request.POST.get('MFGDate')
            data.ExpiryDate=request.POST.get('ExpiryDate')
            data.save()
            messages.success(request,'Product Edit Successfully.')
            return redirect('/Product')
        data={"Category":Category,'data':data}
        return render(request,'admin/editproduct.html',data)
    return redirect('/')

@login_required(login_url='Login')
def DeleteProduct(request,id):
    if is_admin(request.user):
        data=ProductModel.objects.get(id=id)
        data.delete()
        messages.success(request,'Delete Product Successfully.')
        return redirect('/Product')
    return redirect('/')

@login_required(login_url='Login')
def Category(request):
    if is_admin(request.user):
        data=CategoryModel.objects.filter(user=request.user)
        return render(request,'admin/category.html',{'data':data})
    if is_user(request.user):
        data=CategoryModel.objects.filter(user=request.user)
        return render(request,'category.html',{'data':data})

    
@login_required(login_url='Login')
def AddCategory(request):
    if request.method=="POST": 
        user=str(request.user)   
        Category=request.POST.get('Category')
        dt=CategoryModel.objects.create(user=user,Category=Category)
        dt.save()
        messages.success(request,'Add Category Successfully.')
        return redirect('/AddCategory')
    if is_admin(request.user):
        return render(request,'admin/addcategory.html')
    if is_user(request.user):
        return render(request,'addcategory.html')
    

@login_required(login_url='Login')
def EditCategory(request,id):
    if is_admin(request.user):
        data=CategoryModel.objects.get(id=id)
        if request.method=="POST":  
            data.Category=request.POST.get('Category')
            data.save()
            messages.success(request,'Category Edit Successfully.')
            return redirect('/Category')
        return render(request,'admin/editcategory.html',{'data':data})
    return redirect('/')

@login_required(login_url='Login')
def DeleteCategory(request,id):
    if is_admin(request.user):
        data=CategoryModel.objects.get(id=id)
        data.delete()
        messages.success(request,'Delete Category Successfully.')
        return redirect('/Category')
    return redirect('/')

@login_required(login_url='Login')
def DeliveryBoy(request):
    if is_admin(request.user):
        data=DeliveryBoyModel.objects.filter(user=request.user)
        return render(request,'admin/deliveryboy.html',{'data':data})
    if is_user(request.user):
        data=DeliveryBoyModel.objects.filter(user=request.user)
        return render(request,'deliveryboy.html',{'data':data})

@login_required(login_url='Login')
def AddDeliveryBoy(request):
    if request.method=="POST":  
        user=str(request.user)
        Name=request.POST.get('Name')
        Number=request.POST.get('Number')
        Address=request.POST.get('Address')
        Licence=request.FILES.get('Licence')
        AdharCard=request.FILES.get('AdharCard')
        PanCard=request.FILES.get('PanCard')
        Email=request.POST.get('Email')
        PassWord=request.POST.get('Password')
        dt=DeliveryBoyModel.objects.create(user=user,Name=Name,Number=Number,Address=Address,Licence=Licence,AdharCard=AdharCard,PanCard=PanCard,Email=Email,PassWord=PassWord)
        dt.save()
        messages.success(request,'DeliveryBoy Add Successfully.')
        return redirect('/AddDeliveryBoy')
    if is_admin(request.user):
        return render(request,'admin/adddeliveryboy.html')
    if is_user(request.user):
        return render(request,'adddeliveryboy.html')
    

@login_required(login_url='Login')
def DeliveryBoyDetails(request,pk):
    data=DeliveryBoyModel.objects.get(id=pk)
    return render(request,'admin/deliveryboydetails.html',{'data':data})

@login_required(login_url='Login')
def EditDeliveryBoy(request,pk):
    if is_admin(request.user):
        data=DeliveryBoyModel.objects.get(id=pk)
        if request.method=="POST":    
            data.Name=request.POST.get('Name')
            data.Number=request.POST.get('Number')
            data.Address=request.POST.get('Address')
            data.Email=request.POST.get('Email')
            data.PassWord=request.POST.get('Password')
            if request.FILES.get('Licence'):
                os.remove(data.Licence.path)
                data.Licence=request.FILES.get('Licence')
            if request.FILES.get('AdharCard'):
                os.remove(data.AdharCard.path)
                data.AdharCard=request.FILES.get('AdharCard')
            if request.FILES.get('PanCard'):
                os.remove(data.PanCard.path)
                data.PanCard=request.FILES.get('PanCard')
            data.save()
            messages.success(request,'Delivery Boy Edit Successfully.')
            return redirect('/DeliveryBoy')
        return render(request,'admin/editdeliveryboy.html',{'data':data})
    return redirect('/')

@login_required(login_url='Login')
def DeleteDeliveryBoy(request,pk):
    if is_admin(request.user):
        data=DeliveryBoyModel.objects.get(id=pk)
        data.delete()
        messages.success(request,'Delete Delivery Boy Successfully.')
        return redirect('/DeliveryBoy')
    return redirect('/')

@login_required(login_url='Login')
def Expanse(request):
    if is_admin(request.user):
        data=ExpanseModel.objects.filter(user=request.user.username)
        return render(request,'admin/expanse.html',{'data':data})
    if is_user(request.user):
        data=ExpanseModel.objects.filter(user=request.user.username)
        return render(request,'expanse.html',{'data':data})

@login_required(login_url='Login')
def AddExpanse(request):
    if request.method=="POST": 
        user=str(request.user.username)   
        Expanse=request.POST.get('Expanse')
        Type=request.POST.get('Type')
        dt=ExpanseModel.objects.create(user=user,Expanse=Expanse,Type=Type)
        dt.save()
        messages.success(request,'Add Expanse Successfully.')
        return redirect('/AddExpanse')
    if is_admin(request.user):
        return render(request,'admin/addexpanse.html')
    if is_user(request.user):
        return render(request,'addexpanse.html')

@login_required(login_url='Login')
def EditExpanse(request,id):
    if is_admin(request.user):
        data=ExpanseModel.objects.get(id=id)
        if request.method=="POST":   
            data.Expanse=request.POST.get('Expanse')
            data.Type=request.POST.get('Type')
            data.save()
            messages.success(request,'Expanse Edit Successfully.')
            return redirect('/Expanse')
        return render(request,'admin/editexpanse.html',{'data':data})
    return redirect('/')

@login_required(login_url='Login')
def DeleteExpanse(request,id):
    if is_admin(request.user):
        data=ExpanseModel.objects.get(id=id)
        data.delete()
        messages.success(request,'Delete Expanse Successfully.')
        return redirect('/Expanse')
    return redirect('/')

@login_required(login_url='Login')
def Charges(request):
    if is_admin(request.user):
        data=ChargesModel.objects.filter(user=request.user.username)
        return render(request,'admin/charges.html',{'data':data})
    if is_user(request.user):
        data=ChargesModel.objects.filter(user=request.user.username)
        return render(request,'charges.html',{'data':data})

@login_required(login_url='Login')
def AddCharges(request):
    if request.method=="POST": 
        user=str(request.user.username)   
        Charges=request.POST.get('Charges')
        dt=ChargesModel.objects.create(user=user,Charges=Charges)
        dt.save()
        messages.success(request,'Add Charges Successfully.')
        return redirect('/AddCharges')
    if is_admin(request.user):
        return render(request,'admin/addcharges.html')
    if is_user(request.user):
        return render(request,'addcharges.html')
    
@login_required(login_url='Login')
def EditCharges(request,id):
    if is_admin(request.user):
        data=ChargesModel.objects.get(id=id)
        if request.method=="POST":   
            data.Charges=request.POST.get('Charges')
            data.save()
            messages.success(request,'Charges Edit Successfully.')
            return redirect('/Charges')
        return render(request,'admin/editcharges.html',{'data':data})
    return redirect('/')

@login_required(login_url='Login')
def DeleteCharges(request,id):
    if is_admin(request.user):
        data=ChargesModel.objects.get(id=id)
        data.delete()
        messages.success(request,'Delete Charges Successfully.')
        return redirect('/Charges')
    return redirect('/')

@login_required(login_url='Login')
def PurchaseEntry(request):
    if is_admin(request.user):
        Purchase = PurchaseEntryModel.objects.filter(Type='Purchase')
        data = {'Purchase':Purchase}
        return render(request,'admin/purchaseentry.html',data)
    if is_user(request.user):
        return render(request,'purchaseentry.html')

@login_required(login_url='Login')
def Purchase(request):
    if is_admin(request.user):
        purchase = PurchaseEntryModel.objects.filter(user=request.user,Type='Purchase')
        data = {'purchase':purchase}
        return render(request,'admin/purchase.html',data)
    if is_user(request.user):
        purchase = PurchaseEntryModel.objects.filter(user=request.user,Type='Purchase')
        data = {'purchase':purchase}
        return render(request,'purchase.html',data)

@login_required(login_url='Login')
def AddPurchaseEntry(request):
    try:
        user=str(request.user.username)
        type = 'Purchase'
        cp = NMModel.objects.get(user=user,type=type)
        ProductId = cp.ProductId
    except NMModel.DoesNotExist:
        user = request.user.username
        ProductId = '1'
        type = 'Purchase'
        nm=NMModel.objects.create(ProductId=ProductId,user=user,type=type)
        nm.save()
        cp = NMModel.objects.get(user=user,type=type)
        ProductId = cp.ProductId
    try:
        user=str(request.user.username)
        type = 'Purchase'
        BN= BiilNoModel.objects.get(user=user,type=type)
        BiilNo = BN.BillNo
    except BiilNoModel.DoesNotExist:
        user = request.user.username
        ProductId = '1'
        type = 'Purchase'
        nm=BiilNoModel.objects.create(BillNo=ProductId,user=user,type=type)
        nm.save()
        BN= BiilNoModel.objects.get(user=user,type=type)
        BiilNo = BN.BillNo
    stock = StockModel.objects.filter(ProductId=ProductId,user=user,type=type)
    Category=CategoryModel.objects.filter(user=request.user)
    Product = ProductModel.objects.filter(user=request.user)
    Party = PartyModel.objects.filter(user=request.user)
    tamonut = 0
    for i in stock:
        tamonut+=float(i.Amount)
    tamonut= str(tamonut)
    Charges=ChargesModel.objects.filter(user=request.user.username)
    ChargesList = ChargesListModel.objects.filter(user=request.user,ProductId=ProductId,type='Purchase')
    TCA = 0
    for i in ChargesList:
        TCA += float(i.TotalAmount)
    TCA = TCA
    data={'Category':Category,'Product':Product,'ProductId':ProductId,'BiilNo':BiilNo,'TCA':TCA,'ChargesList':ChargesList,'Charges':Charges,'Party':Party,'type':type,'stock':stock,'tamonut':tamonut}
    if request.method=="POST":    
        user=str(request.user.username)
        TypeofPurchase=request.POST.get('TypeofPurchase')
        Bill=request.POST.get('BillNo')
        InvoiceNo=request.POST.get('InvoiceNo')
        TypeofPayment=request.POST.get('TypeofPayment')
        PartyName=request.POST.get('PartyName')
        ProductId=request.POST.get('ProductId')
        DueDate=request.POST.get('DueDate')
        Date=request.POST.get('Date')
        Type='Purchase'
        Amount=request.POST.get('Amount')
        stock=StockModel.objects.filter(ProductId=ProductId,user=request.user)
        tamonut= 0
        quantity = 0
        purchaseprice = 0
        purchaseinctax = 0
        for i in stock:
            tamonut+=float(i.Amount)
            quantity+=int(i.Quantity)
            purchaseprice+=float(i.PurchasePrice)
            purchaseinctax+=float(i.PurchaseIncTax)
        tamonut= str(tamonut)
        quantity= str(quantity)
        purchaseprice= str(purchaseprice)
        purchaseinctax= str(purchaseinctax)
        tamonut = str(float(tamonut) + float(TCA))
        dt=PurchaseEntryModel.objects.create(user=user,TypeofPurchase=TypeofPurchase,BillNo=Bill,InvoiceNo=InvoiceNo,TypeofPayment=TypeofPayment,PartyName=PartyName,ProductId=ProductId,Type=Type,Amount=tamonut,DueDate=DueDate,TQuantity=quantity,TPurchasePrice=purchaseprice,TPurchaseIncTax=purchaseinctax,Date=Date,TChargesAmount=TCA)
        dt.save()
        stock = StockModel.objects.filter(ProductId=ProductId,user=user,type=type)
        for i in stock:
            MainS=MainStockModel.objects.create(OldProductId=i.id,ProductId=i.ProductId,user=user,type=type,ProductName=i.ProductName,Category=i.Category,Tax=i.Tax,Unit=i.Unit,PurchasePrice=i.PurchasePrice,PurchaseIncTax=i.PurchaseIncTax,MinQty=i.MinQty,MaxQty=i.MaxQty,BarcodeNo=i.BarcodeNo,Quantity=i.Quantity,Amount=i.Amount)
            MainS.save()
        user=str(request.user.username)
        cp = NMModel.objects.get(user=user,type='Purchase')
        cp.ProductId =str(int(cp.ProductId)+1)
        cp.save()
        BN = BiilNoModel.objects.get(user=user,type='Purchase')
        BN.BillNo =str(int(BN.BillNo)+1)
        BN.save()
        messages.success(request,'Purchase Successfully.')
        return redirect('/AddPurchaseEntry')
    if is_admin(request.user):
        return render(request,'admin/addpurchaseentry.html',data)
    if is_user(request.user):
        return render(request,'addpurchaseentry.html',data)

@login_required(login_url='Login')
@csrf_exempt
def SProducts(request,PN,id,type):
    prd = ProductModel.objects.get(id=id)
    user = str(request.user.username)
    val= NMModel.objects.get(user=user,type=type)
    stockproduct = StockModel.objects.create(ProductId=val.ProductId,user=user,type=type,ProductName=prd.ProductName,Category=prd.Category,Tax=prd.Tax,Unit=prd.Unit,PurchasePrice='0',PurchaseIncTax='0',MinQty=prd.MinQty,MaxQty=prd.MaxQty,BarcodeNo=prd.BarcodeNo,Quantity='0',Amount='0')
    stockproduct.save()
    get = StockModel.objects.filter(ProductId=val.ProductId,user=user,type=type).values()
    Sc = list(get)
    tamonut = 0
    for i in get:
        tamonut+=float(i['Amount'])
    PT = "%.2f" % tamonut
    tamonut= str(PT)
    return JsonResponse({'Sc':Sc,'tamonut':tamonut})

@login_required(login_url='Login')
@csrf_exempt
def ProductE(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        id = request.POST.get('id')
        val = request.POST.get('val')
        type = request.POST.get('type')
    dt=StockModel.objects.get(id=id)
    if 'Quantity' == name:
        if val == '':
            dt.Quantity = '0'
        else: 
            dt.Quantity = val
        dt.save()
    if 'PurchasePrice' == name:
        if val == '':
            dt.PurchasePrice = '0'
        else:
            dt.PurchasePrice = val
        dt.save()
    dt=StockModel.objects.get(id=id) 
    if dt.PurchasePrice == '':
        PurchasePrice = 0
    else:
        PurchasePrice = float(dt.PurchasePrice)
    if PurchasePrice == 0:
        dt.PurchaseIncTax = '0'
    else:
        if dt.Tax == 'TaxFree':
            PT = 1 * PurchasePrice
            PT = "%.2f" % PT
            dt.PurchaseIncTax = str(PT)
        else:
            PT = 1 * PurchasePrice * int(dt.Tax) / 100  + PurchasePrice
            PT = "%.2f" % PT
            dt.PurchaseIncTax = str(PT)
    if dt.Quantity == '':
        Quantity = 0
    else:
        Quantity = int(dt.Quantity)
    if dt.Quantity == 0:
        dt.Amount = '' 
    else:
        if PurchasePrice == 0:
            pp= 0
        else:
            PT = "%.2f" % PurchasePrice
            pp = float(PT)
        if dt.Tax == 'TaxFree':
            PT = 1 * pp 
            PT = "%.2f" % PT
            PT =Quantity * float(PT)
            PT = "%.2f" % PT
            dt.Amount = str(PT)
        else:
            PT = 1 * pp * int(dt.Tax) / 100  + PurchasePrice
            dfgr = "%.2f" % Quantity
            PT = "%.2f" % PT
            PT = float(dfgr) * float(PT)
            PT = "%.2f" % PT
            dt.Amount = str(PT) 
    dt.save()
    get = StockModel.objects.filter(ProductId=dt.ProductId,user=request.user.username,type=type).values()
    Sc = list(get)
    tamonut = 0
    for i in get:
        tamonut+=float(i['Amount'])
    PT = "%.2f" % tamonut
    tamonut= str(PT)
    return JsonResponse({'Sc':Sc,'tamonut':tamonut})

@login_required(login_url='Login')
@csrf_exempt
def ProductsDelete(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        type = request.POST.get('type')
        data=StockModel.objects.get(id=id,type=type)
        data.delete()
        val= NMModel.objects.get(user=request.user,type=type)
        get = StockModel.objects.filter(ProductId=val.ProductId,user=request.user,type=type).values()
        tamonut = 0
        for i in get:
            tamonut+=float(i['Amount'])
        tamonut= str(tamonut)
        return JsonResponse({'status':1,'tamonut':tamonut})
    else:
        return JsonResponse({'status':0})

@login_required(login_url='Login')
def PurchaseCancel(request,id):
    data=StockModel.objects.filter(ProductId=id,user=request.user,type='Purchase')
    data.delete()
    return redirect('/Purchase')

@login_required(login_url='Login')
def PurchaseDetails(request,id):
    data=PurchaseEntryModel.objects.get(id=id,Type='Purchase')
    stock=StockModel.objects.filter(ProductId=data.ProductId,type='Purchase',user=request.user)
    tamonut = 0
    quantity = 0
    purchaseprice = 0
    purchaseinctax = 0
    for i in stock:
        tamonut+=float(i.Amount)
        quantity+=int(i.Quantity)
        purchaseprice+=float(i.PurchasePrice)
        purchaseinctax+=float(i.PurchaseIncTax)
    tamonut= str(tamonut)
    quantity= str(quantity)
    purchaseprice= str(purchaseprice)
    purchaseinctax= str(purchaseinctax)
    Charges=ChargesListModel.objects.filter(ProductId=data.ProductId,type='Purchase',user=request.user)
    CA,TCA = 0,0
    for i in Charges:
        CA +=float(i.Amount)
        TCA +=float(i.TotalAmount)
    CA = str(CA)
    TCA= str(TCA)
    if is_admin(request.user):
        return render(request,'admin/purchasedetails.html',{'data':data,'stock':stock,'tamonut':tamonut,'quantity':quantity,'purchaseprice':purchaseprice,'purchaseinctax':purchaseinctax,'Charges':Charges,'CA':CA,'TCA':TCA})
    if is_user(request.user):
        return render(request,'purchasedetails.html',{'data':data,'stock':stock,'tamonut':tamonut,'quantity':quantity,'purchaseprice':purchaseprice,'purchaseinctax':purchaseinctax,'Charges':Charges,'CA':CA,'TCA':TCA})

@login_required(login_url='Login')
def SalesEntry(request):
    if is_admin(request.user):
        sales = SalesEntryModel.objects.filter(Type='Sales')
        sp = {i.PartyName for i in sales}
        data = {'sales':sales,'sp':sp}
        return render(request,'admin/salesentry.html',data)
    if is_user(request.user):
        return render(request,'salesentry.html')

@login_required(login_url='Login')
def Sales(request):
    if is_admin(request.user):
        sales = SalesEntryModel.objects.filter(Type='Sales',user=request.user)
        data = {'sales':sales}
        return render(request,'admin/sales.html',data)
    if is_user(request.user):
        sales = SalesEntryModel.objects.filter(Type='Sales',user=request.user)
        data = {'sales':sales}
        return render(request,'sales.html',data)
    
@login_required(login_url='Login')
def AddSalesEntry(request):
    try:
        user=str(request.user.username)
        type = 'Sales'
        cp = NMModel.objects.get(user=user,type=type)
        ProductId = cp.ProductId
    except NMModel.DoesNotExist:
        user = request.user.username
        ProductId = '1'
        type = 'Sales'
        nm=NMModel.objects.create(ProductId=ProductId,user=user,type=type)
        nm.save()
        cp = NMModel.objects.get(user=user,type=type)
        ProductId = cp.ProductId
    try:
        user=str(request.user.username)
        type = 'Sales'
        BN= InvoiceNoModel.objects.get(user=user,type=type)
        Invoice = BN.InvoiceNo
    except InvoiceNoModel.DoesNotExist:
        user = request.user.username
        ProductId = '1'
        type = 'Sales'
        nm=InvoiceNoModel.objects.create(InvoiceNo=ProductId,user=user,type=type)
        nm.save()
        BN= InvoiceNoModel.objects.get(user=user,type=type)
        Invoice = BN.InvoiceNo
    stock = SalesStockModel.objects.filter(ProductId=ProductId,user=user,type=type)
    Category=CategoryModel.objects.filter(user=request.user)
    stokes=MainStockModel.objects.filter(user=request.user)
    Charges=ChargesModel.objects.filter(user=request.user.username)
    ChargesList = ChargesListModel.objects.filter(user=request.user,ProductId=ProductId,type='Sales')
    TCA = 0
    for i in ChargesList:
        TCA += float(i.TotalAmount)
    TCA = TCA
    productns={i.ProductName for i in stokes}
    Product = ProductModel.objects.filter(user=request.user)
    Party = PartyModel.objects.filter(user=request.user)
    DB =  DeliveryBoyModel.objects.filter(user=request.user)
    tamonut = 0
    for i in stock:
        tamonut += float(i.TotalSales)
    data={'Category':Category,'Product':Product,'ProductId':ProductId,'productns':productns,'Invoice':Invoice,'TCA':TCA,'ChargesList':ChargesList,'Party':Party,'Charges':Charges,'stokes':stokes,'type':type,'stock':stock,'tamonut':tamonut,'DB':DB}
    if request.method=="POST":    
        user=str(request.user)
        DeliveryBoyName=request.POST.get('DeliveryBoyName')
        TypeOfBusiness=request.POST.get('TypeOfBusiness')
        DeliveryTime=request.POST.get('DeliveryTime')
        InvoiceNo=Invoice
        PartyName=request.POST.get('PartyName')
        ProductId=request.POST.get('ProductId')
        Date=request.POST.get('Date')
        Type='Sales'
        Amount=str(float(tamonut) + float(TCA))
        dt=SalesEntryModel.objects.create(user=user,DeliveryBoyName=DeliveryBoyName,TypeOfBusiness=TypeOfBusiness,InvoiceNo=InvoiceNo,DeliveryTime=DeliveryTime,PartyName=PartyName,ProductId=ProductId,Type=Type,Amount=Amount,Date=Date,TChargesAmount=TCA)
        dt.save()
        stock = SalesStockModel.objects.filter(ProductId=ProductId,user=user,type=type)
        wtAmount=0
        for i in stock:
            dt=MainStockModel.objects.get(id=i.sid)
            newQuantity = int(dt.Quantity) - int(i.Quantity)
            if newQuantity == 0:
                dt.delete()
            else:
                wtAmount += float(dt.PurchaseIncTax) * int(newQuantity)
                dt.Quantity = str(newQuantity)
                dt.Amount = str(wtAmount)
                dt.save()
        user=str(request.user)
        cp = NMModel.objects.get(user=user,type = 'Sales')
        cp.ProductId =str(int(cp.ProductId)+1)
        cp.save()
        BN = InvoiceNoModel.objects.get(user=user,type='Sales')
        BN.InvoiceNo =str(int(BN.InvoiceNo)+1)
        BN.save()
        messages.success(request,'Sales Successfully.')
        return redirect('/AddSalesEntry')
    if is_admin(request.user):
        return render(request,'admin/addsalesentry.html',data)
    if is_user(request.user):
        return render(request,'addsalesentry.html',data)
    

def StockDetails(request,name):
    Ms = MainStockModel.objects.filter(user=request.user,ProductName=name).values()
    Ms = list(Ms)
    return JsonResponse({'Ms':Ms})

@login_required(login_url='Login')
@csrf_exempt
def Stockswork(request,PN,id,id2,type):
    user = str(request.user.username)
    val= NMModel.objects.get(user=user,type=type)
    ms = MainStockModel.objects.get(id=id2)
    OldProductId = id
    type = type
    ProductId = val.ProductId
    SalesStock=SalesStockModel.objects.create(ProductId=ProductId,user=user,type=type,ProductName=ms.ProductName,Category=ms.Category,Tax=ms.Tax,Unit=ms.Unit,PurchaseIncTax=ms.PurchaseIncTax,BarcodeNo=ms.BarcodeNo,Quantity=ms.Quantity,Amount='0',sid=ms.id,ProfitMargin='0',BasicSalesPrice='0',Discount='0',SalesPriceAfterDiscount='0',IncSalesPrice='0',TotalSales='0')
    SalesStock.save()
    get = SalesStockModel.objects.filter(ProductId=ProductId,user=user,type=type).values()
    Sc = list(get)
    stock = SalesStockModel.objects.filter(ProductId=ProductId,user=user,type=type)
    tamonut = 0
    for i in stock:
        tamonut+=float(i.TotalSales)
    tamonut = str(tamonut)
    return JsonResponse({'Sc':Sc,'tamonut':tamonut})

@login_required(login_url='Login')
@csrf_exempt
def StockPDelete(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        type = request.POST.get('type')
        data= SalesStockModel.objects.get(id=id,type=type)
        data.delete()
        val= NMModel.objects.get(user=request.user,type=type)
        get = SalesStockModel.objects.filter(ProductId=val.ProductId,user=request.user,type=type).values()
        tamonut = 0
        for i in get:
            tamonut+=float(i['TotalSales'])
        tamonut= str(tamonut)
        return JsonResponse({'status':1,'tamonut':tamonut})
    else:
        return JsonResponse({'status':0})

@login_required(login_url='Login')
@csrf_exempt
def ProductE2(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        id = request.POST.get('id')
        val = request.POST.get('val')
        type = request.POST.get('type')
    dt=SalesStockModel.objects.get(id=id)
    if name == 'ProfitMargin':
        if val == '':
            dt.ProfitMargin = ''
        else:
            dt.ProfitMargin = val
        dt.save()
    if name == 'Quantity':
        if val == '':
            dt.Quantity = ''
        else:
            mstock = MainStockModel.objects.get(id=dt.sid)
            if mstock.Unit == 'KG':
                if int(mstock.Quantity) < float(val):
                    return JsonResponse({'msg':'Stoke is not Avilabel.'})
                else:
                    dt.Quantity = val
            else:
                if int(val):
                    if int(mstock.Quantity) < int(val):
                        return JsonResponse({'msg':'Stoke is not Avilabel.'})
                    else:
                        dt.Quantity = val
                else:
                    return JsonResponse({'msg':'Quantity Value is not Perfact.'})
        dt.save()
    if name == 'Discount':
        if val == '':
            dt.Discount = ''
        else:
            dt.Discount = val
        dt.save()
    if name == 'Amount':
        if val == '':
            dt.Amount = ''
        else:
            dt.Amount = val
        dt.save()
        return JsonResponse({'msg':'Stoke is not Avilabel.'})
    dt=SalesStockModel.objects.get(id=id)
    if dt.ProfitMargin == '' or dt.ProfitMargin == '0':
        dt.BasicSalesPrice = '0'
    else:
        PT =float(dt.PurchaseIncTax) * int(dt.ProfitMargin) / 100
        BSP = float(dt.PurchaseIncTax)+PT
        dt.BasicSalesPrice =  "%.2f" % BSP
    if dt.Discount == '' or dt.Discount == '0':
        dt.SalesPriceAfterDiscount = '0'
    else:
        PT =float(dt.BasicSalesPrice) * int(dt.Discount) / 100
        dt.SalesPriceAfterDiscount =  str(round(float(dt.BasicSalesPrice)-PT,2))
        if dt.Tax == 'TaxFree':
            PT2 = float(dt.SalesPriceAfterDiscount)
            dt.IncSalesPrice =  str(round(float(dt.SalesPriceAfterDiscount),2))
        else:
            PT2 = float(dt.SalesPriceAfterDiscount) * int(dt.Tax) /100
            dt.IncSalesPrice =  str(round(float(dt.SalesPriceAfterDiscount)+PT2,2))
        if dt.Quantity == '' or dt.Quantity == '0':
            dt.TotalSales = '0'
        else:
            dt.TotalSales = str(round(float(dt.Quantity)* float(dt.IncSalesPrice),2))
    dt.save()
    get = SalesStockModel.objects.filter(ProductId=dt.ProductId,user=request.user.username,type=type).values()
    Sc = list(get)
    rt= 0
    for i in get:
        rt += float(i['TotalSales'])
    rt = str(rt)
    return JsonResponse({'Sc':Sc,'rt':rt})

@login_required(login_url='Login')
def SalesDetails(request,id):
    data=SalesEntryModel.objects.get(id=id,Type='Sales')
    stock=SalesStockModel.objects.filter(ProductId=data.ProductId,type='Sales',user=request.user)
    tamonut = 0
    quantity = 0
    purchaseprice = 0
    bps = 0
    sp = 0
    isp = 0
    for i in stock:
        tamonut+=float(i.TotalSales)
        quantity+=int(i.Quantity)
        purchaseprice+=float(i.PurchaseIncTax)
        bps +=float(i.BasicSalesPrice)
        sp+= float(i.SalesPriceAfterDiscount)
        isp += float(i.IncSalesPrice)
    tamonut= str(tamonut)
    quantity= str(quantity)
    purchaseprice= str(purchaseprice)
    bps= str(bps)
    sp =str(sp)
    isp =str(isp)
    Charges=ChargesListModel.objects.filter(ProductId=data.ProductId,type='Sales',user=request.user)
    CA,TCA = 0,0
    for i in Charges:
        CA +=float(i.Amount)
        TCA +=float(i.TotalAmount)
    CA = str(CA)
    TCA= str(TCA)
    if is_admin(request.user):
        return render(request,'admin/salesdetails.html',{'data':data,'stock':stock,'tamonut':tamonut,'quantity':quantity,'purchaseprice':purchaseprice,'bsp':bps,'sp':sp,'isp':isp,'Charges':Charges,'CA':CA,'TCA':TCA})
    if is_user(request.user):
        return render(request,'salesdetails.html',{'data':data,'stock':stock,'tamonut':tamonut,'quantity':quantity,'purchaseprice':purchaseprice,'bsp':bps,'sp':sp,'isp':isp,'Charges':Charges,'CA':CA,'TCA':TCA})

@login_required(login_url='Login')
def SalesCancel(request,id):
    data=SalesStockModel.objects.filter(ProductId=id,user=request.user,type='Sales')
    data.delete()
    return redirect('/Sales')

@login_required(login_url='Login')
def PurchaseReturn(request):
    if is_admin(request.user):
        purchase = PurchaseEntryModel.objects.filter(user=request.user,Type='PurchaseReturn')
        data = {'purchase':purchase}
        return render(request,'admin/purchasereturn.html',data)
    if is_user(request.user):
        purchase = PurchaseEntryModel.objects.filter(user=request.user,Type='PurchaseReturn')
        data = {'purchase':purchase}
        return render(request,'purchasereturn.html',data)

@login_required(login_url='Login')
def AddPurchaseReturnEntry(request):
    try:
        user=str(request.user.username)
        type = 'PurchaseReturn'
        cp = NMModel.objects.get(user=user,type=type)
        ProductId = cp.ProductId
    except NMModel.DoesNotExist:
        user = request.user.username
        ProductId = '1'
        type = 'PurchaseReturn'
        nm=NMModel.objects.create(ProductId=ProductId,user=user,type=type)
        nm.save()
        cp = NMModel.objects.get(user=user,type=type)
        ProductId = cp.ProductId
    try:
        user=str(request.user.username)
        type = 'PurchaseReturn'
        BN= BiilNoModel.objects.get(user=user,type=type)
        BiilNo = BN.BillNo
    except BiilNoModel.DoesNotExist:
        user = request.user.username
        ProductId = '1'
        type = 'PurchaseReturn'
        nm=BiilNoModel.objects.create(BillNo=ProductId,user=user,type=type)
        nm.save()
        BN= BiilNoModel.objects.get(user=user,type=type)
        BiilNo = BN.BillNo
    stock = StockModel.objects.filter(ProductId=ProductId,user=user,type=type)
    Category=CategoryModel.objects.filter(user=request.user)
    stokes=MainStockModel.objects.filter(user=request.user)
    productns={i.ProductName for i in stokes}
    Product = ProductModel.objects.filter(user=request.user)
    Party = PartyModel.objects.filter(user=request.user)
    tamonut = 0
    for i in stock:
        tamonut+=float(i.Amount)
    tamonut= str(tamonut)
    data={'Category':Category,'Product':Product,'ProductId':ProductId,'productns':productns,'BiilNo':BiilNo,'Party':Party,'type':type,'stock':stock,'tamonut':tamonut}
    if request.method=="POST":    
        user=str(request.user.username)
        TypeofPurchase=request.POST.get('TypeofPurchase')
        Bill=request.POST.get('BillNo')
        InvoiceNo=request.POST.get('InvoiceNo')
        TypeofPayment=request.POST.get('TypeofPayment')
        PartyName=request.POST.get('PartyName')
        ProductId=request.POST.get('ProductId')
        DueDate=request.POST.get('DueDate')
        Date=request.POST.get('Date')
        Type='PurchaseReturn'
        Amount=request.POST.get('Amount')
        stock=StockModel.objects.filter(ProductId=ProductId,user=request.user,type='PurchaseReturn')
        tamonut= 0
        quantity = 0
        purchaseprice = 0
        purchaseinctax = 0
        for i in stock:
            tamonut+=float(i.Amount)
            quantity+=int(i.Quantity)
            purchaseprice+=float(i.PurchasePrice)
            purchaseinctax+=float(i.PurchaseIncTax)
        tamonut= str(tamonut)
        quantity= str(quantity)
        purchaseprice= str(purchaseprice)
        purchaseinctax= str(purchaseinctax)
        dt=PurchaseEntryModel.objects.create(user=user,TypeofPurchase=TypeofPurchase,BillNo=Bill,InvoiceNo=InvoiceNo,TypeofPayment=TypeofPayment,PartyName=PartyName,ProductId=ProductId,Type=Type,Amount=tamonut,DueDate=DueDate,TQuantity=quantity,TPurchasePrice=purchaseprice,TPurchaseIncTax=purchaseinctax,Date=Date)
        dt.save()
        stock = StockModel.objects.filter(ProductId=ProductId,user=user,type=type)
        for i in stock:
            dt=MainStockModel.objects.get(id=i.sid)
            newQuantity = int(dt.Quantity) - int(i.Quantity)
            if newQuantity == 0:
                dt.delete()
            else:
                wtAmount = float(dt.PurchaseIncTax) * int(newQuantity)
                dt.Quantity = str(newQuantity)
                PT = "%.2f" % wtAmount
                dt.Amount = str(PT)
                dt.save()
        user=str(request.user.username)
        cp = NMModel.objects.get(user=user,type='PurchaseReturn')
        cp.ProductId =str(int(cp.ProductId)+1)
        cp.save()
        BN = BiilNoModel.objects.get(user=user,type='PurchaseReturn')
        BN.BillNo =str(int(BN.BillNo)+1)
        BN.save()
        messages.success(request,'Purchase Return Successfully.')
        return redirect('/AddPurchaseReturnEntry')
    if is_admin(request.user):
        return render(request,'admin/addpurchasereturnentry.html',data)
    if is_user(request.user):
        return render(request,'addpurchasereturnentry.html',data)
    

@login_required(login_url='Login')
@csrf_exempt
def PRStock(request,PN,id,id2,type):
    user = str(request.user.username)
    val= NMModel.objects.get(user=user,type=type)
    ms = MainStockModel.objects.get(id=id2)
    type = type
    ProductId = val.ProductId
    stockproduct = StockModel.objects.create(ProductId=val.ProductId,user=user,type=type,ProductName=ms.ProductName,Category=ms.Category,Tax=ms.Tax,Unit=ms.Unit,PurchasePrice=ms.PurchasePrice,PurchaseIncTax=ms.PurchaseIncTax,MinQty=ms.MinQty,MaxQty=ms.MaxQty,BarcodeNo=ms.BarcodeNo,Quantity=ms.Quantity,Amount=ms.Amount,sid=id2)
    stockproduct.save()
    get = StockModel.objects.filter(ProductId=ProductId,user=user,type=type).values()
    Sc = list(get)
    tamonut = 0
    for i in get:
        tamonut+=float(i['Amount'])
    PT = "%.2f" % tamonut
    tamonut= str(PT)
    return JsonResponse({'Sc':Sc,'tamonut':tamonut})

@login_required(login_url='Login')
@csrf_exempt
def PRSDelete(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        type = request.POST.get('type')
        data=StockModel.objects.get(id=id,type=type)
        data.delete()
        val= NMModel.objects.get(user=request.user,type=type)
        get = StockModel.objects.filter(ProductId=val.ProductId,user=request.user,type=type).values()
        tamonut = 0
        for i in get:
            tamonut+=float(i['Amount'])
        tamonut= str(tamonut)
        return JsonResponse({'status':1,'tamonut':tamonut})
    else:
        return JsonResponse({'status':0})

@login_required(login_url='Login')
def PRDetails(request,id):
    data=PurchaseEntryModel.objects.get(id=id,Type='PurchaseReturn')
    stock=StockModel.objects.filter(ProductId=data.ProductId,type='PurchaseReturn',user=request.user)
    tamonut = 0
    quantity = 0
    purchaseprice = 0
    purchaseinctax = 0
    for i in stock:
        tamonut+=float(i.Amount)
        quantity+=int(i.Quantity)
        purchaseprice+=float(i.PurchasePrice)
        purchaseinctax+=float(i.PurchaseIncTax)
    tamonut= str(tamonut)
    quantity= str(quantity)
    purchaseprice= str(purchaseprice)
    purchaseinctax= str(purchaseinctax)
    if is_admin(request.user):
        return render(request,'admin/prdetails.html',{'data':data,'stock':stock,'tamonut':tamonut,'quantity':quantity,'purchaseprice':purchaseprice,'purchaseinctax':purchaseinctax})
    if is_user(request.user):
        return render(request,'prdetails.html',{'data':data,'stock':stock,'tamonut':tamonut,'quantity':quantity,'purchaseprice':purchaseprice,'purchaseinctax':purchaseinctax})

@login_required(login_url='Login')
def SalesReturn(request):
    if is_admin(request.user):
        salesReturn = SalesEntryModel.objects.filter(Type='SalesReturn',user=request.user)
        data = {'salesReturn':salesReturn}
        return render(request,'admin/salesreturn.html',data)
    if is_user(request.user):
        salesReturn = SalesEntryModel.objects.filter(Type='SalesReturn',user=request.user)
        data = {'salesReturn':salesReturn}
        return render(request,'salesreturn.html',data)

@login_required(login_url='Login')
def AddSalesReturnEntry(request):
    try:
        user=str(request.user.username)
        type = 'SalesReturn'
        cp = NMModel.objects.get(user=user,type=type)
        ProductId = cp.ProductId
    except NMModel.DoesNotExist:
        user = request.user.username
        ProductId = '1'
        type = 'SalesReturn'
        nm=NMModel.objects.create(ProductId=ProductId,user=user,type=type)
        nm.save()
        cp = NMModel.objects.get(user=user,type=type)
        ProductId = cp.ProductId
    try:
        user=str(request.user.username)
        type = 'SalesReturn'
        BN= InvoiceNoModel.objects.get(user=user,type=type)
        Invoice = BN.InvoiceNo
    except InvoiceNoModel.DoesNotExist:
        user = request.user.username
        ProductId = '1'
        type = 'SalesReturn'
        nm=InvoiceNoModel.objects.create(InvoiceNo=ProductId,user=user,type=type)
        nm.save()
        BN= InvoiceNoModel.objects.get(user=user,type=type)
        Invoice = BN.InvoiceNo
    stock = SalesStockModel.objects.filter(ProductId=ProductId,user=user,type=type)
    Category=CategoryModel.objects.filter(user=request.user)
    stokes=MainStockModel.objects.filter(user=request.user)
    productns={i.ProductName for i in stokes}
    Product = ProductModel.objects.filter(user=request.user)
    Party = PartyModel.objects.filter(user=request.user)
    DB =  DeliveryBoyModel.objects.filter(user=request.user)
    tamonut = 0
    for i in stock:
        tamonut += float(i.TotalSales)
    tamonut = tamonut
    print(tamonut)
    data={'Category':Category,'Product':Product,'ProductId':ProductId,'productns':productns,'Invoice':Invoice,'Party':Party,'stokes':stokes,'type':type,'stock':stock,'tamonut':tamonut,'DB':DB}
    if request.method=="POST":    
        user=str(request.user)
        DeliveryBoyName=request.POST.get('DeliveryBoyName')
        TypeOfBusiness=request.POST.get('TypeOfBusiness')
        DeliveryTime=request.POST.get('DeliveryTime')
        InvoiceNo=Invoice
        PartyName=request.POST.get('PartyName')
        ProductId=request.POST.get('ProductId')
        Date=request.POST.get('Date')
        Type='SalesReturn'
        Amount=tamonut
        dt=SalesEntryModel.objects.create(user=user,DeliveryBoyName=DeliveryBoyName,TypeOfBusiness=TypeOfBusiness,InvoiceNo=InvoiceNo,DeliveryTime=DeliveryTime,PartyName=PartyName,ProductId=ProductId,Type=Type,Amount=Amount,Date=Date)
        dt.save()
        stock = SalesStockModel.objects.filter(ProductId=ProductId,user=user,type=type)
        for i in stock:
            MainS=MainStockModel.objects.create(OldProductId='0',ProductId=i.ProductId,user=user,type=type,ProductName=i.ProductName,Category=i.Category,Tax=i.Tax,Unit=i.Unit,PurchasePrice=i.PurchaseIncTax,PurchaseIncTax=i.PurchaseIncTax,MinQty='0',MaxQty='0',BarcodeNo=i.BarcodeNo,Quantity=i.Quantity,Amount=i.Amount)
            MainS.save()
        user=str(request.user)
        cp = NMModel.objects.get(user=user,type = 'SalesReturn')
        cp.ProductId =str(int(cp.ProductId)+1)
        cp.save()
        BN = InvoiceNoModel.objects.get(user=user,type='SalesReturn')
        BN.InvoiceNo =str(int(BN.InvoiceNo)+1)
        BN.save()
        messages.success(request,'Sales Return Successfully.')
        return redirect('/AddSalesReturnEntry')
    if is_admin(request.user):
        return render(request,'admin/addsalesreturnentry.html',data)
    if is_user(request.user):
        return render(request,'addsalesreturnentry.html',data)
    
@login_required(login_url='Login')
@csrf_exempt
def SRStocks(request,PN,id,type):
    user = str(request.user.username)
    val= NMModel.objects.get(user=user,type=type)
    type = type
    pd = ProductModel.objects.get(id=id)
    ProductId = val.ProductId
    SalesStock=SalesStockModel.objects.create(ProductId=ProductId,user=user,type=type,ProductName=pd.ProductName,Category=pd.Category,Tax=pd.Tax,Unit=pd.Unit,PurchaseIncTax='0',BarcodeNo=pd.BarcodeNo,Quantity='0',Amount='0',ProfitMargin='0',BasicSalesPrice='0',Discount='0',SalesPriceAfterDiscount='0',IncSalesPrice='0',TotalSales='0')
    SalesStock.save()
    get = SalesStockModel.objects.filter(ProductId=ProductId,user=user,type=type).values()
    Sc = list(get)
    stock = SalesStockModel.objects.filter(ProductId=ProductId,user=user,type=type)
    tamonut = 0
    for i in stock:
        tamonut+=float(i.TotalSales)
    PT = "%.2f" % tamonut
    tamonut = str(PT)
    return JsonResponse({'Sc':Sc,'tamonut':tamonut})

@login_required(login_url='Login')
@csrf_exempt
def SRDelete(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        type = request.POST.get('type')
        data= SalesStockModel.objects.get(id=id,type=type)
        data.delete()
        val= NMModel.objects.get(user=request.user,type=type)
        get = SalesStockModel.objects.filter(ProductId=val.ProductId,user=request.user,type=type).values()
        tamonut = 0
        for i in get:
            tamonut+=float(i['TotalSales'])
        tamonut= str(tamonut)
        return JsonResponse({'status':1,'tamonut':tamonut})
    else:
        return JsonResponse({'status':0})
    
@login_required(login_url='Login')
@csrf_exempt
def SRSEdit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        id = request.POST.get('id')
        val = request.POST.get('val')
        type = request.POST.get('type')
    dt=SalesStockModel.objects.get(id=id,type=type)
    if name == 'PurchaseIncTax':
        if val == '':
            dt.PurchaseIncTax = ''
        else:
            dt.PurchaseIncTax = val
        dt.save()
    if name == 'ProfitMargin':
        if val == '':
            dt.ProfitMargin = ''
        else:
            dt.ProfitMargin = val
        dt.save()
    if name == 'Quantity':
        if val == '':
            dt.Quantity = ''
        else:
            dt.Quantity = val
        dt.save()
    if name == 'Discount':
        if val == '':
            dt.Discount = ''
        else:
            dt.Discount = val
        dt.save()
    if name == 'Amount':
        if val == '':
            dt.Amount = ''
        else:
            dt.Amount = val
        dt.save()
    dt=SalesStockModel.objects.get(id=id)
    if dt.ProfitMargin == '' or dt.ProfitMargin == '0':
        dt.BasicSalesPrice = '0'
    else:
        PT =float(dt.PurchaseIncTax) * int(dt.ProfitMargin) / 100
        BSP = float(dt.PurchaseIncTax)+PT
        dt.BasicSalesPrice =  "%.2f" % BSP
    if dt.Discount == '' or dt.Discount == '0':
        dt.SalesPriceAfterDiscount = '0'
    else:
        PT =float(dt.BasicSalesPrice) * int(dt.Discount) / 100
        dt.SalesPriceAfterDiscount =  str(round(float(dt.BasicSalesPrice)-PT,2))
        if dt.Tax == 'TaxFree':
            PT2 = float(dt.SalesPriceAfterDiscount)
            dt.IncSalesPrice =  str(round(float(dt.SalesPriceAfterDiscount),2))
        else:
            PT2 = float(dt.SalesPriceAfterDiscount) * int(dt.Tax) /100
            dt.IncSalesPrice =  str(round(float(dt.SalesPriceAfterDiscount)+PT2,2))
        if dt.Quantity == '' or dt.Quantity == '0':
            dt.TotalSales = '0'
        else:
            dt.TotalSales = str(round(float(dt.Quantity)* float(dt.IncSalesPrice),2))
    dt.save()
    get = SalesStockModel.objects.filter(ProductId=dt.ProductId,user=request.user.username,type=type).values()
    Sc = list(get)
    rt= 0
    for i in get:
        rt += float(i['TotalSales'])
    rt = str(rt)
    return JsonResponse({'Sc':Sc,'rt':rt})

@login_required(login_url='Login')
def SRDetails(request,id):
    data=SalesEntryModel.objects.get(id=id,Type='SalesReturn')
    stock=SalesStockModel.objects.filter(ProductId=data.ProductId,type='SalesReturn',user=request.user)
    tamonut = 0
    quantity = 0
    purchaseprice = 0
    bps = 0
    sp = 0
    isp = 0
    for i in stock:
        tamonut+=float(i.TotalSales)
        quantity+=int(i.Quantity)
        purchaseprice+=float(i.PurchaseIncTax)
        bps +=float(i.BasicSalesPrice)
        sp+= round(float(i.SalesPriceAfterDiscount),2)
        isp += round(float(i.IncSalesPrice),2)
    tamonut= str(tamonut)
    quantity= str(quantity)
    purchaseprice= str(purchaseprice)
    bps= str(bps)
    sp =str(sp)
    isp =str(isp)
    if is_admin(request.user):
        return render(request,'admin/srdetails.html',{'data':data,'stock':stock,'tamonut':tamonut,'quantity':quantity,'purchaseprice':purchaseprice,'bsp':bps,'sp':sp,'isp':isp})
    if is_user(request.user):
        return render(request,'srdetails.html',{'data':data,'stock':stock,'tamonut':tamonut,'quantity':quantity,'purchaseprice':purchaseprice,'bsp':bps,'sp':sp,'isp':isp})

@login_required(login_url='Login')
def SRCancel(request,id):
    data=SalesStockModel.objects.filter(ProductId=id,user=request.user,type='SalesReturn')
    data.delete()
    return redirect('/SalesReturn')

@login_required(login_url='Login')
def ExpensesEntry(request):
    if is_admin(request.user):
        EEM = ExpanseEntryModel.objects.filter(user=request.user)
        data = {'EEM':EEM}
        return render(request,'admin/expensesentry.html',data)
    if is_user(request.user):
        EEM = ExpanseEntryModel.objects.filter(user=request.user,Type='Expenses')
        data = {'EEM':EEM}
        return render(request,'expensesentry.html',data)

@login_required(login_url='Login')
def AddExpensesEntry(request):
    try:
        user=str(request.user.username)
        type = 'Expenses'
        cp = NMModel.objects.get(user=user,type=type)
        ProductId = cp.ProductId
    except NMModel.DoesNotExist:
        user = request.user.username
        ProductId = '1'
        type = 'Expenses'
        nm=NMModel.objects.create(ProductId=ProductId,user=user,type=type)
        nm.save()
        cp = NMModel.objects.get(user=user,type=type)
        ProductId = cp.ProductId
    Expens = ExpanseModel.objects.filter(user=request.user)
    Party = PartyModel.objects.filter(user=request.user)
    ELM = ExpanseListModel.objects.filter(ProductId=ProductId,user=user)
    tamonut = 0
    for i in ELM:
        tamonut+=float(i.Amount)
    PT = "%.2f" % tamonut
    tamonut = str(PT)
    data={'ProductId':ProductId,'Expens':Expens,'Party':Party,'type':type,'ELM':ELM,'tamonut':tamonut}
    if request.method=="POST":    
        user=str(request.user.username)
        TypeofPayment=request.POST.get('TypeofPayment')
        PartyName=request.POST.get('PartyName')
        ProductId=request.POST.get('ProductId')
        Date=request.POST.get('Date')
        Amount=tamonut
        dt=ExpanseEntryModel.objects.create(user=user,TypeofPayment=TypeofPayment,PartyName=PartyName,ProductId=ProductId,Amount=Amount,Date=Date)
        dt.save()
        cp = NMModel.objects.get(user=user,type = 'Expenses')
        cp.ProductId =str(int(cp.ProductId)+1)
        cp.save()
        messages.success(request,'Add Expenses Entry Successfully.')
        return redirect('/AddExpensesEntry')
    if is_admin(request.user):
        return render(request,'admin/addexpensesentry.html',data)
    if is_user(request.user):
        return render(request,'addexpensesentry.html',data)

@login_required(login_url='Login')
@csrf_exempt
def ExpanseList(request,id):
    user = str(request.user.username)
    val= NMModel.objects.get(user=user,type='Expenses')
    ProductId = val.ProductId
    ed=ExpanseModel.objects.get(id=id)
    ELM=ExpanseListModel.objects.create(ProductId=ProductId,user=user,Expanse=ed.Expanse,Amount='0')
    ELM.save()
    get = ExpanseListModel.objects.filter(ProductId=ProductId,user=user).values()
    Sc = list(get)
    ET = ExpanseListModel.objects.filter(ProductId=ProductId,user=user)
    tamonut = 0
    for i in ET:
        tamonut+=float(i.Amount)
    PT = "%.2f" % tamonut
    tamonut = str(PT)
    return JsonResponse({'Sc':Sc,'tamonut':tamonut})

@login_required(login_url='Login')
@csrf_exempt
def EAmount(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        val = request.POST.get('val')
    dt=ExpanseListModel.objects.get(id=id)
    if val == '':
        dt.Amount = '0'
    else:
        dt.Amount = val
    dt.save()
    user=str(request.user.username)
    val= NMModel.objects.get(user=user,type='Expenses')
    ProductId = val.ProductId
    ET = ExpanseListModel.objects.filter(ProductId=ProductId,user=user).values()
    tamonut = 0
    for i in ET:
        tamonut+=float(i['Amount'])
    PT = "%.2f" % tamonut
    tamonut = str(PT)
    return JsonResponse({'tamonut':tamonut})

@login_required(login_url='Login')
@csrf_exempt
def EXDelete(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        data= ExpanseListModel.objects.get(id=id)
        data.delete()
        user=str(request.user.username)
        val= NMModel.objects.get(user=user,type='Expenses')
        ProductId = val.ProductId
        ET = ExpanseListModel.objects.filter(ProductId=ProductId,user=user).values()
        tamonut = 0
        for i in ET:
            tamonut+=float(i['Amount'])
        PT = "%.2f" % tamonut
        tamonut = str(PT)
        return JsonResponse({'status':1,'tamonut':tamonut})
    else:
        return JsonResponse({'status':0})
    
@login_required(login_url='Login')
def EXDetails(request,id):
    data=ExpanseEntryModel.objects.get(id=id)
    ELM=ExpanseListModel.objects.filter(ProductId=data.ProductId,user=request.user)
    tamonut = 0
    for i in ELM:
        tamonut+=float(i.Amount)
    PT = "%.2f" % tamonut
    tamonut = str(PT)
    if is_admin(request.user):
        return render(request,'admin/exdetails.html',{'data':data,'ELM':ELM,'tamonut':tamonut})
    if is_user(request.user):
        return render(request,'exdetails.html',{'data':data,'ELM':ELM,'tamonut':tamonut})
    
@login_required(login_url='Login')
@csrf_exempt
def CreateCharges(request):
    if request.method == 'POST':
        ChargesID = request.POST.get('ChargesID')
        Type = request.POST.get('type')
        user = request.user.username
        PN = NMModel.objects.get(type=Type,user=user)
        Ch = ChargesModel.objects.get(id=ChargesID)
        data = ChargesListModel.objects.create(user=user,Charges=Ch.Charges,ProductId=PN.ProductId,Amount='0',Tax='',TotalAmount='0',type=Type)
        data.save()
        if data.save:
            print("created")
        get = ChargesListModel.objects.filter(ProductId=PN.ProductId,user=user,type=Type).values()
        Sc = list(get)
        ET = ChargesListModel.objects.filter(ProductId=PN.ProductId,user=user,type=Type)
        tamonut = 0
        for i in ET:
            tamonut+=float(i.TotalAmount)
            PT = "%.2f" % tamonut
        tamonut = str(PT)
        return JsonResponse({'Sc':Sc,'tamonut':tamonut})

@login_required(login_url='Login')
@csrf_exempt
def CharegesEdit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        id = request.POST.get('id')
        val = request.POST.get('val')
        type = request.POST.get('type')
    dt=ChargesListModel.objects.get(id=id,type=type)
    if name == 'Amount':
        if val == '':
            dt.Amount = '0'
        else:
            dt.Amount = val
        dt.save()
    if name == 'Tax':
        if val == 'TaxFree':
            dt.Tax = 'TaxFree'
        else:
            dt.Tax = val
        dt.save()
    if dt.Tax == 'TaxFree' or dt.Tax =='':
        dt.TotalAmount = dt.Amount
    else:
        ta = float(dt.Amount) * float(dt.Tax) / 100
        ta = float(dt.Amount) + ta
        dt.TotalAmount =str("%.2f" % ta)

    dt.save()
    get = ChargesListModel.objects.filter(ProductId=dt.ProductId,user=request.user.username,type=type).values()
    Sc = list(get)
    rt= 0
    for i in get:
        rt += float(i['TotalAmount'])
    rt = str("%.2f" % rt)
    rt = str(rt)
    return JsonResponse({'Sc':Sc,'rt':rt})


@login_required(login_url='Login')
@csrf_exempt
def ChargesDelete(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        type = request.POST.get('type')
        data= ChargesListModel.objects.get(id=id,type=type)
        data.delete()
        val= NMModel.objects.get(user=request.user,type=type)
        get = ChargesListModel.objects.filter(ProductId=val.ProductId,user=request.user,type=type).values()
        tamonut = 0
        for i in get:
            tamonut+=float(i['TotalAmount'])
        PT = "%.2f" % tamonut
        tamonut= str(PT)
        return JsonResponse({'status':1,'tamonut':tamonut})
    else:
        return JsonResponse({'status':0})
    
# error pages
def error_404_view(request,exception):
    return redirect("/")

@login_required(login_url='Login')
def AllDelete(request):
    # data=ChargesListModel.objects.all()
    # data.delete()
    # data2=CategoryModel.objects.all()
    # data2.delete()
    # data4=DeliveryBoyModel.objects.all()
    # data4.delete()
    # data1=ProductModel.objects.all()
    # data1.delete()
    # data5=StockModel.objects.all()
    # data5.delete()
    # data6=NMModel.objects.all()
    # data6.delete()
    # data7=PurchaseEntryModel.objects.all()
    # data7.delete()
    # data8=SalesEntryModel.objects.all()
    # data8.delete()
    # data0=MainStockModel.objects.all()
    # data0.delete()
    # dt=SalesStockModel.objects.all()
    # dt.delete()
    # datad=NMModel.objects.get(user=request.user)
    # datad.ProductId='1'
    # datad.save()
    # user = str(request.user.username)
    # BN = BiilNoModel.objects.get(user=user,type='Purchase')
    # BN.BillNo =str(int(BN.BillNo)+1)
    # BN.save()
    return redirect('/')

@login_required(login_url='Login')
def StockReport(request):
    stock = MainStockModel.objects.filter(user=request.user.username)
    Productname = {i.ProductName for i in stock}
    data = {'stock':Productname}
    if is_admin(request.user):
        return render(request,'admin/stock.html',data)
    if is_user(request.user):
        return render(request,'stock.html',data)
    
@login_required(login_url='Login')
def ProductsDetails(request,name):
    stock = MainStockModel.objects.filter(user=request.user,ProductName=name)
    Quantity = 0
    Amount = 0
    for i in stock:
        Quantity += float(i.Quantity)
        Amount += float(i.Amount)
    Quantity = Quantity
    Amount = Amount
    data = {'stock':stock,'Quantity':Quantity,'Amount':Amount}
    if is_admin(request.user):
        return render(request,'admin/productsdetails.html',data)
    if is_user(request.user):
        return render(request,'productsdetails.html',data)

@login_required(login_url='Login')
def InvoiceNoDetails(request,IN,type):
    data=SalesEntryModel.objects.filter(InvoiceNo=IN,Type=type).values()
    dt = list(data)
    if dt == []:
        mgs='No matching records found'
        Sc=''
    else:
        Sc= dt
        mgs=''
    return JsonResponse({'Sc':Sc,'mgs':mgs})
    
@login_required(login_url='Login')
def SalesStockReport(request):
    # stock = SalesEntryModel.objects.filter(user=request.user.username,Type='Sales')
    ss=SalesStockModel.objects.filter(user=request.user.username)
    Productname = {i.ProductName for i in ss}
    data = {'stock':Productname}
    if is_admin(request.user):
        return render(request,'admin/salesstock.html',data)
    if is_user(request.user):
        return render(request,'stock.html',data)