from django.shortcuts import render
from company.models import CompanyMaster
from user.models import UserMaster
from role.models import RoleMaster, RoleTypeMaster
from .forms import RoleForm

from django.http import HttpResponseRedirect

# Create your views here.


def create(request):
	if(request.session.has_key('company_id') == False):
		return HttpResponseRedirect('/')
	company_id = request.session.get('company_id')
	company_obj = CompanyMaster.objects.get(id=company_id)
	user_id = request.session.get('user_id')
	user_obj = UserMaster.objects.get(id=user_id)
	print("  create role ====== ")
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = RoleForm(request.POST,request)
		if form.is_valid():
			# role Master
			print("111===")
			role_name = request.POST['role_name']
			if 'role_type' in request.POST:
				try:
					role_type = request.POST['role_type']
					try:
						role_type_obj = RoleTypeMaster.objects.get(id=role_type)
					except ValueError:
						pass
				except ValueError:
					pass
			is_active = request.POST['is_active']
			# created_by = request.POST['created_by']
			role_master = RoleMaster(
									 role_name= role_name,
									 role_type= str(role_type_obj),
									 is_active= is_active,
									 company_id= company_obj,
									 created_by= user_obj
			)
			print("2222 ====")
			role_master.save()
			print("save successfully =====")
			#role Propery Address  Master
			return HttpResponseRedirect('/role/list/')
		
	else:
		form = RoleForm()
	return render(request, 
					'role/create.html',
					{'form': form}
					)

def index(request):
	if request.session.has_key('company_id') == False:
		return HttpResponseRedirect('/')
	company_id = request.session.get('company_id')
	company_obj = CompanyMaster.objects.get(id=company_id)
	#role_list = RoleMaster.objects.filter(company_id=company_obj) #or any kind of queryset	
	
	role_list = RoleMaster.objects.filter(company_id=company_obj)
	
	print("company_obj  ========",company_obj)
	print("role_list  ========",role_list)
	return render(request, 
					'role/list.html',
					{'role_master':role_list})