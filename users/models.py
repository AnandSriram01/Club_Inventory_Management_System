from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Club(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name


class UserProfile(models.Model):
	ROLES = (
				('None', 'None'),
                ('Member', 'Member'),
                ('Convenor', 'Convenor')
           )

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'userprofile', null=True, default=None)
	name = models.CharField(max_length=200, null=True)
	club =  models.ForeignKey(Club, null=True, default='None', on_delete= models.CASCADE, related_name = 'user_club')
	role = models.CharField(max_length=200, null=True, choices=ROLES, default='None')

	def __str__(self):
		return self.name


class Item(models.Model):
	name = models.CharField(max_length=200, null=True)
	quantity = models.IntegerField()
	club =  models.ForeignKey(Club, null=True, on_delete=models.CASCADE, related_name = 'items_of_club')
	# image = models.ImageField()

	def __str__(self):
		return self.name


class Request(models.Model):
	STATUS = (
				('Awaiting Approval', 'Awaiting Approval'),
				('Accepted by Convenor', 'Accepted by Convenor'),
				('Rejected by Convenor', 'Rejected by Convenor'),
			 )

	status = models.CharField(max_length=200, null=True, choices=STATUS)
	comment = models.CharField(max_length=200, null=True)
	member = models.ForeignKey(UserProfile, null=True, on_delete=models.CASCADE, related_name = 'requests_of_user')
	item = models.ForeignKey(Item, null=True, on_delete=models.CASCADE, related_name = 'requests_of_item')
	timestamp_placed = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.status
