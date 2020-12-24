from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserForm,EditUserForm
from .forms import UserProfileForm
from django.http import HttpResponseRedirect
from user.models import UserMaster,UserRoleMap 
from company.models import CompanyMaster
from role.models import RoleMaster,RoleFeatureMap
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import hashlib 
# Create your views here.

def validations(name):
    """ Validate username with removing the unwanted spaces"""
    name = name.strip()
    return name

# Login Request 
def add(request):
	if(request.session.has_key('company_id') == False):
		return HttpResponseRedirect('/')
	company_id = request.session.get('company_id')
	company_obj = CompanyMaster.objects.get(id=company_id)
	user_id = request.session.get('user_id')
	user_obj = UserMaster.objects.get(id=user_id)
	role_master_obj = RoleMaster.objects.filter(company_id=company_obj)
	role_id = request.session.get('role_id')
	if role_id != None:
		role_obj = RoleMaster.objects.get(id=role_id)
		role_feature = RoleFeatureMap.objects.filter(role_id=role_obj).values_list('feature_id', flat=True)
		role_feature = list(role_feature)
	else:
		role_feature = []
	if '10' not in role_feature:
		return HttpResponseRedirect('/dashboard/')	
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = UserForm(request.POST,request)
		# check whether it's valid:
		if form.is_valid():
			
			user_id = request.POST['user_id']
			user_name = request.POST['user_name']
			password = request.POST['password']
			email = request.POST['email']
			is_active = request.POST['is_active']
			role = request.POST['role_list']
			encrypted_password = hashlib.md5(password.encode()) 
			if 'nmls_id' in request.POST:
				nmls_id = request.POST['nmls_id']
				nmls_id = validations(nmls_id)
			else:
				nmls_id = None
			if 'phone' in request.POST:
				phone = request.POST['phone']
				phone = validations(phone)
			else:
				phone = None
			if 'company' in request.POST:
				company = request.POST['company']
				company = validations(company)
			else:
				company = None
			
			if 'fax' in request.POST:
				fax = request.POST['fax']
				fax = validations(fax)
			else:
				fax = None

			usermaster = UserMaster(
									user_id = validations(user_id),
									user_name = validations(user_name),
									password = encrypted_password.hexdigest(),
									is_active = is_active,
									email=validations(email),
									company_id=company_obj,
									nmls_id=nmls_id,
									created_by=user_obj,
									officer_company = company,
									phone=phone,
									fax=fax
									)
			usermaster.save()
			role_obj = RoleMaster.objects.get(id=role)

			if(role_obj):
				userrolemap = UserRoleMap(
									user_id = usermaster,
									role_id = role_obj,
									is_active='Y',
									created_by=user_obj
									)
				userrolemap.save()
			return HttpResponseRedirect('/user/list/')
	else:
		form = UserForm()
	return render(request, 
					'user/create.html',
					{'form': form,'role_list':role_master_obj,'role_feature':role_feature, 'user_obj':user_obj}
				)

# List of Users 
def index(request):
	if(request.session.has_key('company_id') == False):
		return HttpResponseRedirect('/')
	company_id = request.session.get('company_id')
	company_obj = CompanyMaster.objects.get(id=company_id)

	user_id = request.session.get('user_id')
	user_obj = UserMaster.objects.get(id=user_id)
	
	object_list = UserMaster.objects.filter(company_id=company_obj) #or any kind of queryset	
	role_id = request.session.get('role_id')
	if role_id != None:
		role_obj = RoleMaster.objects.get(id=role_id)
		role_feature = RoleFeatureMap.objects.filter(role_id=role_obj).values_list('feature_id', flat=True)
		role_feature = list(role_feature)
	else:
		role_feature = []
	if '4' not in role_feature:
		return HttpResponseRedirect('/dashboard/')
	return render(request, 
					'user/list.html',
					{'user_list':object_list,'role_feature':role_feature, 'user_obj':user_obj}
				)
@csrf_exempt
def getField(request):
	if(request.session.has_key('company_id') == False):
		return HttpResponseRedirect('/')
	company_id = request.session.get('company_id')
	company_obj = CompanyMaster.objects.get(id=company_id)
	user_id = request.session.get('user_id')
	user_obj = UserMaster.objects.get(id=user_id)
	role_master_obj = RoleMaster.objects.filter(company_id=company_obj)
	if request.method == 'POST':
		role_id = request.POST['role_id']
		role_obj = RoleMaster.objects.filter(id=role_id)
		role_row = role_obj[0]
		return render(request, 
					'user/field.html',
					{'role_row':role_row, 'user_obj':user_obj}
				)

