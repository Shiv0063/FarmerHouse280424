from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User,Group
from django.http import HttpResponse,JsonResponse
from .models import PartyModel,CategoryModel,DeliveryBoyModel,ProductModel,UserDetails,ExpanseModel,NMModel,BiilNoModel,StockModel,PurchaseEntryModel,MainStockModel
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
    return render(request,'addparty.html')

@login_required(login_url='Login')
def PartyDetails(request,id):
    data=PartyModel.objects.get(id=id)
    return render(request,'admin/partydetails.html',{'data':data})

@login_required(login_url='Login')
def EditParty(request,id):
    data=PartyModel.objects.get(id=id)
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
        dt=ProductModel.objects.create(user=user,ProductName=ProductName,Tax=Tax,Category=Category,Unit=Unit,MinQty=MinQty,MaxQty=MaxQty,BarcodeNo=BarcodeNo,HSNCode=HSNCode,MRP=MRP)
        dt.save()
        messages.success(request,'Product Add Successfully.')
        return redirect('/AddProduct')
    return render(request,'addproduct.html',data)

@login_required(login_url='Login')
def EditProduct(request,id):
    if is_admin(request.user):
        Category = CategoryModel.objects.filter(user=request.user)
        data=ProductModel.objects.get(id=id)
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
    return render(request,'addcategory.html')

@login_required(login_url='Login')
def EditCategory(request,id):
    if is_admin(request.user):
        data=CategoryModel.objects.get(id=id)
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
            messages.success(request,'Edit Delivery Boy Successfully.')
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
        Amount=request.POST.get('Amount')
        dt=ExpanseModel.objects.create(user=user,Expanse=Expanse,Amount=Amount)
        dt.save()
        messages.success(request,'Add Expanse Successfully.')
        return redirect('/AddExpanse')
    return render(request,'addexpanse.html')

@login_required(login_url='Login')
def EditExpanse(request,id):
    if is_admin(request.user):
        data=ExpanseModel.objects.get(id=id)
        return render(request,'admin/editexpanse.html',{'data':data})
    return redirect('/')

@login_required(login_url='Login')
def DeleteExpanse(request,id):
    if is_admin(request.user):
        data=ExpanseModel.objects.get(id=id)
        data.delete()
        messages.success(request,'Delete Category Successfully.')
        return redirect('/Expanse')
    return redirect('/')

@login_required(login_url='Login')
def PurchaseEntry(request):
    if is_admin(request.user):
        # Purchase = PurchaseEntryModel.objects.filter(Type='Purchase')
        # data = {'Purchase':Purchase}
        return render(request,'admin/purchaseentry.html')
    if is_user(request.user):
        return render(request,'purchaseentry.html')

@login_required(login_url='Login')
def Purchase(request):
    if is_admin(request.user):
        purchase = PurchaseEntryModel.objects.filter(user=request.user)
        data = {'purchase':purchase}
        return render(request,'admin/purchase.html',data)
    if is_user(request.user):
        return render(request,'purchase.html')

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
    tamonut = 0
    for i in stock:
        tamonut+=float(i.Amount)
    tamonut= str(tamonut)
    data={'Category':Category,'Product':Product,'ProductId':ProductId,'BiilNo':BiilNo,'Party':Party,'type':type,'stock':stock,'tamonut':tamonut}
    if request.method=="POST":    
        user=str(request.user.username)
        TypeofPurchase=request.POST.get('TypeofPurchase')
        Bill=request.POST.get('BillNo')
        InvoiceNo=request.POST.get('InvoiceNo')
        TypeofPayment=request.POST.get('TypeofPayment')
        PartyName=request.POST.get('PartyName')
        ProductId=request.POST.get('ProductId')
        Type='Purchase'
        Amount=request.POST.get('Amount')
        dt=PurchaseEntryModel.objects.create(user=user,TypeofPurchase=TypeofPurchase,BillNo=Bill,InvoiceNo=InvoiceNo,TypeofPayment=TypeofPayment,PartyName=PartyName,ProductId=ProductId,Type=Type,Amount=Amount)
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
    return render(request,'addpurchaseentry.html',data)
    # return render(request,'addpurchaseentry.html')

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
    tamonut= str(tamonut)
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
        PurchasePrice = int(dt.PurchasePrice)
    if PurchasePrice == 0:
        dt.PurchaseIncTax = '0'
    else:
        PT = 1 * PurchasePrice * int(dt.Tax) / 100  + PurchasePrice
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
            pp = PurchasePrice
        PT = 1 * pp * int(dt.Tax) / 100  + PurchasePrice
        dt.Amount = str(Quantity * PT ) 
    dt.save()
    get = StockModel.objects.filter(ProductId=dt.ProductId,user=request.user.username,type=type).values()
    Sc = list(get)
    return JsonResponse({'Sc':Sc})

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
def SalesEntry(request):
    if is_admin(request.user):
        # sales = SalesEntryModel.objects.filter(Type='Sales')
        # data = {'sales':sales}
        return render(request,'admin/salesentry.html')
    if is_user(request.user):
        return render(request,'salesentry.html')

