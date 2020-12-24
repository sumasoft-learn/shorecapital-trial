from django import forms
from user.models import UserMaster 
from role.models import RoleMaster
from company.models import CompanyMaster
from django.forms import ClearableFileInput
from file.models import RateTypeMaster,LoanStatusMaster,LoanPurposeMaster,TermMaster,StateMaster,CompensationPayerTypeMaster,ImpoundMaster,OccupancyMaster,PropertyTypeMaster,PasswordTypeMaster, DocumentsTypeMaster, DocumentsType
from file.models import DateTracker
from file.models import LoanSubStatusMaster
from file.models import AppraisalOrderedMaster, TaxTranscriptMaster, ClosingDisclosureMaster
import hashlib 
class FileForm(forms.Form):
	improvement_type = [('made','Made'),
         ('to_be_made','To be made')]
	CHOICES=[('Y','Yes'),
         ('N','No')]

	deliver_disclosures=(('M','Manual'),
         ('D','Digital'))
	
	deliver_disclosures_type_value=(('B','Borrower'),
         ('L','Loan officer'))
	
	refinance_reverse_status = [('Counseled','Counseled'),
         ('Not counseled','Not counseled')]
	
	company_obj = CompanyMaster.objects.get(id=1)
	status = forms.ModelChoiceField(queryset=LoanStatusMaster.objects.filter(is_active='Y'), widget=forms.Select(
											attrs={'class': 'form-control'}
										))
	brokerage = forms.CharField(label='Brokerage', max_length=50, required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Brokerage'})
									)
	ae_name = forms.CharField(label='A/E Name', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'A/E Name'})
									)
	ae_fax = forms.CharField(label='A/E Fax', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'A/E Fax'})
									)
	ae_direct = forms.CharField(label='A/E Direct#', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'A/E Direct#'})
									)
	ae_email = forms.CharField(label='A/E Email', max_length=50,required=False,
									widget=forms.EmailInput(attrs={'class': 'form-control ','placeholder':'A/E Email'})
									)
	lo_name = forms.ModelChoiceField(queryset=UserMaster.objects.filter(is_active='Y'),required=False, widget=forms.Select(
											attrs={'class': 'form-control','data-live-search':'true'}
										))
	lo_fax = forms.CharField(label='L/O Fax', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'L/O Fax'})
									)
	lo_direct = forms.CharField(label='L/O Direct#', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'L/O Direct#'})
									)
	lo_email = forms.CharField(label='L/O Email', max_length=50,required=False,
									widget=forms.EmailInput(attrs={'class': 'form-control ','placeholder':'L/O Email'})
									)
	nmls_id = forms.CharField(label='NMLS ID', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'NMLS ID'})
									)
	lender = forms.CharField(label='Lender', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Lender'})
									)
	charge_processing_fee = forms.ChoiceField(choices=CHOICES, 
									widget=forms.RadioSelect(
											attrs={'class': 'form-check-input','placeholder':'Charge Processing Fee'}
										)
									)
	ae_company_id = forms.CharField(label='Company Id', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Company Id'})
									)
	#date = forms.DateTimeField(input_formats=['%d/%m/%Y'],widget=forms.DateTimeInput(attrs={'class': 'form-control','data-target': '#datetimepicker1'}))
	loan_purpose = forms.ModelChoiceField(queryset=LoanPurposeMaster.objects.filter(is_active='Y'),required=False, widget=forms.Select(
											attrs={'class': 'form-control','data-live-search':'true'}
										))
	
	reverse_status = forms.ChoiceField(choices=refinance_reverse_status, required=False,
									widget=forms.Select(
											attrs={'class': 'reverse_check form-check-input','placeholder':'reverse status'}
										)
									)
	
	rate_type = forms.ModelChoiceField(queryset=RateTypeMaster.objects.filter(is_active='Y'),required=False, widget=forms.Select(
											attrs={'class': 'form-control','data-live-search':'true'}
										))
	loan_amount = forms.CharField(label='Loan Amount:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'calculate_ltv form-control','placeholder':'Loan Amount:'})
									)
	subordination = forms.ChoiceField(choices=CHOICES, required=False,
									widget=forms.RadioSelect(
											attrs={'class': 'calculate_ltv form-check-input subordination','placeholder':'Subordination'}
										)
									)
	loan_number = forms.CharField(label='Loan Number:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Loan Number'})
									)
	appraised_value = forms.CharField(label='Appraised Value:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'calculate_ltv form-control','placeholder':'Appraised Value'})
									)
	piw = forms.ChoiceField(choices=CHOICES, required=False,
									widget=forms.RadioSelect(
											attrs={'class': 'form-check-input','placeholder':'PIW'}
										)
									)
	ltv = forms.CharField(label='LTV:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'LTV'})
									)
	cltv = forms.CharField(label='CLTV:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'CLTV'})
									)
	rate = forms.CharField(label='Rate:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Rate'})
									)
	float = forms.ChoiceField(choices=CHOICES, required=False,
									widget=forms.RadioSelect(
											attrs={'class': 'float_type form-check-input','placeholder':'Float'}
										)
									)
	property_type = forms.ModelChoiceField(queryset=PropertyTypeMaster.objects.filter(is_active='Y'),required=False, widget=forms.Select(
											attrs={'class': 'form-control','data-live-search':'true'}
										))
	occupancy_master = forms.ModelChoiceField(queryset=OccupancyMaster.objects.filter(is_active='Y'),required=False, widget=forms.Select(
											attrs={'class': 'form-control','data-live-search':'true'}
										))
	impound = forms.ModelChoiceField(queryset=ImpoundMaster.objects.filter(is_active='Y'),required=False, widget=forms.Select(
											attrs={'class': 'form-control','data-live-search':'true'}
										))
	program_code = forms.CharField(label='Program Code:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Program Code'})
									)
	compensation_payer_type = forms.ModelChoiceField(queryset=CompensationPayerTypeMaster.objects.filter(is_active='Y'),required=False, widget=forms.Select(
											attrs={'class': 'form-control','data-live-search':'true'}
										))
	lender_pd_comp = forms.CharField(label='Lender Pd. Comp:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Lender Pd. Comp'})
									)
	borrower_ysp = forms.CharField(label='Borrower YSP:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Borrower YSP'})
									)
	bwr_pd_comp = forms.CharField(label='Bwr. Pd. Comp:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Bwr. Pd. Comp'})
									)

	borrower_name = forms.CharField(label='Borrower Name:', max_length=50,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Borrower Name'})
								)
	borrower_phone = forms.CharField(label='Borrower Phone:', max_length=10,
									widget=forms.TextInput(attrs={'pattern':'\d*','class': 'form-control','autocomplete':'off'})
									)
	borrower_email = forms.CharField(label='Borrower Email:', max_length=50,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Borrower Email','autocomplete':'off'})
									)
	property_address = forms.CharField(label='Property Address:', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Property Address'})
									)
	property_city = forms.CharField(label='City:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'City'})
									)
	property_zipcode = forms.CharField(label='Zipcode:', max_length=20,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Zipcode'})
									)
	property_state = forms.ModelChoiceField(queryset=StateMaster.objects.filter(is_active='Y'),required=False, widget=forms.Select(
											attrs={'class': 'form-control'}
										))
	mailing_address = forms.CharField(label='Mailing Address:', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Mailing Address'})
									)
	mailing_city = forms.CharField(label='City:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'City'})
									)
	mailing_zipcode = forms.CharField(label='Zipcode:', max_length=20,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Zipcode'})
									)
	mailing_state = forms.ModelChoiceField(queryset=StateMaster.objects.filter(is_active='Y'), required=False,widget=forms.Select(
											attrs={'class': 'form-control'}
										))
	deliver_disclosures = forms.ChoiceField(choices=deliver_disclosures, required=False,
									widget=forms.RadioSelect(
											attrs={'class': 'form-check-input','placeholder':'Email'}
										)
									)
	url = forms.CharField(label='URL:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'URL'})
									)
	customer_id = forms.CharField(label='Customer Id:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Customer Id'})
									)
	deliver_disclosures_type = forms.ChoiceField(choices=deliver_disclosures_type_value, required=False,
									widget=forms.RadioSelect(
											attrs={'class': 'form-check-input','placeholder':'Email'}
										)
									)
	request_conditions_stips_from = forms.ChoiceField(choices=deliver_disclosures_type_value, required=False,
									widget=forms.RadioSelect(
											attrs={'class': 'form-check-input','placeholder':'Email'}
										)
									)

	charge_credit_report = forms.ChoiceField(choices=CHOICES, required=False,
									widget=forms.RadioSelect(
											attrs={'class': 'form-check-input','placeholder':'Charge Credit Report'}
										)
									)
	charge_appraisal = forms.ChoiceField(choices=CHOICES, required=False,
									widget=forms.RadioSelect(
											attrs={'class': 'form-check-input','placeholder':'Charge Appraisal'}
										)
									)
	escrow_company = forms.CharField(label='Escrow Company', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Escrow Company'})
									)
	escrow_number = forms.CharField(label='Escrow Number', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Escrow Number'})
									)	
	escrow_officer = forms.CharField(label='Escrow Officer', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Escrow Officer'})
									)
	escrow_phone = forms.CharField(label='Escrow Officer Phone', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Escrow Officer Phone','autocomplete':'off'})
									)
	escrow_email = forms.CharField(label='Escrow Officer Email', max_length=250,required=False,
									widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Escrow Officer Email','autocomplete':'off'})
									)	
	please_open = forms.ChoiceField(choices=CHOICES, required=False,
									widget=forms.RadioSelect(
											attrs={'class': 'please_open_check form-check-input','placeholder':'Please Open'}
										)
									)
	escrow_assistant = forms.CharField(label='Escrow Assistant', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Escrow Assistant'})
									)
	assistant_phone = forms.CharField(label='Assistant Phone', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Assistant Phone','autocomplete':'off'})
									)
	assistant_email = forms.CharField(label='Assistant Email', max_length=250,required=False,
									widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Assistant Email','autocomplete':'off'})
									)
	title = forms.CharField(label='Title', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Title'})
									)
	title_order = forms.CharField(label='Title Order', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Title Order'})
									)
	title_rep = forms.CharField(label='Title Rep', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Title Rep'})
									)
	title_rep_phone = forms.CharField(label='Title Rep Phone', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Title Rep Phone'})
									)
	title_rep_email = forms.CharField(label='Title Rep Email', max_length=250,required=False,
									widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Title Rep Email'})
									)	
	hoa = forms.CharField(label='HOA', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'HOA'})
									)
	hoa_phone = forms.CharField(label='HOA Phone', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'HOA Phone','autocomplete':'off'})
									)
	hoa_email = forms.CharField(label='HOA Email', max_length=250,required=False,
									widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'HOA Email','autocomplete':'off'})
									)
	listing_office = forms.CharField(label='Listing Office', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Listing Office'})
									)
	listing_agent = forms.CharField(label='Listing Agent', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Listing Agent'})
									)
	listing_agent_phone = forms.CharField(label='L/Agent Phone', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'L/Agent Phone'})
									)
	listing_agent_email = forms.CharField(label='L/Agent Email', max_length=250,required=False,
									widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'L/Agent Email'})
									)
	buyer_office = forms.CharField(label='Buyer RE Office', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Buyer RE Office'})
									)
	buyer_agent = forms.CharField(label='Buyer Agent', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Buyer Agent'})
									)
	buyer_agent_phone = forms.CharField(label='B/Agent Phone', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'B/Agent Phone'})
									)
	buyer_agent_email = forms.CharField(label='B/Agent Email', max_length=250,required=False,
									widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'B/Agent Email'})
									)
	requested_escrow_fees = forms.ChoiceField(choices=CHOICES, required=False,
									widget=forms.RadioSelect(
											attrs={'class': 'form-check-input','placeholder':'Has Loan Officer Requested Escrow Fees'}
										)
									)
	
	term = forms.ModelChoiceField(queryset=TermMaster.objects.filter(is_active='Y'),required=False, widget=forms.Select(
											attrs={'class': 'form-control','data-live-search':'true'}
										))	
	password_type = forms.ModelChoiceField(queryset=PasswordTypeMaster.objects.filter(is_active='Y'),required=False, widget=forms.Select(
											attrs={'class': 'form-control','data-live-search':'true'}
										))
	password_name = forms.CharField(label='Password Name', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Password Name'})
									)
	user_name = forms.CharField(label='Password Name', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'User Name'})
									)
	user_password = forms.CharField(label='Password', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'User Password'})
									)
	user_password_url = forms.CharField(label='URL', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'URL'})
									)	
	va_base_loan = forms.CharField(label='VA BASE LOAN', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'VA BASE LOAN'})
									)	
	va_base_ff = forms.CharField(label='VA BASE + FF', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'VA BASE + FF'})
									)	
	fha_base_loan = forms.CharField(label='FHA BASE LOAN', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'FHA BASE LOAN'})
									)	
	fha_base_mip = forms.CharField(label='FHA BASE + MIP', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'FHA BASE + MIP'})
									)
	appraisal_ordered = forms.ModelChoiceField(queryset=AppraisalOrderedMaster.objects.filter(status='Y'), required=False, widget=forms.Select(
											attrs={'class': 'form-control AppraisalOrderedText ','data-live-search':'true'}
										))
	sub_status_id = forms.ModelChoiceField(queryset=LoanSubStatusMaster.objects.filter(is_active='Y'), required=True, widget=forms.Select(
											attrs={'class': 'form-control SubStatus'}
										))
	assigned_user_id = forms.ModelChoiceField(queryset=UserMaster.objects.filter(is_active='Y'), required=False,widget=forms.Select(
											attrs={'class': 'form-control Assign processor'}
										))
	closing_disclosure = forms.ModelChoiceField(queryset=ClosingDisclosureMaster.objects.filter(status='Y'), required=False, widget=forms.Select(
											attrs={'class': 'form-control ClosingDisclosureText','data-live-search':'true'}
										))
	tax_transcript = forms.ModelChoiceField(queryset=TaxTranscriptMaster.objects.filter(status='Y'), required=False, widget=forms.Select(
											attrs={'class': 'form-control TaxTranscripts','data-live-search':'true'}
										))
	

