from django import forms
from user.models import UserMaster 
from role.models import RoleMaster,RoleTypeMaster
from company.models import CompanyMaster
import hashlib 

class RoleForm(forms.Form):
	CHOICES=[('Y','Yes'),
         ('N','No')]
		 
	role_type_choices=(('A','Admin Type'),
         ('L','Loan Processor'),
         ('LO','Loan officer'),
         ('A','Assistant'))
	
	company_obj = CompanyMaster.objects.get(id=1)
	role_name = forms.CharField(label='Role Name', max_length=50,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Role Name'})
									)
	role_type = forms.ModelChoiceField(queryset=RoleTypeMaster.objects.filter(is_active='Y'),required=False, widget=forms.Select(
											attrs={'class': 'form-control','data-live-search':'true'}
										))
	# created_by = forms.CharField(label='Created By', max_length=50,
	# 								widget=forms.TextInput(attrs={'class': 'form-control py-3 pl-4','placeholder':'Created By'})
	# 								)								
	is_active = forms.ChoiceField(choices=CHOICES, 
									widget=forms.RadioSelect(
											attrs={'class': 'form-control','placeholder':'Active'}
										)
									)
									
	