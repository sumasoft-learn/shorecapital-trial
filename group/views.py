from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import GroupForm,EditGroupForm
from django.http import HttpResponseRedirect
from user.models import UserMaster,UserRoleMap 
from company.models import CompanyMaster
from role.models import RoleMaster,RoleFeatureMap
from django.core import serializers
from .models import GroupMaster,UserGroupMap
from django.db.models import Q
import hashlib 
# Create your views here.
# Login Request 
def checkaccess(self, feature_id):
    role_id = request.session.get('role_id')
    if role_id != None:
        role_obj = RoleMaster.objects.get(id=role_id)
        feature_obj = FeatureMaster.objects.get(id=feature_id)
        role_feature_count = RoleFeatureMap.objects.filter(role_id=role_obj,feature_id=feature_obj)
        if role_feature_count.count()>0:
            return True
        else:
            return False
    else:
        return False
def create(request):
	if(request.session.has_key('company_id') == False):
		return HttpResponseRedirect('/')
	company_id = request.session.get('company_id')
	company_obj = CompanyMaster.objects.get(id=company_id)

	user_master_obj = UserRoleMap.objects.filter(Q(role_id__role_type='Loan Processor',user_id__company_id=company_obj) | Q(role_id__role_type='Assistant',user_id__company_id=company_obj))
	user_id = request.session.get('user_id')
	user_obj = UserMaster.objects.get(id=user_id)
	role_id = request.session.get('role_id')
	if role_id != None:
		role_obj = RoleMaster.objects.get(id=role_id)
		role_feature = RoleFeatureMap.objects.filter(role_id=role_obj).values_list('feature_id', flat=True)
		role_feature = list(role_feature)
	else:
		role_feature = []
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = GroupForm(request.POST,request)
		# check whether it's valid:
		if form.is_valid():
			
			group_name = request.POST['group_name']
			user_list = request.POST.getlist('userlist[]')
			print(user_list)
			is_active = request.POST['is_active']
			groupmaster = GroupMaster(
									group_name = group_name,
									company_id=company_obj.id,
									status = is_active,
									created_by=user_obj
									)
			groupmaster.save()
			for user_id in user_list:
				user_grp_obj = UserMaster.objects.get(id=user_id)
				usergroupmap = UserGroupMap(
					user_id = user_grp_obj,
					group_id = groupmaster,
					created_by = user_obj
				)
				usergroupmap.save()
			return HttpResponseRedirect('/group/list/')
	else:
        
		form = GroupForm()
	return render(request, 
					'group/create.html',
					{'form': form,'user_list':user_master_obj,'company_id':company_id,'role_feature':role_feature,'user_obj':user_obj}
				)

# List of Users 
def index(request):
	if(request.session.has_key('company_id') == False):
		return HttpResponseRedirect('/')
	company_id = request.session.get('company_id')
	company_obj = CompanyMaster.objects.get(id=company_id)

	user_id = request.session.get('user_id')
	user_obj = UserMaster.objects.get(id=user_id)

	object_list = GroupMaster.objects.filter(company_id=company_id) #or any kind of queryset	
	role_id = request.session.get('role_id')
	if role_id != None:
		role_obj = RoleMaster.objects.get(id=role_id)
		role_feature = RoleFeatureMap.objects.filter(role_id=role_obj).values_list('feature_id', flat=True)
		role_feature = list(role_feature)
	else:
		role_feature = []
	return render(request, 
					'group/list.html',
					{'group_list':object_list,'role_feature':role_feature, 'user_obj':user_obj}
				)

def edit(request,group_id):
	if(request.session.has_key('company_id') == False):
		return HttpResponseRedirect('/')
	company_id = request.session.get('company_id')
	company_obj = CompanyMaster.objects.get(id=company_id)

	user_master_obj = UserRoleMap.objects.filter(Q(role_id__role_type='Loan Processor',user_id__company_id=company_obj) | Q(role_id__role_type='Assistant',user_id__company_id=company_obj))
	user_id = request.session.get('user_id')
	user_obj = UserMaster.objects.get(id=user_id)
	group_obj = GroupMaster.objects.filter(id=group_id)
	role_id = request.session.get('role_id')
	if role_id != None:
		role_obj = RoleMaster.objects.get(id=role_id)
		role_feature = RoleFeatureMap.objects.filter(role_id=role_obj).values_list('feature_id', flat=True)
		role_feature = list(role_feature)
	else:
		role_feature = []
	if(group_obj.count()==0):
		return HttpResponseRedirect('/group/list/')
	group_obj = GroupMaster.objects.get(id=group_id)
	user_grp_map_obj = UserGroupMap.objects.filter(group_id=group_obj.id)
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = EditGroupForm(request.POST,request)
		# check whether it's valid:
		if form.is_valid():
			user_list = request.POST.getlist('userlist[]')
			is_active = request.POST['is_active']
			groupmaster = GroupMaster.objects.get(pk = group_id)
			
			groupmaster_update = GroupMaster.objects.filter(id=groupmaster.id).update(status = is_active,updated_by=user_obj)
			UserGroupMap.objects.filter(group_id=groupmaster).delete()
			for user_id in user_list:
				user_grp_obj = UserMaster.objects.get(id=user_id)
				usergroupmap = UserGroupMap(
					user_id = user_grp_obj,
					group_id = groupmaster,
					created_by = user_obj
				)
				usergroupmap.save()
			return HttpResponseRedirect('/group/list/')
	else:
        
		form = EditGroupForm()
	return render(request, 
					'group/edit.html',
					{'form': form,'user_list':user_master_obj,'company_id':company_id,'group_obj':group_obj,'user_grp_map_obj':user_grp_map_obj,'role_feature':role_feature, 'user_obj':user_obj}
				)