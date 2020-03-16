from django.db import models
import uuid

class Company(models.Model):
    # First 4 character of the UUID will be used as user-friend short reference.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)

    class Meta: 
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name + ', Id: ' + str(self.id)
    
class UnitOfMeasure(models.Model):
    acronym = models.CharField(max_length=10)
    full_name = models.CharField(max_length=30)

    def __str__(self):
        return self.full_name + ', ' + self.acronym
    
class Product(models.Model):
    # First 4 character of the UUID will be used as user-friend short reference.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=200)
    quantity = models.FloatField()

    uom = models.ForeignKey(UnitOfMeasure,
        models.CASCADE, related_name='products')
    company = models.ForeignKey(Company,
        models.CASCADE, related_name='products')

    def __str__(self):
        return self.full_name + ', ' + str(self.quantity) + ' ' + self.uom.acronym + ', Id: ' + str(self.id)

class Agent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    whatsapp_no = models.CharField(max_length=200, blank=True, null=True)
    wechat_no = models.CharField(max_length=200, blank=True, null=True)
    wechat_id = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        if self.last_name != None:
            return self.first_name + ' ' + self.last_name + ', Id: ' + str(self.id)
        
        return self.first_name + ', Id: ' + str(self.id)

class ProductsList(models.Model):
    # First 4 character of the UUID will be used as user-friend short reference.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(blank=True, null=True, default=None)

    products = models.ManyToManyField(Product, related_name='products_lists')
    agent = models.ForeignKey(Agent,
        models.CASCADE, related_name='products_list',
        blank=True, null=True)

    def __str__(self):
        product_count = self.products.count()
        if product_count > 0:
            product_str = 'products'
        else:
            product_str = 'product'

        return self.title + ', ' + self.agent.first_name + ' ' + self.agent.last_name + ', ' + str(product_count) + ' ' + product_str + ', ' + str(self.created)

class ProductsListAccessLogEntry(models.Model):
    accessed = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=500, blank=True, null=True)
    referrer = models.CharField(max_length=2000, blank=True, null=True)

    products_list = models.ForeignKey(ProductsList,
        models.CASCADE, related_name='log_entries')

    def __str__(self):
        if self.user_agent != None:
            return self.ip_address + ', ' + self.user_agent

        return self.ip_address

    class Meta: 
        verbose_name_plural = "Products list access log entries"
        ordering = ['-accessed']

class Lead(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.full_name + ', ' + self.email

class ProductsInterestsList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submitted = models.DateTimeField(auto_now_add=True)

    products = models.ManyToManyField(Product, related_name='interests_lists')
    products_list = models.ForeignKey(ProductsList,
        models.CASCADE, related_name='interests_lists')
    lead = models.ForeignKey(Lead,
        models.CASCADE, related_name='interests')

    def __str__(self):
        return str(self.lead) + ', ' + str(self.products.count()) + ' products'