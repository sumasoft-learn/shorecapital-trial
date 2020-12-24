from django import forms
from user.models import UserMaster 
from file.models import TaxTranscriptMaster,LoanStatusMaster,LoanSubStatusMaster,ClosingDisclosureMaster,AppraisalOrderedMaster
import hashlib 
class LoginForm(forms.Form):
	user_name = forms.CharField(label='User Name', max_length=50,
									widget=forms.TextInput(attrs={'class': 'form-control pl-4','placeholder':'User Name'})
									)
	password = forms.CharField(label='Password', max_length=20,
									widget=forms.PasswordInput(attrs={'class': 'form-control  pl-4','placeholder':'Password'})
									)
	def __init__(self, *args, **kwargs):
        # we explicit define the foo keyword argument, cause otherwise kwargs will 
        # contain it and passes it on to the super class, who fails cause it's not
        # aware of a foo keyword argument.
		self.company_code = kwargs.pop('company_code', None) # THIS PARAMETER
		super(LoginForm, self).__init__(*args, **kwargs)
		print(self.company_code)  # prints the value of the foo url conf param
	def clean(self):
		company_code = self.company_code
		user_name = self.cleaned_data['user_name']
		password = self.cleaned_data['password']
		encrypted_password = hashlib.md5(password.encode()) 
		data = UserMaster.objects.filter(company_id_id__company_code=company_code,
										user_id__contains=user_name,
										password=encrypted_password.hexdigest()
										).filter(user_id=user_name)
		if(data.count()>0):
			#self.request.session['user_id'] = data[0].id
			self.user_name = data[0].id
		else:
			raise forms.ValidationError('User or Password is Invalid')
	
class DashboardFileForm(forms.Form):
	status_id = forms.ModelChoiceField(queryset=LoanStatusMaster.objects.filter(is_active='Y'),  widget=forms.Select(
											attrs={'class': 'form-control','data-live-search':'true'}
										))
	file_id = forms.CharField(label='File Name', max_length=20,
									widget=forms.TextInput(attrs={'class': 'form-control FileName','placeholder':'File Name'})
									)
	appraisal_ordered = forms.ModelChoiceField(queryset=AppraisalOrderedMaster.objects.filter(status='Y'), required=False, widget=forms.Select(
											attrs={'class': 'form-control AppraisalOrderedText ','data-live-search':'true'}
										))
	sub_status_id = forms.ModelChoiceField(queryset=LoanSubStatusMaster.objects.filter(is_active='Y'),  widget=forms.Select(
											attrs={'class': 'form-control SubStatus','data-live-search':'true'}
										))
	closing_disclosure = forms.ModelChoiceField(queryset=ClosingDisclosureMaster.objects.filter(status='Y'), required=False, widget=forms.Select(
											attrs={'class': 'form-control ClosingDisclosureText','data-live-search':'true'}
										))
	tax_transcript = forms.ModelChoiceField(queryset=TaxTranscriptMaster.objects.filter(status='Y'), required=False, widget=forms.Select(
											attrs={'class': 'form-control TaxTranscripts','data-live-search':'true'}
										))
	lender = forms.CharField(label='Lender', max_length=20,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control Lender','placeholder':'Lender'})
									)
	escrow_company = forms.CharField(label='Escrow Company', max_length=20, required=False,
									widget=forms.TextInput(attrs={'class': 'form-control EscrowCompany','placeholder':'Escrow Company'})
									)