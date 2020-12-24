from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.core import serializers
import hashlib 
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import check_password
from password.forms import PasswordForm
from user.forms import UserForm 
from user.models import UserMaster,UserRoleMap
from password.models import PasswordMaster
import hashlib 


# Reset Password 
def changepassword(request, user_id):
	if(request.session.has_key('company_id') == False):
		return HttpResponseRedirect('/')
	
	company_user_id = request.session['user_id']
	if request.method == 'POST':	
		# user_id =request.session['user_id']	
		user_data = UserMaster.objects.filter(id=user_id)
		old_password = user_data[0].password	
		form = PasswordForm(request.POST)
		
		if form.is_valid():		
			data = form.cleaned_data
			current_password =data['current_password']

			encrypted_password = hashlib.md5(current_password.encode())
			current_password = encrypted_password.hexdigest()

			if old_password == current_password:			
				if data['new_password'] == data['confirm_password']:
				
					form = PasswordMaster.objects.create(
						current_password= data['current_password'],
						confirm_password= data['confirm_password']
						)
					
					confirm_password= data['confirm_password']
					encrypted_password = hashlib.md5(confirm_password.encode())
					confirm_password = encrypted_password.hexdigest()

					UserMaster.objects.filter(id=user_id).update(password = confirm_password)
					print(" save Password successfully ",)
					
					#user_form =form.save()
					#update_session_auth_hash(request, user_form)
					print("old_password --- ",old_password)
					print("current_password --- ",data['current_password'])
					print("new_password --- ",data['new_password'])
					print("new_password --- ",data['new_password'])
					

					messages.success(request, _('Your password was successfully updated!'))
					return HttpResponseRedirect('/dashboard/')
				else:
					print(" both pass are not match")
					raise form.ValidationError(_("New Password does not match with the Confirm password"))
			else:
				print("old password not match ")
				messages.error(request, _('Current Password is Invalid.'))
		else:
			messages.error(request, _('Please correct the error below.'))
	else:
		form = PasswordForm()
	return render(request, 
					'password/create.html',
					{'form': form, 'company_user_id':company_user_id}, 
				)