class UpdateFileForm(forms.Form):
	improvement_type = [('made','Made'),
         ('to_be_made','To be made')]
	CHOICES=[('Y','Yes'),
         ('N','No')]

	deliver_disclosures=(('M','Manual'),
         ('D','Digital'))
	
	deliver_disclosures_type_value=(('B','Borrower'),
         ('L','Loan officer'))
	
	refinance_reverse_status = [('Counseled','Counseled'),
         ('Not counseled','Not counseled')]

	company_obj = CompanyMaster.objects.get(id=1)
	status = forms.ModelChoiceField(queryset=LoanStatusMaster.objects.filter(is_active='Y'), widget=forms.Select(
											attrs={'class': 'form-control','data-live-search':'true'}
										))
	brokerage = forms.CharField(label='Brokerage', max_length=50, required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Brokerage'})
									)
	ae_name = forms.CharField(label='A/E Name', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'A/E Name'})
									)
	ae_fax = forms.CharField(label='A/E Fax', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'A/E Fax'})
									)
	ae_direct = forms.CharField(label='A/E Direct#', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'A/E Direct#'})
									)
	ae_email = forms.CharField(label='A/E Email', max_length=50,required=False,
									widget=forms.EmailInput(attrs={'class': 'form-control ','placeholder':'A/E Email'})
									)
	lo_name = forms.ModelChoiceField(queryset=UserMaster.objects.filter(is_active='Y'),required=False, widget=forms.Select(
											attrs={'class': 'form-control','data-live-search':'true'}
										))
	lo_fax = forms.CharField(label='L/O Fax', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'L/O Fax'})
									)
	lo_direct = forms.CharField(label='L/O Direct#', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'L/O Direct#'})
									)
	lo_email = forms.CharField(label='L/O Email', max_length=50,required=False,
									widget=forms.EmailInput(attrs={'class': 'form-control ','placeholder':'L/O Email'})
									)
	nmls_id = forms.CharField(label='NMLS ID', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'NMLS ID'})
									)
	lender = forms.CharField(label='Lender', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Lender'})
									)
	charge_processing_fee = forms.ChoiceField(choices=CHOICES, 
									widget=forms.RadioSelect(
											attrs={'class': 'form-check-input','placeholder':'Charge Processing Fee'}
										)
									)
	ae_company_id = forms.CharField(label='Company Id', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Company Id'})
									)
	#date = forms.DateTimeField(input_formats=['%d/%m/%Y'],widget=forms.DateTimeInput(attrs={'class': 'form-control','data-target': '#datetimepicker1'}))
	loan_purpose = forms.ModelChoiceField(queryset=LoanPurposeMaster.objects.filter(is_active='Y'),required=False, widget=forms.Select(
											attrs={'class': 'form-control','data-live-search':'true'}
										))
	reverse_status = forms.ChoiceField(choices=refinance_reverse_status, required=False,
									widget=forms.Select(
											attrs={'class': 'form-control','placeholder':'Reverse Status'}
										)
									)
	rate_type = forms.ModelChoiceField(queryset=RateTypeMaster.objects.filter(is_active='Y'),required=False, widget=forms.Select(
											attrs={'class': 'form-control','data-live-search':'true'}
										))
	loan_amount = forms.CharField(label='Loan Amount:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'calculate_ltv form-control','placeholder':'Loan Amount:'})
									)
	subordination = forms.ChoiceField(choices=CHOICES, required=False,
									widget=forms.RadioSelect(
											attrs={'class': 'calculate_ltv form-check-input subordination','placeholder':'Subordination'}
										)
									)
	loan_number = forms.CharField(label='Loan Number:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Loan Number'})
									)
	appraised_value = forms.CharField(label='Appraised Value:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'calculate_ltv form-control','placeholder':'Appraised Value'})
									)
	piw = forms.ChoiceField(choices=CHOICES, required=False,
									widget=forms.RadioSelect(
											attrs={'class': 'form-check-input','placeholder':'PIW'}
										)
									)
	ltv = forms.CharField(label='LTV:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'LTV'})
									)
	cltv = forms.CharField(label='CLTV:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'CLTV'})
									)
	rate = forms.CharField(label='Rate:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Rate'})
									)
	float = forms.ChoiceField(choices=CHOICES, required=False,
									widget=forms.RadioSelect(
											attrs={'class': 'float_type form-check-input','placeholder':'Float'}
										)
									)
	property_type = forms.ModelChoiceField(queryset=PropertyTypeMaster.objects.filter(is_active='Y'),required=False, widget=forms.Select(
											attrs={'class': 'form-control','data-live-search':'true'}
										))
	occupancy_master = forms.ModelChoiceField(queryset=OccupancyMaster.objects.filter(is_active='Y'),required=False, widget=forms.Select(
											attrs={'class': 'form-control','data-live-search':'true'}
										))
	impound = forms.ModelChoiceField(queryset=ImpoundMaster.objects.filter(is_active='Y'),required=False, widget=forms.Select(
											attrs={'class': 'form-control','data-live-search':'true'}
										))
	program_code = forms.CharField(label='Program Code:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Program Code'})
									)
	compensation_payer_type = forms.ModelChoiceField(queryset=CompensationPayerTypeMaster.objects.filter(is_active='Y'),required=False, widget=forms.Select(
											attrs={'class': 'form-control','data-live-search':'true'}
										))
	lender_pd_comp = forms.CharField(label='Lender Pd. Comp:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Lender Pd. Comp'})
									)
	borrower_ysp = forms.CharField(label='Borrower YSP:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Borrower YSP'})
									)
	bwr_pd_comp = forms.CharField(label='Bwr. Pd. Comp:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Bwr. Pd. Comp'})
									)

	borrower_name = forms.CharField(label='Borrower Name:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Borrower Name'})
								)
	borrower_phone = forms.CharField(label='Borrower Phone:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'(123) 456–7890','pattern':'/^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/'})
									)
	borrower_email = forms.CharField(label='Borrower Email:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Borrower Email'})
									)
	property_address = forms.CharField(label='Property Address:', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Property Address'})
									)
	property_city = forms.CharField(label='City:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'City'})
									)
	property_zipcode = forms.CharField(label='Zipcode:', max_length=20,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Zipcode'})
									)
	property_state = forms.ModelChoiceField(queryset=StateMaster.objects.filter(is_active='Y'),required=False, widget=forms.Select(
											attrs={'class': 'form-control'}
										))
	mailing_address = forms.CharField(label='Mailing Address:', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Mailing Address'})
									)
	mailing_city = forms.CharField(label='City:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'City'})
									)
	mailing_zipcode = forms.CharField(label='Zipcode:', max_length=20,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Zipcode'})
									)
	mailing_state = forms.ModelChoiceField(queryset=StateMaster.objects.filter(is_active='Y'), required=False,widget=forms.Select(
											attrs={'class': 'form-control'}
										))
	deliver_disclosures = forms.ChoiceField(choices=deliver_disclosures, required=False,
									widget=forms.RadioSelect(
											attrs={'class': 'form-check-input','placeholder':'Email'}
										)
									)
	url = forms.CharField(label='URL:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'URL'})
									)
	customer_id = forms.CharField(label='Customer Id:', max_length=50,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Customer Id'})
									)
	deliver_disclosures_type = forms.ChoiceField(choices=deliver_disclosures_type_value, required=False,
									widget=forms.RadioSelect(
											attrs={'class': 'form-check-input','placeholder':'Email'}
										)
									)
	request_conditions_stips_from = forms.ChoiceField(choices=deliver_disclosures_type_value, required=False,
									widget=forms.RadioSelect(
											attrs={'class': 'form-check-input','placeholder':'Email'}
										)
									)

	charge_credit_report = forms.ChoiceField(choices=CHOICES, required=False,
									widget=forms.RadioSelect(
											attrs={'class': 'form-check-input','placeholder':'Charge Credit Report'}
										)
									)
	charge_appraisal = forms.ChoiceField(choices=CHOICES, required=False,
									widget=forms.RadioSelect(
											attrs={'class': 'form-check-input','placeholder':'Charge Appraisal'}
										)
									)
	escrow_company = forms.CharField(label='Escrow Company', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Escrow Company'})
									)
	escrow_number = forms.CharField(label='Escrow Number', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Escrow Number'})
									)	
	escrow_officer = forms.CharField(label='Escrow Officer', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Escrow Officer'})
									)
	escrow_phone = forms.CharField(label='Escrow Officer Phone', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Escrow Officer Phone'})
									)
	escrow_email = forms.CharField(label='Escrow Officer Email', max_length=250,required=False,
									widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Escrow Officer Email'})
									)	
	please_open = forms.ChoiceField(choices=CHOICES, required=False,
									widget=forms.RadioSelect(
											attrs={'class': 'please_open_check form-check-input','placeholder':'Please Open'}
										)
									)
	escrow_assistant = forms.CharField(label='Escrow Assistant', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Escrow Assistant'})
									)
	assistant_phone = forms.CharField(label='Assistant Phone', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Assistant Phone'})
									)
	assistant_email = forms.CharField(label='Assistant Email', max_length=250,required=False,
									widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Assistant Email'})
									)
	title = forms.CharField(label='Title', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Title'})
									)
	title_order = forms.CharField(label='Title Order', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Title Order'})
									)
	title_rep = forms.CharField(label='Title Rep', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Title Rep'})
									)
	title_rep_phone = forms.CharField(label='Title Rep Phone', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Title Rep Phone'})
									)
	title_rep_email = forms.CharField(label='Title Rep Email', max_length=250,required=False,
									widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Title Rep Email'})
									)	
	hoa = forms.CharField(label='HOA', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'HOA'})
									)
	hoa_phone = forms.CharField(label='HOA Phone', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'HOA Phone'})
									)
	hoa_email = forms.CharField(label='HOA Email', max_length=250,required=False,
									widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'HOA Email'})
									)
	listing_office = forms.CharField(label='Listing Office', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Listing Office'})
									)
	listing_agent = forms.CharField(label='Listing Agent', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Listing Agent'})
									)
	listing_agent_phone = forms.CharField(label='L/Agent Phone', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'L/Agent Phone'})
									)
	listing_agent_email = forms.CharField(label='L/Agent Email', max_length=250,required=False,
									widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'L/Agent Email'})
									)
	buyer_office = forms.CharField(label='Buyer RE Office', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Buyer RE Office'})
									)
	buyer_agent = forms.CharField(label='Buyer Agent', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Buyer Agent'})
									)
	buyer_agent_phone = forms.CharField(label='B/Agent Phone', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'B/Agent Phone'})
									)
	buyer_agent_email = forms.CharField(label='B/Agent Email', max_length=250,required=False,
									widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'B/Agent Email'})
									)
	requested_escrow_fees = forms.ChoiceField(choices=CHOICES, required=False,
									widget=forms.RadioSelect(
											attrs={'class': 'form-check-input','placeholder':'Has Loan Officer Requested Escrow Fees'}
										)
									)
	
	term = forms.ModelChoiceField(queryset=TermMaster.objects.filter(is_active='Y'),required=False, widget=forms.Select(
											attrs={'class': 'form-control','data-live-search':'true'}
										))	
	password_type = forms.ModelChoiceField(queryset=PasswordTypeMaster.objects.filter(is_active='Y'),required=False, widget=forms.Select(
											attrs={'class': 'form-control','data-live-search':'true'}
										))
	password_name = forms.CharField(label='Password Name', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Password Name'})
									)
	user_name = forms.CharField(label='Password Name', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'User Name'})
									)
	user_password = forms.CharField(label='Password', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'User Password'})
									)
	user_password_url = forms.CharField(label='URL', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'URL'})
									)	
	va_base_loan = forms.CharField(label='VA BASE LOAN', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'VA BASE LOAN'})
									)	
	va_base_ff = forms.CharField(label='VA BASE + FF', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'VA BASE + FF'})
									)	
	fha_base_loan = forms.CharField(label='FHA BASE LOAN', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'FHA BASE LOAN'})
									)	
	fha_base_mip = forms.CharField(label='FHA BASE + MIP', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'FHA BASE + MIP'})
									)
	# Property Detail Page
	construction_lot_year = forms.CharField(label='Year Lot Acquired', max_length=250,required=False,
									widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Year Lot Acquired'})
									)	
	construction_amount = forms.CharField(label='Amount Existing Liens', max_length=250,required=False,
									widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Amount Existing Liens'})
									)
	construction_original_cost = forms.CharField(label='Original Cost', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Original Cost'})
									)	
	construction_present_value = forms.CharField(label='Present Value of Lot', max_length=250,required=False,
									widget=forms.NumberInput(attrs={'class': 'form-control sum_add','placeholder':'Present Value of Lot'})
									)	
	construction_cost = forms.CharField(label='Cost of Improvements', max_length=250,required=False,
									widget=forms.NumberInput(attrs={'class': 'form-control sum_add','placeholder':'Cost of Improvements'})
									)	
	construction_total = forms.CharField(label='Total', max_length=250,required=False,
									widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Total'})
									)	
	refinance_lot_year = forms.CharField(label='Year Lot Acquired', max_length=250,required=False,
									widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Year Lot Acquired'})
									)	
	refinance_amount = forms.CharField(label='Amount Existing Liens', max_length=250,required=False,
									widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Amount Existing Liens'})
									)
	refinance_original_cost = forms.CharField(label='Original Cost', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Original Cost'})
									)	
	refinance_purpose = forms.CharField(label='Purpose of Refinance', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Purpose of Refinance'})
									)	
	refinance_cost = forms.CharField(label='Cost', max_length=250,required=False,
									widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Cost'})
									)	
	refinance_describe_improvements = forms.ChoiceField(required=False,choices=improvement_type, 
									widget=forms.RadioSelect(
											attrs={'class': 'form-check-input','placeholder':'PIW'}
										)
									)
	no_of_units = forms.CharField(label='No. of Units', max_length=250,required=False,
									widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'No. of Units'})
									)
	year_built = forms.CharField(label='Year Built', max_length=250,required=False,
									widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Year Built'})
									)
	source_of_down = forms.CharField(label='Source of Down Payment, Settlement Charges and/or Subordinate Financing (explain):', max_length=180,required=False,
									widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'Source of Down Payment, Settlement Charges and/or Subordinate Financing (explain):'})
									)	
	agency_case_number = forms.CharField(label='Agency Case Number', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Agency Case Number'})
									)
	lender_case_number = forms.CharField(label='Lender Case Number', max_length=250,required=False,
									widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Lender Case Number'})
									)
	
	appraisal_ordered = forms.ModelChoiceField(queryset=AppraisalOrderedMaster.objects.filter(status='Y'), required=False, widget=forms.Select(
											attrs={'class': 'form-control AppraisalOrderedText ','data-live-search':'true'}
										))
	sub_status_id = forms.ModelChoiceField(queryset=LoanSubStatusMaster.objects.filter(is_active='Y'), required=True, widget=forms.Select(
											attrs={'class': 'form-control SubStatus'}
										))
	assigned_user_id = forms.ModelChoiceField(queryset=UserMaster.objects.filter(is_active='Y'), required=False, widget=forms.Select(
											attrs={'class': 'form-control Assign processor'}
										))
	closing_disclosure = forms.ModelChoiceField(queryset=ClosingDisclosureMaster.objects.filter(status='Y'), required=False, widget=forms.Select(
											attrs={'class': 'form-control ClosingDisclosureText','data-live-search':'true'}
										))
	tax_transcript = forms.ModelChoiceField(queryset=TaxTranscriptMaster.objects.filter(status='Y'), required=False, widget=forms.Select(
											attrs={'class': 'form-control TaxTranscripts','data-live-search':'true'}
										))

	# Property Detail Page	
		

class DocumentUpload(forms.ModelForm):
    # document_type_id = forms.ModelChoiceField(queryset=DocumentsType.objects.filter(is_active='Y'),required=False, widget=forms.Select(
	# 										attrs={'class': 'form-control','data-live-search':'true', 'aria-expanded':'true'}
	# 									))
    class Meta:
        model = DocumentsTypeMaster
        fields = ['document_file_path']
        widgets = {
            'document_file_path': ClearableFileInput(attrs={'multiple': True, 'class':"form-control-file"}),
        }


class DateTrackerForm(forms.ModelForm):
    class Meta:
        model = DateTracker
        fields = '__all__'