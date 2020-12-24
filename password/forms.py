from django import forms
from .models import PasswordMaster 
from user.models import UserMaster 
from role.models import RoleMaster
from company.models import CompanyMaster
import hashlib 
class PasswordForm(forms.ModelForm):
	
	company_obj = CompanyMaster.objects.get(id=1)
	current_password = forms.CharField(label='Current Password', max_length=30,
									widget=forms.TextInput(attrs={'class': 'form-control  py-3 pl-4','placeholder':'Current Password'})
									)
	new_password = forms.CharField(label='New Password', max_length=30,
									widget=forms.TextInput(attrs={'class': 'form-control  py-3 pl-4','placeholder':'New Password'})
									)
	confirm_password = forms.CharField(label='Confirm Password', max_length=40,
									widget=forms.TextInput(attrs={'class': 'form-control  py-3 pl-4','placeholder':'Confirm Password'})
									)
	
	def clean(self,*args,**kwargs):
	
		password1 = self.cleaned_data.get("new_password")
		password2 = self.cleaned_data.get("confirm_password")
		if password1 != password2:
			raise forms.ValidationError("The New Password does not match with the Confirm password.")
		if not password1:
			raise forms.ValidationError("Enter The New password.")
		if not password2:
			raise forms.ValidationError("Enter The Confirm password.")
		return super(PasswordForm,self).clean(*args,**kwargs)
		
		
	class Meta:
		model = PasswordMaster
		fields = '__all__'
		