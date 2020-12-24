from django import forms
from user.models import UserMaster 
from role.models import RoleMaster
from company.models import CompanyMaster
from .models import GroupMaster,UserGroupMap
import hashlib 
class GroupForm(forms.Form):
    CHOICES=[('Y','Yes'),
         ('N','No')]
    group_name = forms.CharField(label='Group Name', max_length=50,
									widget=forms.TextInput(attrs={'class': 'form-control pl-4','placeholder':'Group Name'})
									)
    is_active = forms.ChoiceField(choices=CHOICES, 
									widget=forms.RadioSelect(
											attrs={'class': 'form-control  py-3 pl-4','placeholder':'Email'}
										)
									)
    def __init__(self, *args, **kwargs):
        # we explicit define the foo keyword argument, cause otherwise kwargs will 
        # contain it and passes it on to the super class, who fails cause it's not
        # aware of a foo keyword argument.
        if len(args)>0:
            self.company_id =args[0]['company_id'] # THIS PARAMETER
        else:
            self.company_id = None
        super(GroupForm, self).__init__(*args, **kwargs)
        #print()  # prints the value of the foo url conf param
    def clean(self):
        company_id = self.company_id
        company_obj = CompanyMaster.objects.get(id=company_id)
        group_name = self.cleaned_data['group_name']
        data = GroupMaster.objects.filter(company_id=company_obj.id,group_name=group_name)
        if(data.count()>0):
			#self.request.session['user_id'] = data[0].id
            raise forms.ValidationError('Group is already Exist')
class EditGroupForm(forms.Form):
    CHOICES=[('Y','Yes'),
         ('N','No')]

    is_active = forms.ChoiceField(choices=CHOICES, 
									widget=forms.RadioSelect(
											attrs={'class': 'form-control  py-3 pl-4','placeholder':'Email'}
										)
									)




			
		