from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import LoginForm
from user.models import UserMaster
from company.models import CompanyMaster
from file.models import FileMaster
from django.http import HttpResponseRedirect
# Create your views here.
# Login Request 
def index(request):
    if(request.session.has_key('is_admin') == True):
        print("code")
        #return HttpResponseRedirect('/superadmin/manage/')
    if request.method == 'POST':
		# create a form instance and populate it with data from the request:
        form = LoginForm(request.POST,request)
		# check whether it's valid:
        if form.is_valid():
            user_name = request.POST['user_name']
            data = UserMaster.objects.filter(
										user_id=user_name,
                                        user_type='ADMIN'
										)
            request.session['is_admin'] = 'Y'
            request.session['user_id'] = data[0].id
            request.session['user_name'] = data[0].user_name
            return HttpResponseRedirect('/superadmin/dashboard')
        else:
            return render(request, 
					'login/index.html',
					{'form': form}
				)
    else:
        form = LoginForm()
        return render(request, 
					'login/index.html',
					{'form': form}
				)
def dashboard(request):
    if(request.session.has_key('is_admin') == False):
	    return HttpResponseRedirect('/superadmin/')
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)
    company_master = CompanyMaster.objects.filter().order_by('-id')
    return render(request, 
					'superadmin/company/list.html',
					{'company_master': company_master}
				)