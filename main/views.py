from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User,Group
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from .models import PartyModel,CategoryModel,DeliveryBoyModel,ProductModel,UserDetails,ExpanseModel,NMModel,BiilNoModel,StockModel,PurchaseEntryModel,EditSalesStockModel,AmountModel,UserAmountModel
from .models import LedgerReportModel,PendingAmountModel,MainStockModel,SalesStockModel,SalesEntryModel,ExpanseListModel,ExpanseEntryModel,ChargesModel,ChargesListModel,InvoiceNoModel
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import Http404
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
                messages.success(request,'UserName Is Allready Register.')
                return redirect('/AddUserAccount')
            if useremail(emailaddress):
                messages.success(request,'Email Is Allready Register.')
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
    data=DeliveryBoyModel.objects.filter(user=request.user)
    if is_admin(request.user):    
        return render(request,'admin/deliveryboy.html',{'data':data})
    if is_user(request.user):
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
    data=DeliveryBoyModel.objects.get(user=request.user,id=pk)
    if is_admin(request.user):    
        return render(request,'admin/deliveryboydetails.html',{'data':data})
    if is_user(request.user):
        return render(request,'deliveryboydetails.html',{'data':data})
    
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
def Amount(request):
    if is_admin(request.user):
        user=User.objects.all()
        try:
            ca=UserAmountModel.objects.get(user=request.user)
            ca = ca.Amount
        except UserAmountModel.DoesNotExist:
            ca = ''
        dt = AmountModel.objects.all()
        data={'user':user,'dt':dt,'ca':ca}
        if request.method=="POST":
            method=request.POST.get('method')
            Username=request.POST.get('Username')
            Amount=request.POST.get('Amount')
            if method == 'AddAmount':
                try:
                    UAM=UserAmountModel.objects.get(user=Username)
                    if UAM:
                        amount = eval(UAM.Amount) + eval(Amount)
                        UAM.Amount = amount
                        UAM.save()
                        UAM=UserAmountModel.objects.get(user=Username)
                        LR=LedgerReportModel.objects.create(user=Username,PartyName='Opneing Balance',Type='',BiilNo='',Debited='0',Cedited=Amount,Balance=UAM.Amount)
                        LR.save()
                except UserAmountModel.DoesNotExist:
                    UAM=UserAmountModel.objects.create(user=Username,Amount=Amount)
                    UAM.save()
                    LR=LedgerReportModel.objects.create(user=Username,PartyName='Opneing Balance',Type='',BiilNo='',Debited='0',Cedited=Amount,Balance=Amount)
                    LR.save()
                Method = 'Cedited'
            else:
                try:
                    UAM=UserAmountModel.objects.get(user=Username)
                    if UAM:
                        if eval(UAM.Amount) >= eval(Amount):
                            amount = eval(UAM.Amount) - eval(Amount)
                            UAM.Amount = amount
                            UAM.save()
                            UAM=UserAmountModel.objects.get(user=Username)
                            LR=LedgerReportModel.objects.create(user=Username,PartyName='Closing Balance',Type='',BiilNo='',Debited=Amount,Cedited='0',Balance=UAM.Amount)
                            LR.save()
                        else:
                            messages.success(request,'You Have Not Sufficient Balance.')
                            return redirect('/Amount')
                except UserAmountModel.DoesNotExist:
                    messages.success(request,'You Have Not Sufficient Balance.')
                    return redirect('/Amount')
                Method = 'Debited'
            data = AmountModel.objects.create(user=Username,Amount=Amount,Method=Method)
            data.save()
            return redirect('/Amount')
        return render(request,'admin/amount.html',data)
    if is_user(request.user):
        dt = AmountModel.objects.all()
        return render(request,'expanse.html',{'dt':dt})

@login_required(login_url='Login')
def DAmount(request,id):
    if is_admin(request.user):
        dt = AmountModel.objects.get(id=id)
        dt.delete()
        return redirect('/Amount')

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

def render_to_pdf(template, context):
   template = get_template(template)
   html  = template.render(context)
   result = BytesIO()
   pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
   if not pdf.err:
       return HttpResponse(result.getvalue(), content_type='application/pdf')
   return None

@login_required(login_url='Login')
def PurchaseEntry(request):
    if is_admin(request.user):
        Purchase = PurchaseEntryModel.objects.filter(Type='Purchase',user=request.user)
        sp = {i.PartyName for i in Purchase}
        data = {'Purchase':Purchase,'sp':sp}
        if request.method=="POST": 
            StartDate = request.POST.get('StartDate')
            EndDate = request.POST.get('EndDate')
            PartyName = request.POST.get('PartyName')
            BillNo = request.POST.get('BillNo')
            if (StartDate == '' and EndDate == '') and (PartyName == 'Select' and BillNo == ''):
                Pl = PurchaseEntryModel.objects.filter(Type='Purchase',user=request.user)
            elif (StartDate == '' and EndDate == '') and (PartyName == 'Select' and BillNo != ''):
                Pl = PurchaseEntryModel.objects.filter(Type='Purchase',user=request.user,BillNo=BillNo)
            elif (StartDate == '' and EndDate == '') and (PartyName != 'Select' and BillNo == ''):
                Pl = PurchaseEntryModel.objects.filter(Type='Purchase',user=request.user,PartyName=PartyName)
            elif (StartDate != '' and EndDate != '') and (PartyName != 'Select' and BillNo == ''):
                Pl = PurchaseEntryModel.objects.filter(Type='Purchase',user=request.user,PartyName=PartyName,Date__range=[StartDate, EndDate])
            elif (StartDate != '' and EndDate != '') and (PartyName == 'Select' and BillNo == ''):
                Pl = PurchaseEntryModel.objects.filter(Type='Purchase',user=request.user,Date__range=[StartDate, EndDate])
            elif StartDate != '' and EndDate == '':
                if PartyName != 'Select':
                    Pl = PurchaseEntryModel.objects.filter(Type='Purchase',user=request.user,Date=StartDate,PartyName=PartyName)
                elif PartyName == 'Select':
                    Pl = PurchaseEntryModel.objects.filter(Type='Purchase',user=request.user,Date=StartDate,BillNo=BillNo)
                elif BillNo != '':
                    Pl = PurchaseEntryModel.objects.filter(Type='Purchase',user=request.user,Date=StartDate,BillNo=BillNo)
                elif BillNo == '':
                    Pl = PurchaseEntryModel.objects.filter(Type='Purchase',user=request.user,Date=StartDate)
                # Pl = PurchaseEntryModel.objects.filter(Type='Purchase',user=request.user,Date__range=[StartDate, EndDate])
            else:
                Pl = PurchaseEntryModel.objects.filter(Type='Purchase',user=request.user)
            sp = {i.PartyName for i in Purchase}
            data = {'Purchase':Pl,'sp':sp,'StartDate':StartDate,'EndDate':EndDate,'PartyName':PartyName,'BillNo':BillNo}
            return render(request,'admin/purchaseentry.html',data)
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
        Terms=request.POST.get('Terms')
        PartyName=request.POST.get('PartyName')
        ProductId=request.POST.get('ProductId')
        DueDate=request.POST.get('DueDate')
        Date=request.POST.get('Date')
        PayableAmount=request.POST.get('PayableAmount')
        Type='Purchase'
        Amount=request.POST.get('Amount')
        stock=StockModel.objects.filter(ProductId=ProductId,user=request.user)
        tamonut= 0
        quantity = 0
        purchaseprice = 0
        purchaseinctax = 0
        for i in stock:
            tamonut+=float(i.Amount)
            quantity+=float(i.Quantity)
            purchaseprice+=float(i.PurchasePrice)
            purchaseinctax+=float(i.PurchaseIncTax)
        tamonut= str(tamonut)
        quantity= str(quantity)
        purchaseprice= str(purchaseprice)
        purchaseinctax= str(purchaseinctax)
        tamonut = str(float(tamonut) + float(TCA))
        UAM=UserAmountModel.objects.get(user=request.user)
        if Terms == 'Debit':
            if eval(UAM.Amount) >= eval(tamonut):
                amount = eval(UAM.Amount) - eval(tamonut)
                UAM.Amount = "%.2f" % amount 
                UAM.save()
                PendingAmount = ''
            else:
                messages.success(request,'You Have Not Sufficient Balance.')
                return redirect('/AddPurchaseEntry')
        else:
            PA = eval(tamonut)- eval(PayableAmount)
            PendingAmount = PA
            amount = eval(UAM.Amount) - eval(PayableAmount)
            UAM.Amount =  "%.2f" % amount
            UAM.save()
        if Terms == 'Debit':
            st = '0'
        else:
            st = '1'
        pt= PartyModel.objects.get(user=request.user,Number=PartyName)
        if pt.Debited == '0':
            pt.Debited = tamonut
            pt.save()
        else:
            pot = eval(pt.Debited) + eval(tamonut)
            pt.Debited = str(pot)
            pt.save()
        PartyName = pt.PartyName
        dt=PurchaseEntryModel.objects.create(user=user,TypeofPurchase=TypeofPurchase,BillNo=Bill,InvoiceNo=InvoiceNo,TypeofPayment=TypeofPayment,Terms=Terms,PartyName=PartyName,ProductId=ProductId,Type=Type,Amount=tamonut,DueDate=DueDate,TQuantity=quantity,TPurchasePrice=purchaseprice,TPurchaseIncTax=purchaseinctax,Date=Date,TChargesAmount=TCA,PayableAmount=PayableAmount,status=st,PendingAmount=PendingAmount)
        dt.save()
        stock = StockModel.objects.filter(ProductId=ProductId,user=user,type=type)
        for i in stock:
            MainS=MainStockModel.objects.create(OldProductId=i.id,ProductId=i.ProductId,user=user,type=type,ProductName=i.ProductName,Category=i.Category,Tax=i.Tax,Unit=i.Unit,PurchasePrice=i.PurchasePrice,PurchaseIncTax=i.PurchaseIncTax,MinQty=i.MinQty,MaxQty=i.MaxQty,BarcodeNo=i.BarcodeNo,Quantity=i.Quantity,Amount=i.Amount)
            MainS.save()
        UAM=UserAmountModel.objects.get(user=request.user)
        LR=LedgerReportModel.objects.create(user=user,PartyName=PartyName,Type='Purchase',BiilNo=Bill,Debited=PayableAmount,Cedited='0',Balance=UAM.Amount)
        LR.save()
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
def SProducts(request,PN,id,type,PId=None):
    prd = ProductModel.objects.get(id=id)
    user = str(request.user.username)
    val= NMModel.objects.get(user=user,type=type)
    if PId == None:
        stockproduct = StockModel.objects.create(ProductId=val.ProductId,user=user,type=type,ProductName=prd.ProductName,Category=prd.Category,Tax=prd.Tax,Unit=prd.Unit,PurchasePrice='0',PurchaseIncTax='0',MinQty=prd.MinQty,MaxQty=prd.MaxQty,BarcodeNo=prd.BarcodeNo,Quantity='0',Amount='0')
        stockproduct.save()
        get = StockModel.objects.filter(ProductId=val.ProductId,user=user,type=type).values()
    else:
        stockproduct = StockModel.objects.create(ProductId=PId,user=user,type=type,ProductName=prd.ProductName,Category=prd.Category,Tax=prd.Tax,Unit=prd.Unit,PurchasePrice='0',PurchaseIncTax='0',MinQty=prd.MinQty,MaxQty=prd.MaxQty,BarcodeNo=prd.BarcodeNo,Quantity='0',Amount='0')
        stockproduct.save()
        get = StockModel.objects.filter(ProductId=PId,user=user,type=type).values()
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
        Quantity = float(dt.Quantity)
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
    return JsonResponse({'Sc':Sc,'tamonut':tamonut,})

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
    data2=ChargesListModel.objects.filter(ProductId=id,user=request.user,type='Purchase')
    data2.delete()
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
        quantity+=float(i.Quantity)
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
def DeletePurchase(request,id):
    dt=PurchaseEntryModel.objects.get(id=id)
    sl=StockModel.objects.filter(ProductId=dt.ProductId)
    msl=MainStockModel.objects.filter(ProductId=dt.ProductId)
    msl.delete()
    sl.delete()
    dt.delete()
    return redirect('/Purchase')

