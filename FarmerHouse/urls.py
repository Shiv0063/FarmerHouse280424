"""
URL configuration for FarmerHouse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login',views.Login,name='Login'),
    path('logout',views.Logout,name='Logout'),
    path('',views.dashboard,name='dashboard'),
    path('Party',views.Party,name="Party"),
    path('AddParty',views.AddParty,name="Add Party"),
    path('PartyDetails/<int:id>',views.PartyDetails,name="Party Details"),
    path('EditParty/<int:id>',views.EditParty,name="Edit Party"),
    path('DeleteParty/<int:id>',views.DeleteParty,name="Delete Party"),
    path('UserAccount',views.UserAccount,name='User Account'),
    path('AddUserAccount',views.AddUserAccount,name='Add User Account'),
    path('EditUser/<int:id>',views.EditUserAccount,name="Edit User Account"),
    path('DeleteUser/<int:id>',views.DeleteUserAccount,name="Delete User Account"),
    path('Product',views.Product,name='Product'),
    path('AddProduct',views.AddProduct,name="Add Product"),
    path('EditProduct/<int:id>',views.EditProduct,name="Edit Product"),
    path('DeleteProduct/<int:id>',views.DeleteProduct,name="Delete Product"),
    path('Category',views.Category,name='Category'),
    path('AddCategory',views.AddCategory,name='Add Category'),
    path('EditCategory/<int:id>',views.EditCategory,name='Edit Category'),
    path('DeleteCategory/<int:id>',views.DeleteCategory,name='Delete Category'),
    path('DeliveryBoy',views.DeliveryBoy,name='Delivery Boy'),
    path('AddDeliveryBoy',views.AddDeliveryBoy,name='Add Delivery Boy'),
    path('EditDeliveryBoy/<int:pk>',views.EditDeliveryBoy,name='Edit Delivery Boy'),
    path('DeleteDeliveryBoy/<int:pk>',views.DeleteDeliveryBoy,name='Delete Delivery Boy'),
    path('DeliveryBoyDetails/<int:pk>',views.DeliveryBoyDetails,name='Delivery Boy Details'),
    path('Expanse',views.Expanse,name='Expanse'),
    path('AddExpanse',views.AddExpanse,name='Add Expanse'),
    path('EditExpanse/<int:id>',views.EditExpanse,name='Edit Expanse'),
    path('DeleteExpanse/<int:id>',views.DeleteExpanse,name='Delete Expanse'),
    path('PurchaseEntry',views.PurchaseEntry,name="Purchase Entry"),
    path('Purchase',views.Purchase,name="purchase"),
    path('AddPurchaseEntry',views.AddPurchaseEntry,name="Add Purchase Entry"),
    path('SProducts/<str:PN>/<int:id>/<str:type>',views.SProducts,name='SProducts'),
    path('ProductE',views.ProductE,name='ProductE'),
    path('ProductsDelete',views.ProductsDelete,name='Products Delete'),
    path('PurchaseCancel/<int:id>',views.PurchaseCancel,name='Purchase Cancel'),
    path('PurchaseDetails/<int:id>',views.PurchaseDetails,name='Products Details'),
    path('SalesEntry',views.SalesEntry,name="Sales Entry"),
    path('Sales',views.Sales,name="Sales"),
    path('AddSalesEntry',views.AddSalesEntry,name="Add Sales Entry"),
    path('Stockswork/<str:PN>/<int:id>/<int:id2>/<str:type>',views.Stockswork,name='Stockswork'),
    path('ProductE2',views.ProductE2,name='ProductE2'),
    path('StockPDelete',views.StockPDelete,name='Products Delete'),
    path('SalesCancel/<int:id>',views.SalesCancel,name='Sales Cancel'),
    path('SalesDetails/<int:id>',views.SalesDetails,name='Products Details'),
    path('StockDetails/<str:name>',views.StockDetails,name='Products Details'),
    path('PurchaseReturn',views.PurchaseReturn,name='Purchase Return'),
    path('AddPurchaseReturnEntry',views.AddPurchaseReturnEntry,name='Add Purchase Return Entry'),
    path('PRStock/<str:PN>/<int:id>/<int:id2>/<str:type>',views.PRStock,name='PRStock'),
    path('StockReport',views.StockReport,name='Stock Report'),
    path('PRSDelete',views.PRSDelete,name='PRSDelete'),
    path('PRDetails/<int:id>',views.PRDetails,name='PR Details'),
    path('SalesReturn',views.SalesReturn,name='Sales Return'),
    path('AddSalesReturnEntry',views.AddSalesReturnEntry,name="Add Sales Return Entry"),
    path('SRStocks/<str:PN>/<int:id>/<str:type>',views.SRStocks,name='SRStocks'),
    path('SRDelete',views.SRDelete,name='SRDelete'),
    path('SRSEdit',views.SRSEdit,name='SRSEdit'),
    path('SRDetails/<int:id>',views.SRDetails,name='SRDetails'),
    path('AllDelete',views.AllDelete,name="AllDelete"),
    path('SRCancel/<int:id>',views.SRCancel,name='Sales Cancel'),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404='main.views.error_404_view'