from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=60,unique=True)
    UID = models.CharField(max_length=30,unique=True)
    address = models.TextField(max_length=400)
    created_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
    	return self.name

class Type(models.Model):
    name = models.CharField(max_length=30,unique=True)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
    	return self.name


class Plan(models.Model):
	plan_type = models.ForeignKey('Type')
	company = models.ForeignKey('Company')
	free_req_in_plan = models.IntegerField()
	free_kms_in_plan = models.IntegerField()
	free_kms_per_req = models.IntegerField()
	kms_eqivalent_per_hour= models.IntegerField(null=True)
	validity_in_months = models.IntegerField()
	no_of_req_remaining = models.IntegerField()
	kms_remaining = models.IntegerField()
	created_date = models.DateTimeField(auto_now=True)
	last_updated = models.DateTimeField()

	def __str__(self):
		return str(self.company) +"--"+ str(self.plan_type)+"( Free Reqs : "+str(self.free_req_in_plan) +"&  free Kms : "+str(self.free_kms_in_plan) +" )"
    

class Order(models.Model):
	plan = models.ForeignKey('Plan')
	kms_run = models.IntegerField()
	weight = models.IntegerField(null=True)
	created_by = models.CharField(max_length = 70,editable=False)
	created_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.plan.company) +"--"+ str(self.kms_run)+"km" +"--"+str(self.created_date)+" created by --" + str(self.created_by)