@login_required(login_url='Login')
def EditPurchase(request,id):
    dt=PurchaseEntryModel.objects.get(id=id)
    user = request.user
    stock = StockModel.objects.filter(ProductId=dt.ProductId,user=user,type='Purchase')
    Category=CategoryModel.objects.filter(user=user)
    Product = ProductModel.objects.filter(user=user)
    Party = PartyModel.objects.filter(user=user)
    tamonut = 0
    for i in stock:
        tamonut+=float(i.Amount)
    tamonut= str(tamonut)
    Charges=ChargesModel.objects.filter(user=user.username)
    ChargesList = ChargesListModel.objects.filter(user=user,ProductId=dt.ProductId,type='Purchase')
    TCA = 0
    for i in ChargesList:
        TCA += float(i.TotalAmount)
    TCA = TCA
    data={'Category':Category,'Product':Product,'dt':dt,'TCA':TCA,'ChargesList':ChargesList,'Charges':Charges,'Party':Party,'stock':stock,'tamonut':tamonut}
    dt=PurchaseEntryModel.objects.get(id=id)
    if request.method=="POST":    
        dt.user=str(request.user.username)
        dt.TypeofPurchase=request.POST.get('TypeofPurchase')
        dt.BillNo=request.POST.get('BillNo')
        dt.InvoiceNo=request.POST.get('InvoiceNo')
        dt.TypeofPayment=request.POST.get('TypeofPayment')
        dt.Terms=request.POST.get('Terms')
        dt.PartyName=request.POST.get('PartyName')
        ProductId=request.POST.get('ProductId')
        dt.ProductId = ProductId
        dt.DueDate=request.POST.get('DueDate')
        dt.Date=request.POST.get('Date')
        dt.Type='Purchase'
        stock=StockModel.objects.filter(ProductId=ProductId,user=request.user.username)
        tamonut= 0
        quantity = 0
        purchaseprice = 0
        purchaseinctax = 0
        for i in stock:
            tamonut+=float(i.Amount)
            quantity+=float(i.Quantity)
            purchaseprice+=float(i.PurchasePrice)
            purchaseinctax+=float(i.PurchaseIncTax)
        tamonut= str(tamonut)
        dt.TQuantity= str(quantity)
        dt.TPurchasePrice= str(purchaseprice)
        dt.TPurchaseIncTax= str(purchaseinctax)
        dt.Amount = str(float(tamonut) + float(TCA))
        dt.TChargesAmount=TCA
        dt.save()
        user=request.user.username
        msm=MainStockModel.objects.filter(ProductId=ProductId,user=user,type='Purchase')
        msm.delete()
        stock = StockModel.objects.filter(ProductId=ProductId,user=user,type='Purchase')
        for i in stock:
            MainS=MainStockModel.objects.create(OldProductId=i.id,ProductId=i.ProductId,user=user,type='Purchase',ProductName=i.ProductName,Category=i.Category,Tax=i.Tax,Unit=i.Unit,PurchasePrice=i.PurchasePrice,PurchaseIncTax=i.PurchaseIncTax,MinQty=i.MinQty,MaxQty=i.MaxQty,BarcodeNo=i.BarcodeNo,Quantity=i.Quantity,Amount=i.Amount)
            MainS.save()
        return redirect('/Purchase')
    return render(request,'admin/editpurchaseentry.html',data)

@login_required(login_url='Login')
def SalesEntry(request):
    if is_admin(request.user):
        sales = SalesEntryModel.objects.filter(Type='Sales',user=request.user)
        sp = {i.PartyName for i in sales}
        data = {'sales':sales,'sp':sp}
        if request.method=="POST": 
            StartDate = request.POST.get('StartDate')
            EndDate = request.POST.get('EndDate')
            PartyName = request.POST.get('PartyName')
            if (StartDate != '' and EndDate != '') and (PartyName == 'Select' ):
                ss = SalesEntryModel.objects.filter(Type='Sales',Date__range=[StartDate, EndDate],user=request.user)
            elif (StartDate == '' and EndDate == '') and (PartyName == 'Select'):
                ss = SalesEntryModel.objects.filter(Type='Sales',user=request.user)
            elif StartDate == '' and EndDate == '':
                if PartyName == 'Select':
                    ss = SalesEntryModel.objects.filter(Type='Sales',user=request.user)
                else :  
                    ss = SalesEntryModel.objects.filter(Type='Sales',user=request.user,PartyName=PartyName)
            elif (StartDate != '' and EndDate == '') and (PartyName == 'Select'):
                    ss = SalesEntryModel.objects.filter(Type='Sales',user=request.user,Date=StartDate)
            else:
                ss = SalesEntryModel.objects.filter(Type='Sales',Date__range=[StartDate, EndDate],user=request.user,PartyName=PartyName)
            sp = {i.PartyName for i in sales}
            data = {'sales':ss,'sp':sp,'StartDate':StartDate,'EndDate':EndDate,'PartyName':PartyName}
            return render(request,'admin/salesentry.html',data)
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
def AddSalesEntry(request,A2=None):
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
    stokes=MainStockModel.objects.filter(user=request.user,out='0')
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
        TypeofPayment=request.POST.get('TypeofPayment')
        Terms=request.POST.get('Terms')
        ProductId=request.POST.get('ProductId')
        PayableAmount=request.POST.get('PayableAmount')
        Date=request.POST.get('Date')
        Type='Sales'
        Amount=str(float(tamonut) + float(TCA))
        UAM=UserAmountModel.objects.get(user=request.user)
        if Terms == 'Debit':
            PendingAmount = ''
            amount = eval(UAM.Amount) + eval(Amount)
            UAM.Amount =  "%.2f" % amount 
            UAM.save()
        else:
            PA = eval(Amount)- eval(PayableAmount)
            PendingAmount = PA
            amount = eval(UAM.Amount) + eval(PayableAmount)
            UAM.Amount =  "%.2f" % amount 
            UAM.save()
        pt= PartyModel.objects.get(user=request.user,Number=PartyName)
        if pt.Cedited == '0':
            pt.Cedited = Amount
            pt.save()
        else:
            pot = eval(pt.Cedited) + eval(Amount)
            pt.Cedited = str(pot)
            pt.save()
        if Terms == 'Debit':
            st = '0'
        else:
            st = '1'
        PartyName = pt.PartyName
        dt=SalesEntryModel.objects.create(user=user,DeliveryBoyName=DeliveryBoyName,TypeOfBusiness=TypeOfBusiness,Terms=Terms,TypeofPayment=TypeofPayment,InvoiceNo=InvoiceNo,DeliveryTime=DeliveryTime,PartyName=PartyName,ProductId=ProductId,Type=Type,Amount=Amount,Date=Date,TChargesAmount=TCA,PayableAmount=PayableAmount,status=st,PendingAmount=PendingAmount)
        dt.save()
        UAM=UserAmountModel.objects.get(user=request.user)
        LR=LedgerReportModel.objects.create(user=user,PartyName=PartyName,Type='Sales',BiilNo=InvoiceNo,Debited='0',Cedited=PayableAmount,Balance=UAM.Amount)
        LR.save()
        stock = SalesStockModel.objects.filter(ProductId=ProductId,user=user,type=type)
        wtAmount=0
        for i in stock:
            dt=MainStockModel.objects.get(id=i.sid)
            newQuantity = float(dt.Quantity) - float(i.Quantity)
            if newQuantity == 0:
                dt.Quantity = '0'
                dt.Amount = '0'
                dt.out = '1'
                dt.save()
            else:
                wtAmount += float(dt.PurchaseIncTax) * float(newQuantity)
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
        if A2 != None:
                data = MainStockModel.objects.all()
                context = {'data':data}
                pdf = render_to_pdf('admin/vbill.html',context)
                if pdf:
                    response = HttpResponse(pdf,content_type='application/pdf')
                    filename = "New123.pdf"
                    # content = f"attachment; filename={filename}"
                    content = f"inline; filename={filename}"
                    response['Content-Disposition'] = content
                    return response
                return HttpResponse("Not Found")
        else:
            pass
        messages.success(request,'Sales Successfully.')
        return redirect('/AddSalesEntry')
    if is_admin(request.user):
        return render(request,'admin/addsalesentry.html',data)
    if is_user(request.user):
        return render(request,'addsalesentry.html',data)
    
