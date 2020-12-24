from django import forms
from user.models import UserMaster 
from role.models import RoleMaster
from company.models import CompanyMaster
import hashlib 
class UserForm(forms.Form):
	CHOICES=[('Y','Yes'),
         ('N','No')]
	
	company_obj = CompanyMaster.objects.get(id=1)
	user_name = forms.CharField(label='User Name', max_length=50,
									widget=forms.TextInput(attrs={'class': 'form-control  py-3 pl-4','placeholder':'User Name','autocomplete':'off'})
									)
	user_id = forms.CharField(label='User Id', max_length=50,
									widget=forms.TextInput(attrs={'class': 'form-control py-3 pl-4','placeholder':'User Id','autocomplete':'off'})
									)
	password = forms.CharField(label='Password', max_length=50,
									widget=forms.PasswordInput(attrs={'class': 'form-control  py-3 pl-4','placeholder':'Password','autocomplete':'off'})
									)
	confirm_password = forms.CharField(label='Confirm Password', max_length=50,
									widget=forms.PasswordInput(attrs={'class': 'form-control py-3 pl-4','placeholder':'Confirm Password'})
									)
	email = forms.CharField(label='Email', max_length=50,
									widget=forms.EmailInput(attrs={'class': 'form-control  py-3 pl-4','placeholder':'Email','autocomplete':'off'})
									)
	is_active = forms.ChoiceField(choices=CHOICES, 
									widget=forms.RadioSelect(
											attrs={'class': 'form-control  py-3 pl-4','placeholder':'Email'}
										)
									)
	nmls_id =  forms.CharField(label='NMLS ID',required=False, max_length=50,
									widget=forms.TextInput(attrs={'class': 'form-control py-3 pl-4','placeholder':'NMLS Id'})
									)
	fax =  forms.CharField(label='Fax',required=False, max_length=50,
									widget=forms.TextInput(attrs={'class': 'form-control py-3 pl-4','placeholder':'Fax'})
									)
	
	def __init__(self, *args, **kwargs):
        # we explicit define the foo keyword argument, cause otherwise kwargs will 
        # contain it and passes it on to the super class, who fails cause it's not
        # aware of a foo keyword argument.
		self.company_code = kwargs.pop('company_code', None) # THIS PARAMETER
		super(UserForm, self).__init__(*args, **kwargs)
		if len(args)>1:
			request = args[1]
			self.company_id = request.session.get('company_id')
		else:
			self.company_id = None
		
	def clean(self):
		
		password = self.cleaned_data['password']
		confirm_password = self.cleaned_data['confirm_password']
		user_id = self.cleaned_data['user_id']
		print(self.company_id)
		company_obj = CompanyMaster.objects.get(id=self.company_id)
		if password and confirm_password:
			if password != confirm_password:
				raise forms.ValidationError("Confirm Password and Password  must match.")
		data = UserMaster.objects.filter(company_id=company_obj,
										user_id=user_id
										)
		if(data.count()>0):
			raise forms.ValidationError('User Id is already Exist')

class EditUserForm(forms.Form):
	CHOICES=[('Y','Yes'),
         ('N','No')]
	
	company_obj = CompanyMaster.objects.get(id=1)
	user_name = forms.CharField(label='User Name', max_length=50,
									widget=forms.TextInput(attrs={'class': 'form-control  py-3 pl-4','placeholder':'User Name'})
									)
	email = forms.CharField(label='Email', max_length=50,
									widget=forms.EmailInput(attrs={'class': 'form-control  py-3 pl-4','placeholder':'Email'})
									)
	is_active = forms.ChoiceField(choices=CHOICES, 
									widget=forms.RadioSelect(
											attrs={'class': 'form-control  py-3 pl-4','placeholder':'Email'}
										)
									)
	nmls_id =  forms.CharField(label='NMLS ID',required=False, max_length=50,
									widget=forms.TextInput(attrs={'class': 'form-control py-3 pl-4','placeholder':'NMLS Id'})
									)
	fax =  forms.CharField(label='Fax',required=False, max_length=50,
									widget=forms.TextInput(attrs={'class': 'form-control py-3 pl-4','placeholder':'Fax'})
									)
									
class UserProfileForm(forms.Form):
	CHOICES=[('Y','Yes'),
         ('N','No')]
	
	company_obj = CompanyMaster.objects.get(id=1)
	user_name = forms.CharField(label='User Name', max_length=50,
									widget=forms.TextInput(attrs={'class': 'form-control  py-3 pl-4','placeholder':'User Name'})
									)
	
	email = forms.CharField(label='Email', max_length=50,
									widget=forms.EmailInput(attrs={'class': 'form-control  py-3 pl-4','placeholder':'Email'})
									)
	
	nmls_id =  forms.CharField(label='NMLS ID',required=False, max_length=50,
									widget=forms.TextInput(attrs={'class': 'form-control py-3 pl-4','placeholder':'NMLS Id'})
									)
	fax =  forms.CharField(label='Fax',required=False, max_length=50,
									widget=forms.TextInput(attrs={'class': 'form-control py-3 pl-4','placeholder':'Fax'})
									)