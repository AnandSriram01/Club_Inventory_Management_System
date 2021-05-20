from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Club(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name


class UserProfile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	club =  models.ForeignKey(Club, null=True, on_delete= models.SET_NULL)

	# def __str__(self):
	# 	return self.name


class Item(models.Model):
	name = models.CharField(max_length=200, null=True)
	quantity = models.IntegerField()
	club =  models.ManyToManyField(Club)
	# image = models.ImageField()


class Request(models.Model):
	STATUS = (
				('Awaiting Approval', 'Awaiting Approval'),
				('Accepted by Convenor', 'Accepted by Convenor'),
				('Rejected by Convenor', 'Rejected by Convenor'),
			 )

	status = models.CharField(max_length=200, null=True, choices=STATUS)
	comment = models.CharField(max_length=200, null=True)
	member = models.ForeignKey(User, null=True, on_delete= models.SET_NULL)
	item = models.ForeignKey(Item, null=True, on_delete= models.SET_NULL)
	timestamp_placed = models.DateTimeField(auto_now_add=True, null=True)











# class Tag(models.Model):
# 	name = models.CharField(max_length=200, null=True)
#
# 	def __str__(self):
# 		return self.name
#
# class Product(models.Model):
# 	CATEGORY = (
# 			('Indoor', 'Indoor'),
# 			('Out Door', 'Out Door'),
# 			)
#
# 	name = models.CharField(max_length=200, null=True)
# 	price = models.FloatField(null=True)
# 	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
# 	description = models.CharField(max_length=200, null=True, blank=True)
# 	date_created = models.DateTimeField(auto_now_add=True, null=True)
# 	tags = models.ManyToManyField(Tag)
#
# 	def __str__(self):
# 		return self.name
#
# class Order(models.Model):
# 	STATUS = (
# 			('Pending', 'Pending'),
# 			('Out for delivery', 'Out for delivery'),
# 			('Delivered', 'Delivered'),
# 			)
#
# 	customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
# 	product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
# 	date_created = models.DateTimeField(auto_now_add=True, null=True)
# 	status = models.CharField(max_length=200, null=True, choices=STATUS)
# 	note = models.CharField(max_length=1000, null=True)
#
# 	def __str__(self):
# 		return self.product.name