def StockDetails(request,name):
    Ms = MainStockModel.objects.filter(user=request.user,ProductName=name,out='0').values()
    Ms = list(Ms)
    return JsonResponse({'Ms':Ms})

@login_required(login_url='Login')
@csrf_exempt
def Stockswork(request,PN=None,id=None,id2=None,type=None,PID=None,Barcode=None):
    user = str(request.user.username)
    val= NMModel.objects.get(user=user,type=type)
    if Barcode == None:
        ms = MainStockModel.objects.get(id=id2)
    else:
        ms = MainStockModel.objects.get(BarcodeNo=Barcode)
    PRD = ProductModel.objects.get(BarcodeNo=ms.BarcodeNo)
    type = type
    if PID == None:
        ProductId = val.ProductId
    else:
        ProductId = PID
    TSP = eval(ms.Quantity) * eval(ms.PurchaseIncTax)
    if ms.Tax != 'TaxFree':
        tax = int(ms.Tax)
        ISP = eval(ms.PurchaseIncTax) +(eval(ms.PurchaseIncTax) * tax /100)
        ISP =  "%.2f" % ISP
    else:
        ISP = eval(ms.PurchaseIncTax)
        ISP =  "%.2f" % ISP    
    TSP = eval(ms.Quantity) * eval(ISP)
    TSP =  "%.2f" % TSP
    SalesStock=SalesStockModel.objects.create(ProductId=ProductId,user=user,type=type,ProductName=ms.ProductName,Category=ms.Category,Tax=ms.Tax,Unit=ms.Unit,PurchaseIncTax=ms.PurchaseIncTax,BarcodeNo=ms.BarcodeNo,Quantity=ms.Quantity,Amount=PRD.MRP,sid=ms.id,ProfitMargin='0',BasicSalesPrice=ms.PurchaseIncTax,Discount='0',SalesPriceAfterDiscount=ms.PurchaseIncTax,IncSalesPrice=ISP,TotalSales=str(TSP))
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
    dt=SalesStockModel.objects.get(id=id,type=type)
    if name == 'Quantity':
        if val == '':
            dt.Quantity = '0'
        else:
            mstock = MainStockModel.objects.get(id=dt.sid)
            if mstock.Unit == 'KG':
                if eval(mstock.Quantity) < eval(val):
                    return JsonResponse({'msg':'Stoke is not Avilabel.'})
                else:
                    dt.Quantity = val
                    if dt.ProfitMargin == '' or dt.ProfitMargin == '0':
                        if dt.Tax != 'TaxFree':
                            tax = int(dt.Tax)
                            pass
                        else:
                            dt.IncSalesPrice = eval(dt.PurchaseIncTax)
                            dt.TotalSales = eval(val) * eval(dt.PurchaseIncTax)
                    elif dt.ProfitMargin != '':
                        dt.IncSalesPrice = eval(dt.BasicSalesPrice)
                        dt.TotalSales = eval(val) * eval(dt.BasicSalesPrice)
            else:
                if int(val):
                    if eval(mstock.Quantity) < int(val):
                        return JsonResponse({'msg':'Stoke is not Avilabel.'})
                    else:
                        dt.Quantity = val
                else:
                    return JsonResponse({'msg':'Quantity Value is not Perfact.'})
        dt.save()
    if name == 'ProfitMargin':
        if val != '':
            dt.ProfitMargin = val
            val = eval(val)
            if val == 0: 
                pt = eval(dt.PurchaseIncTax)
            else:
                pt = eval(dt.PurchaseIncTax) + (val * eval(dt.PurchaseIncTax) /100)
            dt.BasicSalesPrice= "%.2f" % pt
            if dt.Discount == '0':
                dt.SalesPriceAfterDiscount = "%.2f" % pt
            else:
                gh =  eval("%.2f" % pt) - (eval("%.2f" % pt) * 3 /100) 
                dt.SalesPriceAfterDiscount = "%.2f" % gh
        else : 
            dt.ProfitMargin = '0'
            pt = eval(dt.PurchaseIncTax)
            dt.BasicSalesPrice= "%.2f" % pt
            if dt.Discount == '0':
                dt.SalesPriceAfterDiscount = "%.2f" % pt
            else:
                gh =  eval("%.2f" % pt) - (eval("%.2f" % pt) * 3 /100) 
                dt.SalesPriceAfterDiscount = "%.2f" % gh
        dt.save()
    if name == 'Discount':
        if val != '':
            dt.Discount = val
            val = eval(val)
            if val == 0:
                dt.SalesPriceAfterDiscount = dt.BasicSalesPrice
            else:
                pt = eval(dt.BasicSalesPrice) - (eval(dt.BasicSalesPrice) * val / 100 )
                dt.SalesPriceAfterDiscount = "%.2f" % pt
            dt.save()
        else:
            dt.Discount = '0'
            if dt.BasicSalesPrice == '0' or dt.BasicSalesPrice == '0':
                dt.SalesPriceAfterDiscount = dt.PurchaseIncTax
            else:
                dt.SalesPriceAfterDiscount = dt.BasicSalesPrice
            dt.save()
    dt=SalesStockModel.objects.get(id=id)
    if dt.Tax != 'TaxFree':
        tax = int(dt.Tax)
        pt = eval(dt.SalesPriceAfterDiscount) + (eval(dt.SalesPriceAfterDiscount) * tax / 100)
        pt = float("%.2f" % pt)
        dt.IncSalesPrice = pt
        pt = pt * eval(dt.Quantity)
        dt.TotalSales = "%.2f" % pt
    else:
        dt.IncSalesPrice = dt.SalesPriceAfterDiscount
        pt = eval(dt.IncSalesPrice) * eval(dt.Quantity)
        dt.TotalSales = "%.2f" % pt
    dt.save()
    get = SalesStockModel.objects.filter(ProductId=dt.ProductId,user=request.user.username,type=type).values()
    Sc = list(get)
    rt= 0
    for i in get:
        rt += float(i['TotalSales'])
    rt = "%.2f" % rt
    return JsonResponse({'Sc':Sc,'rt':rt})

