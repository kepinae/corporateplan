from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime,timedelta
from mailer import send_mail
from django.conf import settings
# Create your views here.
def DT_login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('/order')
		else:
			return redirect('/login')
	return render(request,'login.html',{})


@login_required(login_url='/login')
def insert_order(request):
	comp_list = Company.objects.all()
	type_list = Type.objects.all()
	msg=''
	if request.method == "POST":
		comp_id = request.POST['company']
		type_id = request.POST['type']
		kms_run = float(request.POST['kms_run'])
		task_type = request.POST['task_type']
		time_spent = request.POST['time_spent']
		if time_spent:
			time_spent = int(time_spent)
		plan_of_comp = Plan.objects.filter(plan_type__id = type_id,company__id = comp_id)
		
		if plan_of_comp and task_type.lower() =='pick and drop':
			plan = plan_of_comp[0]
			req_used = 0
			kms_used = 0
			rest_kms_of_ride = int(round(kms_run%plan.free_kms_per_req))
			if plan.no_of_req_remaining >0 and (plan.no_of_req_remaining*plan.free_kms_per_req+plan.kms_remaining) >= kms_run: 
				expiry_date = plan.created_date.date() + timedelta(days = plan.validity_in_months*30) 
				if expiry_date >= datetime.now().date():
					if kms_run >= plan.free_kms_per_req:
						req_used += int(kms_run/plan.free_kms_per_req)
						if req_used > plan.no_of_req_remaining:
							req_used = req_used - (req_used-plan.no_of_req_remaining)
							rest_kms_of_ride = rest_kms_of_ride+plan.no_of_req_remaining*plan.free_kms_per_req

					if rest_kms_of_ride:
						if rest_kms_of_ride >= plan.free_kms_per_req*0.7 :
							if plan.no_of_req_remaining - req_used >= 1:
								req_used += 1
							else:
								kms_used += rest_kms_of_ride
						elif rest_kms_of_ride < plan.free_kms_per_req*0.50:
							if rest_kms_of_ride < plan.kms_remaining:
								kms_used += rest_kms_of_ride
							elif plan.no_of_req_remaining - req_used >= 1:
								req_used += 1	
							else:
								kms_used += rest_kms_of_ride	

						elif rest_kms_of_ride >= plan.free_kms_per_req*0.5 and  rest_kms_of_ride < plan.free_kms_per_req*0.7 :
							if plan.kms_remaining >= 3*plan.free_kms_per_req:
								kms_used += rest_kms_of_ride
							elif plan.no_of_req_remaining - req_used >= 1:
								req_used += 1	
							else:
								kms_used += rest_kms_of_ride 		
					plan.no_of_req_remaining = plan.no_of_req_remaining - req_used
					plan.kms_remaining = plan.kms_remaining - kms_used
					plan.save()
					Order.objects.create(plan=plan_of_comp[0],kms_run=kms_run,created_by=request.user)
				else:
					msg = "Unable To Make This Request Because The Plan Requested For This Company Has Expired On  "+str(expiry_date)+"."	
			else:
				msg = "Unable To Make This Request Because, For This Company "+ str(plan_of_comp[0].no_of_req_remaining) +" Reqs and "+str(plan_of_comp[0].kms_remaining)+" Free Kms remaining."
		
		elif plan_of_comp and task_type.lower() =='task':
			plan = plan_of_comp[0]
			req_used = 0
			kms_used = 0
			least_time = 0
			kms_eqivalent_per_hour = plan.kms_eqivalent_per_hour
			if time_spent%30:
				least_time = 1
			if plan.no_of_req_remaining >0 and (plan.no_of_req_remaining*kms_eqivalent_per_hour+plan.kms_remaining) >= kms_run and plan.no_of_req_remaining > time_spent/60: 
				expiry_date = plan.created_date.date() + timedelta(days = plan.validity_in_months*30)
				if expiry_date >= datetime.now().date(): 
					print kms_run,(time_spent/60)*kms_eqivalent_per_hour + ((time_spent%60)/30)*(0.5*kms_eqivalent_per_hour) + least_time*(0.5*kms_eqivalent_per_hour)
					if (time_spent/60)*kms_eqivalent_per_hour + ((time_spent%60)/30)*(0.5*kms_eqivalent_per_hour) + least_time*(0.5*kms_eqivalent_per_hour) <= kms_run:
						
						req_used += time_spent/60
						kms_used = kms_run - kms_eqivalent_per_hour*(time_spent/60)
						if not time_spent/60:
							req_used += 1
							kms_used += kms_run - 1*kms_eqivalent_per_hour
						if kms_used > plan.kms_remaining:
							req_used += (kms_used/kms_eqivalent_per_hour)
							kms_used = (kms_used%kms_eqivalent_per_hour)
							if plan.kms_remaining < kms_used:
								req_used += 1

					else:
						req_used += time_spent/60 
						if not time_spent/60 or time_spent%60:
							req_used += 1

					plan.no_of_req_remaining = plan.no_of_req_remaining - req_used
					plan.kms_remaining = plan.kms_remaining - kms_used
					plan.save()
					Order.objects.create(plan=plan_of_comp[0],kms_run=kms_run,created_by=request.user)			

				else:
					msg = "Unable To Make This Request Because The Plan Requested For This Company Has Expired On  "+str(expiry_date)+"."			

			else:
				msg = "Unable To Make This Request Because, For This Company "+ str(plan_of_comp[0].no_of_req_remaining) +" Reqs and "+str(plan_of_comp[0].kms_remaining)+" Free Kms remaining."		

		else:
			msg = Type.objects.get(id=type_id).name  +" plan for "+Company.objects.get(id=comp_id).name +" does not exist.Available plans are "+str([str(x) for x in Plan.objects.filter(company__id=comp_id).values_list('plan_type__name',flat=True)])

	return render(request,'entryform.html',{'comp_list':comp_list,'type_list':type_list,'msg': msg})



@login_required(login_url='/login')
def view_company_plans(request):
	planslist = Plan.objects.all()
	return render(request,'planslist.html',{'plan_list':planslist})	



@login_required(login_url='/login')
def order_list(request):
	order_list = Order.objects.all()
	return render(request,'orderlist.html',{'order_list':order_list})	


def send_DT_mail(request):
	send_mail('Subject here','Here is the message.',settings.DEFAULT_FROM_EMAIL,['ashraf.asif663@gmail.com'],fail_silently=False)
	return HttpResponse('mail send')



def logout_view(request):
    logout(request)
    return redirect('/login')