from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import LoginForm,DashboardFileForm
from user.models import UserMaster
from company.models import CompanyMaster
from file.models import FileMaster,FileNoteMap,FileEscrowMap,LoanStatusMaster,LoanSubStatusMaster,TaxTranscriptMaster,ClosingDisclosureMaster,AppraisalOrderedMaster
from django.http import HttpResponseRedirect
from user.models import UserRoleMap
from role.models import RoleMaster,RoleFeatureMap
from datetime import datetime,date
from django.views.decorators.csrf import csrf_exempt
from group.models import GroupMaster, UserGroupMap
from role.models import RoleTypeMaster
from django.template import *
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.
# Login Request 
def date_convertion_create(date_formate):
    """
    Converting the date format to on single formate.
    """
    try:
        if len(date_formate)>1:
            convert_date = datetime.strptime(date_formate, '%m/%d/%Y')
            date_of_birth = convert_date.strftime("%Y/%m/%d")
            dob = datetime.strptime(date_of_birth, "%Y/%m/%d").date()
            return dob
        return None
    except Exception as e:
        return None
def company_list(request):
	company_list = CompanyMaster.objects.all()
	return render(request, 
					'login/company_list.html',
					{'company_list': company_list}
				)	
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
def index(request,company_code='testing123'):
	if(request.session.has_key('company_id') == True):
		return HttpResponseRedirect('/dashboard/')
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = LoginForm(request.POST,request,company_code=company_code)
		# check whether it's valid:
		if form.is_valid():
			company_code = company_code
			user_name = request.POST['user_name']
			data = UserMaster.objects.filter(company_id_id__company_code=company_code,
										user_id=user_name
										)
			user_role = UserRoleMap.objects.filter(user_id=data[0])
			if(user_role.count()>0):
				request.session['role_id'] = user_role[0].role_id.id
			else:
				request.session['role_id'] = None
			request.session['company_id'] = data[0].company_id.id
			request.session['company_code'] = company_code
			request.session['user_id'] = data[0].id
			request.session['user_name'] = data[0].user_name

			return HttpResponseRedirect('/dashboard/')
	else:
		form = LoginForm(company_code=company_code)
	return render(request, 
					'login/index.html',
					{'form': form}
				)