@login_required(login_url='Login')
@csrf_exempt
def ProductE3(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        id = request.POST.get('id')
        val = request.POST.get('val')
        type = request.POST.get('type')
    dt=SalesStockModel.objects.get(id=id,type=type)
    if name == 'Quantity':
        if val == '':
            dt.Quantity = '0'
        else:
            mstock = MainStockModel.objects.get(id=dt.sid)
            ESS = EditSalesStockModel.objects.get(ProductId=dt.ProductId)
            Qtt = eval(mstock.Quantity) + eval(ESS.Quantity)
            if mstock.Unit == 'KG':
                if Qtt < eval(val):
                    return JsonResponse({'msg':'Stoke is not Avilabel.'})
                else:
                    dt.Quantity = val
                    if dt.ProfitMargin == '' or dt.ProfitMargin == '0':
                        if dt.Tax != 'TaxFree':
                            tax = int(dt.Tax)
                            pass
                        else:
                            dt.IncSalesPrice = eval(dt.PurchaseIncTax)
                            dt.TotalSales = eval(val) * eval(dt.PurchaseIncTax)
                    elif dt.ProfitMargin != '':
                        dt.IncSalesPrice = eval(dt.BasicSalesPrice)
                        dt.TotalSales = eval(val) * eval(dt.BasicSalesPrice)
            else:
                if int(val):
                    if eval(mstock.Quantity) < int(val):
                        return JsonResponse({'msg':'Stoke is not Avilabel.'})
                    else:
                        dt.Quantity = val
                else:
                    return JsonResponse({'msg':'Quantity Value is not Perfact.'})
        dt.save()
    if name == 'ProfitMargin':
        if val != '':
            dt.ProfitMargin = val
            val = eval(val)
            if val == 0: 
                pt = eval(dt.PurchaseIncTax)
            else:
                pt = eval(dt.PurchaseIncTax) + (val * eval(dt.PurchaseIncTax) /100)
            dt.BasicSalesPrice= "%.2f" % pt
            if dt.Discount == '0':
                dt.SalesPriceAfterDiscount = "%.2f" % pt
            else:
                gh =  eval("%.2f" % pt) - (eval("%.2f" % pt) * 3 /100) 
                dt.SalesPriceAfterDiscount = "%.2f" % gh
        else : 
            dt.ProfitMargin = '0'
            pt = eval(dt.PurchaseIncTax)
            dt.BasicSalesPrice= "%.2f" % pt
            if dt.Discount == '0':
                dt.SalesPriceAfterDiscount = "%.2f" % pt
            else:
                gh =  eval("%.2f" % pt) - (eval("%.2f" % pt) * 3 /100) 
                dt.SalesPriceAfterDiscount = "%.2f" % gh
        dt.save()
    if name == 'Discount':
        if val != '':
            dt.Discount = val
            val = eval(val)
            if val == 0:
                dt.SalesPriceAfterDiscount = dt.BasicSalesPrice
            else:
                pt = eval(dt.BasicSalesPrice) - (eval(dt.BasicSalesPrice) * val / 100 )
                dt.SalesPriceAfterDiscount = "%.2f" % pt
            dt.save()
        else:
            dt.Discount = '0'
            if dt.BasicSalesPrice == '0' or dt.BasicSalesPrice == '0':
                dt.SalesPriceAfterDiscount = dt.PurchaseIncTax
            else:
                dt.SalesPriceAfterDiscount = dt.BasicSalesPrice
            dt.save()
    dt=SalesStockModel.objects.get(id=id)
    if dt.Tax != 'TaxFree':
        tax = int(dt.Tax)
        pt = eval(dt.SalesPriceAfterDiscount) + (eval(dt.SalesPriceAfterDiscount) * tax / 100)
        pt = float("%.2f" % pt)
        dt.IncSalesPrice = pt
        pt = pt * eval(dt.Quantity)
        dt.TotalSales = "%.2f" % pt
    else:
        dt.IncSalesPrice = dt.SalesPriceAfterDiscount
        pt = eval(dt.IncSalesPrice) * eval(dt.Quantity)
        dt.TotalSales = "%.2f" % pt
    dt.save()
    get = SalesStockModel.objects.filter(ProductId=dt.ProductId,user=request.user.username,type=type).values()
    Sc = list(get)
    rt= 0
    for i in get:
        rt += float(i['TotalSales'])
    rt = "%.2f" % rt
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
        quantity+=float(i.Quantity)
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
    dt = ChargesListModel.objects.filter(ProductId=id,user=request.user,type='Sales')
    dt.delete()
    return redirect('/Sales')

@login_required(login_url='Login')
def DeleteSales(request,id):
    dt=SalesEntryModel.objects.get(id=id)
    sl=SalesStockModel.objects.filter(ProductId=dt.ProductId)
    for i in sl:
        msl=MainStockModel.objects.get(id=i.sid)
        msl.Quantity =float(msl.Quantity) + float(i.Quantity)
        msl.Amount = float(msl.PurchaseIncTax) * float(msl.Quantity)
        msl.out = '0'
        msl.save()
    sl.delete()
    dt.delete()
    return redirect('/Sales')

@login_required(login_url='Login')
def EditSales(request,id):
    user=str(request.user.username)
    type = 'Sales'
    dt = SalesEntryModel.objects.get(id=id)
    ProductId = dt.ProductId
    Invoice = dt.InvoiceNo
    SRtoESR(user,ProductId,type)
    stock = SalesStockModel.objects.filter(ProductId=ProductId,user=user,type=type)
    Category=CategoryModel.objects.filter(user=request.user)
    stokes=MainStockModel.objects.filter(user=request.user)
    Charges=ChargesModel.objects.filter(user=request.user.username)
    ChargesList = ChargesListModel.objects.filter(user=request.user,ProductId=ProductId,type='Sales')
    TCA = 0
    for i in ChargesList:
        TCA += float(i.TotalAmount)
    TCA = "%.2f" % TCA
    productns={i.ProductName for i in stokes}
    Product = ProductModel.objects.filter(user=request.user)
    Party = PartyModel.objects.filter(user=request.user)
    DB =  DeliveryBoyModel.objects.filter(user=request.user)
    tamonut = 0
    for i in stock:
        tamonut += eval(i.TotalSales)
    tamonut = "%.2f" % tamonut
    data={'Category':Category,'Product':Product,'dt':dt,'ProductId':ProductId,'productns':productns,'Invoice':Invoice,'TCA':TCA,'ChargesList':ChargesList,'Party':Party,'Charges':Charges,'stokes':stokes,'type':type,'stock':stock,'tamonut':tamonut,'DB':DB}
    dt=SalesEntryModel.objects.get(id=id)
    if request.method=="POST":
        dt.DeliveryBoyName=request.POST.get('DeliveryBoyName')
        dt.TypeOfBusiness=request.POST.get('TypeOfBusiness')
        dt.DeliveryTime=request.POST.get('DeliveryTime')
        dt.PartyName=request.POST.get('PartyName')
        dt.TypeofPayment=request.POST.get('TypeofPayment')
        dt.Terms=request.POST.get('Terms')
        dt.Date=request.POST.get('Date')
        stock = SalesStockModel.objects.filter(ProductId=dt.ProductId,user=dt.user,type='Sales')
        tamonut = 0
        for i in stock:
            TS=float(i.TotalSales)
            tamonut += TS
        tamonut = "%.2f" % tamonut
        ChargesList = ChargesListModel.objects.filter(user=request.user,ProductId=dt.ProductId,type='Sales')
        TCA = 0
        for i in ChargesList:
            TCA += float(i.TotalAmount)
        TCA = "%.2f" % TCA
        ta = eval(tamonut) + eval(TCA)
        dt.Amount= str(ta)
        dt.TChargesAmount = TCA
        dt.save()
        messages.success(request,'Edit Sales Successfully.')
        return redirect('/Sales')
    return render(request,'admin/editsalesentry.html',data)

@login_required(login_url='Login')
def PurchaseReturnEntry(request):
    if is_admin(request.user):
        Purchase = PurchaseEntryModel.objects.filter(Type='PurchaseReturn',user=request.user)
        sp = {i.PartyName for i in Purchase}
        data = {'Purchase':Purchase,'sp':sp}
        if request.method=="POST": 
            StartDate = request.POST.get('StartDate')
            EndDate = request.POST.get('EndDate')
            PartyName = request.POST.get('PartyName')
            BillNo = request.POST.get('BillNo')
            if (StartDate == '' and EndDate == '') and (PartyName == 'Select' and BillNo == ''):
                Pl = PurchaseEntryModel.objects.filter(Type='PurchaseReturn',user=request.user)
            elif (StartDate == '' and EndDate == '') and (PartyName == 'Select' and BillNo != ''):
                Pl = PurchaseEntryModel.objects.filter(Type='PurchaseReturn',user=request.user,BillNo=BillNo)
            elif (StartDate == '' and EndDate == '') and (PartyName != 'Select' and BillNo == ''):
                Pl = PurchaseEntryModel.objects.filter(Type='PurchaseReturn',user=request.user,PartyName=PartyName)
            elif (StartDate != '' and EndDate != '') and (PartyName != 'Select' and BillNo == ''):
                Pl = PurchaseEntryModel.objects.filter(Type='PurchaseReturn',user=request.user,PartyName=PartyName,Date__range=[StartDate, EndDate])
            elif (StartDate != '' and EndDate != '') and (PartyName == 'Select' and BillNo == ''):
                Pl = PurchaseEntryModel.objects.filter(Type='PurchaseReturn',user=request.user,Date__range=[StartDate, EndDate])
            elif StartDate != '' and EndDate == '':
                if PartyName != 'Select':
                    Pl = PurchaseEntryModel.objects.filter(Type='PurchaseReturn',user=request.user,Date=StartDate,PartyName=PartyName)
                elif PartyName == 'Select':
                    Pl = PurchaseEntryModel.objects.filter(Type='PurchaseReturn',user=request.user,Date=StartDate,BillNo=BillNo)
                elif BillNo != '':
                    Pl = PurchaseEntryModel.objects.filter(Type='PurchaseReturn',user=request.user,Date=StartDate,BillNo=BillNo)
                elif BillNo == '':
                    Pl = PurchaseEntryModel.objects.filter(Type='PurchaseReturn',user=request.user,Date=StartDate)
                # Pl = PurchaseEntryModel.objects.filter(Type='PurchaseReturn',user=request.user,Date__range=[StartDate, EndDate])
            else:
                Pl = PurchaseEntryModel.objects.filter(Type='PurchaseReturn',user=request.user)
            sp = {i.PartyName for i in Purchase}
            data = {'Purchase':Pl,'sp':sp,'StartDate':StartDate,'EndDate':EndDate,'PartyName':PartyName,'BillNo':BillNo}
            return render(request,'admin/purchasereturnentry.html',data)
        return render(request,'admin/purchasereturnentry.html',data)
    if is_user(request.user):
        return render(request,'purchasereturnentry.html')

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
        Terms=request.POST.get('Terms')
        DueDate=request.POST.get('DueDate')
        Date=request.POST.get('Date')
        PayableAmount=request.POST.get('PayableAmount')
        Type='PurchaseReturn'
        Amount=request.POST.get('Amount')
        stock=StockModel.objects.filter(ProductId=ProductId,user=request.user,type='PurchaseReturn')
        tamonut= 0
        quantity = 0
        purchaseprice = 0
        purchaseinctax = 0
        for i in stock:
            tamonut+=float(i.Amount)
            quantity+=float(i.Quantity)
            purchaseprice+=float(i.PurchasePrice)
            purchaseinctax+=float(i.PurchaseIncTax)
        tamonut= str(tamonut)
        quantity= str(quantity)
        purchaseprice= str(purchaseprice)
        purchaseinctax= str(purchaseinctax)
        UAM=UserAmountModel.objects.get(user=request.user)
        if Terms == 'Debit':
            PendingAmount = ''
            amount = eval(UAM.Amount) + eval(tamonut)
            UAM.Amount =  "%.2f" % amount 
            UAM.save()
        else:
            PA = eval(tamonut) - eval(PayableAmount)
            PendingAmount = PA
            amount = eval(UAM.Amount) + eval(PayableAmount)
            UAM.Amount =  "%.2f" % amount 
            UAM.save()
        pt= PartyModel.objects.get(user=request.user,Number=PartyName)
        if pt.Cedited == '0':
            pt.Cedited = Amount
            pt.save()
        else:
            pot = eval(pt.Cedited) + eval(Amount)
            pt.Cedited = str(pot)
            pt.save()
        if Terms == 'Debit':
            st = '0'
        else:
            st = '1'
        PartyName = pt.PartyName
        dt=PurchaseEntryModel.objects.create(user=user,TypeofPurchase=TypeofPurchase,BillNo=Bill,InvoiceNo=InvoiceNo,TypeofPayment=TypeofPayment,PartyName=PartyName,ProductId=ProductId,Type=Type,Amount=tamonut,DueDate=DueDate,TQuantity=quantity,TPurchasePrice=purchaseprice,TPurchaseIncTax=purchaseinctax,Date=Date,PayableAmount=PayableAmount,status=st,PendingAmount=PendingAmount)
        dt.save()
        UAM=UserAmountModel.objects.get(user=request.user)
        LR=LedgerReportModel.objects.create(user=user,PartyName=PartyName,Type='PurchaseReturn',BiilNo=InvoiceNo,Debited='0',Cedited=PayableAmount,Balance=UAM.Amount)
        LR.save()
        stock = StockModel.objects.filter(ProductId=ProductId,user=user,type=type)
        for i in stock:
            dt=MainStockModel.objects.get(id=i.sid)
            newQuantity = float(dt.Quantity) - float(i.Quantity)
            if newQuantity == 0:
                dt.delete()
            else:
                wtAmount = float(dt.PurchaseIncTax) * float(newQuantity)
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
        quantity+=float(i.Quantity)
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
def SalesReturnEntry(request):
    if is_admin(request.user):
        sales = SalesEntryModel.objects.filter(Type='SalesReturn',user=request.user)
        sp = {i.PartyName for i in sales}
        data = {'sales':sales,'sp':sp}
        if request.method=="POST":
            StartDate = request.POST.get('StartDate')
            EndDate = request.POST.get('EndDate')
            PartyName = request.POST.get('PartyName')
            if (StartDate != '' and EndDate != '') and (PartyName == 'Select' ):
                ss = SalesEntryModel.objects.filter(Type='SalesReturn',Date__range=[StartDate, EndDate],user=request.user)
            elif (StartDate == '' and EndDate == '') and (PartyName == 'Select'):
                ss = SalesEntryModel.objects.filter(Type='SalesReturn',user=request.user)
            elif StartDate == '' and EndDate == '':
                if PartyName == 'Select':
                    ss = SalesEntryModel.objects.filter(Type='SalesReturn',user=request.user)
                else :  
                    ss = SalesEntryModel.objects.filter(Type='SalesReturn',user=request.user,PartyName=PartyName)
            elif (StartDate != '' and EndDate == '') and (PartyName == 'Select'):
                    ss = SalesEntryModel.objects.filter(Type='SalesReturn',user=request.user,Date=StartDate)
            else:
                ss = SalesEntryModel.objects.filter(Type='SalesReturn',Date__range=[StartDate, EndDate],user=request.user,PartyName=PartyName)
            sp = {i.PartyName for i in sales}
            data = {'sales':ss,'sp':sp,'StartDate':StartDate,'EndDate':EndDate,'PartyName':PartyName}
            return render(request,'admin/salesreturnentry.html',data)
        return render(request,'admin/salesreturnentry.html',data)
    if is_user(request.user):
        return render(request,'salesreturnentry.html')

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
    data={'Category':Category,'Product':Product,'ProductId':ProductId,'productns':productns,'Invoice':Invoice,'Party':Party,'stokes':stokes,'type':type,'stock':stock,'tamonut':tamonut,'DB':DB}
    if request.method=="POST":    
        user=str(request.user)
        DeliveryBoyName=request.POST.get('DeliveryBoyName')
        TypeOfBusiness=request.POST.get('TypeOfBusiness')
        DeliveryTime=request.POST.get('DeliveryTime')
        InvoiceNo=Invoice
        PartyName=request.POST.get('PartyName')
        ProductId=request.POST.get('ProductId')
        TypeofPayment=request.POST.get('TypeofPayment')
        PayableAmount=request.POST.get('PayableAmount')
        Terms=request.POST.get('Terms')
        Date=request.POST.get('Date')
        Type='SalesReturn'
        Amount=tamonut
        UAM=UserAmountModel.objects.get(user=request.user)
        if Terms == 'Debit':
            if eval(UAM.Amount) >= float(Amount):
                PendingAmount = ''
                amount = eval(UAM.Amount) - float(Amount)
                UAM.Amount = "%.2f" % amount 
                UAM.save()
            else:
                messages.success(request,'You Have Not Sufficient Balance.')
                return redirect('/AddSalesReturnEntry')
        else:
            PA = float(Amount)- eval(PayableAmount)
            PendingAmount = "%.2f" % PA
            amount = eval(UAM.Amount) - eval(PayableAmount)
            UAM.Amount =  "%.2f" % amount 
            UAM.save()
        pt= PartyModel.objects.get(user=request.user,Number=PartyName)
        if pt.Debited == '0':
            pt.Debited = Amount
            pt.save()
        else:
            pot = eval(pt.Debited) + float(Amount)
            pt.Debited = str(pot)
            pt.save()
        if Terms == 'Debit':
            st = '0'
        else:
            st = '1'
        PartyName = pt.PartyName
        dt=SalesEntryModel.objects.create(user=user,DeliveryBoyName=DeliveryBoyName,TypeOfBusiness=TypeOfBusiness,Terms=Terms,TypeofPayment=TypeofPayment,InvoiceNo=InvoiceNo,DeliveryTime=DeliveryTime,PartyName=PartyName,ProductId=ProductId,Type=Type,Amount=Amount,Date=Date,PayableAmount=PayableAmount,status=st,PendingAmount=PendingAmount)
        dt.save()
        LR=LedgerReportModel.objects.create(user=user,PartyName=PartyName,Type='SalesReturn',BiilNo=InvoiceNo,Debited=PayableAmount,Cedited='0',Balance=UAM.Amount)
        LR.save()
        stock = SalesStockModel.objects.filter(ProductId=ProductId,user=user,type=type)
        for i in stock:
            MainS=MainStockModel.objects.create(OldProductId='0',ProductId=i.ProductId,user=user,type=type,ProductName=i.ProductName,Category=i.Category,Tax=i.Tax,Unit=i.Unit,PurchasePrice=i.PurchaseIncTax,PurchaseIncTax=i.PurchaseIncTax,MinQty='0',MaxQty='0',BarcodeNo=i.BarcodeNo,Quantity=i.Quantity,Amount=i.TotalSales)
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
def SRStocks(request,PN,id,type,PD=None):
    user = str(request.user.username)
    val= NMModel.objects.get(user=user,type=type)
    type = type
    pd = ProductModel.objects.get(id=id)
    if PD == None:
        ProductId = val.ProductId
    else:
        ProductId = PD
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
    if name == 'Quantity':
        if val == '':
            dt.Quantity = '0'
        else:
            dt.Quantity = val
        dt.save()
    if name == 'PurchaseIncTax':
        if val == '':
            dt.PurchaseIncTax = '0'
        else:
            dt.PurchaseIncTax = val
        dt.save()
    if name == 'ProfitMargin':
        if val != '':
            dt.ProfitMargin = val
            val = eval(val)
            if val == 0: 
                pt = eval(dt.PurchaseIncTax)
            else:
                pt = eval(dt.PurchaseIncTax) + (val * eval(dt.PurchaseIncTax) /100)
            dt.BasicSalesPrice= "%.2f" % pt
            if dt.Discount == '0':
                dt.SalesPriceAfterDiscount = "%.2f" % pt
            else:
                gh =  eval("%.2f" % pt) - (eval("%.2f" % pt) * 3 /100) 
                dt.SalesPriceAfterDiscount = "%.2f" % gh
        else : 
            dt.ProfitMargin = '0'
            pt = eval(dt.PurchaseIncTax)
            dt.BasicSalesPrice= "%.2f" % pt
            if dt.Discount == '0':
                dt.SalesPriceAfterDiscount = "%.2f" % pt
            else:
                gh =  eval("%.2f" % pt) - (eval("%.2f" % pt) * 3 /100) 
                dt.SalesPriceAfterDiscount = "%.2f" % gh
        dt.save()
    if name == 'Discount':
        if val != '':
            dt.Discount = val
            val = eval(val)
            if val == 0:
                dt.SalesPriceAfterDiscount = dt.BasicSalesPrice
            else:
                pt = eval(dt.BasicSalesPrice) - (eval(dt.BasicSalesPrice) * val / 100 )
                dt.SalesPriceAfterDiscount = "%.2f" % pt
            dt.save()
        else:
            dt.Discount = '0'
            if dt.BasicSalesPrice == '0' or dt.BasicSalesPrice == '0':
                dt.SalesPriceAfterDiscount = dt.PurchaseIncTax
            else:
                dt.SalesPriceAfterDiscount = dt.BasicSalesPrice
            dt.save()
    dt=SalesStockModel.objects.get(id=id)
    if dt.Tax != 'TaxFree':
        tax = int(dt.Tax)
        pt = eval(dt.SalesPriceAfterDiscount) + (eval(dt.SalesPriceAfterDiscount) * tax / 100)
        pt = float("%.2f" % pt)
        dt.IncSalesPrice = pt
        pt = pt * eval(dt.Quantity)
        dt.TotalSales = "%.2f" % pt
    else:
        dt.IncSalesPrice = dt.SalesPriceAfterDiscount
        pt = eval(dt.IncSalesPrice) * eval(dt.Quantity)
        dt.TotalSales = "%.2f" % pt
    dt.save()
    get = SalesStockModel.objects.filter(ProductId=dt.ProductId,user=request.user.username,type=type).values()
    Sc = list(get)
    rt= 0
    for i in get:
        rt += float(i['TotalSales'])
    rt = "%.2f" % rt
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
        quantity+=float(i.Quantity)
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
def DeleteSR(request,id):
    data=SalesEntryModel.objects.get(id=id)
    data.delete()
    return redirect('/SalesReturn')

def SRtoESR(user,ProductId,type):
    stock = SalesStockModel.objects.filter(ProductId=ProductId,user=user,type=type)
    try:
        dt=EditSalesStockModel.objects.filter(ProductId=ProductId,user=user,type=type)
        if dt:
            pass
        else:
            for i in stock:
                ESR = EditSalesStockModel.objects.create(ProductId=i.ProductId,user=i.user,type=i.type,ProductName=i.ProductName,Category=i.Category,Tax=i.Tax,Unit=i.Unit,PurchaseIncTax=i.PurchaseIncTax,BarcodeNo=i.BarcodeNo,Quantity=i.Quantity,Amount=i.Amount,ProfitMargin=i.ProfitMargin,BasicSalesPrice=i.BasicSalesPrice,Discount=i.Discount,SalesPriceAfterDiscount=i.SalesPriceAfterDiscount,IncSalesPrice=i.IncSalesPrice,TotalSales=i.TotalSales)
                ESR.save()
    except:
        for i in stock:
                ESR = EditSalesStockModel.objects.create(ProductId=i.ProductId,user=i.user,type=i.type,ProductName=i.ProductName,Category=i.Category,Tax=i.Tax,Unit=i.Unit,PurchaseIncTax=i.PurchaseIncTax,BarcodeNo=i.BarcodeNo,Quantity=i.Quantity,Amount=i.Amount,ProfitMargin=i.ProfitMargin,BasicSalesPrice=i.BasicSalesPrice,Discount=i.Discount,SalesPriceAfterDiscount=i.SalesPriceAfterDiscount,IncSalesPrice=i.IncSalesPrice,TotalSales=i.TotalSales)
                ESR.save()

@login_required(login_url='Login')
def EditSR(request,id):
    user=str(request.user.username)
    type = 'SalesReturn'
    dt = SalesEntryModel.objects.get(id=id)
    ProductId = dt.ProductId
    Invoice = dt.InvoiceNo
    SRtoESR(user,ProductId,type)
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
    tamonut = str("%.2f" % tamonut )
    data={'Category':Category,'Product':Product,'dt':dt,'ProductId':ProductId,'productns':productns,'Invoice':Invoice,'Party':Party,'stokes':stokes,'type':type,'stock':stock,'tamonut':tamonut,'DB':DB}
    dt = SalesEntryModel.objects.get(id=id)
    if request.method=="POST":    
        dt.DeliveryBoyName=request.POST.get('DeliveryBoyName')
        dt.TypeOfBusiness=request.POST.get('TypeOfBusiness')
        dt.DeliveryTime=request.POST.get('DeliveryTime')
        dt.PartyName=request.POST.get('PartyName')
        dt.ProductId=request.POST.get('ProductId')
        dt.TypeofPayment=request.POST.get('TypeofPayment')
        dt.Terms=request.POST.get('Terms')
        dt.Date=request.POST.get('Date')
        tamonut = 0
        for i in stock:
            tamonut += float(i.TotalSales)
        tamonut = "%.2f" % tamonut
        dt.Amount=str(tamonut)
        dt.save()
        stokes=MainStockModel.objects.filter(user=request.user,ProductId=ProductId,type='SalesReturn')
        stokes.delete()
        stock = SalesStockModel.objects.filter(ProductId=ProductId,user=user,type=type)
        for i in stock:
            MainS=MainStockModel.objects.create(OldProductId='0',ProductId=i.ProductId,user=user,type=type,ProductName=i.ProductName,Category=i.Category,Tax=i.Tax,Unit=i.Unit,PurchasePrice=i.PurchaseIncTax,PurchaseIncTax=i.PurchaseIncTax,MinQty='0',MaxQty='0',BarcodeNo=i.BarcodeNo,Quantity=i.Quantity,Amount=i.TotalSales)
            MainS.save()
        df = EditSalesStockModel.objects.filter(ProductId=ProductId,user=user,type='SalesReturn')
        df.delete()
        messages.success(request,'Edit Sales Return Successfully.')
        return redirect('/SalesReturn')
    if is_admin(request.user):
        return render(request,'admin/editsalesreturnentry.html',data)
    if is_user(request.user):
        return render(request,'editsalesreturnentry.html',data)

@login_required(login_url='Login')
def CancelSR(request,PID):
    ProductId=PID
    type='SalesReturn'
    user=request.user
    stokes=SalesStockModel.objects.filter(user=request.user,ProductId=ProductId,type=type)
    stokes.delete()
    stock = EditSalesStockModel.objects.filter(ProductId=ProductId,user=user,type=type)
    for i in stock:
        MainS=SalesStockModel.objects.create(ProductId=i.ProductId,user=i.user,type=i.type,ProductName=i.ProductName,Category=i.Category,Tax=i.Tax,Unit=i.Unit,PurchaseIncTax=i.PurchaseIncTax,BarcodeNo=i.BarcodeNo,Quantity=i.Quantity,Amount=i.Amount,ProfitMargin=i.ProfitMargin,BasicSalesPrice=i.BasicSalesPrice,Discount=i.Discount,SalesPriceAfterDiscount=i.SalesPriceAfterDiscount,IncSalesPrice=i.IncSalesPrice,TotalSales=i.TotalSales)
        MainS.save()
    df = EditSalesStockModel.objects.filter(ProductId=ProductId,user=user,type='SalesReturn')
    df.delete()
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
        Terms=request.POST.get('Terms')
        PartyName=request.POST.get('PartyName')
        ProductId=request.POST.get('ProductId')
        Date=request.POST.get('Date')
        PayableAmount=request.POST.get('PayableAmount')
        Amount=tamonut
        UAM=UserAmountModel.objects.get(user=request.user)
        if Terms == 'Debit':
            if eval(UAM.Amount) >= eval(Amount):
                amount = eval(UAM.Amount) - eval(Amount)
                UAM.Amount = "%.2f" % amount 
                UAM.save()
            else:
                messages.success(request,'You Have Not Sufficient Balance.')
                return redirect('/AddExpensesEntry')
        else:
            amount = eval(UAM.Amount) - eval(PayableAmount)
            UAM.Amount =  "%.2f" % amount 
            UAM.save()
        pt= PartyModel.objects.get(user=request.user,Number=PartyName)
        if pt.Debited == '0':
            pt.Debited = Amount
            pt.save()
        else:
            pot = eval(pt.Debited) + eval(Amount)
            pt.Debited = str(pot)
            pt.save()
        if Terms == 'Debit':
            st = '0'
        else:
            st = '1'
        PartyName = pt.PartyName
        dt=ExpanseEntryModel.objects.create(user=user,TypeofPayment=TypeofPayment,Terms=Terms,PartyName=PartyName,ProductId=ProductId,Amount=Amount,Date=Date,PayableAmount=PayableAmount,status=st)
        dt.save()
        LR=LedgerReportModel.objects.create(user=user,PartyName=PartyName,Type='Expenses',BiilNo='',Debited=PayableAmount,Cedited='0',Balance=UAM.Amount)
        LR.save()
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
def ExpenseCancel(request,id):
    ProductId=id
    user=request.user
    ELM = ExpanseListModel.objects.filter(ProductId=ProductId,user=user)
    ELM.delete()
    return redirect('/ExpensesEntry')

@login_required(login_url='Login')
@csrf_exempt
def ExpanseList(request,id,pid=None):
    user = str(request.user.username)
    val= NMModel.objects.get(user=user,type='Expenses')
    if pid == None:
        ProductId = val.ProductId
    else:
        ProductId = pid
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
def DeleteEx(request,id):
    data=ExpanseEntryModel.objects.get(id=id)
    ELM=ExpanseListModel.objects.filter(ProductId=data.ProductId,user=request.user)
    ELM.delete()
    data.delete()
    return redirect('/ExpensesEntry')

@login_required(login_url='Login')
def EditEx(request,id):
    data=ExpanseEntryModel.objects.get(id=id)
    user=str(request.user.username)
    type = 'Expenses'
    ProductId = data.ProductId
    Expens = ExpanseModel.objects.filter(user=request.user)
    Party = PartyModel.objects.filter(user=request.user)
    ELM = ExpanseListModel.objects.filter(ProductId=ProductId,user=user)
    tamonut = 0
    for i in ELM:
        tamonut+=float(i.Amount)
    PT = "%.2f" % tamonut
    tamonut = str(PT)
    data={'ProductId':ProductId,'data':data,'Expens':Expens,'Party':Party,'type':type,'ELM':ELM,'tamonut':tamonut}
    dt=ExpanseEntryModel.objects.get(id=id)
    if request.method=="POST":
        dt.TypeofPayment=request.POST.get('TypeofPayment')
        dt.Terms=request.POST.get('Terms')
        dt.PartyName=request.POST.get('PartyName')
        dt.Date=request.POST.get('Date')
        dt.Amount=tamonut
        dt.save()
        messages.success(request,'Edit Expenses Entry Successfully.')
        return redirect('/ExpensesEntry')
    if is_admin(request.user):
        return render(request,'admin/editexpensesentry.html',data)
    if is_user(request.user):
        return render(request,'editexpensesentry.html',data)


@login_required(login_url='Login')
@csrf_exempt
def CreateCharges(request):
    if request.method == 'POST':
        ChargesID = request.POST.get('ChargesID')
        Type = request.POST.get('type')
        Productid = request.POST.get('Productid')
        user = request.user.username
        PN = NMModel.objects.get(type=Type,user=user)
        Ch = ChargesModel.objects.get(id=ChargesID)
        if Productid == None:
            data = ChargesListModel.objects.create(user=user,Charges=Ch.Charges,ProductId=PN.ProductId,Amount='0',Tax='',TotalAmount='0',type=Type)
            data.save()
            get = ChargesListModel.objects.filter(ProductId=PN.ProductId,user=user,type=Type).values()
        else:
            data = ChargesListModel.objects.create(user=user,Charges=Ch.Charges,ProductId=Productid,Amount='0',Tax='',TotalAmount='0',type=Type)
            data.save()
            get = ChargesListModel.objects.filter(ProductId=Productid,user=user,type=Type).values()
        Sc = list(get)
        tamonut = 0
        for i in Sc:
            tamonut+=float(i['TotalAmount'])
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
    data=PartyModel.objects.all()
    data.delete()
    # data2=CategoryModel.objects.all()
    # data2.delete()
    # data4=DeliveryBoyModel.objects.all()
    # data4.delete()
    # data1=ProductModel.objects.all()
    # data1.delete()
    data5=StockModel.objects.all()
    data5.delete()
    data6=NMModel.objects.all()
    data6.delete()
    data7=PurchaseEntryModel.objects.all()
    data7.delete()
    data8=SalesEntryModel.objects.all()
    data8.delete()
    data0=MainStockModel.objects.all()
    data0.delete()
    dt=SalesStockModel.objects.all()
    dt.delete()
    df=BiilNoModel.objects.all()
    df.delete()
    df1=AmountModel.objects.all()
    df1.delete()
    df2=UserAmountModel.objects.all()
    df2.delete()
    df3=LedgerReportModel.objects.all()
    df3.delete()
    du=PendingAmountModel.objects.all()
    du.delete()
    # du=PendingAmountModel.objects.all()
    # du.delete()
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
    stock = MainStockModel.objects.filter(user=request.user)
    Productname = []
    for i in stock:
        if int(i.out) != 1:
            Productname.append(i.ProductName)
    Productname = set(Productname)
    data = {'stock':Productname}
    if is_admin(request.user):
        return render(request,'admin/stock.html',data)
    if is_user(request.user):
        return render(request,'stock.html',data)
    
@login_required(login_url='Login')
def ProductsDetails(request,name):
    stock = MainStockModel.objects.filter(user=request.user,ProductName=name,out='0')
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
def RProductsDetails(request,name):
    stock = SalesStockModel.objects.filter(user=request.user,type='SalesReturn',ProductName=name)
    Quantity = 0
    Amount = 0
    for i in stock:
        Quantity += eval(i.Quantity)
        Amount += eval(i.TotalSales)
    Quantity = Quantity
    Amount = Amount
    data = {'stock':stock,'Quantity':Quantity,'Amount':Amount}
    if is_admin(request.user):
        return render(request,'admin/rproductsdetails.html',data)
    if is_user(request.user):
        return render(request,'rproductsdetails.html',data)

@login_required(login_url='Login')
def InvoiceNoDetails(request,IN,type):
    if IN == '':
        print('balnak')
    else:
        print('value')
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
    try:
        ss=SalesStockModel.objects.filter(user=request.user.username,type='SalesReturn')
        Productname = {i.ProductName for i in ss}
    except SalesStockModel.DoesNotExist:
        Productname = ''
    data = {'stock':Productname}
    if is_admin(request.user):
        return render(request,'admin/salesstock.html',data)
    if is_user(request.user):
        return render(request,'salesstock.html',data)
    
@login_required(login_url='Login')
def DeliveryReport(request):
    sales = SalesEntryModel.objects.filter(Type='Sales',user=request.user)
    sp = {i.DeliveryBoyName for i in sales}
    ta = 0
    PB = 0
    BB = 0
    CB = 0
    for i in sales:
        if i.TypeofPayment == 'Credit':
            PB += eval(i.Amount)
        elif i.TypeofPayment == 'Case':
            CB += eval(i.Amount)
        else:
            BB += eval(i.Amount)
        ta += eval(i.Amount)
    ta = "%.2f" % ta
    data = {'sales':sales,'sp':sp,'ta':ta,'PB':PB,'BB':BB,'CB':CB}
    if request.method=="POST": 
        StartDate = request.POST.get('StartDate')
        EndDate = request.POST.get('EndDate')
        DeliveryBoyName = request.POST.get('DeliveryBoyName')
        if (StartDate != '' and EndDate != '') and (DeliveryBoyName == 'Select' ):
            ss = SalesEntryModel.objects.filter(Type='Sales',Date__range=[StartDate, EndDate],user=request.user)
            ta = 0
            for i in ss:
                ta += eval(i.Amount)
            ta = "%.2f" % ta
        elif (StartDate == '' and EndDate == '') and (DeliveryBoyName == 'Select'):
            ss = SalesEntryModel.objects.filter(Type='Sales',user=request.user)
            ta = 0
            for i in ss:
                ta += eval(i.Amount)
            ta = "%.2f" % ta
        elif StartDate == '' and EndDate == '':
            if DeliveryBoyName == 'Select':
                ss = SalesEntryModel.objects.filter(Type='Sales',user=request.user)
                ta = 0
                for i in ss:
                    ta += eval(i.Amount)
                ta = "%.2f" % ta
            else :  
                ss = SalesEntryModel.objects.filter(Type='Sales',user=request.user,DeliveryBoyName=DeliveryBoyName)
                ta = 0
                for i in ss:
                    ta += eval(i.Amount)
                ta = "%.2f" % ta
        elif (StartDate != '' and EndDate == '') and (DeliveryBoyName == 'Select'):
                ss = SalesEntryModel.objects.filter(Type='Sales',user=request.user,Date=StartDate)
                ta = 0
                for i in ss:
                    ta += eval(i.Amount)
                ta = "%.2f" % ta
        else:
            ss = SalesEntryModel.objects.filter(Type='Sales',Date__range=[StartDate, EndDate],user=request.user,DeliveryBoyName=DeliveryBoyName)
            ta = 0
            for i in ss:
                ta += eval(i.Amount)
            ta = "%.2f" % ta
        sp = {i.DeliveryBoyName for i in sales}
        ta = 0
        PB = 0
        BB = 0
        CB = 0
        for i in ss:
            if i.TypeofPayment == 'Credit':
                PB += eval(i.Amount)
            elif i.TypeofPayment == 'Case':
                CB += eval(i.Amount)
            else:
                BB += eval(i.Amount)
            ta += eval(i.Amount)
        ta = "%.2f" % ta
        data = {'sales':ss,'sp':sp,'StartDate':StartDate,'EndDate':EndDate,'ta':ta,'DeliveryBoyName':DeliveryBoyName,'PB':PB,'BB':BB,'CB':CB}
        return render(request,'admin/deliveryreport.html',data)
    if is_admin(request.user):
        return render(request,'admin/deliveryreport.html',data)
    if is_user(request.user):
        return render(request,'deliveryreport.html')
    
# @login_required(login_url='Login')
# def LedgerReport(request):
#     if is_admin(request.user):
#         sales = SalesEntryModel.objects.filter(user=request.user)
#         Purchase = PurchaseEntryModel.objects.filter(user=request.user)
#         sp = {i.PartyName for i in sales}
#         pp = {i.PartyName for i in Purchase}
#         data = {'sales':sales,'pem':Purchase,'sp':sp,'pp':pp}
#         if request.method=="POST": 
#             StartDate = request.POST.get('StartDate')
#             EndDate = request.POST.get('EndDate')
#             PartyName = request.POST.get('PartyName')
#             if (StartDate != '' and EndDate != '') and (PartyName == 'Select' ):
#                 ss = SalesEntryModel.objects.filter(Date__range=[StartDate, EndDate],user=request.user)
#                 pem = PurchaseEntryModel.objects.filter(Date__range=[StartDate, EndDate],user=request.user)
#             elif (StartDate == '' and EndDate == '') and (PartyName == 'Select'):
#                 ss = SalesEntryModel.objects.filter(user=request.user)
#                 pem = PurchaseEntryModel.objects.filter(user=request.user)
#             elif StartDate == '' and EndDate == '':
#                 if PartyName == 'Select':
#                     ss = SalesEntryModel.objects.filter(user=request.user)
#                     pem = PurchaseEntryModel.objects.filter(user=request.user)
#                 else :  
#                     ss = SalesEntryModel.objects.filter(user=request.user,PartyName=PartyName)
#                     pem = PurchaseEntryModel.objects.filter(user=request.user,PartyName=PartyName)
#             elif (StartDate != '' and EndDate == '') and (PartyName == 'Select'):
#                     ss = SalesEntryModel.objects.filter(user=request.user,Date=StartDate)
#                     pem = PurchaseEntryModel.objects.filter(user=request.user,Date=StartDate)
#             else:
#                 ss = SalesEntryModel.objects.filter(Date__range=[StartDate, EndDate],user=request.user,PartyName=PartyName)
#                 pem = PurchaseEntryModel.objects.filter(Date__range=[StartDate, EndDate],user=request.user,PartyName=PartyName)
#             sp = {i.PartyName for i in sales}
#             pp = {i.PartyName for i in Purchase}
#             data = {'sales':ss,'pem':pem,'sp':sp,'pp':pp,'StartDate':StartDate,'EndDate':EndDate,'PartyName':PartyName}
#             return render(request,'admin/ledgerreport.html',data)
#         return render(request,'admin/ledgerreport.html',data)
#     if is_user(request.user):
#         return render(request,'ledgerreport.html')

@login_required(login_url='Login')
def LedgerReport(request):
    if is_admin(request.user):
        Lr = LedgerReportModel.objects.filter(user=request.user)
        Party = PartyModel.objects.filter(user=request.user)
        data = {'Lr':Lr,'Party':Party}
        if request.method=="POST": 
            StartDate = request.POST.get('StartDate')
            EndDate = request.POST.get('EndDate')
            PartyName = request.POST.get('PartyName')
            if (StartDate != '' and EndDate != ''):
                if PartyName == 'Select':
                    Lr = LedgerReportModel.objects.filter(LRDate__range=[StartDate, EndDate],user=request.user)
                else:
                    Lr = LedgerReportModel.objects.filter(LRDate__range=[StartDate, EndDate],PartyName=PartyName,user=request.user)
            elif(StartDate != '' or EndDate != ''):
                if PartyName == 'Select':
                    Lr = LedgerReportModel.objects.filter(LRDate__range=[StartDate, EndDate],user=request.user)
                else:
                    Lr = LedgerReportModel.objects.filter(LRDate__range=[StartDate, EndDate],PartyName=PartyName,user=request.user)
                Lr = LedgerReportModel.objects.filter(LRDate__range=[StartDate, EndDate],user=request.user)
            elif(StartDate == '' and EndDate == ''):
                if PartyName == 'Select':
                    Lr = LedgerReportModel.objects.filter(user=request.user)
                else:
                    Lr = LedgerReportModel.objects.filter(user=request.user,PartyName=PartyName)
            data = {'Lr':Lr,'StartDate':StartDate,'EndDate':EndDate,'PartyName':PartyName,'Party':Party}
            return render(request,'admin/ledgerreport.html',data)
        return render(request,'admin/ledgerreport.html',data)
    if is_user(request.user):
        return render(request,'ledgerreport.html')

def SPDF(request):
   data = MainStockModel.objects.all()
   context = {
      'data':data
   }
   pdf = render_to_pdf('admin/vbill.html',context)
   if pdf:
      response = HttpResponse(pdf,content_type='application/pdf')
      filename = "Bill123.pdf"
      content = f"attachment; filename={filename}"
    #   if download:
    #     content = f"inline; filename={filename}"
      response['Content-Disposition'] = content
      return response
   return HttpResponse("Not Found")

@login_required(login_url='Login')
@csrf_exempt
def Link(request,name):
    user = str(request.user.username)  
    if name == 'Charges':
        if request.method=="POST":          
            Charges=request.POST.get('Charge')
            try:
                dt=ChargesModel.objects.get(Charges=Charges)
                if dt.Charges == Charges:
                    mgs = 'Add Charges.'
                    ld = ChargesModel.objects.filter(user=user).values()
                    ld = list(ld)
                    return JsonResponse({'ld':ld,'mgs':mgs})
                else:
                    dt=ChargesModel.objects.create(user=user,Charges=Charges)
                    dt.save()
                    mgs = 'Add Charges.'
                    ld = ChargesModel.objects.filter(user=user).values()
                    ld = list(ld)
                    return JsonResponse({'ld':ld,'mgs':mgs})
            except:
                dt=ChargesModel.objects.create(user=user,Charges=Charges)
                dt.save()
                mgs = 'Add Charges.'
                ld = ChargesModel.objects.filter(user=user).values()
                ld = list(ld)
                return JsonResponse({'ld':ld,'mgs':mgs})
    if name == 'Products':
        if request.method=="POST":
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
            mgs = 'Add Products.'
            ld = ProductModel.objects.filter(user=user).values()
            ld = list(ld)
            return JsonResponse({'ld':ld,'mgs':mgs})
    if name == 'Party':
        if request.method=="POST":
            Type=request.POST.get('Type')
            PartyName=request.POST.get('PartyName')
            Number=request.POST.get('Number')
            Address=request.POST.get('Address')
            GSTNo=request.POST.get('GSTNo')
            Email=request.POST.get('Email')
            City=request.POST.get('City')
            try:
                d=PartyModel.objects.filter(user=request.user)
                if d:
                    df=0
                    for i in d:
                        if i.Number == Number:
                            NUM = 'This Number is Allready Available.'
                            ld = 0
                            df += 1
                            return JsonResponse({'ld':ld,'NUM':NUM})
                        elif i.Email == Email:
                            EM = 'This Email is Allready Available.'
                            ld = 0
                            df += 2
                            return JsonResponse({'ld':ld,'EM':EM})
                    if df == 0:
                        dt=PartyModel.objects.create(user=user,Type=Type,PartyName=PartyName,Number=Number,Address=Address,GSTNo=GSTNo,Email=Email,City=City)
                        dt.save()
                        mgs = 'Add Party Successfully.'
                        ld = PartyModel.objects.filter(user=user).values()
                        ld = list(ld)
                        return JsonResponse({'ld':ld,'mgs':mgs}) 
                else:
                    dt=PartyModel.objects.create(user=user,Type=Type,PartyName=PartyName,Number=Number,Address=Address,GSTNo=GSTNo,Email=Email,City=City)
                    dt.save()
                    mgs = 'Add Party Successfully.'
                    ld = PartyModel.objects.filter(user=user).values()
                    ld = list(ld)
                    return JsonResponse({'ld':ld,'mgs':mgs}) 
            except:
                dt=PartyModel.objects.create(user=user,Type=Type,PartyName=PartyName,Number=Number,Address=Address,GSTNo=GSTNo,Email=Email,City=City)
                dt.save()
                mgs = 'Add Party Successfully.'
                ld = PartyModel.objects.filter(user=user).values()
                ld = list(ld)
                return JsonResponse({'ld':ld,'mgs':mgs})
    if name == 'Expanse':
        if request.method=="POST":
            Expanse=request.POST.get('Expanse')
            Type=request.POST.get('Type')
            try:
                ex = ExpanseModel.objects.get(user=user,Expanse=Expanse,Type=Type)
                if ex:
                    mgs = 'Add Expanse Successfully.'
                    ld = ExpanseModel.objects.filter(user=user).values()
                    ld = list(ld)
                    return JsonResponse({'ld':ld,'mgs':mgs})
                else:
                    dt=ExpanseModel.objects.create(user=user,Expanse=Expanse,Type=Type)
                    dt.save()
                    mgs = 'Add Party Successfully.'
                    ld = ExpanseModel.objects.filter(user=user).values()
                    ld = list(ld)
                    return JsonResponse({'ld':ld,'mgs':mgs})
            except:
                dt=ExpanseModel.objects.create(user=user,Expanse=Expanse,Type=Type)
                dt.save()
                mgs = 'Add Party Successfully.'
                ld = ExpanseModel.objects.filter(user=user).values()
                ld = list(ld)
                return JsonResponse({'ld':ld,'mgs':mgs})

def PageTest(request):
        return render(request,'admin/test.html')

@login_required(login_url='Login')
def OutstandingReport(request):
    if is_admin(request.user):
        return render(request,'admin/outstandingreport.html')
    if is_user(request.user):
        return render(request,'outstandingreport.html')

@login_required(login_url='Login')
def QuickPayment(request):
    PAM = PendingAmountModel.objects.filter(user=request.user,Type='QuickPayment')
    data={'PAM':PAM}
    if request.method == 'POST':
        Date = request.POST.get('Date')
        BillNo = request.POST.get('BillNo')
        PartyName = request.POST.get('PartyName')
        Id = request.POST.get('Id')
        TypeofPayment = request.POST.get('TypeofPayment')
        CeditedAmount = request.POST.get('CeditedAmount')
        PayableAmount = request.POST.get('PayableAmount')
        TransactionID = request.POST.get('TransactionID')
        Description = request.POST.get('Description')
        if eval(CeditedAmount) == eval(PayableAmount):
            UAM=UserAmountModel.objects.get(user=request.user)
            if eval(UAM.Amount) >= eval(PayableAmount):
                amount = eval(UAM.Amount) - eval(PayableAmount)
                amount = "%.2f" % amount 
                UAM.Amount = amount
                UAM.save()
                LR=LedgerReportModel.objects.create(user=request.user.username,PartyName=PartyName,Type='QuickPayment',BiilNo=BillNo,Debited=PayableAmount,Cedited='0',Balance=amount)
                LR.save()
                dt=PurchaseEntryModel.objects.get(id=Id)
                dt.PendingAmount = '0'
                dt.status = '0'
                dt.save()
                main = PendingAmountModel.objects.create(user=request.user.username,Type='QuickPayment',Date=Date,PartyName=PartyName,Number=BillNo,CeditedAmount=CeditedAmount,PayableAmount=PayableAmount,TypeofPayment=TypeofPayment,TransactionID=TransactionID,Description=Description)
                main.save()
                messages.success(request,'Quick Payment Successfully.')
                return redirect('/QuickPayment')
            else:
                messages.success(request,'You Have Not Sufficient Balance.')
                return redirect('/QuickPayment')
        elif eval(CeditedAmount) < eval(PayableAmount):
            messages.success(request,'Payable Amount Is High To The Cedited Amount.')
            return redirect('/QuickPayment')
        else:
            UAM=UserAmountModel.objects.get(user=request.user)
            if eval(UAM.Amount) >= eval(PayableAmount):
                amount = eval(UAM.Amount) - eval(PayableAmount)
                amount = "%.2f" % amount 
                UAM.Amount = amount
                UAM.save()
                LR=LedgerReportModel.objects.create(user=request.user.username,PartyName=PartyName,Type='QuickPayment',BiilNo=BillNo,Debited=PayableAmount,Cedited='0',Balance=amount)
                LR.save()
                dt=PurchaseEntryModel.objects.get(id=Id)
                Pa = eval(CeditedAmount) - eval(PayableAmount)
                dt.PendingAmount = "%.2f" % Pa 
                dt.status = '1'
                dt.save()
                main = PendingAmountModel.objects.create(user=request.user.username,Type='QuickPayment',Date=Date,PartyName=PartyName,Number=BillNo,CeditedAmount=CeditedAmount,PayableAmount=PayableAmount,TypeofPayment=TypeofPayment,TransactionID=TransactionID,Description=Description)
                main.save()
                messages.success(request,'Quick Payment Successfully.')
                return redirect('/QuickPayment')
            else:
                messages.success(request,'You Have Not Sufficient Balance.')
                return redirect('/QuickPayment')
    if is_admin(request.user):
        return render(request,'admin/quickpayment.html',data)
    if is_user(request.user):
        return render(request,'quickpayment.html',data)

@login_required(login_url='Login')
@csrf_exempt
def QuickPaymentBill(request):
    if request.method == 'POST':
        BillNo = request.POST.get('BillNo')
        try:
            dt=PurchaseEntryModel.objects.get(user=request.user,Type='Purchase',BillNo=BillNo,status='1')
            PN = dt.PartyName
            PA = dt.PendingAmount
            Id = dt.id
        except PurchaseEntryModel.DoesNotExist:
            PN = ''
            PA = ''
            Id = ''
        return JsonResponse({'status':1,'PN':PN,'PA':PA,'Id':Id})
    else:
        return JsonResponse({'status':0})

@login_required(login_url='Login')
def QuickReceipt(request):
    if is_admin(request.user):
        return render(request,'admin/quickreceipt.html')
    if is_user(request.user):
        return render(request,'quickreceipt.html')

@login_required(login_url='Login')
def DebitNote(request):
    if is_admin(request.user):
        return render(request,'admin/debitnote.html')
    if is_user(request.user):
        return render(request,'debitnote.html')

@login_required(login_url='Login')
def CreditNote(request):
    if is_admin(request.user):
        return render(request,'admin/creditnote.html')
    if is_user(request.user):
        return render(request,'creditnote.html')
