from django.db import models

PAYMENT_METHOD=(('Cash','Cash'),('Card','Card'),('UPI','UPI'),('Bank','Bank'))
# Create your models here.
class BaseModel(models.Model):
    created_by=models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now=True)
    modified_by=models.CharField(max_length=50,null=True,blank=True)
    modified_date=models.DateTimeField(auto_now_add=True,null=True,blank=True)

class LoginRole(BaseModel):
    role_name=models.CharField(max_length=50)
    class Meta:
        db_table = 'login_role'
      

class Account(BaseModel):
    role_name=models.ForeignKey(LoginRole,on_delete=models.CASCADE,null=True,blank=True)
    user_name= models.CharField(max_length=100)
    password=models.CharField(max_length=200)
    account_holder=models.CharField(max_length=100)
    mail_id=models.EmailField(max_length=200,unique=True)
    mobile_number=models.CharField(max_length=20,null=True,blank=True)
    dob=models.DateField(null=True,blank=True)
    profile_url=models.URLField(null=True,blank=True)
    del_address=models.TextField(null=True,blank=True)
    login_count= models.IntegerField(null=True,blank=True,default=0)
    is_acc_lock=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    
    # def delete(self):
    #     if self.shipper:
    #         self.shipper.delete()
    #     if self.carrier:
    #         self.carrier.delete()
    #     if self.affiliat:
    #         self.affiliat.delete()
    #     super(Profile, self).delete()
    class Meta:
        db_table = 'account_detail'

class Product(BaseModel):
    product_name=models.CharField(max_length=100,null=True,blank=True)
    quantity= models.IntegerField(null=True,blank=True)
    amount_net=models.DecimalField(default=0,decimal_places=2,max_digits=10)
    is_active=models.BooleanField(default=True)
    
    class  Meta:
        db_table = 'Product'
class InvoiceDetails(BaseModel):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    bill_amount =models.DecimalField(default=0,decimal_places=2,max_digits=10)
    disc_amount =models.DecimalField(default=0,decimal_places=2,max_digits=10)
    bill_number=models.CharField(max_length=15,null=True,blank=True)
    is_active=models.BooleanField(default=True)

    class Meta:
        db_table='invoice'

class ProductPurchase(BaseModel):
    invoice=models.ForeignKey(InvoiceDetails,on_delete=models.CASCADE)
    products=models.ForeignKey(Product,on_delete=models.CASCADE)
    amount_net=models.DecimalField(default=0,decimal_places=2,max_digits=10)
    paid_amount=models.DecimalField(default=0,decimal_places=2,max_digits=10)
    payment_type=models.CharField(choices=PAYMENT_METHOD,max_length=100,null=True,blank=True)
    is_active=models.BooleanField(default=True)


    class Meta:
        db_table='purchase'