@login_required(login_url='Login')
def Sales(request):
    if is_admin(request.user):
        # sales = SalesEntryModel.objects.filter(Type='Sales')
        # data = {'sales':sales}
        return render(request,'admin/sales.html')
    if is_user(request.user):
        return render(request,'sales.html')
    
@login_required(login_url='Login')
def AddSalesEntry(request):
    # try:
    #     user=str(request.user.username)
    #     type = 'Sales'
    #     cp = NMModel.objects.get(user=user,type=type)
    #     ProductId = cp.ProductId
    # except NMModel.DoesNotExist:
    #     user = request.user.username
    #     ProductId = '1'
    #     type = 'Sales'
    #     nm=NMModel.objects.create(ProductId=ProductId,user=user,type=type)
    #     nm.save()
    #     cp = NMModel.objects.get(user=user,type=type)
    #     ProductId = cp.ProductId
    # stock = StockModel.objects.filter(ProductId=ProductId,user=user,type=type)
    # Category=CategoryModel.objects.filter(user=request.user)
    # stokes=MainStockModel.objects.filter(user=request.user)
    # Product = ProductModel.objects.filter(user=request.user)
    # Party = PartyModel.objects.filter(user=request.user)
    # DB =  DeliveryBoyModel.objects.filter(user=request.user)
    # tamonut = 0
    # for i in stock:
    #     tamonut += float(i.Amount)
    # data={'Category':Category,'Product':Product,'ProductId':ProductId,'Party':Party,'stokes':stokes,'type':type,'stock':stock,'tamonut':tamonut,'DB':DB}
    # if request.method=="POST":    
    #     user=str(request.user)
    #     DeliveryBoyName=request.POST.get('DeliveryBoyName')
    #     TypeOfBusiness=request.POST.get('TypeOfBusiness')
    #     DeliveryTime=request.POST.get('DeliveryTime')
    #     InvoiceNo=request.POST.get('InvoiceNo')
    #     PartyName=request.POST.get('PartyName')
    #     ProductId=request.POST.get('ProductId')
    #     Type='Sales'
    #     Amount=tamonut
    #     dt=SalesEntryModel.objects.create(user=user,DeliveryBoyName=DeliveryBoyName,TypeOfBusiness=TypeOfBusiness,InvoiceNo=InvoiceNo,DeliveryTime=DeliveryTime,PartyName=PartyName,ProductId=ProductId,Type=Type,Amount=Amount)
    #     dt.save()
    #     stock = StockModel.objects.filter(ProductId=ProductId,user=user,type=type)
    #     for i in stock:
    #         dt=MainStockModel.objects.get(id=i.sid)
    #         newQuantity = int(dt.Quantity) - int(i.Quantity)
    #         if newQuantity == 0:
    #             dt.delete()
    #         else:
    #             wtAmount = 0
    #             try:
    #                 if int(i.Tax):
    #                     tax = int(dt.MRP) * int(newQuantity) * int(i.Tax) /100 
    #                     wtAmount += int(dt.MRP) * int(newQuantity) + (tax * 2)
    #             except:
    #                 wtAmount += int(dt.MRP) * int(newQuantity)
    #             dt.Quantity = str(newQuantity)
    #             dt.Amount = str(wtAmount)
    #             dt.save()
    #     user=str(request.user)
    #     cp = NMModel.objects.get(user=user,type = 'Sales')
    #     cp.ProductId =str(int(cp.ProductId)+1)
    #     cp.save()
    #     messages.success(request,'Sales Successfully.')
    #     return redirect('/AddSalesEntry')
    return render(request,'addsalesentry.html')

# error pages
def error_404_view(request,exception):
    return redirect("/")

@login_required(login_url='Login')
def AllDelete(request):
    # data=PartyModel.objects.all()
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
    data = {'stock':stock}
    if is_admin(request.user):
        return render(request,'admin/stock.html',data)
    if is_user(request.user):
        return render(request,'stock.html',data)