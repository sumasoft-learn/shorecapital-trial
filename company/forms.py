from django import forms
from user.models import UserMaster 
from .models import CompanyMaster
import hashlib 
class CompanyForm(forms.Form):
    CHOICES=[('Y','Yes'),
         ('N','No')]
    company_type=[('P','Proccessor'),
         ('M','Mortgage Company')]
    company_code = forms.CharField(label='Company Code', max_length=50,
									widget=forms.TextInput(attrs={'class': 'form-control pl-4','placeholder':'Company Code'})
									)
    company_name = forms.CharField(label='Company Name', max_length=20,
									widget=forms.TextInput(attrs={'class': 'form-control  pl-4','placeholder':'Company Name'})
									)
    user_name = forms.CharField(label='Admin User Name', max_length=50,
									widget=forms.TextInput(attrs={'class': 'form-control  py-3 pl-4','placeholder':'Admin Name'})
									)
    user_id = forms.CharField(label='User Id', max_length=50,
									widget=forms.TextInput(attrs={'class': 'form-control py-3 pl-4','placeholder':'Admin Login Id'})
									)
    password = forms.CharField(label='Password', max_length=50,
									widget=forms.PasswordInput(attrs={'class': 'form-control  py-3 pl-4','placeholder':'Password'})
									)
    confirm_password = forms.CharField(label='Confirm Password', max_length=50,
									widget=forms.PasswordInput(attrs={'class': 'form-control py-3 pl-4','placeholder':'Confirm Password'})
									)
    is_active = forms.ChoiceField(choices=CHOICES, 
									widget=forms.RadioSelect(
											attrs={'class': 'form-control  py-3 pl-4','placeholder':'Email'}
										)
									)
    email = forms.CharField(label='Email', max_length=50,
									widget=forms.EmailInput(attrs={'class': 'form-control  py-3 pl-4','placeholder':'Email'})
									)
    def clean(self):
        company_code = self.cleaned_data['company_code']
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Confirm Password and Password  must match.")
        data = CompanyMaster.objects.filter(company_code=company_code)
        if(data.count()>0):
            raise forms.ValidationError('Company Code is already Exist')

		