# Login Request 
def dashboard(request):
	if(request.session.has_key('company_id') == False):
		return HttpResponseRedirect('/')
	
	company_id = request.session['company_id']

	if 'transaction_info' in request.session:
		del request.session['transaction_info']

	if(request.session.has_key('is_create') == False):
		is_create_flag = False
	else:
		is_create_flag = request.session.get('is_create')
		if(is_create_flag == 'Y'):
			is_create_flag = True
		else:
			is_create_flag = False
	
	if(request.session.has_key('div_status_id') == False):
		div_status_id = None
	else:
		div_status_id =  request.session.get('div_status_id')
	
	if(request.session.has_key('div_sub_status_id') == False):
		div_sub_status_id = None
	else:
		div_sub_status_id =  request.session.get('div_sub_status_id')

	request.session['is_create'] ='N'
	request.session['div_status_id'] = None
	request.session['div_sub_status_id'] = None
	company_obj = CompanyMaster.objects.get(id=company_id)
	company_obj = CompanyMaster.objects.get(id=company_id)
	object_list = UserMaster.objects.filter(company_id=company_obj) #or any kind of queryset	
	user_id = request.session.get('user_id')
	
	user_obj = UserMaster.objects.get(id=user_id)
	role_id = request.session.get('role_id')
	user_role_type = RoleMaster.objects.get(id=role_id)
	
	
	if user_role_type.role_type == 'Admin Type':
		file_master = FileMaster.objects.filter(company_id=user_obj.company_id)
	else:
		file_master = []
		user_group_objs = UserGroupMap.objects.filter(user_id=user_obj)
		for group_obj in user_group_objs:
			file_master_assign_objs = FileMaster.objects.filter(assigned_group_id=group_obj.group_id).order_by('lock_expiration_date')
			for file_master_assign_obj in file_master_assign_objs:
				file_master.append(file_master_assign_obj)

		file_master_created_objs = FileMaster.objects.filter(created_by=user_obj).order_by('lock_expiration_date')
		for file_master_created_obj in file_master_created_objs:
			file_master.append(file_master_created_obj)

	for file_obj in file_master:
		file_escrow = FileEscrowMap.objects.filter(file_id=file_obj.id)
		if file_escrow.count() > 0:
			file_obj.escrow_company = file_escrow[0].company_name
			file_obj.escrow_opened_date = file_escrow[0].opened_date
		else:
			file_obj.escrow_company = None
			file_obj.escrow_opened_date = None
	role_id = request.session.get('role_id')
	if role_id != None:
		role_obj = RoleMaster.objects.get(id=role_id)
		role_feature = RoleFeatureMap.objects.filter(role_id=role_obj).values_list('feature_id', flat=True)
		role_feature = list(role_feature)
	else:
		role_feature = []

	status_obj = LoanStatusMaster.objects.filter(is_visible_dashboard= 'Y').order_by('sequence')
	for status_row in status_obj:
		substatus_obj = LoanSubStatusMaster.objects.filter(is_visible_dashboard= 'Y').order_by('sequence')
		status_row.substatus = substatus_obj
	form = DashboardFileForm()
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = DashboardFileForm(request.POST,request)
		# check whether it's valid:
		if form.is_valid():
			file_name = request.POST['file_id']
			tax_transcript = request.POST['tax_transcript']
			lender = request.POST['lender']
			status_id = request.POST['status_id']
			sub_status_id = request.POST['sub_status_id']
			closing_disclosure = request.POST['closing_disclosure']
			cd_date = request.POST['cd_date']
			appraisal_ordered = request.POST['appraisal_ordered']
			ad_date = request.POST['ad_date']
			tt_date = request.POST['tt_date']
			file_id = request.POST['id']
			escrow_opened = request.POST['escrow_opened']
			escrow_company = request.POST['escrow_company']
			note = request.POST['note']
			payoff_date = request.POST['payoff_date']
			div_status_id = request.POST['div_status_id']
			div_sub_status_id = request.POST['div_sub_status_id']
			request.session['div_status_id'] = div_status_id
			request.session['div_sub_status_id'] = div_sub_status_id
			if 'le_date_checkbox' in request.POST:
				le_date_checkbox = request.POST['le_date_checkbox']
				if( le_date_checkbox == 'on'):
					if len(request.POST['lock_expiration_date']) == 0:
						lock_expiration_date = None
					else:
						lock_expiration_date = date_convertion_create(request.POST['lock_expiration_date'])
				else:
					lock_expiration_date = None
			else:
				lock_expiration_date = None
			if len(request.POST['lock_expiration_date']) == 0:
				lock_expiration_date = None
			else:
				lock_expiration_date = request.POST['lock_expiration_date']
			if len(status_id)==0:
				status_obj = None
			else:
				status_obj = LoanStatusMaster.objects.get(id=status_id)
			if len(sub_status_id)==0:
				sub_status_obj = None
			else:
				sub_status_obj = LoanSubStatusMaster.objects.get(id=sub_status_id)
			if len(tax_transcript)==0:
				tax_transcript_obj = None
			else:
				tax_transcript_obj = TaxTranscriptMaster.objects.get(id=tax_transcript)
			if len(closing_disclosure)>0:
				closing_disclosure_obj = ClosingDisclosureMaster.objects.get(id=closing_disclosure)
			else:
				closing_disclosure_obj = None
			if len(appraisal_ordered)>0:
				appraisal_ordered_obj = AppraisalOrderedMaster.objects.get(id=appraisal_ordered)
				
			else:
				appraisal_ordered_obj = None
			id = int(file_id)
			if len(tt_date)==0:
				tt_date = None
			else:
				if tax_transcript_obj.id == 1 or tax_transcript_obj.id == 2 :
					tt_date = None
			if len(cd_date) == 0:
				cd_date = None
			else:
				if len(closing_disclosure) < 1 :
					cd_date = None
			if len(ad_date) == 0:
				ad_date = None
			else:
				if appraisal_ordered_obj.id == 5 or appraisal_ordered_obj.id == 7 :
					ad_date = ad_date
				else:
					ad_date = None
			if len(payoff_date) == 0:
				payoff_date = None
			if (len(note)==0):
				file_object = FileMaster.objects.filter(id=id)
				note= file_object[0].note

			if len(escrow_opened) == 0:
				escrow_opened = None
			
			
			file_object = FileMaster.objects.filter(id=id).update(
				lender=lender,
				status_id= status_obj,
				sub_status_id=sub_status_obj,
				file_id=file_name,
				tax_transcript=tax_transcript_obj,
				closing_disclosure=closing_disclosure_obj,
				appraisal_ordered=appraisal_ordered_obj,
				lock_expiration_date=date_convertion_create(lock_expiration_date),
				note=note,
				appraisal_ordered_date=date_convertion_create(ad_date),
				closing_disclosure_date=date_convertion_create(cd_date),
				tax_transcript_date=date_convertion_create(tt_date),
				payoff_exp=date_convertion_create(payoff_date)
			)
			file_escrow_object = FileEscrowMap.objects.filter(file_id=id).update(
				opened_date=date_convertion_create(escrow_opened),
				company_name= escrow_company
			)
			note_new = request.POST['note']
			if(len(note_new)>0):
				file_obj = FileMaster.objects.get(id=id)
				file_note_map = FileNoteMap(note=note,file_id=file_obj,created_by=user_obj)
				file_note_map.save()
			messages.add_message(request, messages.INFO, 'File Updated Successfully')
			request.session['is_create'] ='Y'
			return HttpResponseRedirect('/dashboard/')
	return render(request, 
					'dashboard/dashboard.html',
					{'div_sub_status_id':div_sub_status_id,'div_status_id':div_status_id,'all_file_master': file_master,'user_obj':user_obj,'role_feature':role_feature,'form':form,'status_obj':status_obj,'is_create_flag':is_create_flag}
				)
