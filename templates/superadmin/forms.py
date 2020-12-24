from django import forms
from user.models import UserMaster 
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
		super(LoginForm, self).__init__(*args, **kwargs)
		
	def clean(self):
		user_name = self.cleaned_data['user_name']
		password = self.cleaned_data['password']
		encrypted_password = hashlib.md5(password.encode()) 
		data = UserMaster.objects.filter(
										user_id=user_name,
                                        password=encrypted_password.hexdigest()
										)
		if(data.count()>0):
			#self.request.session['user_id'] = data[0].id
			self.user_name = data[0].id
		else:
			raise forms.ValidationError('User or Password is Invalid')
		