from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CompanyForm
from user.models import UserMaster,UserRoleMap 
from company.models import CompanyMaster
from role.models import RoleMaster,RoleTypeMaster,RoleFeatureMap,FeatureMaster
from django.http import HttpResponseRedirect
import hashlib 
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
# Create your views here.
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
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)
    if(request.session.has_key('is_admin') == False):
	    return HttpResponseRedirect('/superadmin/')
    if request.method == 'POST':
		# create a form instance and populate it with data from the request:
        form = CompanyForm(request.POST,request)
		# check whether it's valid:
        if form.is_valid():
            company_code = request.POST['company_code']
            #company_type = request.POST['company_type']
            company_name = request.POST['company_name']
            user_id = request.POST['user_id']
            is_active = request.POST['is_active']
            user_name = request.POST['user_name']
            password = request.POST['password']
            email = request.POST['email']
            encrypted_password = hashlib.md5(password.encode()) 
            companymaster = CompanyMaster(
									company_code = company_code,
									company_name = company_name,
									company_type = 'P',
									status = is_active,
									created_by=user_obj
									)
            companymaster.save()
            usermaster = UserMaster(
									user_id = user_id,
									user_name = user_name,
									password = encrypted_password.hexdigest(),
									is_active = 'Y',
									email=email,
									company_id=companymaster,
									created_by=user_obj
									)   
            usermaster.save()
            role_type_obj = RoleTypeMaster.objects.get(id=1)
            rolemaster = RoleMaster(
                                    role_name='admin',
                                    is_active = 'Y',
                                    role_type=role_type_obj,
                                    company_id=companymaster,
                                    )
            rolemaster.save()
            admin_feature_array = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
            for admin_feature_list in admin_feature_array:
                feature_obj = FeatureMaster.objects.get(id=admin_feature_list)
                rolefeaturemap = RoleFeatureMap(feature_id= feature_obj,role_id = rolemaster )
                rolefeaturemap.save()
            userrolemap = UserRoleMap(
									user_id = usermaster,
									role_id = rolemaster,
									is_active='Y',
									created_by=user_obj
									)
            userrolemap.save()
            thisdict =	{
                        "3": "Loan Officer",
                        "2": "Processor",
                        "4": "Assistant"
                        }
            for x, y in thisdict.items():
                role_type_obj = RoleTypeMaster.objects.get(id=x)
                rolemaster = RoleMaster(
                                    role_name=y,
                                    role_type=role_type_obj,
                                    is_active = 'Y',
                                    company_id=companymaster,
                                    )
                rolemaster.save()
                if x== '3':
                    admin_feature_array = [1,2,3,9,13,14,16,17,19,20]
                    for admin_feature_list in admin_feature_array:
                        feature_obj = FeatureMaster.objects.get(id=admin_feature_list)
                        rolefeaturemap = RoleFeatureMap(
                            feature_id= feature_obj,
                            role_id = rolemaster
                        )
                        rolefeaturemap.save()
                if x== '2':
                    admin_feature_array = [1,9,12,13,14,15,17,18,19,6,20]
                    for admin_feature_list in admin_feature_array:
                        feature_obj = FeatureMaster.objects.get(id=admin_feature_list)
                        rolefeaturemap = RoleFeatureMap(
                            feature_id= feature_obj,
                            role_id = rolemaster
                        )
                        rolefeaturemap.save()
                if x=='4':
                    admin_feature_array = [1,9,12,13,14,15,17,18,19,6,20]
                    for admin_feature_list in admin_feature_array:
                        feature_obj = FeatureMaster.objects.get(id=admin_feature_list)
                        rolefeaturemap = RoleFeatureMap(
                            feature_id= feature_obj,
                            role_id = rolemaster
                        )
                        rolefeaturemap.save()
            return HttpResponseRedirect('/superadmin/dashboard')
        else:
            return render(request, 
					'superadmin/company/create.html',
					{'form': form}
				)
    else:
        form = CompanyForm()
        return render(request, 
					'superadmin/company/create.html',
					{'form': form}
				)
    