# Login Request 
def logout(request):
	company_code = None
	if(request.session.has_key('company_id') == True):
		company_code = request.session.get('company_code')
		request.session.flush()
		request.session.modified = True
		return HttpResponseRedirect('/'+company_code)
	return HttpResponseRedirect('/')

@csrf_exempt	
def noteHistory(request):
	if(request.session.has_key('company_id') == False):
		return HttpResponseRedirect('/')
	
	company_id = request.session['company_id']
	company_obj = CompanyMaster.objects.get(id=company_id)
	
	object_list = UserMaster.objects.filter(company_id=company_obj) #or any kind of queryset	
	user_id = request.session.get('user_id')
	user_obj = UserMaster.objects.get(id=user_id)
	if request.method == 'POST':
		file_id = request.POST['file_id']
		file_master = FileMaster.objects.get(id=file_id)
		file_history = FileNoteMap.objects.filter(file_id=file_master.id).order_by('-id')
		return render(request, 
						'dashboard/note_history.html',
						{'file_history': file_history, 'user_obj':user_obj}
					)

def editNote(request):
	if(request.session.has_key('company_id') == False):
		return HttpResponseRedirect('/')
	company_id = request.session['company_id']
	company_obj = CompanyMaster.objects.get(id=company_id)
	
	object_list = UserMaster.objects.filter(company_id=company_obj) #or any kind of queryset	
	user_id = request.session.get('user_id')
	user_obj = UserMaster.objects.get(id=user_id)
	note = request.GET.get('note_text', None)
	file_id = request.GET.get('edit_note_file_id', None)
	file_master = FileMaster.objects.filter(id=file_id)
	file_history = FileNoteMap.objects.filter(file_id=file_master[0])
	file_object = FileMaster.objects.filter(id=file_id).update(note=note)
	file_obj = FileMaster.objects.get(id=file_id)
	file_note_map = FileNoteMap(note=note,file_id=file_obj,created_by=user_obj)
	file_note_map.save()


	file_master = FileMaster.objects.get(id=file_id)
	file_history = FileNoteMap.objects.filter(file_id=file_master.id).order_by('-id')

	return render(request, 
					'dashboard/note_history.html',
					{'file_history': file_history, 'user_obj':user_obj}
				)