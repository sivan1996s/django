from django.contrib import admin

# Register your models here.
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
# Register your models here.

class AccountGroup(ImportExportModelAdmin):
    list_display=['id','user_name','account_holder','mail_id','mobile_number']
admin.site.register(Account,AccountGroup)

class LoginRoleGroup(ImportExportModelAdmin):
    list_display=['id','role_name']
admin.site.register(LoginRole,LoginRoleGroup)

class ProductRoleGroup(ImportExportModelAdmin):
    list_display=['id','product_name','quantity','amount_net']
admin.site.register(Product,ProductRoleGroup)

class InvoiceDetailsRoleGroup(ImportExportModelAdmin):
    list_display=['id','bill_amount','disc_amount','bill_number']
admin.site.register(InvoiceDetails,InvoiceDetailsRoleGroup)

class ProductPurchaseGroup(ImportExportModelAdmin):
    list_display=['id','invoice','products','amount_net','paid_amount']
admin.site.register(ProductPurchase,ProductPurchaseGroup)