def edit(request,id):
	if(request.session.has_key('company_id') == False):
		return HttpResponseRedirect('/')
	company_id = request.session.get('company_id')
	company_obj = CompanyMaster.objects.get(id=company_id)

	role_master_obj = RoleMaster.objects.filter(company_id=company_obj)
	
	user_id = request.session.get('user_id')
	user_obj = UserMaster.objects.get(id=user_id)
	role_id = request.session.get('role_id')
	user_id_detail = UserMaster.objects.get(id=id)
	
	if role_id != None:
		role_obj = RoleMaster.objects.get(id=role_id)
		role_feature = RoleFeatureMap.objects.filter(role_id=role_obj).values_list('feature_id', flat=True)
		role_feature = list(role_feature)
	else:
		role_feature = []
	if '7' not in role_feature:
		return HttpResponseRedirect('/dashboard/')
	user_role_map = UserRoleMap.objects.filter(user_id=user_id_detail)
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = EditUserForm(request.POST,request)
		# check whether it's valid:
		if form.is_valid():
			user_name = request.POST['user_name']
			email = request.POST['email']
			is_active = request.POST['is_active']
			role = request.POST['role_list']
			if 'nmls_id' in request.POST:
				nmls_id = request.POST['nmls_id']
			else:
				nmls_id = None
			if 'phone' in request.POST:
				phone = request.POST['phone']
			else:
				phone = None
			if 'company' in request.POST:
				company = request.POST['company']
			else:
				company = None
			
			if 'fax' in request.POST:
				fax = request.POST['fax']
			else:
				fax = None

			UserMaster.objects.filter(id=user_id_detail.id).update(
									user_name = user_name,
									is_active = is_active,
									email=email,
									company_id=company_obj,
									nmls_id=nmls_id,
									created_by=user_obj,
									officer_company = company,
									phone=phone,
									fax=fax
									)
			role_obj = RoleMaster.objects.get(id=role)

			if(role_obj):
				UserRoleMap.objects.filter(user_id=user_id_detail).delete()
				userrolemap = UserRoleMap(
									user_id = user_id_detail,
									role_id = role_obj,
									is_active='Y',
									created_by=user_obj
									)
				userrolemap.save()
			return HttpResponseRedirect('/user/list/')
	else:
        
		form = EditUserForm()
	return render(request, 
					'user/edit.html',
					{'form': form,'role_list':role_master_obj,'user_id_detail':user_id_detail,'user_role_map':user_role_map,'role_feature':role_feature, 'user_obj':user_obj}
				)
				
def updateprofile(request):
	if(request.session.has_key('company_id') == False):
		return HttpResponseRedirect('/')
	company_id = request.session.get('company_id')
	company_obj = CompanyMaster.objects.get(id=company_id)
	role_master_obj = RoleMaster.objects.filter(company_id=company_obj)	
	user_id = request.session.get('user_id')
	
	print("user_id ===============",user_id)

	
	user_obj = UserMaster.objects.get(id=user_id)
	role_id = request.session.get('role_id')
	user_id_detail = UserMaster.objects.get(id=user_id)
	
	if role_id != None:
		role_obj = RoleMaster.objects.get(id=role_id)
		role_feature = RoleFeatureMap.objects.filter(role_id=role_obj).values_list('feature_id', flat=True)
		role_feature = list(role_feature)
	else:
		role_feature = []
	user_role_map = UserRoleMap.objects.filter(user_id=user_id_detail)
	print(" before post ")
	if request.method == 'POST':
		print(" aftr post ")
		
		form = UserProfileForm(request.POST,request)
		# check whether it's valid:
		if form.is_valid():
			user_name = request.POST['user_name']
			email = request.POST['email']
			
			if 'nmls_id' in request.POST:
				nmls_id = request.POST['nmls_id']
			else:
				nmls_id = None
			if 'phone' in request.POST:
				phone = request.POST['phone']
			else:
				phone = None
			if 'company' in request.POST:
				company = request.POST['company']
			else:
				company = None
			
			if 'fax' in request.POST:
				fax = request.POST['fax']
			else:
				fax = None

			UserMaster.objects.filter(id=user_id_detail.id).update(
									user_name = user_name,
									email=email,
									company_id=company_obj,
									nmls_id=nmls_id,
									created_by=user_obj,
									officer_company = company,
									phone=phone,
									fax=fax
									)
			return HttpResponseRedirect('/dashboard/')
			print(" success ")
	else:
        
		form = EditUserForm()
	return render(request, 
					'user/update.html',
					{'form': form,'role_list':role_master_obj,'user_id_detail':user_id_detail,'user_role_map':user_role_map,'role_feature':role_feature, 'user_obj':user_obj}
				)
	print(" unsuccess ")