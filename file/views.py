import hashlib
from datetime import datetime
import zipfile
import mimetypes  
import requests
import json
from django.core import serializers
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import os
from django.http import JsonResponse
from django_drf_filepond.models import TemporaryUpload
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from company.models import CompanyMaster
from role.models import RoleMaster,RoleFeatureMap
from file.models import (
    CompensationPayerTypeMaster, FileCoBorrower,
    FileEscrowMap, FileHoa, FileListingBuyer, FileMaster,
    FilePassword, FilePropertyMap, FileTitleMap,
    ImpoundMaster, LoanPurposeMaster, LoanStatusMaster,
    OccupancyMaster, PasswordTypeMaster,
    PropertyTypeMaster, RateTypeMaster, StateMaster,
    TermMaster, BorrowerEmploymentDetails, BorrowerAdditionalEmploymentDetails,
    CoBorrowerAdditionalEmploymentDetails, CoBorrowerEmploymentDetails,
    DeclarationMap,DetailsTransactionMap, FileLiabilities, FileAssets,
    FileMortage, FileExpensesCoBorrower, FileExpensesBorrower,
    FileHouseExpensesPresent, FileHouseExpensesProposed,
    FileLiabilitiesPledgedAssets, FileSavingsAccount
)
from group.models import GroupMaster
from role.models import RoleMaster
from user.models import UserMaster, UserRoleMap
from datetime import datetime
from .forms import FileForm,UpdateFileForm
from .forms import DocumentUpload, DateTrackerForm
from .models import DocumentsTypeMaster, DocumentsType, DateTracker,LoanSubStatusMaster, TaxTranscriptMaster, ClosingDisclosureMaster, AppraisalOrderedMaster
from login.forms import DashboardFileForm
from .models import FileNoteMap
from role.models import RoleFeatureMap,FeatureMaster
from group.models import UserGroupMap
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse

# Create your views here.
# Login Request

def date_convertion(date_formate):
    """
    Converting the date format to on single formate.
    """
    try:
        if len(date_formate)>1:
            convert_date = datetime.strptime(date_formate, '%Y%m%d')
            date_of_birth = convert_date.strftime("%m/%d/%Y")
            dob = datetime.strptime(date_of_birth, "%m/%d/%Y").date()
            return dob
        return None
    except Exception:
        return None
def date_convertion_create(date_formate):
    """
    Converting the date format to on single formate.
    """
    try:
        if len(date_formate)>1:
            convert_date = datetime.strptime(date_formate, '%m/%d/%Y')
            date_of_birth = convert_date.strftime("%Y/%m/%d")
            dob = datetime.strptime(date_of_birth, "%Y/%m/%d").date()
            return dob
        return None
    except Exception as e:
        return None

def create(request):
    if(request.session.has_key('company_id') == False):
        return HttpResponseRedirect('/')
    Boolen_field = {
        'Yes': True,
        'No': False
    }
    company_id = request.session.get('company_id')
    company_obj = CompanyMaster.objects.get(id=company_id)
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)
    role_id = request.session.get('role_id')
    if role_id != None:
        role_obj = RoleMaster.objects.get(id=role_id)
        role_feature = RoleFeatureMap.objects.filter(role_id=role_obj).values_list('feature_id', flat=True)
        role_feature = list(role_feature)
    else:
        role_feature = []
    if '2' not in role_feature:
	    return HttpResponseRedirect('/dashboard/')
    if role_obj.role_type == 'Admin Type':
        user_obj.email = ''
    if role_obj.role_type == 'Admin Type':
        user_obj.fax = ''
    loan_officers_list = []
    loan_officers = RoleMaster.objects.filter(company_id=company_id, role_type='Loan officer')
    for officers in loan_officers:
        user_role = UserRoleMap.objects.filter(role_id=officers.id)
        for role in user_role:
            users = UserMaster.objects.filter(id=role.user_id.id)
            for i in users:
                loan_officers_list.append(i)

    assign_processor_list = UserRoleMap.objects.filter(role_id__role_type='Loan Processor', role_id__company_id=company_obj)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FileForm(request.POST, request)
        if form.is_valid():
            # File Master
            filepound_files = request.POST.getlist('filepond')
            status_id = request.POST['status']
            status_obj = LoanStatusMaster.objects.get(id=status_id)
            brokerage = request.POST['brokerage']
            loan_officer_id = None
            if 'lo_name' in request.POST:
                loan_officer_id = request.POST['lo_name']
            loan_officer__obj = None
            if loan_officer_id:
                loan_officer__obj = UserMaster.objects.get(id=loan_officer_id)

            lo_direct = request.POST['lo_direct']
            lo_email = request.POST['lo_email']
            lender = request.POST['lender']
            ae_name = request.POST['ae_name']
            ae_direct = request.POST['ae_direct']
            ae_email = request.POST['ae_email']
            ae_company_id = request.POST['ae_company_id']
            processor_id = request.POST['assigned_name']
            tax_transcript = request.POST['tax_transcript']
            sub_status_id = []
            if 'sub_status_id' in request.POST:
                sub_status_id = request.POST['sub_status_id']
            closing_disclosure = request.POST['closing_disclosure']
            cd_date = request.POST['cd_date']
            appraisal_ordered = request.POST['appraisal_ordered']
            ad_date = request.POST['ad_date']
            tt_date = request.POST['tt_date']
            note = request.POST['note']
            recieved_date = request.POST['recieved_date']
            if len(sub_status_id)==0:
                    sub_status_obj = None
            else:
                sub_status_obj = LoanSubStatusMaster.objects.get(id=sub_status_id)
            if len(tax_transcript)==0:
                tax_transcript_obj = None
            else:
                tax_transcript_obj = TaxTranscriptMaster.objects.get(id=tax_transcript)
            if len(closing_disclosure)>0:
                closing_disclosure_obj = ClosingDisclosureMaster.objects.get(id=closing_disclosure)
            else:
                closing_disclosure_obj = None
            if len(appraisal_ordered)>0:
                appraisal_ordered_obj = AppraisalOrderedMaster.objects.get(id=appraisal_ordered)
            else:
                appraisal_ordered_obj = None
            
            if len(tt_date)==0:
                tt_date = None
            else:
                tt_date = date_convertion_create(tt_date)
            if len(cd_date) == 0:
                cd_date = None
            else:
                cd_date = date_convertion_create(cd_date)
            if len(ad_date) == 0:
                ad_date = None
            else:
                ad_date = date_convertion_create(ad_date)
            if len(recieved_date)==0:
                recieved_date = None
            else:
                recieved_date = date_convertion_create(recieved_date)
            
            estimate_close_date = None
            if 'est_closure_date' in request.POST:
                estimate_close_date = request.POST['est_closure_date']
            
            nmls_id = request.POST['nmls_id']
            charge_processing_fee = request.POST['charge_processing_fee']
            lo_fax = request.POST['lo_fax']
            ae_fax = request.POST['ae_fax']
            program_code = request.POST['program_code']
            customer_id = request.POST['customer_id']
            url = request.POST['url']
            loan_purpose_obj = None
            if 'loan_purpose' in request.POST:
                loan_purpose = request.POST['loan_purpose']
                try:
                    loan_purpose_obj = LoanPurposeMaster.objects.get(id=loan_purpose)
                except ValueError:
                    pass
            loan_amount = request.POST['loan_amount']
            loan_number = request.POST['loan_number']
            appraised_value = request.POST['appraised_value']
            ltv = request.POST['ltv']
            property_type_obj = None
            if 'property_type' in request.POST:
                property_type = request.POST['property_type']
                try:
                    property_type_obj = PropertyTypeMaster.objects.get(
                        id=property_type)
                except ValueError:
                    pass
            rate = request.POST['rate']
            lock_expiration_date = None
            if 'lock_expiration_date' in request.POST and len(request.POST['lock_expiration_date']) >1:
                lock_expiration_date = request.POST['lock_expiration_date']

            
            impound_obj = None
            if 'impound' in request.POST:
                impound = request.POST['impound']
                try:
                    impound_obj = ImpoundMaster.objects.get(id=impound)
                except ValueError:
                    pass

            compensation_payer_type_obj = None
            if 'compensation_payer_type' in request.POST:
                compensation_payer_type = request.POST['compensation_payer_type']
                try:
                    compensation_payer_type_obj = CompensationPayerTypeMaster.objects.get(
                        id=compensation_payer_type)
                except ValueError:
                    pass

            lender_pd_comp = request.POST['lender_pd_comp']
            subordination = None
            piw = None
            cltv = None
            rate_type_obj = None
            term_obj = None
            occupancy_master_obj = None
            if 'subordination' in request.POST:
                subordination = request.POST['subordination']

            if 'piw' in request.POST:
                piw = request.POST['piw']

            if 'cltv' in request.POST:
                cltv = request.POST['cltv']

            if 'rate_type' in request.POST:
                rate_type = request.POST['rate_type']
                try:
                    rate_type_obj = RateTypeMaster.objects.get(id=rate_type)
                except ValueError:
                    pass

            if 'term' in request.POST:
                term = request.POST['term']
                try:
                    term_obj = TermMaster.objects.get(id=term)
                except ValueError:
                    pass

            if 'occupancy_master' in request.POST:
                try:
                    occupancy_master = request.POST['occupancy_master']
                    try:
                        occupancy_master_obj = OccupancyMaster.objects.get(id=term)
                    except ValueError:
                        pass
                except ValueError:
                    pass

            borrower_ysp = request.POST['borrower_ysp']
            bwr_pd_comp = request.POST['bwr_pd_comp']
            property_address = request.POST['property_address']
            borrower_name = request.POST['borrower_name']
            borrower_phone = request.POST['borrower_phone']
            borrower_email = request.POST['borrower_email']
            loan_amount_2 = request.POST['loan_amount_2']
            deliver_disclosures = None
            deliver_disclosures_type = None
            request_conditions_stips_from = None
            charge_credit_report = None
            charge_appraisal = None
            file_float = None
            if 'deliver_disclosures' in request.POST:
                deliver_disclosures = request.POST['deliver_disclosures']
           
            if 'deliver_disclosures_type' in request.POST:
                deliver_disclosures_type = request.POST['deliver_disclosures_type']
            
            if 'request_conditions_stips_from' in request.POST:
                request_conditions_stips_from = request.POST['request_conditions_stips_from']
            
            if 'charge_credit_report' in request.POST:
                charge_credit_report = request.POST['charge_credit_report']
            
            if 'charge_appraisal' in request.POST:
                charge_appraisal = request.POST['charge_appraisal']
            
            if 'float' in request.POST:
                file_float = request.POST['float']
            else:
                file_float = None
            if 'va_base_loan' in request.POST:
                va_base_loan = request.POST['va_base_loan']
            else:
                va_base_loan = None
            if 'va_base_ff' in request.POST:
                va_base_ff = request.POST['va_base_ff']
            else:
                va_base_ff = None
            if 'fha_base_loan' in request.POST:
                fha_base_loan = request.POST['fha_base_loan']
            else:
                fha_base_loan = None
            if 'fha_base_mip' in request.POST:
                fha_base_mip = request.POST['fha_base_mip']
            else:
                fha_base_mip = None
            
            if 'reverse_status' in request.POST:
                reverse_status = request.POST['reverse_status']
            else:
                reverse_status = None
            
            if len(processor_id) > 0:
                try:
                    user_processor_obj = UserMaster.objects.get(id=processor_id)
                except Exception:
                    user_processor_obj = None

                if user_processor_obj:
                    try:
                        user_group_id = UserGroupMap.objects.get(user_id=user_processor_obj)
                        user_group_id = user_group_id.group_id
                    except Exception:
                        user_group_id = None
                else:
                    user_group_id = None
            else:
                user_processor_obj = None
                user_group_id = None

            if 'transaction_info' not in request.session:
                borrower_name = str(borrower_name).strip()
                file_master_file_name = borrower_name.split(' ')[-1]
            else:
                file_master_file_name = None

            filemaster = FileMaster.objects.create(
                va_base_loan=va_base_loan,
                va_base_ff=va_base_ff,
                fha_base_loan=fha_base_loan,
                fha_base_mip=fha_base_mip,
                status_id=status_obj,
                brokerage=brokerage,
                loan_officer_id=loan_officer__obj,
                assigned_group_id = user_group_id,
                assigned_user_id = user_processor_obj,
                loan_officer_direct=lo_direct,
                loan_officer_email=lo_email,
                lender=lender,
                ae_name=ae_name,
                ae_direct=ae_direct,
                ae_email=ae_email,
                ae_company_id=ae_company_id,
                company_id=company_obj,
                est_closure_date=estimate_close_date,
                nmls_id=nmls_id,
                loan_officer_fax=lo_fax,
                charging_processing_fees=charge_processing_fee,
                ae_fax=ae_fax,
                program_code=program_code,
                customer_id=customer_id,
                url=url,
                loan_number=loan_number,
                loan_amount=loan_amount,
                appraisal_value=appraised_value,
                ltv=ltv,
                rate=rate,
                float=file_float,
                lock_expiration_date=lock_expiration_date,
                loan_purpose_id=loan_purpose_obj,
                reverse_status=reverse_status,
                property_type=property_type_obj,
                impound=impound_obj,
                compensation_pay_type=compensation_payer_type_obj,
                lender_pd_comp=lender_pd_comp,
                subordination=subordination,
                sub_status_id=sub_status_obj,
				tax_transcript=tax_transcript_obj,
				closing_disclosure=closing_disclosure_obj,
				appraisal_ordered=appraisal_ordered_obj,
				note=note,
                recieved_date=recieved_date,
				appraisal_ordered_date=ad_date,
				closing_disclosure_date=cd_date,
				tax_transcript_date=tt_date,
                piw=piw,
                cltv=cltv,
                term=term_obj,
                rate_type=rate_type_obj,
                occupancy=occupancy_master_obj,
                borrower_ysp=borrower_ysp,
                borrower_pwd_comp=bwr_pd_comp,
                loan_amount_2=loan_amount_2,
                borrower_name=borrower_name,
                borrower_phone=borrower_phone,
                borrower_email=borrower_email,
                charge_appraisal=charge_appraisal,
                delievery_disclosure=deliver_disclosures,
                delievery_disclosure_type=deliver_disclosures_type,
                req_condition_stip_from=request_conditions_stips_from,
                charge_credit_report=charge_credit_report,
                created_by=user_obj,
                file_id=file_master_file_name
            )
            filemaster.save()
            
            if len(note)>0:
                FileNoteMap.objects.create(
                    file_id=filemaster,
                    note = note,
                    created_by=user_obj
                )

            if 'transaction_info' in request.session:
                transaction_info = request.session['transaction_info']
                filemaster = FileMaster.objects.get(id=filemaster.id)
                filemaster.agency_case_number = transaction_info.get("Agency Case Number")
                filemaster.mortgage_applied = transaction_info.get("Mortgage Applied For")
                filemaster.lender_case_number = transaction_info.get("Case Number")
                filemaster.no_of_units = transaction_info.get("No. of Units")
                filemaster.year_built = transaction_info.get("Year Built")
                # filemaster.refinance_cost = transaction_info.get("Year Built")
                # filemaster.refinance_amount = transaction_info.get("Year Built")
                filemaster.refinance_original_cost = transaction_info.get("Original Cost (Construction or Refinance)")
                filemaster.refinance_describe_improvements = transaction_info.get("Describe Improvements")
                filemaster.refinance_purpose = transaction_info.get("Purpose of Refinance")
                filemaster.refinance_lot_year = transaction_info.get("Year Lot Acquired (Construction) or Year Acquired (Refinance)")

                filemaster.construction_original_cost = transaction_info.get("Original Cost (Construction or Refinance)")
                filemaster.construction_lot_year = transaction_info.get("Year Lot Acquired (Construction) or Year Acquired (Refinance)")
                filemaster.save()

                for details in transaction_info.get('Applicant'):
                    if details.get("Applicant / Co-Applicant Indicator") == "BW":
                        # Convert the Date of Birth to date formate
                        bw_dob = date_convertion(details.get('Date of Birth'))

                        # Get the Particualr Borrower deatils using SSN number
                        bw_details = transaction_info.get(details.get('SSN'))

                        try:
                            state = StateMaster.objects.get(is_active='Y',fnm_state_value=bw_details.get('Residence State'))
                            state = state.id
                        except StateMaster.DoesNotExist:
                            state = None

                        # save the all the details in backend with out showing in the webpage
                        filemaster = FileMaster.objects.get(id=filemaster.id)
                        filemaster.file_id = details.get('Applicant Last Name')
                        filemaster.borrower_first_name = details.get('Applicant First Name')
                        filemaster.borrower_middle_name = details.get('Applicant Middle Name')
                        filemaster.borrower_last_name = details.get('Applicant Last Name')
                        filemaster.borrower_dependents = details.get('Dependents (no.)')
                        filemaster.borrower_social_security_number = details.get('SSN')
                        filemaster.borrower_date_of_birth = bw_dob
                        filemaster.borrower_years_in_school = str(details.get('Yrs. School'))
                        filemaster.borrower_marital_status = details.get('Marital Status')
                        filemaster.borrower_street = bw_details.get('Residence Street Address')
                        filemaster.borrower_city = bw_details.get('Residence City')
                        filemaster.borrower_state = state
                        filemaster.borrower_zip = bw_details.get('Residence Zip Code')
                        filemaster.borrower_country = bw_details.get('Country')
                        filemaster.borrower_address_type = bw_details.get('Own/Rent/Living Rent Free')
                        filemaster.borrower_years_in_address = bw_details.get('No. Yrs.')
                        filemaster.save()

                        try:
                            state = StateMaster.objects.get(is_active='Y',fnm_state_value=bw_details.get('Employer State'))
                            state = state.id
                        except StateMaster.DoesNotExist:
                            state = None

                        bw_emp_details = BorrowerEmploymentDetails.objects.create(
                            file_id=filemaster,
                            employer_name=bw_details.get('Employer Name'),
                            employer_street_address=bw_details.get('Employer Street Address'),
                            employer_city=bw_details.get('Employer City'),
                            employer_zip=bw_details.get('Employer Zip Code'),
                            employer_state=state,
                            self_employed=Boolen_field.get(bw_details.get('Self Employed')),
                            no_of_years_in_this_job=bw_details.get('Yrs. on this job'),
                            yrs_employed_in_this_line_of_work_profession=bw_details.get('Yrs. employed in this line of work/profession'),
                            position_title_type_of_business=bw_details.get('Position / Title / Type of Business'),
                            business_phone=bw_details.get('Business Phone', None),
                        )
                        bw_emp_details.save()

                        assets_details = FileAssets.objects.create(
                            file_id=filemaster,
                            file_assets=bw_details.get('Asset Description'),
                            file_cash_or_description_market_value=bw_details.get('Cash or Market Value'),
                            file_months_left_to_pay = bw_details.get('Months Left to Pay'),
                            file_acct_no=bw_details.get('Acct. no.'),
                        )

                        liabilities_details = FileLiabilities.objects.create(
                            file_id=filemaster,
                            file_liabilities_name = bw_details.get('Creditor Name'),
                            file_liabilities_street_address = bw_details.get('Creditor Street Address'),
                            file_liabilities_city = bw_details.get('Creditor City'),
                            file_liabilities_state = bw_details.get('Creditor State'),
                            file_liabilities_zip = bw_details.get('Creditor Zip Code'),
                            file_liabilities_monthly_payment = bw_details.get('Monthly Payment Amount'),
                            file_liabilities_unpaid_balance = bw_details.get('Unpaid Balance'),
                        )

                        bw_expense = FileExpensesBorrower.objects.create(
                            file_id=filemaster,
                            monthly_income=bw_details.get('Monthly Income'),
                            net_rental_income=bw_details.get('Net Rental Income')
                        )
                        bw_expense.save()
            # File Master

            # File Escrow Master
            company_name = request.POST['escrow_company']
            number = request.POST['escrow_number']
            officer_name = request.POST['escrow_officer']
            officer_phone = request.POST['escrow_phone']
            officer_email = request.POST['escrow_email']
            
            opened_date = None
            if 'escrow_open_date' in request.POST and len(request.POST['escrow_open_date']) > 1:
                opened_date = request.POST['escrow_open_date']

            is_open = None
            if 'please_open' in request.POST:
                is_open = request.POST['please_open']

            assistant_name = request.POST['escrow_assistant']
            assitant_phone = request.POST['assistant_phone']
            assistant_email = request.POST['assistant_email']

            requested_escrow_fees = None
            if 'requested_escrow_fees' in request.POST:
                requested_escrow_fees = request.POST['requested_escrow_fees']

            
            fileescrowmap = FileEscrowMap(
                file_id=filemaster,
                company_name=company_name,
                number=number,
                officer_name=officer_name,
                officer_phone=officer_phone,
                officer_email=officer_email,
                opened_date=date_convertion_create(opened_date),
                is_open=is_open,
                assistant_name=assistant_name,
                assitant_phone=assitant_phone,
                assistant_email=assistant_email,
                requested_escrow_fees=requested_escrow_fees,
                created_by=user_obj
            )
            fileescrowmap.save()
            # File Escrow Master

            # File HOA Master
            hoa = request.POST['hoa']
            hoa_phone = request.POST['hoa_phone']
            hoa_email = request.POST['hoa_email']
            filehoa = FileHoa(
                file_id=filemaster,
                hoa_name=hoa,
                hoa_phone=hoa_phone,
                hoa_email=hoa_email,
                created_by=user_obj
            )
            filehoa.save()
            # File HOA Master
            # File Title Master
            title_name = request.POST['title']
            title_order = request.POST['title_order']
            title_rep_name = request.POST['title_rep']
            title_rep_phone = request.POST['title_rep_phone']
            title_rep_email = request.POST['title_rep_email']
            filetitlemap = FileTitleMap(
                file_id=filemaster,
                title_name=title_name,
                title_order=title_order,
                title_rep_name=title_rep_name,
                title_rep_phone=title_rep_phone,
                title_rep_email=title_rep_email,
                created_by=user_obj
            )
            filetitlemap.save()
            # File Title Master
            # File Lisiting Buyer Master
            listing_office = request.POST['listing_office']
            listing_agent = request.POST['listing_agent']
            listing_agent_phone = request.POST['listing_agent_phone']
            listing_agent_email = request.POST['listing_agent_email']
            buyer_re_office = request.POST['buyer_office']
            buyer_agent = request.POST['buyer_agent']
            buyer_agent_phone = request.POST['buyer_agent_phone']
            buyer_agent_email = request.POST['buyer_agent_email']
            file_listing_buyer = FileListingBuyer(
                file_id=filemaster,
                listing_office=listing_office,
                listing_agent=listing_agent,
                listing_agent_phone=listing_agent_phone,
                listing_agent_email=listing_agent_email,
                buyer_re_office=buyer_re_office,
                buyer_agent=buyer_agent,
                buyer_agent_phone=buyer_agent_phone,
                buyer_agent_email=buyer_agent_email,
                created_by=user_obj
            )
            file_listing_buyer.save()
            # File Lisiting Buyer Master
			# File Co Borrower List
            dec_list = [
                'a. Are there any outstanding judgments against you?',
                'b. Have you been declared bankrupt within the past 7 years?',
                'c. Have you had property foreclosed upon or given title or deed in lieu thereof in the last 7 years?',
                'd. Are you a party to a lawsuit?',
                'e. Have you directly or indirectly been obligated on any loan…',
                'f. Are you presently delinquent or in default on any Federal debt…',
                'g. Are you obligated to pay alimony child support or separate maintenance?',
                'h. Is any part of the down payment borrowed?',
                'i. Are you a co-maker or',
                'j. Are you a U.S. citizen? k. Are you a permanent resident alien?',
                'l. Do you intend to occupy…',
                'm. Have you had an ownership interest…',
                'm. (1) What type of property…',
                'm. (2) How did you hold title…'
            ]
            transaction_list = [
                "a. Purchase price",
                "b. Alterations, improvements, repairs",
                "c. Land",
                "d. Refinance (Inc. debts to be paid off)",
                "e. Estimated prepaid items",
                "f. Estimated closing costs",
                "g. PMI MIP, Funding Fee",
                "h. Discount",
                "j. Subordinate financing",
                "n. PMI, MIP, Funding Fee financed",
                'Total costs (add items a through h)',
                "Borrower's closing costs paid by Seller",
                'm. Loan amount (exclude PMI, MIP,Funding Fee financed)',
                'o. Loan amount (add m & n)',
                'p. Cash from/to Borrower (subtract j, k, l & o from i)'
            ]
            if not 'transaction_info' in request.session:
                FileExpensesBorrower.objects.create(
                    file_id=filemaster
                )
                BorrowerEmploymentDetails.objects.create(
                    file_id=filemaster
                )
                for dec in dec_list:
                    DeclarationMap.objects.create(
                        file_id=filemaster,
                        declaration_description=dec,
                        types='borrower'
                    )

            co_borrower_name_array = request.POST.getlist('co_borrower_name[]')
            co_borrower_email_array = request.POST.getlist(
                'co_borrower_email[]')
            co_borrower_phone_array = request.POST.getlist(
                'co_borrower_phone[]')

            co_borrower_length = len(co_borrower_name_array)
            co_borrower_ids = []
            co_borrower_count = 0
            while co_borrower_count < co_borrower_length:
                file_co_borrower = FileCoBorrower(
                    file_id=filemaster,
                    co_borrower_name=co_borrower_name_array[co_borrower_count],
                    co_borrower_email=co_borrower_email_array[co_borrower_count],
                    co_borrower_phone=co_borrower_phone_array[co_borrower_count],
                    created_by=user_obj
                )
                file_co_borrower.save()
                co_borrower_ids.append(file_co_borrower)
                co_borrower_count += 1

            # If user doesn't import FNM file
            if not 'transaction_info' in request.session:
                if len(co_borrower_ids) > 0:
                    for co_br_ids in co_borrower_ids:
                        FileExpensesCoBorrower.objects.create(
                            file_id=filemaster,
                            cw_id=co_br_ids
                        )
                        CoBorrowerEmploymentDetails.objects.create(
                            file_id=filemaster,
                            cw_id=co_br_ids
                        )
                        for dec in dec_list:
                            DeclarationMap.objects.create(
                                file_id=filemaster,
                                cw_id=co_br_ids,
                                declaration_description=dec,
                                types='co-borrower'
                            )

            non_co_borrower_fnm = []
            if 'transaction_info' in request.session:
                transaction_info = request.session['transaction_info']
                for details in transaction_info.get('Applicant'):
                    for co_borrower_info in co_borrower_ids:
                        if details.get("Applicant / Co-Applicant Indicator") == "QZ":
                            if co_borrower_info.co_borrower_name == details.get('Applicant First Name'):
                                # Convert the Date of Birth to date formate
                                cw_dob = date_convertion(
                                    details.get('Date of Birth'))

                                # Get the Particualr Borrower deatils using SSN number
                                cw_details = transaction_info.get(
                                    details.get('SSN'))
                                try:
                                    state = StateMaster.objects.get(is_active='Y',fnm_state_value=cw_details.get('Residence State'))
                                    state = state.id
                                except StateMaster.DoesNotExist:
                                    state = None
                                # save the all the details in backend with out showing in the webpage
                                file_co_borrower = FileCoBorrower.objects.get(
                                    id=co_borrower_info.id)
                                file_co_borrower.co_borrower_first_name = details.get('Applicant First Name')
                                file_co_borrower.co_borrower_middle_name = details.get('Applicant Middle Name')
                                file_co_borrower.co_borrower_last_name = details.get('Applicant Last Name')
                                file_co_borrower.co_borrower_dependents = details.get('Dependents (no.)')    
                                file_co_borrower.co_borrower_social_security_number = details.get('SSN')
                                file_co_borrower.co_borrower_date_of_birth = cw_dob
                                file_co_borrower.co_borrower_years_in_school = details.get('Yrs. School')
                                file_co_borrower.co_borrower_marital_status = details.get('Marital Status')
                                file_co_borrower.co_borrower_street = cw_details.get('Residence Street Address')
                                file_co_borrower.co_borrower_city = cw_details.get('Residence City')
                                file_co_borrower.co_borrower_state = state
                                file_co_borrower.co_borrower_zip = cw_details.get('Residence Zip Code')
                                file_co_borrower.co_borrower_country = cw_details.get('Country')
                                file_co_borrower.co_borrower_address_type = cw_details.get('Own/Rent/Living Rent Free')
                                file_co_borrower.co_borrower_years_in_address = cw_details.get('No. Yrs.')
                                file_co_borrower.save()

                                try:
                                    state = StateMaster.objects.get(is_active='Y',fnm_state_value=cw_details.get('Employer State'))
                                    state = state.id
                                except StateMaster.DoesNotExist:
                                    state = None

                                cw_emp_details = CoBorrowerEmploymentDetails.objects.create(
                                    file_id=filemaster,
                                    cw_id=co_borrower_info,
                                    employer_name=cw_details.get('Employer Name'),
                                    employer_street_address=cw_details.get('Employer Street Address'),
                                    employer_city=cw_details.get('Employer City'),
                                    employer_zip=cw_details.get('Employer Zip Code'),
                                    employer_state=state,
                                    self_employed=Boolen_field.get(bw_details.get('Self Employed')),
                                    no_of_years_in_this_job=cw_details.get('Yrs. on this job'),
                                    yrs_employed_in_this_line_of_work_profession=cw_details.get('Yrs. employed in this line of work/profession'),
                                    position_title_type_of_business=cw_details.get('Position / Title / Type of Business'),
                                    business_phone=cw_details.get('Business Phone', None),
                                )

                                cw_expense = FileExpensesCoBorrower.objects.create(
                                    file_id=filemaster,
                                    monthly_income=cw_details.get('Monthly Income'),
                                    net_rental_income=cw_details.get('Net Rental Income'),
                                    cw_id=co_borrower_info
                                )
                                for dec in dec_list:
                                    DeclarationMap.objects.create(
                                        file_id=filemaster,
                                        cw_id=co_borrower_info,
                                        declaration_description=dec,
                                        value=cw_details.get(dec),
                                        types='co-borrower',
                                        co_borrower_id=details.get('SSN')
                                    )
                            else:
                                non_co_borrower_fnm.append(co_borrower_info)
            
            # If Co-borrower added manullay
            if len(non_co_borrower_fnm) > 0:
                for ids in non_co_borrower_fnm:
                    CoBorrowerEmploymentDetails.objects.create(
                        file_id=filemaster,
                        cw_id=ids,
                    )
                    FileExpensesCoBorrower.objects.create(
                        file_id=filemaster,
                        cw_id=ids
                    )
                    for dec in dec_list:
                        DeclarationMap.objects.create(
                            file_id=filemaster,
                            cw_id=co_borrower_info,
                            declaration_description=dec,
                            types='co-borrower'
                        )

            if 'transaction_info' in request.session:
                transaction_info = request.session['transaction_info']

                # Details of Transactions
                for tran_details in transaction_list:
                    tran_map = DetailsTransactionMap.objects.create(
                        file_id=filemaster,
                        transaction_description=tran_details,
                        value=transaction_info.get(tran_details)
                    )

                for details in transaction_info.get('Applicant'):

                    if details.get("Applicant / Co-Applicant Indicator") == "BW":
                        # Get the Particualr Borrower deatils using SSN number
                        bw_details = transaction_info.get(
                            details.get('SSN'))
                        
                        for dec in dec_list:
                            desc_values = DeclarationMap.objects.create(
                                file_id=filemaster,
                                declaration_description=dec,
                                value=bw_details.get(dec),
                                types='borrower',
                                borrower_id=details.get('SSN')
                            )

                # File Co Borrower List
            # File Propery Address  Master
            property_address = None
            property_state_master_obj = None
            mailing_state_master_obj = None
            if 'property_address' in request.POST :
                property_address = request.POST['property_address']
            
            property_city = request.POST['property_city']
            if 'property_state' in request.POST :
                property_state = request.POST['property_state']
                try:
                    property_state_master_obj = StateMaster.objects.get(id=property_state)
                except ValueError:
                    pass
            
            address_fill = None
            if 'address_fill' in request.POST:
                address_fill = request.POST['address_fill']
           
            property_zipcode = request.POST['property_zipcode']
            mailing_address = request.POST['mailing_address']
            mailing_city = request.POST['mailing_city']
            if 'property_state' in request.POST :
                mailing_state = request.POST['mailing_state']
                try:
                    mailing_state_master_obj = StateMaster.objects.get(
                    id=mailing_state)
                except ValueError:
                    pass

            mailing_zipcode = request.POST['mailing_zipcode']
            file_property_map = FilePropertyMap(
                file_id=filemaster,
                property_address=property_address,
                property_city=property_city,
                property_state=property_state_master_obj,
                property_zipcode=property_zipcode,
                mailing_address=mailing_address,
                mailing_city=mailing_city,
                mailing_state=mailing_state_master_obj,
                mailing_zipcode=mailing_zipcode,
                mailing_address_check=address_fill,
                created_by=user_obj
            )
            file_property_map.save()
            # File Propery Address  Master
            # File Co Borrower List
            user_password_name_array = request.POST.getlist('user_password_name_array[]')
            user_password_type_array = request.POST.getlist('user_password_type_array[]')
            user_name_array = request.POST.getlist('user_name_array[]')
            user_password_array = request.POST.getlist('user_password_array[]')
            user_password_length = len(user_password_name_array)
            user_password_count = 0
            
            while user_password_count < user_password_length:
                file_password = FilePassword(
                    file_id=filemaster,
                    password_name=user_password_name_array[user_password_count],
                    user_name=user_name_array[user_password_count],
                    password=user_password_array[user_password_count],
                    password_type=user_password_type_array[user_password_count],
                    created_by=user_obj
                )
                file_password.save()
                user_password_count += 1
            # File Co Borrower List
            try:
                for f in filepound_files:
                    tu = TemporaryUpload.objects.get(upload_id=f)
                    file_pond_path = settings.DJANGO_DRF_FILEPOND_FILE_STORE_PATH + '/' + str(tu.file)
                    try:
                        os.mkdir('media/document_{}'.format(filemaster.id))
                    except Exception:
                        pass

                    try:
                        os.rename(tu.get_file_path(), 'media/document_{}/{}'.format(filemaster.id, tu.upload_name)) # Delete the temporary upload record and the temporary directory tu.delete()
                    except Exception:
                        pass

                    file_instance = DocumentsTypeMaster(
                        file_id=filemaster,
                        document_file_path='document_{}/{}'.format(filemaster.id,tu.upload_name),
                        document_file_name=tu.upload_name,
                        created_by=user_obj
                    )
                    file_instance.save()

            except Exception:
                pass
            
            if len(filemaster.file_id)<=0:
                messages.add_message(request, messages.INFO, 'File Created ')
                
            else:
                messages.add_message(request, messages.INFO, 'File Created - {}'. format(filemaster.file_id))
            request.session['is_create'] ='Y'
            return HttpResponseRedirect('/dashboard/')

    else:
        form = FileForm()
    return render(request,
                  'file/new.html',
                  {'form': form, 'user_obj': user_obj,'role_feature':role_feature, 'loan_officers_list': loan_officers_list, 'assign_processor_list':assign_processor_list}
                  )


def index(request):
    if(request.session.has_key('company_id') == False):
        return HttpResponseRedirect('/')
    company_id = request.session.get('company_id')
    company_obj = CompanyMaster.objects.get(id=company_id)
    object_list = UserMaster.objects.filter(
        company_id=company_obj)  # or any kind of queryset
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)
    file_master = FileMaster.objects.filter(created_by=user_obj)
    role_id = request.session.get('role_id')
    if role_id != None:
        role_obj = RoleMaster.objects.get(id=role_id)
        role_feature = RoleFeatureMap.objects.filter(role_id=role_obj).values_list('feature_id', flat=True)
        role_feature = list(role_feature)
    else:
        role_feature = []
    if '6' not in role_feature:
	    return HttpResponseRedirect('/dashboard/')
    return render(request,
                  'file/list.html',
                  {'file_master': file_master,'role_feature':role_feature, 'user_obj':user_obj}
                  )


def view(request, file_id):
    form = UpdateFileForm()
    if(request.session.has_key('company_id') == False):
        return HttpResponseRedirect('/')

    if 'transaction_info' in request.session:
        del request.session['transaction_info']
    
    if(request.session.has_key('div_id') == False):
        div_id = False
    else:
        div_id = request.session.get('div_id')
    request.session['div_id'] = None
    company_obj = CompanyMaster.objects.get(id=1)
    company_obj = CompanyMaster.objects.get(id=1)
    object_list = UserMaster.objects.filter(
        company_id=company_obj)  # or any kind of queryset
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)
    file_master = FileMaster.objects.get(id=file_id)
    co_borrower = FileCoBorrower.objects.filter(file_id=file_id)
    role_id = request.session.get('role_id')
    if role_id != None:
        role_obj = RoleMaster.objects.get(id=role_id)
        role_feature = RoleFeatureMap.objects.filter(role_id=role_obj).values_list('feature_id', flat=True)
        role_feature = list(role_feature)
    else:
        role_feature = []
    if '9' not in role_feature:
	    return HttpResponseRedirect('/dashboard/')

    file_property_count = FilePropertyMap.objects.filter(file_id=file_master.id).count()
    if file_property_count>0:
        file_property_map = FilePropertyMap.objects.get(file_id=file_master.id)
    else:
        file_property_map = None

    try:
        borrower_employment_detail = BorrowerEmploymentDetails.objects.get_or_create(file_id=file_master)
        borrower_employment_detail = borrower_employment_detail[0]
    except Exception:
        borrower_employment_detail = None

    co_borrower_employment_detail_count = CoBorrowerEmploymentDetails.objects.filter(file_id=file_master.id).count()
    if co_borrower_employment_detail_count>0:
        co_borrower_employment_detail = CoBorrowerEmploymentDetails.objects.filter(file_id=file_master.id)
    else:
        co_borrower_employment_detail = None
    co_borrower_detail_count = FileCoBorrower.objects.filter(file_id=file_master.id).count()
    if co_borrower_detail_count>0:
        co_borrower_detail = FileCoBorrower.objects.filter(file_id=file_master.id)
    else:
        co_borrower_detail = None

    borrower_declaration_count = DeclarationMap.objects.filter(file_id=file_master.id,types='borrower').count()
    if borrower_declaration_count>0:
        borrower_declaration = DeclarationMap.objects.filter(file_id=file_master.id,types='borrower')
    else:
        borrower_declaration = None

    co_borrower_declaration_count = DeclarationMap.objects.filter(file_id=file_master.id,types='co-borrower').count()
    if co_borrower_declaration_count>0:
        co_borrower_declaration = DeclarationMap.objects.filter(file_id=file_master.id,types='co-borrower')
    else:
        co_borrower_declaration = None

    co_borrower_declaration_detail_count = co_borrower_declaration_count / 14
    detail_transaction_count = DetailsTransactionMap.objects.filter(file_id=file_master.id).count()
    if detail_transaction_count>0:
        detail_transaction = DetailsTransactionMap.objects.filter(file_id=file_master.id)
    else:
        detail_transaction = None

    try:
        states = StateMaster.objects.filter(is_active='Y')
    except StateMaster.DoesNotExist:
        states = None
        
    try:
        particular_state = StateMaster.objects.get(id=file_master.borrower_state, is_active='Y')
    except StateMaster.DoesNotExist:
        particular_state = None

    file_escrow_count = FileEscrowMap.objects.filter(file_id=file_master.id).count()
    if file_escrow_count>0:
        detail_file_escrow = FileEscrowMap.objects.filter(file_id=file_master.id)
    else:
        detail_file_escrow = None

    file_title_count = FileTitleMap.objects.filter(file_id=file_master.id).count()
    if file_title_count>0:
        detail_file_title = FileTitleMap.objects.filter(file_id=file_master.id)
    else:
        detail_file_title = None

    file_hoa_count = FileHoa.objects.filter(file_id=file_master.id).count()
    if file_hoa_count>0:
        detail_file_hoa = FileHoa.objects.filter(file_id=file_master.id)
    else:
        detail_file_hoa = None

    file_password_count = FilePassword.objects.filter(file_id=file_master.id).count()
    if file_password_count>0:
        detail_file_password_record = FilePassword.objects.filter(file_id=file_master)
    else:
        detail_file_password_record = None

    try:
        mortgage = FileMortage.objects.filter(is_active='Y')
    except Exception:
        mortgage = None
    
    try:
        assets_details = FileAssets.objects.filter(file_id=file_master.id)
    except Exception:
        assets_details = None

    try:
        list_saving_details = FileSavingsAccount.objects.filter(file_id=file_master.id)
    except Exception:
        list_saving_details = None
    
    try:
        liabilities_details = FileLiabilities.objects.filter(file_id=file_master.id)
    except Exception:
        liabilities_details = None
    
    try:
        liabilities_pledged_assets_details = FileLiabilitiesPledgedAssets.objects.filter(file_id=file_master.id)
    except Exception:
        liabilities_pledged_assets_details = None
    
    try:
        bw_expenses = FileExpensesBorrower.objects.get(file_id=file_master.id)
    except Exception:
        bw_expenses = None

    try:
        cw_expenses = FileExpensesCoBorrower.objects.filter(file_id=file_master.id)
    except Exception:
        cw_expenses = None
    
    try:
        escrow_details = FileEscrowMap.objects.get(file_id=file_master.id)
    except Exception:
        escrow_details = None
    
    try:
        listing_buyers = FileListingBuyer.objects.get(file_id=file_master.id)
    except Exception:
        listing_buyers = None
    
    document_form = DocumentUpload()

    try:
        document_detail_obj = DocumentsTypeMaster.objects.filter(file_id=file_master).order_by('created_date').reverse()
    except Exception:
        document_detail_obj = None
    
    try:
        loan_purpose_list = LoanPurposeMaster.objects.filter(is_active='Y')
    except Exception:
        loan_purpose_list = None

    try:
        property_type_list = PropertyTypeMaster.objects.filter(is_active='Y')
    except Exception:
        property_type_list = None
    
    try:
        expense_proposed = FileHouseExpensesProposed.objects.get(file_id=file_master.id)
    except Exception:
        expense_proposed = None
    
    try:
        expense_present = FileHouseExpensesPresent.objects.get(file_id=file_master.id)
    except Exception:
        expense_present = None

    file_document_details = []
    for i in document_detail_obj:
        file_name_doc = i.document_file_name
        file_url = settings.MEDIA_URL+file_name_doc
        i.file_type=mimetypes.guess_type(file_url,strict = True)
        i.file_extension = '.' + str(file_name_doc).split('.')[-1]
        if file_name_doc.endswith('.FNM') or file_name_doc.endswith('.fnm'):
            file_document_details.append(i)
    
    lock_expiration_date = file_master.lock_expiration_date
    if lock_expiration_date:
        lock_expiration_date = str(lock_expiration_date.date())

    return render(request,
                  'file/detail.html',
                  {'form':form,
                  'div_id':div_id,
                  'borrower_declaration':borrower_declaration,
                  'co_borrower_declaration':co_borrower_declaration,
                  'borrower_employment_detail':borrower_employment_detail,
                  'detail_transaction':detail_transaction,
                  'file_master': file_master, 
                  'file_property_map': file_property_map,
                  'co_borrower': co_borrower,
                  'co_borrower_employment_detail':co_borrower_employment_detail,
                  'states': states,
                  'particular_state': particular_state,
                  'detail_file_hoa':detail_file_hoa,
                  'detail_file_escrow':detail_file_escrow,
                  'detail_file_title':detail_file_title,
                  'detail_file_password_record':detail_file_password_record,
                  'mortgage': mortgage,
                  'assets_details': assets_details,
                  'liabilities_details':liabilities_details,
                  'bw_expenses': bw_expenses,
                  'cw_expenses': cw_expenses,
                  'escrow_details':escrow_details,
                  'listing_buyers':listing_buyers,
                  'document_form':document_form,
                  'document_details':document_detail_obj,
                  'file_document_details':file_document_details,
                  'lock_expiration_date': lock_expiration_date,
                  'role_feature':role_feature,
                  'user_obj':user_obj,
                  'loan_purpose_list':loan_purpose_list,
                  'property_type_list':property_type_list,
                  'expense_present':expense_present,
                  'expense_proposed':expense_proposed,
                  'list_saving_details':list_saving_details,
                  'liabilities_pledged_assets_details':liabilities_pledged_assets_details
                  }
                  )


def import_file(request):
    """
    For auto populate the data in the create transaction fields.
    we have import file and populate the fields with the data
    """
    if(request.session.has_key('company_id') == False):
        return HttpResponseRedirect('/')
    
    company_id = request.session.get('company_id')
    company_obj = CompanyMaster.objects.get(id=company_id)
    # Initial form empty data
    form = FileForm()
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)
    role_id = request.session.get('role_id')
    if role_id != None:
        role_obj = RoleMaster.objects.get(id=role_id)
        role_feature = RoleFeatureMap.objects.filter(role_id=role_obj).values_list('feature_id', flat=True)
        role_feature = list(role_feature)
    else:
        role_feature = []
    
    loan_officers_list = []
    loan_officers = RoleMaster.objects.filter(company_id=company_id, role_type='Loan officer')
    for officers in loan_officers:
        user_role = UserRoleMap.objects.filter(role_id=officers.id)
        for role in user_role:
            users = UserMaster.objects.filter(id=role.user_id.id)
            for i in users:
                loan_officers_list.append(i)

    assign_processor_list = UserRoleMap.objects.filter(role_id__role_type='Loan Processor', role_id__company_id=company_obj)

    if request.method == 'POST' and request.FILES.get('myfile'):
        transaction_file = request.FILES.get('myfile')
        # Store the file in the Media Directory
        fs = FileSystemStorage(settings.MEDIA_ROOT)
        filename = fs.save(transaction_file.name, transaction_file)
        
        try:
            files = {'file': open(
                str(settings.MEDIA_ROOT) + '/' + filename, 'rb')}
            r = requests.post(settings.PARSER_ENDPOINT, files=files)
            if not r.ok:
                return HttpResponseRedirect('/file/create/')
        except Exception as e:
            return HttpResponseRedirect('/file/create/')

        transaction_info = r.json()
        request.session['transaction_info'] = transaction_info
        borrower = {}
        co_borrower_list = []
        for details in transaction_info.get('Applicant'):
            if details.get("Applicant / Co-Applicant Indicator") == "BW":
                borrower.update({
                    'borrower_name': details.get('Applicant First Name'),
                    'borrower_phone': details.get('Home Phone'),
                    'borrower_email': details.get('Email Address'),
                })

            if details.get("Applicant / Co-Applicant Indicator") == "QZ":
                co_borrower = {}
                co_borrower.update({
                    'co_borrower_name': details.get('Applicant First Name'),
                    'co_borrower_phone': details.get('Home Phone'),
                    'co_borrower_email': details.get('Email Address'),
                })
                co_borrower_list.append(co_borrower)
        try:
            rate_type = RateTypeMaster.objects.get(is_active='Y', fnm_applied_value=transaction_info.get('Amortization Type'))
            rate_type = rate_type.id
        except RateTypeMaster.DoesNotExist:
            rate_type = None
        
        try:
            loan_purpose = LoanPurposeMaster.objects.get(is_active='Y',fnm_purpose_value=transaction_info.get('Purpose of Loan'),fnm_applied_value=transaction_info.get('Mortgage Applied For') )
            loan_purpose = loan_purpose.id
        except LoanPurposeMaster.DoesNotExist:
            loan_purpose = None

        try:
            property_type = PropertyTypeMaster.objects.get(is_active='Y',fnm_property_value=transaction_info.get('Property will be'))
            property_type = property_type.id
        except PropertyTypeMaster.DoesNotExist:
            property_type = None
        
        try:
            state = StateMaster.objects.get(is_active='Y',fnm_state_value=transaction_info.get('Property State'))
            state = state.id
        except StateMaster.DoesNotExist:
            state = None
        
        months_to_years = transaction_info.get('No. of Months')
        if months_to_years and len(months_to_years)>0:
            try:
                term = TermMaster.objects.get(is_active='Y', term=int(int(months_to_years) / 12))
                term = term.id
            except TermMaster.DoesNotExist:
                term = None
        else:
            term = None

        final_dict = {
            'loan_amount': transaction_info.get('Loan Amount'),
            'property_type': property_type,
            'property_address': transaction_info.get('Property Street Address'),
            'property_city': transaction_info.get('Property City'),
            'property_state': state,
            'property_zipcode': transaction_info.get('Property Zip Code'),
            'appraised_value': transaction_info.get('Property Appraised Value'),
			"rate_type": rate_type,
			'loan_purpose': loan_purpose,
			'rate': transaction_info.get('Interest Rate'),
			'term': term,
        }
        final_dict.update(borrower)
        # Fill the form with initial data to see after importing the file
        form = FileForm(initial=final_dict)
        return render(request, 'file/new.html', {'form': form, 'co_applicants': co_borrower_list,'user_obj':user_obj, 'role_feature':role_feature, 'loan_officers_list':loan_officers_list, 'assign_processor_list':assign_processor_list})
    return render(request, 'file/new.html', {'form': form,'user_obj':user_obj, 'role_feature':role_feature, 'loan_officers_list':loan_officers_list, 'assign_processor_list':assign_processor_list})


def upload_documents(request, file_id):
    try:
        file_master = FileMaster.objects.get(id=file_id)
    except DocumentsType.DoesNotExist:
        file_master = None
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)
    document_form = DocumentUpload()
    if request.method == "POST":
        document_form = DocumentUpload(request.POST, request.FILES)
        files = request.POST.getlist('filepond')
        for f in files:
            tu = TemporaryUpload.objects.get(upload_id=f)
            file_pond_path = settings.DJANGO_DRF_FILEPOND_FILE_STORE_PATH + '/' + str(tu.file)
            try:
                os.mkdir('media/document_{}'.format(file_master.id))
            except Exception:
                pass

            try:
                os.rename(tu.get_file_path(), 'media/document_{}/{}'.format(file_master.id, tu.upload_name)) # Delete the temporary upload record and the temporary directory tu.delete()
            except Exception:
                pass

            file_instance = DocumentsTypeMaster(
                file_id=file_master,
                document_file_path='document_{}/{}'.format(file_master.id,tu.upload_name),
                document_file_name=tu.upload_name,
                created_by= user_obj
            )
            file_instance.save()
            request.session['div_id'] = 'documents-tracking'

        return HttpResponseRedirect(reverse('view_file', args=[file_master.id]))
    return render(request, "file/detail_upload_file.html", {"document_form": document_form, 'user_obj':user_obj })


def sub_status_filter(request):
    status_id = request.GET.get('status_id', None)
    sub_status = LoanSubStatusMaster.objects.filter(status_id=status_id)
    return render(request, 'file/sub_status.html',{'sub_status': sub_status})

def loan_officer_filter(request):
    user_id = request.GET.get('user_id', None)
    user_master = UserMaster.objects.get(id=user_id)
    loan_officer_details = {
        'email': user_master.email,
        'fax': user_master.fax,
        'nmls_id': user_master.nmls_id,
        'lo_direct': user_master.phone,
        'borkerage': user_master.officer_company
    }
    return JsonResponse(loan_officer_details)


@csrf_exempt
def download_files(request):
    file_id = request.POST.get('file_id', None)

    try:
        file_master = FileMaster.objects.get(id=int(file_id))
    except Exception:
        file_master = None

    try:
        document_details = list(DocumentsTypeMaster.objects.filter(file_id=file_master).values())
    except Exception:
        document_details = None

    media_path = str(settings.MEDIA_ROOT)
    fantasy_zip = zipfile.ZipFile(media_path + '/' + 'document_{}.zip'.format(file_master.id), 'w')
    for file in document_details:
        fantasy_zip.write(os.path.join('media', file.get('document_file_path')), os.path.relpath(os.path.join('media',file.get('document_file_path')), media_path))
    fantasy_zip.close()

    zip_file = {
        'zip_response': 'document_{}.zip'.format(file_master.id)
    }
    return JsonResponse(zip_file)


def loan_information_update(request, file_id):
    if(request.session.has_key('company_id') == False):
        return HttpResponseRedirect('/')

    Boolen_field = {
        'Yes': True,
        'No': False
    }
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)

    if request.method == 'POST' and (request.FILES.get('myfile') or request.POST.get('updating_file')):
        
        if request.POST.get('updating_file'):
            document_name = DocumentsTypeMaster.objects.get(id=request.POST.get('updating_file'))
            document_name = document_name.document_file_path
        else:
            transaction_file = request.FILES.get('myfile')
            document_name = transaction_file.name
            # Store the file in the Media Directory
            fs = FileSystemStorage(settings.MEDIA_ROOT)
            document_name = fs.save(document_name, transaction_file)

        try:
            files = {'file': open(
                str(settings.MEDIA_ROOT) + '/' + str(document_name), 'rb')}
            r = requests.post(settings.PARSER_ENDPOINT, files=files)
            if not r.ok:
                return HttpResponseRedirect('/file/create/')
        except Exception as e:
            return HttpResponseRedirect('/file/create/')

        transaction_info = r.json()
        request.session['transaction_info'] = transaction_info

        dec_list = [
            'a. Are there any outstanding judgments against you?',
            'b. Have you been declared bankrupt within the past 7 years?',
            'c. Have you had property foreclosed upon or given title or deed in lieu thereof in the last 7 years?',
            'd. Are you a party to a lawsuit?',
            'e. Have you directly or indirectly been obligated on any loan…',
            'f. Are you presently delinquent or in default on any Federal debt…',
            'g. Are you obligated to pay alimony child support or separate maintenance?',
            'h. Is any part of the down payment borrowed?',
            'i. Are you a co-maker or',
            'j. Are you a U.S. citizen? k. Are you a permanent resident alien?',
            'l. Do you intend to occupy…',
            'm. Have you had an ownership interest…',
            'm. (1) What type of property…',
            'm. (2) How did you hold title…'
        ]

        transaction_list = [
            "a. Purchase price",
            "b. Alterations, improvements, repairs",
            "c. Land",
            "d. Refinance (Inc. debts to be paid off)",
            "e. Estimated prepaid items",
            "f. Estimated closing costs",
            "g. PMI MIP, Funding Fee",
            "h. Discount",
            "j. Subordinate financing",
            "n. PMI, MIP, Funding Fee financed",
            'Total costs (add items a through h)',
            "Borrower's closing costs paid by Seller",
            'm. Loan amount (exclude PMI, MIP,Funding Fee financed)',
            'o. Loan amount (add m & n)',
            'p. Cash from/to Borrower (subtract j, k, l & o from i)'
        ]

        months_to_years = transaction_info.get('No. of Months')
        if months_to_years and len(months_to_years)>0:
            try:
                term = TermMaster.objects.get(is_active='Y', term=int(int(months_to_years) / 12))   
            except TermMaster.DoesNotExist:
                term = None
        else:
            term = None
        
        try:
            rate_type = RateTypeMaster.objects.get(is_active='Y', fnm_applied_value=transaction_info.get('Amortization Type'))
        except RateTypeMaster.DoesNotExist:
            rate_type = None

        try:
            loan_purpose = LoanPurposeMaster.objects.get(is_active='Y',fnm_purpose_value=transaction_info.get('Purpose of Loan'),fnm_applied_value=transaction_info.get('Mortgage Applied For') )
        except LoanPurposeMaster.DoesNotExist:
            loan_purpose = None

        try:
            property_type = PropertyTypeMaster.objects.get(is_active='Y',fnm_property_value=transaction_info.get('Property will be'))
        except PropertyTypeMaster.DoesNotExist:
            property_type = None

        try:
            state = StateMaster.objects.get(is_active='Y',fnm_state_value=transaction_info.get('Property State'))
        except StateMaster.DoesNotExist:
            state = None

        filemaster = FileMaster.objects.get(id=file_id)
        filemaster.loan_amount = transaction_info.get("Loan Amount")
        filemaster.rate = transaction_info.get("Interest Rate")
        filemaster.term = term
        filemaster.rate_type = rate_type
        filemaster.loan_purpose_id = loan_purpose
        filemaster.property_type = property_type
        filemaster.appraisal_value = transaction_info.get('Property Appraised Value')
        filemaster.agency_case_number = transaction_info.get("Agency Case Number")
        filemaster.mortgage_applied = transaction_info.get("Mortgage Applied For")
        filemaster.lender_case_number = transaction_info.get("Case Number")
        filemaster.no_of_units = transaction_info.get("No. of Units")
        filemaster.year_built = transaction_info.get("Year Built")
        filemaster.refinance_original_cost = transaction_info.get("Original Cost (Construction or Refinance)")
        filemaster.refinance_describe_improvements = transaction_info.get("Describe Improvements")
        filemaster.refinance_purpose = transaction_info.get("Purpose of Refinance")
        filemaster.refinance_lot_year = transaction_info.get("Year Lot Acquired (Construction) or Year Acquired (Refinance)")
        filemaster.construction_original_cost = transaction_info.get("Original Cost (Construction or Refinance)")
        filemaster.construction_lot_year = transaction_info.get("Year Lot Acquired (Construction) or Year Acquired (Refinance)")
        filemaster.save()

        file_property_map = FilePropertyMap.objects.get(file_id=filemaster)
        file_property_map.property_address=transaction_info.get('Property Street Address')
        file_property_map.property_city=transaction_info.get('Property City')
        file_property_map.property_state=state
        file_property_map.property_zipcode=transaction_info.get('Property Zip Code')
        file_property_map.updated_by=user_obj
        file_property_map.save()

        # Details of Transactions
        for tran_details in transaction_list:

            tran_map = DetailsTransactionMap.objects.get_or_create(
                file_id=filemaster,
                transaction_description=tran_details,
                value=transaction_info.get(tran_details)
            )

        
        if not 'transaction_info' in request.session:
            FileExpensesBorrower.objects.create(
                file_id=filemaster
            )
            BorrowerEmploymentDetails.objects.create(
                file_id=filemaster
            )

        co_borrower_list = []
        co_borrower_applicant_list = []
        for details in transaction_info.get('Applicant'):
            if details.get("Applicant / Co-Applicant Indicator") == "BW":

                FileMaster.objects.filter(id=file_id).update(
                    borrower_name=details.get('Applicant First Name'),
                    borrower_phone=details.get('Home Phone'),
                    borrower_email=details.get('Email Address'),
                    
                )
                
                # Convert the Date of Birth to date formate
                bw_dob = date_convertion(details.get('Date of Birth'))

                # Get the Particualr Borrower deatils using SSN number
                bw_details = transaction_info.get(details.get('SSN'))

                try:
                    state = StateMaster.objects.get(is_active='Y',fnm_state_value=bw_details.get('Residence State'))
                    state = state.id
                except StateMaster.DoesNotExist:
                    state = None

                # save the all the details in backend with out showing in the webpage
                filemaster = FileMaster.objects.get(id=filemaster.id)
                filemaster.file_id = details.get('Applicant Last Name')
                filemaster.borrower_first_name = details.get('Applicant First Name')
                filemaster.borrower_middle_name = details.get('Applicant Middle Name')
                filemaster.borrower_last_name = details.get('Applicant Last Name')
                filemaster.borrower_dependents = details.get('Dependents (no.)')
                filemaster.borrower_social_security_number = details.get('SSN')
                filemaster.borrower_date_of_birth = bw_dob
                filemaster.borrower_years_in_school = str(details.get('Yrs. School'))
                filemaster.borrower_marital_status = details.get('Marital Status')
                filemaster.borrower_street = bw_details.get('Residence Street Address')
                filemaster.borrower_city = bw_details.get('Residence City')
                filemaster.borrower_state = state
                filemaster.borrower_zip = bw_details.get('Residence Zip Code')
                filemaster.borrower_country = bw_details.get('Country')
                filemaster.borrower_address_type = bw_details.get('Own/Rent/Living Rent Free')
                filemaster.borrower_years_in_address = bw_details.get('No. Yrs.')
                filemaster.save()

                try:
                    state = StateMaster.objects.get(is_active='Y',fnm_state_value=bw_details.get('Employer State'))
                    state = state.id
                except StateMaster.DoesNotExist:
                    state = None

                BorrowerEmploymentDetails.objects.filter(file_id=filemaster.id).delete()
                FileAssets.objects.filter(file_id=filemaster.id).delete()
                FileLiabilities.objects.filter(file_id=filemaster.id).delete()
                FileExpensesBorrower.objects.filter(file_id=filemaster.id).delete()
                DeclarationMap.objects.filter(file_id=filemaster.id).delete()

                bw_emp_details = BorrowerEmploymentDetails.objects.get_or_create(
                    file_id=filemaster,
                    employer_name=bw_details.get('Employer Name'),
                    employer_street_address=bw_details.get('Employer Street Address'),
                    employer_city=bw_details.get('Employer City'),
                    employer_zip=bw_details.get('Employer Zip Code'),
                    employer_state=state,
                    self_employed=Boolen_field.get(bw_details.get('Self Employed')),
                    no_of_years_in_this_job=bw_details.get('Yrs. on this job'),
                    yrs_employed_in_this_line_of_work_profession=bw_details.get('Yrs. employed in this line of work/profession'),
                    position_title_type_of_business=bw_details.get('Position / Title / Type of Business'),
                    business_phone=bw_details.get('Business Phone', None),
                )

                assets_details = FileAssets.objects.get_or_create(
                    file_id=filemaster,
                    file_assets=bw_details.get('Asset Description'),
                    file_cash_or_description_market_value=bw_details.get('Cash or Market Value'),
                    file_months_left_to_pay = bw_details.get('Months Left to Pay'),
                    file_acct_no=bw_details.get('Acct. no.')
                )


                liabilities_details = FileLiabilities.objects.get_or_create(
                    file_id=filemaster,
                    file_liabilities_name = bw_details.get('Creditor Name'),
                    file_liabilities_street_address = bw_details.get('Creditor Street Address'),
                    file_liabilities_city = bw_details.get('Creditor City'),
                    file_liabilities_state = bw_details.get('Creditor State'),
                    file_liabilities_zip = bw_details.get('Creditor Zip Code'),
                    file_liabilities_monthly_payment = bw_details.get('Monthly Payment Amount'),
                    file_liabilities_unpaid_balance = bw_details.get('Unpaid Balance'),
                )

                bw_expense = FileExpensesBorrower.objects.get_or_create(
                    file_id=filemaster,
                    monthly_income=bw_details.get('Monthly Income'),
                    net_rental_income=bw_details.get('Net Rental Income')
                )

                for dec in dec_list:
                    desc_values = DeclarationMap.objects.get_or_create(
                        file_id=filemaster,
                        declaration_description=dec,
                        value=bw_details.get(dec),
                        types='borrower',
                        borrower_id=details.get('SSN'),
                    )

            if details.get("Applicant / Co-Applicant Indicator") == "QZ":
                # Convert the Date of Birth to date formate

                cw_dob = date_convertion(details.get('Date of Birth'))

                co_borrower_applicant_list.append(details)
                # Get the Particualr Borrower deatils using SSN number
                cw_details = transaction_info.get(details.get('SSN'))

                co_borrower_list.append(cw_details)

        file_co_borrower = FileCoBorrower.objects.filter(file_id=filemaster).delete()
        for co_br in co_borrower_applicant_list:
            try:
                file_co_borrower = FileCoBorrower.objects.create(
                    file_id=filemaster,
                    co_borrower_social_security_number=co_br.get('SSN'),
                    co_borrower_name=co_br.get('Applicant First Name'),
                    co_borrower_email=co_br.get('Email Address'),
                    co_borrower_phone=co_br.get('Home Phone'),
                    co_borrower_first_name = details.get('Applicant First Name'),
                    co_borrower_middle_name = details.get('Applicant Middle Name'),
                    co_borrower_last_name = details.get('Applicant Last Name'),
                    co_borrower_dependents = details.get('Dependents (no.)'),
                    co_borrower_date_of_birth = date_convertion(details.get('Date of Birth')),
                    co_borrower_years_in_school = details.get('Yrs. School'),
                    co_borrower_marital_status = details.get('Marital Status'),
                    created_by=user_obj
                )
            except Exception as e:
                pass

        cw_emp_details = CoBorrowerEmploymentDetails.objects.filter(file_id=filemaster, cw_id=file_co_borrower).delete()
        cw_expense = FileExpensesCoBorrower.objects.filter(file_id=filemaster, cw_id=file_co_borrower).delete()
        DeclarationMap.objects.filter(file_id=filemaster, cw_id=file_co_borrower).delete()

        for co_br in co_borrower_list:
            try:
                state = StateMaster.objects.get(is_active='Y',fnm_state_value=co_br.get('Residence State'))
                state = state.id
            except StateMaster.DoesNotExist:
                state = None
            
            try:
                employee_state = StateMaster.objects.get(is_active='Y',fnm_state_value=co_br.get('Employer State'))
                employee_state = employee_state.id
            except StateMaster.DoesNotExist:
                employee_state = None

            file_co_borrower = FileCoBorrower.objects.get(id=file_co_borrower.id)
            file_co_borrower.co_borrower_street = co_br.get('Residence Street Address')
            file_co_borrower.co_borrower_city = co_br.get('Residence City')
            file_co_borrower.co_borrower_state = state
            file_co_borrower.co_borrower_zip = co_br.get('Residence Zip Code')
            file_co_borrower.co_borrower_country = co_br.get('Country')
            file_co_borrower.co_borrower_address_type = co_br.get('Own/Rent/Living Rent Free')
            file_co_borrower.co_borrower_years_in_address = co_br.get('No. Yrs.')
            file_co_borrower.updated_by=user_obj
            file_co_borrower.save()

            try:
                cw_emp_details = CoBorrowerEmploymentDetails.objects.create(
                    file_id=filemaster,
                    cw_id=file_co_borrower,
                    employer_name=co_br.get('Employer Name'),
                    employer_street_address=co_br.get('Employer Street Address'),
                    employer_city=co_br.get('Employer City'),
                    employer_zip=co_br.get('Employer Zip Code'),
                    employer_state=employee_state,
                    self_employed=Boolen_field.get(co_br.get('Self Employed')),
                    no_of_years_in_this_job=co_br.get('Yrs. on this job'),
                    yrs_employed_in_this_line_of_work_profession=co_br.get('Yrs. employed in this line of work/profession'),
                    position_title_type_of_business=co_br.get('Position / Title / Type of Business'),
                    business_phone=co_br.get('Business Phone', None),
                )
            except Exception as e:
                pass


            try:
                cw_expense = FileExpensesCoBorrower.objects.create(
                    file_id=filemaster,
                    cw_id=file_co_borrower,
                    monthly_income=co_br.get('Monthly Income'),
                    net_rental_income=co_br.get('Net Rental Income')
                )
            except Exception:
                pass
            
            for dec in dec_list:
                desc_values = DeclarationMap.objects.create(
                    file_id=filemaster, cw_id=file_co_borrower,
                    declaration_description=dec,
                    value=co_br.get(dec),
                    types='co-borrower',
                    co_borrower_id=file_co_borrower.co_borrower_social_security_number
                )
    return HttpResponseRedirect('/file/view/{}'.format(file_id))

def date_tracker_update(request, file_id):
    if(request.session.has_key('company_id') == False):
        return HttpResponseRedirect('/')
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)
    
    if request.method == 'POST':
        appraisal_delivery_date = request.POST.get('appraisal_delivery_date')
        approval_expiration = request.POST.get('approval_expiration', "")
        asset_expiration_date = request.POST.get('asset_expiration_date', "")
        broker_last_upload = request.POST.get('broker_last_upload', "")
        cpl_expiration_date = request.POST.get('cpl_expiration_date')
        credit_expiration_date = request.POST.get('credit_expiration_date', "")
        disclosure_date = request.POST.get('disclosure_date', "")
        hoi_effective_date = request.POST.get('hoi_effective_date')
        income_expiration_date = request.POST.get('income_expiration_date', "")
        oldest_document_expired = request.POST.get('oldest_document_expired',"")
        payoff_exp = request.POST.get('payoff_exp',"")
        short_sale_expiration_date = request.POST.get('short_sale_expiration_date', "")
        title_expiration_date = request.POST.get('title_expiration_date', "")
        vvoe_ordered_date = request.POST.get('vvoe_ordered_date', "")
        vvoe_receive_date = request.POST.get('vvoe_receive_date', "")
        vvoe_expiration_date = request.POST.get('vvoe_expiration_date', "")

        generated_date = request.POST.get('generated_date', "")
        signature_date = request.POST.get('signature_date', "")
        submitted_to_uw = request.POST.get('submitted_to_uw', "")

        initial_loan_estimate = request.POST.get('initial_loan_estimate', "")
        most_recent_loan_estimate = request.POST.get('most_recent_loan_estimate', "")
        initial_closing_disclosure = request.POST.get('initial_closing_disclosure', "")
        

        most_recent_closing_disclosure = request.POST.get('most_recent_closing_disclosure', "")
        cleared_to_close = request.POST.get('cleared_to_close', "")
        estimate_close_date = request.POST.get('estimate_close_date', "")

        tax_transcript_received_date = request.POST.get('tax_transcript_received_date')
        tax_transcript_ordered_date = request.POST.get('tax_transcript_ordered_date')

        closing_datetime = request.POST.get('closing_datetime')
        wire_ordered_date = request.POST.get('wire_ordered_date')
        wire_disbursement = request.POST.get('wire_disbursement')
        wire_date = request.POST.get('wire_date')
        first_payment =request.POST.get('first_payment')
        date_to_avoid_epo =request.POST.get('date_to_avoid_epo')

        
        file_master = FileMaster.objects.get(id=file_id)
        
        if(len(most_recent_closing_disclosure)>0):
           file_master.most_recent_closing_disclosure=most_recent_closing_disclosure
        if(len(credit_expiration_date)>0):
            file_master.credit_expiration_date=credit_expiration_date
        if(len(cleared_to_close)>0):
           file_master.cleared_to_close=cleared_to_close
        if(len(estimate_close_date)>0):
           file_master.estimate_close_date=estimate_close_date

        if(len(generated_date)>0):
           file_master.generated_date=generated_date
        if(len(signature_date)>0):
           file_master.signature_date=signature_date
        if(len(submitted_to_uw)>0):
           file_master.submitted_to_uw=submitted_to_uw
        if(len(initial_loan_estimate)>0):
           file_master.initial_loan_estimate=initial_loan_estimate
        if(len(most_recent_loan_estimate)>0):
           file_master.most_recent_loan_estimate=most_recent_loan_estimate
        if(len(initial_closing_disclosure)>0):
            file_master.initial_closing_disclosure=initial_closing_disclosure
        
        if(len(approval_expiration)>0):
           file_master.approval_expiration=approval_expiration
        if(len(asset_expiration_date)>0):
           file_master.asset_expiration_date=asset_expiration_date
        if(len(broker_last_upload)>0):
           file_master.broker_last_upload=broker_last_upload
        if(len(cpl_expiration_date)>0):
           file_master.cpl_expiration_date=cpl_expiration_date
        if(len(disclosure_date)>0):
           file_master.disclosure_date=disclosure_date
        if(len(hoi_effective_date)>0):
           file_master.hoi_effective_date=hoi_effective_date
        if(len(income_expiration_date)>0):
           file_master.income_expiration_date=income_expiration_date
        if(len(oldest_document_expired)>0):
           file_master.oldest_document_expired=oldest_document_expired
        if(len(payoff_exp)>0):
               file_master.payoff_exp=payoff_exp
        if(len(short_sale_expiration_date)>0):
           file_master.short_sale_expiration_date=short_sale_expiration_date
        if(len(title_expiration_date)>0):
           file_master.title_expiration_date=title_expiration_date
        if(len(vvoe_ordered_date)>0):
           file_master.vvoe_ordered_date=vvoe_ordered_date
        if(len(vvoe_receive_date)>0):
           file_master.vvoe_receive_date=vvoe_receive_date
        if(len(vvoe_expiration_date)>0):
           file_master.vvoe_expiration_date=vvoe_expiration_date
        if(len(tax_transcript_received_date)>0):
               file_master.tax_transcript_received_date=tax_transcript_received_date
        if(len(tax_transcript_ordered_date)>0):
               file_master.tax_transcript_ordered_date=tax_transcript_ordered_date
        if(len(closing_datetime)>0):
            file_master.closing_datetime=closing_datetime
        if(len(wire_ordered_date)>0):
            file_master.wire_ordered_date=wire_ordered_date
        if(len(wire_disbursement)>0):
            file_master.wire_disbursement=wire_disbursement
        if(len(wire_date)>0):
            file_master.wire_date=wire_date
        if(len(first_payment)>0):
            file_master.first_payment=first_payment
        if(len(date_to_avoid_epo)>0):
            file_master.date_to_avoid_epo=date_to_avoid_epo
        if(len(appraisal_delivery_date)>0):
            file_master.appraisal_delivery_date=appraisal_delivery_date
        appraisal_delivery_date

        file_master.save()

        co_borrower_tax_transcript_received_date = request.POST.getlist('co_borrower_tax_transcript_received_date')
        co_borrower_tax_transcript_ordered_date = request.POST.getlist('co_borrower_tax_transcript_ordered_date')
        co_borrower_date_ids = request.POST.getlist('co_borrower_date_ids')

        co_borrowerdateids  = len(co_borrower_date_ids)
        date_count = 0
        while date_count < co_borrowerdateids:
            tt_received_date = co_borrower_tax_transcript_received_date[date_count]
            if len(tt_received_date) == 0:
                tt_received_date=None
            
            tt_ordered_date = co_borrower_tax_transcript_ordered_date[date_count]
            if len(tt_ordered_date) == 0:
                tt_ordered_date=None

            FileCoBorrower.objects.filter(id=co_borrower_date_ids[date_count]).update(
                co_borrower_tax_transcript_ordered_date = tt_ordered_date,
                co_borrower_tax_transcript_received_date = tt_received_date,
            )
            date_count += 1

    request.session['div_id'] = 'date-tracking'
    return HttpResponseRedirect('/file/view/{}'.format(file_id))

def update_transaction_file(request, file_id):
    """Update the transaction details"""
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        # Get status master from status id
        status_id = request.POST['status']
        status_obj = LoanStatusMaster.objects.get(id=status_id)

        # Get sub master with Sub status id
        sub_status_id = None
        if 'sub_status_id' in request.POST:
            sub_status_id = request.POST['sub_status_id']
        if len(sub_status_id)==0:
            sub_status_obj = None
        else:
            sub_status_obj = LoanSubStatusMaster.objects.get(id=sub_status_id)

        # Get group id and user id with the assigned user id
        processor_id = request.POST['assigned_user_id']
        if len(processor_id) > 0:
            try:
                user_processor_obj = UserMaster.objects.get(id=processor_id)
            except Exception:
                user_processor_obj = None
            
            if user_processor_obj:
                try:
                    user_group_id = UserGroupMap.objects.get(user_id=user_processor_obj)
                    user_group_id = user_group_id.group_id
                except Exception:
                    user_group_id = None
            else:
                user_group_id = None
        else:
            user_processor_obj = None
            user_group_id = None

        brokerage = request.POST['brokerage']
        program_code = request.POST['program_code']
        customer_id = request.POST['customer_id']

        # Loan offcier
        loan_officer_id = None
        loan_officer__obj = None
        if 'lo_name' in request.POST:
            loan_officer_id = request.POST['lo_name']
        if loan_officer_id:
            loan_officer__obj = UserMaster.objects.get(id=loan_officer_id)
        
        nmls_id = request.POST['nmls_id']
        lo_email = request.POST['lo_email']
        lo_direct = request.POST['lo_direct']
        lo_fax = request.POST['lo_fax']
        ae_name = request.POST['ae_name']
        ae_direct = request.POST['ae_direct']
        ae_email = request.POST['ae_email']
        ae_fax = request.POST['ae_fax']
        ae_company_id = request.POST['ae_company_id']
        charge_processing_fee = request.POST['charge_processing_fee']
        url = request.POST['url']

        estimate_close_date = request.POST['estimate_close_date']
        lender = request.POST['lender']
        tax_transcript = request.POST['tax_transcript']
        tt_date = request.POST['tt_date']
        closing_disclosure = request.POST['closing_disclosure']
        cd_date = request.POST['cd_date']
        appraisal_ordered = request.POST['appraisal_ordered']
        ad_date = request.POST['ad_date']
        recieved_date = request.POST['recieved_date']
        note = request.POST['note']
        
        if len(tax_transcript)==0:
            tax_transcript_obj = None
        else:
            tax_transcript_obj = TaxTranscriptMaster.objects.get(id=tax_transcript)

        if len(closing_disclosure)>0:
            closing_disclosure_obj = ClosingDisclosureMaster.objects.get(id=closing_disclosure)
        else:
            closing_disclosure_obj = None

        if len(appraisal_ordered)>0:
            appraisal_ordered_obj = AppraisalOrderedMaster.objects.get(id=appraisal_ordered)
        else:
            appraisal_ordered_obj = None
        
        if len(tt_date)==0:
            tt_date = None

        if len(cd_date) == 0:
            cd_date = None

        if len(ad_date) == 0:
            ad_date = None

        if len(recieved_date)==0:
            recieved_date = None

        FileMaster.objects.filter(id=file_id).update(
            status_id=status_obj, sub_status_id=sub_status_obj,
            assigned_group_id=user_group_id, assigned_user_id=user_processor_obj,
            brokerage=brokerage, program_code=program_code,
            loan_officer_id=loan_officer__obj, loan_officer_direct=lo_direct, loan_officer_email=lo_email,
            loan_officer_fax=lo_fax, nmls_id=nmls_id,lender=lender,
            ae_name=ae_name, ae_direct=ae_direct, ae_email=ae_email,ae_fax=ae_fax,
            ae_company_id=ae_company_id, est_closure_date=date_convertion_create(estimate_close_date),
            charging_processing_fees=charge_processing_fee, customer_id=customer_id,
            url=url, tax_transcript=tax_transcript_obj,closing_disclosure=closing_disclosure_obj,
            appraisal_ordered=appraisal_ordered_obj, note=note,
            recieved_date=date_convertion_create(recieved_date), appraisal_ordered_date=date_convertion_create(ad_date), closing_disclosure_date=date_convertion_create(cd_date),
            tax_transcript_date=date_convertion_create(tt_date), updated_by=user_obj
        )

        # Loan information
        loan_purpose_obj = None
        if 'loan_purpose' in request.POST:
            loan_purpose = request.POST['loan_purpose']
            try:
                loan_purpose_obj = LoanPurposeMaster.objects.get(id=loan_purpose)
            except ValueError:
                pass

        loan_number = None
        if 'loan_number' in request.POST:
            loan_number = request.POST['loan_number']

        lock_expiration_date = None
        if 'lock_expiraton_date' in request.POST and len(request.POST['lock_expiraton_date'])>1:
            lock_expiration_date = request.POST['lock_expiraton_date']

        loan_float = None
        if 'float' in request.POST:
            loan_float  = request.POST['float']

        property_type_obj = None
        if 'property_type' in request.POST:
            property_type = request.POST['property_type']
            try:
                property_type_obj = PropertyTypeMaster.objects.get(id=property_type)
            except ValueError:
                pass

        rate_type_obj = None
        if 'rate_type' in request.POST:
            rate_type = request.POST['rate_type']
            try:
                rate_type_obj = RateTypeMaster.objects.get(id=rate_type)
            except ValueError:
                pass
        rate = None
        if 'rate' in request.POST:
            rate = request.POST['rate']
        
        piw = None
        if 'piw' in request.POST:
            piw = request.POST['piw']

        impound_obj = None
        if 'impound' in request.POST:
            impound = request.POST['impound']
            try:
                impound_obj = ImpoundMaster.objects.get(id=impound)
            except ValueError:
                pass

        term_obj = None
        if 'term' in request.POST:
            term = request.POST['term']
            try:
                term_obj = TermMaster.objects.get(id=term)
            except ValueError:
                pass
        
        occupancy_master_obj = None
        if 'occupancy_master' in request.POST:
            try:
                occupancy_master = request.POST['occupancy_master']
                try:
                    occupancy_master_obj = OccupancyMaster.objects.get(id=occupancy_master)
                except ValueError:
                    pass
            except ValueError:
                pass

        subordination = None
        if 'subordination' in request.POST:
            subordination = request.POST['subordination']

        loan_amount = None
        if 'loan_amount' in request.POST:
            loan_amount = request.POST['loan_amount']

        loan_amount_2 = None
        if 'loan_amount_2' in request.POST:
            loan_amount_2 = request.POST['loan_amount_2']

        appraised_value = None
        if 'appraised_value' in request.POST:
            appraised_value = request.POST['appraised_value']
        
        ltv = None
        if 'ltv' in request.POST:
            ltv = request.POST['ltv']

        cltv = None
        if 'cltv' in request.POST:
            cltv = request.POST['cltv']

        reverse_status = None
        if 'reverse_status' in request.POST:
            reverse_status = request.POST['reverse_status']

        compensation_payer_type_obj = None
        if 'compensation_payer_type' in request.POST:
            compensation_payer_type = request.POST['compensation_payer_type']
            try:
                compensation_payer_type_obj = CompensationPayerTypeMaster.objects.get(
                    id=compensation_payer_type)
            except ValueError:
                pass
        
        charge_appraisal = None
        if 'charge_appraisal' in request.POST:
            charge_appraisal = request.POST['charge_appraisal']

        deliver_disclosures = None
        if 'deliver_disclosures' in request.POST:
            deliver_disclosures = request.POST['deliver_disclosures']

        deliver_disclosures_type = None
        if 'deliver_disclosures_type' in request.POST:
            deliver_disclosures_type = request.POST['deliver_disclosures_type']
        
        request_conditions_stips_from = None
        if 'request_conditions_stips_from' in request.POST:
            request_conditions_stips_from = request.POST['request_conditions_stips_from']

        charge_credit_report = None
        if 'charge_credit_report' in request.POST:
            charge_credit_report = request.POST['charge_credit_report']


        FileMaster.objects.filter(id=file_id).update(
            loan_number=loan_number,
            loan_amount=loan_amount,
            loan_amount_2=loan_amount_2, 
            appraisal_value=appraised_value,
            ltv=ltv,
            rate=rate,
            float=loan_float,
            lock_expiration_date=date_convertion_create(lock_expiration_date),
            loan_purpose_id=loan_purpose_obj,
            reverse_status=reverse_status,
            property_type=property_type_obj,
            impound=impound_obj,
            subordination=subordination,
            piw=piw,
            cltv=cltv,
            term=term_obj,
            rate_type=rate_type_obj, 
            occupancy=occupancy_master_obj,
            charge_appraisal=charge_appraisal,
            delievery_disclosure=deliver_disclosures,
            delievery_disclosure_type=deliver_disclosures_type,
            req_condition_stip_from=request_conditions_stips_from,
            charge_credit_report=charge_credit_report,
            updated_by=user_obj
        )

        # property information
        address_fill = None
        if 'address_fill' in request.POST:
            address_fill = request.POST['address_fill']

        property_address = None
        if 'property_address' in request.POST:
            property_address = request.POST['property_address']

        property_city = None
        if 'property_city' in request.POST:
            property_city = request.POST['property_city']
        
        property_state_master_obj = None
        if 'property_state' in request.POST:
            property_state = request.POST['property_state']
            try:
                property_state_master_obj = StateMaster.objects.get(id=property_state)
            except ValueError:
                pass
    
        property_zipcode = None
        if 'property_zipcode' in request.POST:
            property_zipcode = request.POST['property_zipcode']

        mailing_address = None
        if 'mailing_address' in request.POST:
            mailing_address = request.POST['mailing_address']

        mailing_city = None
        if 'mailing_city' in request.POST:
            mailing_city = request.POST['mailing_city']

        mailing_state_master_obj = None
        if 'mailing_state' in request.POST:
            mailing_state = request.POST['mailing_state']
            try:
                mailing_state_master_obj = StateMaster.objects.get(id=mailing_state)
            except ValueError:
                pass

        mailing_zipcode = None
        if 'mailing_zipcode' in request.POST:
            mailing_zipcode = request.POST['mailing_zipcode']

        FilePropertyMap.objects.filter(file_id=file_id).update(
            property_address=property_address,
            property_city=property_city,
            property_state=property_state_master_obj,
            property_zipcode=property_zipcode,
            mailing_address=mailing_address,
            mailing_city=mailing_city,
            mailing_state=mailing_state_master_obj,
            mailing_zipcode=mailing_zipcode,
            mailing_address_check=address_fill,
            updated_by=user_obj
        )
        
        borrower_name = None
        if 'borrower_name' in request.POST:
            borrower_name = request.POST['borrower_name']
        
        borrower_phone = None
        if 'borrower_phone' in request.POST:
            borrower_phone = request.POST['borrower_phone']
        
        borrower_email = None
        if 'borrower_email' in request.POST:
            borrower_email = request.POST['borrower_email']
        try:
            borrower_name = str(borrower_name).strip()
            file_master_file_name = borrower_name.split(' ')[-1]
        except Exception:
            file_master_file_name = None

        FileMaster.objects.filter(id=file_id).update(
            borrower_name=borrower_name,
            borrower_phone=borrower_phone,
            borrower_email=borrower_email,
            file_id=file_master_file_name
        )

        emp_details = BorrowerEmploymentDetails.objects.filter(file_id=file_id)
        if not emp_details:
            file_id_emp = FileMaster.objects.get(id=file_id)
            BorrowerEmploymentDetails.objects.create(
                file_id=file_id_emp
            )

        expenses_details = FileExpensesBorrower.objects.filter(file_id=file_id)
        if not expenses_details:
            file_id_expense = FileMaster.objects.get(id=file_id)
            FileExpensesBorrower.objects.create(
                file_id=file_id_expense
            )


        co_borrower_name_array = []
        if 'co_borrower_name[]' in request.POST:
            co_borrower_name_array = request.POST.getlist('co_borrower_name[]')

        co_borrower_phone_array = []
        if 'co_borrower_phone[]' in request.POST:
            co_borrower_phone_array = request.POST.getlist('co_borrower_phone[]')
        
        co_borrower_email_array = []
        if 'co_borrower_email[]' in request.POST:
            co_borrower_email_array = request.POST.getlist('co_borrower_email[]')

        co_borrower_id_array = []
        if 'co_borrower_id' in request.POST:
            co_borrower_id_array = request.POST.getlist('co_borrower_id')

        co_borrower_length = len(co_borrower_name_array)
        co_borrower_count = 0
        while co_borrower_count < co_borrower_length:
            file_co_borrower = FileCoBorrower.objects.filter(id=co_borrower_id_array[co_borrower_count]).update(
                co_borrower_name=co_borrower_name_array[co_borrower_count],
                co_borrower_email=co_borrower_email_array[co_borrower_count],
                co_borrower_phone=co_borrower_phone_array[co_borrower_count],
                created_by=user_obj
            )
            co_borrower_count += 1

        # File Escrow Master
        company_name = None
        if 'escrow_company' in request.POST:
            company_name = request.POST['escrow_company']
        
        number = None
        if 'escrow_number' in request.POST:
            number = request.POST['escrow_number']

        officer_name = None
        if 'escrow_officer' in request.POST:
            officer_name = request.POST['escrow_officer']
        
        officer_phone = None
        if 'escrow_phone' in request.POST:
            officer_phone = request.POST['escrow_phone']

        officer_email = None
        if 'escrow_email' in request.POST:
            officer_email = request.POST['escrow_email']

        is_open = None
        if 'please_open' in request.POST:
            is_open = request.POST['please_open']

        opened_date = None
        if 'escrow_open_date' in request.POST and len(request.POST['escrow_open_date']) > 1:
            opened_date = request.POST['escrow_open_date']

        assistant_name = None
        if 'escrow_assistant' in request.POST:
            assistant_name = request.POST['escrow_assistant']

        assitant_phone = None
        if 'assistant_phone' in request.POST:
            assitant_phone = request.POST['assistant_phone']

        assistant_email = None
        if 'assistant_email' in request.POST:
            assistant_email = request.POST['assistant_email']

        requested_escrow_fees = None
        if 'requested_escrow_fees' in request.POST:
            requested_escrow_fees = request.POST['requested_escrow_fees']

        
        file_escrow_map = FileEscrowMap.objects.filter(file_id=file_id).update(
            company_name=company_name,
            number=number,
            officer_name=officer_name,
            officer_phone=officer_phone,
            officer_email=officer_email,
            opened_date=date_convertion_create(opened_date),
            is_open=is_open,
            assistant_name=assistant_name,
            assitant_phone=assitant_phone,
            assistant_email=assistant_email,
            requested_escrow_fees=requested_escrow_fees,
            updated_by=user_obj
        )

        # File Title Master
        title_name = None
        if 'title' in request.POST:
            title_name = request.POST['title']
        
        title_order = None
        if 'title_order' in request.POST:
            title_order = request.POST['title_order']

        title_rep_name = None
        if 'title_rep' in request.POST:
            title_rep_name = request.POST['title_rep']

        title_rep_phone =  None
        if 'title_rep_phone' in request.POST:
            title_rep_phone = request.POST['title_rep_phone']

        title_rep_email = None
        if 'title_rep_email' in request.POST:
            title_rep_email = request.POST['title_rep_email']

        FileTitleMap.objects.filter(file_id=file_id).update(
            title_name=title_name,
            title_order=title_order,
            title_rep_name=title_rep_name,
            title_rep_phone=title_rep_phone,
            title_rep_email=title_rep_email,
            updated_by=user_obj
        )

        # File HOA Master
        hoa = None
        if 'hoa' in request.POST:
            hoa = request.POST['hoa']
        hoa_phone = None
        if 'hoa_phone' in request.POST:
            hoa_phone = request.POST['hoa_phone']
        hoa_email = None
        if 'hoa_email' in request.POST:
            hoa_email = request.POST['hoa_email']
        FileHoa.objects.filter(file_id=file_id).update(
            hoa_name=hoa,
            hoa_phone=hoa_phone,
            hoa_email=hoa_email,
            updated_by=user_obj
        )
        # File Lisiting Buyer Master
        listing_office = None
        if 'listing_office' in request.POST:
            listing_office = request.POST['listing_office']
        listing_agent = None
        if 'listing_agent' in request.POST:
            listing_agent = request.POST['listing_agent']
        listing_agent_phone = None
        if 'listing_agent_phone' in request.POST:
            listing_agent_phone = request.POST['listing_agent_phone']
        listing_agent_email = None
        if 'listing_agent_email' in request.POST:
            listing_agent_email = request.POST['listing_agent_email']
        buyer_re_office = None
        if 'buyer_office' in request.POST:
            buyer_re_office = request.POST['buyer_office']
        buyer_agent = None
        if 'buyer_agent' in request.POST:
            buyer_agent = request.POST['buyer_agent']
        buyer_agent_phone = None
        if 'buyer_agent_phone' in request.POST:
            buyer_agent_phone = request.POST['buyer_agent_phone']
        buyer_agent_email = None
        if 'buyer_agent_email' in request.POST:
            buyer_agent_email = request.POST['buyer_agent_email']

        FileListingBuyer.objects.filter(file_id=file_id).update(
            listing_office=listing_office,
            listing_agent=listing_agent,
            listing_agent_phone=listing_agent_phone,
            listing_agent_email=listing_agent_email,
            buyer_re_office=buyer_re_office,
            buyer_agent=buyer_agent,
            buyer_agent_phone=buyer_agent_phone,
            buyer_agent_email=buyer_agent_email,
            created_by=user_obj
        )
        # File Lisiting Buyer Master

    # convert the File object to serialize
    file_obj = FileMaster.objects.get(id=file_id)
    file_obj_to_serializer = serializers.serialize('json', [file_obj,])
    file_json = json.loads(file_obj_to_serializer)
    file_data = json.dumps(file_json[0])
    file_data = json.loads(file_data)

    # Escorw details

    try:
        file_escrow = FileEscrowMap.objects.get(file_id=file_id)
        file_escrow_cn = file_escrow.company_name
        file_escrow_od = file_escrow.opened_date
    except Exception:
        file_escrow_cn = None
        file_escrow_od = None
    file_data = file_data.get('fields')

    try:
        file_loan_officer_id = UserMaster.objects.get(id=file_data.get('loan_officer_id'))
        file_loan_officer_id = file_loan_officer_id.user_name
    except Exception:
        file_loan_officer_id = None

    try:
        file_tax_transcript = TaxTranscriptMaster.objects.get(id=file_data.get('tax_transcript'))
        file_tax_transcript = file_tax_transcript.tt_value
    except Exception:
        file_tax_transcript = None

    try:
        file_appraisal = AppraisalOrderedMaster.objects.get(id=file_data.get('appraisal_ordered'))
        file_appraisal = file_appraisal.ad_value
    except Exception:
        file_appraisal = None
    
    try:
        file_closing_value = ClosingDisclosureMaster.objects.get(id=file_data.get('closing_disclosure'))
        file_closing_value = file_closing_value.cd_value
    except Exception:
        file_closing_value = None


    file_data.update({
        'escrow_company':file_escrow_cn,
        'escrow_opened_date':file_escrow_od,
        'loan_user_name': file_loan_officer_id,
        'file_tax_transcript': file_tax_transcript,
        'file_appraisal_value':file_appraisal,
        'file_closing_value': file_closing_value,
    })  

    return JsonResponse({
        'file':file_data
    })

def delete_co_borrower(request):
    co_borrower_id = request.GET.get('co_borrower_id')
    FileCoBorrower.objects.filter(id=co_borrower_id).delete()
    return JsonResponse({'is_delete':'success'})

def add_co_borrower(request):
    """Add the Co borrower"""
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)

    file_id = request.GET.get('file_id')
    file_id = FileMaster.objects.get(id=file_id)

    co_borrower_name = request.GET.get('co_borrower_name')
    co_borrower_phone = request.GET.get('co_borrower_phone')
    co_borrower_email = request.GET.get('co_borrower_email')

    file_co_borrower = FileCoBorrower.objects.create(
        file_id=file_id,
        co_borrower_name=co_borrower_name,
        co_borrower_email=co_borrower_email,
        co_borrower_phone=co_borrower_phone,
        created_by=user_obj
    )

    dec_list = [
        'a. Are there any outstanding judgments against you?',
        'b. Have you been declared bankrupt within the past 7 years?',
        'c. Have you had property foreclosed upon or given title or deed in lieu thereof in the last 7 years?',
        'd. Are you a party to a lawsuit?',
        'e. Have you directly or indirectly been obligated on any loan…',
        'f. Are you presently delinquent or in default on any Federal debt…',
        'g. Are you obligated to pay alimony child support or separate maintenance?',
        'h. Is any part of the down payment borrowed?',
        'i. Are you a co-maker or',
        'j. Are you a U.S. citizen? k. Are you a permanent resident alien?',
        'l. Do you intend to occupy…',
        'm. Have you had an ownership interest…',
        'm. (1) What type of property…',
        'm. (2) How did you hold title…'
    ]
    for dec in dec_list:
        desc_values = DeclarationMap.objects.create(
            file_id=file_id,
            declaration_description=dec,
            types='co-borrower',
            cw_id=file_co_borrower
        )
    
    FileExpensesCoBorrower.objects.create(
        file_id=file_id,
        cw_id=file_co_borrower
    )

    CoBorrowerEmploymentDetails.objects.create(
        file_id=file_id,
        cw_id=file_co_borrower
    )

    return JsonResponse({'file_co_borrower_id': file_co_borrower.id})

def type_of_mortgage(request):
    """Add the Mortgage details"""
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)

    file_id = request.POST.get('file_id')
    agency_case_number = request.POST.get('agency_case_number')
    lender_case_number = request.POST.get('lender_case_number')
    loan_amount = request.POST.get('loan_amount')
    rate = request.POST.get('rate')
    term = request.POST.get('term')
    rate_type = request.POST.get('rate_type')
    mortage_applied = request.POST.get('mortage_applied')

    
    try:
        rate_type_obj = RateTypeMaster.objects.get(id=rate_type)
    except Exception:
        rate_type_obj = None

    
    try:
        term_obj = TermMaster.objects.get(id=term)
    except Exception:
        term_obj = None
    
    try:
        mortgage = FileMortage.objects.get(id=mortage_applied, is_active='Y')
        mortgage = mortgage.mortage_applied_title
    except Exception:
        mortgage = None

    FileMaster.objects.filter(id=file_id).update(
        agency_case_number=agency_case_number,
        lender_case_number=lender_case_number,
        loan_amount=loan_amount,
        rate=rate,
        term=term_obj,
        rate_type=rate_type_obj,
        mortgage_applied=mortgage,
        updated_by=user_obj
    )
    request.session['div_id'] = 'type_of_mortgage-details'
    return JsonResponse({'is_updated': 'success'})

def property_information(request):
    """Add the property info details"""
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)

    file_id = request.POST.get('file_id')
    property_address = request.POST['property_address']
    property_city = request.POST['property_city']
    property_state = request.POST['property_state']
    try:
        property_state_master_obj = StateMaster.objects.get(id=property_state)
    except Exception:
        property_state_master_obj = None
    property_zipcode = request.POST['property_zipcode']

    no_of_units = request.POST['no_of_units']
    year_built = request.POST['year_built']
    type_loan_purpose = request.POST['type_loan_purpose']
    try:
        loan_purpose_obj = LoanPurposeMaster.objects.get(id=type_loan_purpose)
    except Exception:
        loan_purpose_obj = None
    property_type = request.POST['type_property_type']
    try:
        property_type_obj = PropertyTypeMaster.objects.get(id=property_type)
    except Exception:
        property_type_obj = None
    
    refinance_original_cost = request.POST['refinance_original_cost']
    refinance_purpose = request.POST['refinance_purpose']
    refinance_lot_year = request.POST['refinance_lot_year']
    construction_original_cost = request.POST['construction_original_cost']
    construction_lot_year = request.POST['construction_lot_year']
    source_of_down = request.POST['source_of_down']

    property_name = None
    if 'property_name' in request.POST:
        property_name = request.POST['property_name']

    property_title_will_be_held = None
    if 'property_title_will_be_held' in request.POST:
        property_title_will_be_held = request.POST['property_title_will_be_held']

    settlement_charges = None
    if 'settlement_charges' in request.POST:
        settlement_charges = request.POST['settlement_charges']

    subordinate_financing = None
    if 'subordinate_financing' in request.POST:
        subordinate_financing = request.POST['subordinate_financing']

    estate = None
    if 'estate' in request.POST:
        estate = request.POST['estate']

    construction_amount = None
    if 'construction_amount' in request.POST:
        construction_amount = request.POST['construction_amount']
    
    construction_present_value = None
    if 'construction_present_value' in request.POST:
        construction_present_value = request.POST['construction_present_value']
    
    construction_cost = None
    if 'construction_cost' in request.POST:
        construction_cost = request.POST['construction_cost']

    refinance_cost = None
    if 'refinance_cost' in request.POST:
        refinance_cost = request.POST['refinance_cost']
    
    refinance_amount = None
    if 'refinance_amount' in request.POST:
        refinance_amount = request.POST['refinance_amount']
    
    refinance_describe_improvements = None
    if 'refinance_describe_improvements' in request.POST:
        refinance_describe_improvements = request.POST['refinance_describe_improvements']

    construction_total = None
    if 'construction_total' in request.POST:
        construction_total = request.POST['construction_total']

    FilePropertyMap.objects.filter(file_id=file_id).update(
        property_address=property_address,
        property_city=property_city,
        property_state=property_state_master_obj,
        property_zipcode=property_zipcode,
        updated_by=user_obj
    )

    FileMaster.objects.filter(id=file_id).update(
        no_of_units=no_of_units,
        year_built=year_built,
        loan_purpose_id=loan_purpose_obj,
        property_type=property_type_obj,
        source_of_down=source_of_down,
        property_name=property_name,
        property_title_will_be_held=property_title_will_be_held,
        settlement_charges=settlement_charges,
        subordinate_financing=subordinate_financing,
        estate_will_be=estate,
        refinance_original_cost=refinance_original_cost,
        refinance_purpose=refinance_purpose,
        refinance_lot_year=refinance_lot_year,
        refinance_amount=refinance_amount,
        refinance_cost=refinance_cost,
        refinance_describe_improvements=refinance_describe_improvements,
        construction_original_cost=construction_original_cost,
        construction_lot_year=construction_lot_year,
        construction_amount = construction_amount,
        construction_present_value=construction_present_value,
        construction_cost=construction_cost,
        construction_total=construction_total
    )

    request.session['div_id'] = 'property_information-details'
    return JsonResponse({'is_updated': 'success'})


def declaration_information(request, file_id):
    """Add the property info details"""

    dec_list = [
        'a. Are there any outstanding judgments against you?',
        'b. Have you been declared bankrupt within the past 7 years?',
        'c. Have you had property foreclosed upon or given title or deed in lieu thereof in the last 7 years?',
        'd. Are you a party to a lawsuit?',
        'e. Have you directly or indirectly been obligated on any loan…',
        'f. Are you presently delinquent or in default on any Federal debt…',
        'g. Are you obligated to pay alimony child support or separate maintenance?',
        'h. Is any part of the down payment borrowed?',
        'i. Are you a co-maker or',
        'j. Are you a U.S. citizen? k. Are you a permanent resident alien?',
        'l. Do you intend to occupy…',
        'm. Have you had an ownership interest…',
        'm. (1) What type of property…',
        'm. (2) How did you hold title…'
    ]
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)

    file_id = FileMaster.objects.get(id=file_id)
    
    # Borrower Declaration update section
    br_declaration_ids = request.POST.getlist('br_declaration_ids')    
    br_declaration_names = [
        'borrower_a', 'borrower_b', 'borrower_c', 'borrower_d', 'borrower_e', 
        'borrower_f', 'borrower_g', 'borrower_h', 'borrower_i', 'borrower_j','borrower_l', 
        'borrower_m', 'borrower_n', 'borrower_o'
    ]
    if len(br_declaration_ids)<=0:
        for desc, br_name in zip(dec_list, br_declaration_names):
            desc_values = DeclarationMap.objects.create(
                file_id=file_id,
                declaration_description=desc,
                value=request.POST.get(br_name),
                types='borrower',
                borrower_id=file_id.borrower_social_security_number
            )
    else:
        for names, ids in zip(br_declaration_names,br_declaration_ids):
            update_declaration_value = request.POST.get(names)
            DeclarationMap.objects.filter(id=ids).update(
                value=update_declaration_value
            )


    # Coborrower declaration update section
    co_borrowers_ids = request.POST.getlist('co_borrower_ids')
    declaration_ids = request.POST.getlist('declaration_ids')
    declaration_names = ['co_borrower_a_', 'co_borrower_b_', 'co_borrower_c_', 'co_borrower_d_', 'co_borrower_e_', 
    'co_borrower_f_', 'co_borrower_g_', 'co_borrower_h_', 'co_borrower_i_', 'co_borrower_j_','co_borrower_l_', 
    'co_borrower_m_', 'co_borrower_n_', 'co_borrower_o_']

    for ids in declaration_ids:
        for names in declaration_names:
            names_ids = str(names) + str(ids)
            if names_ids in request.POST:
                update_declaration_value = request.POST.get(names_ids)
                DeclarationMap.objects.filter(id=ids).update(
                    value=update_declaration_value
                )

    request.session['div_id'] = 'declarations-details'
    return JsonResponse({'is_updated': 'success'})

def detail_transaction_details(request, file_id):
    """Add the transactions details"""
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)

    file_id = FileMaster.objects.get(id=file_id)
    transaction_details = ['purchase_price', 'alteration_improvement', 'land', 'refinance', 'estimate_prepaid_items',
    'estimate_closing_costs', 'pmi_mip', 'discount', 'subordinate_financing', 'pmi_mip_funded', 'total_cost', 'borrower_closing_seller',
    'loan_amount_exluded_pmi', 'loan_amount_add', 'cash_from_borower']

    if 'transaction_ids' in request.POST:
        transaction_ids = request.POST.getlist('transaction_ids')
        for ids, names in zip(transaction_ids, transaction_details):
            value = request.POST[names]
            DetailsTransactionMap.objects.filter(id=ids).update(
                value=value
            )
    else:
        for names in transaction_details:
            value = request.POST[names]
            DetailsTransactionMap.objects.create(
                file_id=file_id,
                transaction_description=names,
                value=value
            )

    request.session['div_id'] = 'details_transaction-details'
    return JsonResponse({'is_updated': 'success'})

def monthly_expenses_details(request, file_id):
    """Add the Expenses details"""
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)
    
    file_id = FileMaster.objects.get(id=file_id)

    # House Rent Expenses
    if 'house_present_ids' in request.POST:
        house_present_ids = request.POST['house_present_ids']
        if house_present_ids:
            FileHouseExpensesPresent.objects.filter(id=house_present_ids).update(
                rent=request.POST.get('rent_present', 0),
                first_mortgage=request.POST.get('first_mortgage_present', 0),
                other_financing=request.POST.get('other_financing_present', 0),
                hazard_insurance=request.POST.get('hazard_insurance_present', 0),
                real_estate_taxes=request.POST.get('real_estate_taxes_present', 0),
                mortgage_insurance=request.POST.get('mortgage_insurance_present', 0),
                other=request.POST.get('other_present', 0),
                homeowner_assn_dues=request.POST.get('homeowner_assn_dues_present', 0),
            )
        else:
            FileHouseExpensesPresent.objects.create(
                file_id=file_id,
                rent=request.POST.get('rent_present', 0),
                first_mortgage=request.POST.get('first_mortgage_present', 0),
                other_financing=request.POST.get('other_financing_present', 0),
                hazard_insurance=request.POST.get('hazard_insurance_present', 0),
                real_estate_taxes=request.POST.get('real_estate_taxes_present', 0),
                mortgage_insurance=request.POST.get('mortgage_insurance_present', 0),
                other=request.POST.get('other_present', 0),
                homeowner_assn_dues=request.POST.get('homeowner_assn_dues_present', 0),
            )
    else:
        FileHouseExpensesPresent.objects.create(
            file_id=file_id,
            rent=request.POST.get('rent_present', 0),
            first_mortgage=request.POST.get('first_mortgage_present', 0),
            other_financing=request.POST.get('other_financing_present', 0),
            hazard_insurance=request.POST.get('hazard_insurance_present', 0),
            real_estate_taxes=request.POST.get('real_estate_taxes_present', 0),
            mortgage_insurance=request.POST.get('mortgage_insurance_present', 0),
            other=request.POST.get('other_present', 0),
            homeowner_assn_dues=request.POST.get('homeowner_assn_dues_present', 0),
        )
    
    if 'house_proposed_ids' in request.POST:
        house_proposed_ids = request.POST['house_proposed_ids']
        if house_proposed_ids:
            FileHouseExpensesProposed.objects.filter(id=house_proposed_ids).update(
                rent=request.POST.get('rent_proposed', 0),
                first_mortgage=request.POST.get('first_mortgage_proposed', 0),
                other_financing=request.POST.get('other_financing_proposed', 0),
                hazard_insurance=request.POST.get('hazard_insurance_proposed', 0),
                real_estate_taxes=request.POST.get('real_estate_taxes_proposed', 0),
                mortgage_insurance=request.POST.get('mortgage_insurance_present', 0),
                other=request.POST.get('other_present', 0),
                homeowner_assn_dues=request.POST.get('homeowner_assn_dues_proposed', 0)
            )
        else:
            FileHouseExpensesProposed.objects.create(
            file_id=file_id,
            rent=request.POST.get('rent_proposed', 0),
            first_mortgage=request.POST.get('first_mortgage_proposed', 0),
            other_financing=request.POST.get('other_financing_proposed', 0),
            hazard_insurance=request.POST.get('hazard_insurance_proposed', 0),
            real_estate_taxes=request.POST.get('real_estate_taxes_proposed', 0),
            mortgage_insurance=request.POST.get('mortgage_insurance_present', 0),
            other=request.POST.get('other_present', 0),
            homeowner_assn_dues=request.POST.get('homeowner_assn_dues_proposed', 0)
        )
    else:
        FileHouseExpensesProposed.objects.create(
            file_id=file_id,
            rent=request.POST.get('rent_proposed', 0),
            first_mortgage=request.POST.get('first_mortgage_proposed', 0),
            other_financing=request.POST.get('other_financing_proposed', 0),
            hazard_insurance=request.POST.get('hazard_insurance_proposed', 0),
            real_estate_taxes=request.POST.get('real_estate_taxes_proposed', 0),
            mortgage_insurance=request.POST.get('mortgage_insurance_present', 0),
            other=request.POST.get('other_present', 0),
            homeowner_assn_dues=request.POST.get('homeowner_assn_dues_proposed', 0)
        )

    # Borrower Monthly expenses
    bw_expenses_id = request.POST.get('bw_expenses_id')
    br_base_empl = request.POST.get('br_base_empl')
    br_overtime = request.POST.get('br_overtime')
    br_bonuses = request.POST.get('br_bonuses')
    br_commissions = request.POST.get('br_commissions')
    br_dividends_interest = request.POST.get('br_dividends_interest')
    br_net_rental_income = request.POST.get('br_net_rental_income')
    br_other = request.POST.get('br_other')

    if bw_expenses_id:
        FileExpensesBorrower.objects.filter(id=bw_expenses_id).update(
            monthly_income=br_base_empl,
            overtime=br_overtime,
            bonuses=br_bonuses,
            commissions=br_commissions,
            dividends_interest=br_dividends_interest,
            net_rental_income=br_net_rental_income,
            other=br_other
        )
    else:
        FileExpensesBorrower.objects.create(
            file_id=file_id,
            monthly_income=br_base_empl,
            overtime=br_overtime,
            bonuses=br_bonuses,
            commissions=br_commissions,
            dividends_interest=br_dividends_interest,
            net_rental_income=br_net_rental_income,
            other=br_other
        )

    # Co borrower Monthly expenses
    co_borrower_expense_id = request.POST.getlist('co_borrower_expense_id')
    co_base_empl_array = request.POST.getlist('co_base_empl')
    co_overtime_array = request.POST.getlist('co_overtime')
    co_bonuses_array = request.POST.getlist('co_bonuses')
    co_commissions_array = request.POST.getlist('co_commissions')
    co_dividends_interest = request.POST.getlist('co_dividends_interest')
    co_net_rental_income = request.POST.getlist('co_net_rental_income')
    co_other_array = request.POST.getlist('co_other')

    co_borrower_expense = len(co_borrower_expense_id)
    co_borrower_count = 0
    while co_borrower_count < co_borrower_expense:
        file_co_borrower = FileCoBorrower.objects.get(id=co_borrower_expense_id[co_borrower_count])
        file_expense = FileExpensesCoBorrower.objects.filter(cw_id=file_co_borrower)
        if file_expense:
            file_expense.update(
                monthly_income=co_base_empl_array[co_borrower_count],
                overtime=co_overtime_array[co_borrower_count],
                bonuses=co_bonuses_array[co_borrower_count],
                commissions=co_commissions_array[co_borrower_count],
                dividends_interest=co_dividends_interest[co_borrower_count],
                net_rental_income=co_net_rental_income[co_borrower_count],
                other=co_other_array[co_borrower_count]
            )

        co_borrower_count += 1
    request.session['div_id'] = 'expense_information-details'
    return JsonResponse({'is_updated': 'success'})


def employment_information(request, file_id):
    """Add the Employment details"""
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)
    
    file_id = FileMaster.objects.get(id=file_id)
    borrower_employer_name = request.POST.get('borrower_employer_name', None)
    borrower_employer_address = request.POST.get('borrower_employer_address', None)
    borrower_self_employed = request.POST.get('borrower_self_employed', None)
    borrower_years_on_this_job = request.POST.get('borrower_years_on_this_job', None)
    borrower_years_employee_profession = request.POST.get('borrower_years_employee_profession', None)
    borrower_position = request.POST.get('borrower_position', None)
    borrower_business_phone = request.POST.get('borrower_business_phone', None)

    if borrower_self_employed == 'on':
        borrower_self_employed = True
    else:
        borrower_self_employed = False

    BorrowerEmploymentDetails.objects.filter(file_id=file_id.id).update(
        employer_name=borrower_employer_name,
        employer_street_address=borrower_employer_address,
        self_employed=borrower_self_employed,
        no_of_years_in_this_job=borrower_years_on_this_job,
        yrs_employed_in_this_line_of_work_profession=borrower_years_employee_profession,
        position_title_type_of_business=borrower_position,
        business_phone=borrower_business_phone
    )

    co_borrower_employer_name = request.POST.getlist('co_borrower_employer_name', None)
    co_borrower_employer_address = request.POST.getlist('co_borrower_employer_address', None)
    co_borrower_self_employed = request.POST.getlist('co_borrower_self_employed', None)
    co_borrower_years_on_this_job = request.POST.getlist('co_borrower_years_on_this_job', None)
    co_borrower_years_employee_profession = request.POST.getlist('co_borrower_years_employee_profession', None)
    co_borrower_position = request.POST.getlist('co_borrower_position', None)
    co_borrower_business_phone = request.POST.getlist('co_borrower_business_phone', None)
    co_borrower_employment_ids = request.POST.getlist('co_borrower_employment_ids', None)

    co_borrower_employment  = len(co_borrower_employment_ids)
    co_borrower_count = 0
    while co_borrower_count < co_borrower_employment:
        try:
            s = co_borrower_self_employed[co_borrower_count]
            s  =True
        except Exception:
            s = False

        CoBorrowerEmploymentDetails.objects.filter(id=co_borrower_employment_ids[co_borrower_count]).update(
            employer_name=co_borrower_employer_name[co_borrower_count],
            employer_street_address=co_borrower_employer_address[co_borrower_count],
            self_employed=s,
            no_of_years_in_this_job=co_borrower_years_on_this_job[co_borrower_count],
            yrs_employed_in_this_line_of_work_profession=co_borrower_years_employee_profession[co_borrower_count],
            position_title_type_of_business=co_borrower_position[co_borrower_count],
            business_phone=co_borrower_business_phone[co_borrower_count]
        )
        co_borrower_count += 1

    request.session['div_id'] = 'employment_information-details'
    return JsonResponse({'is_updated': 'success'})


def borrower_information(request, file_id):
    """Add the Borrower details"""
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)
    
    file_id = FileMaster.objects.get(id=file_id)
    

    borrower_first_name = request.POST.get('borrower_first_name', None)
    borrower_middle_name = request.POST.get('borrower_middle_name', None)
    borrower_last_name = request.POST.get('borrower_last_name', None)
    borrower_social_security_number = request.POST.get('borrower_social_security_number', None)
    borrower_phone = request.POST.get('borrower_phone', None)
    borrower_date_of_birth = request.POST.get('borrower_date_of_birth', None)
    borrower_years_in_school = request.POST.get('borrower_years_in_school', None)
    borrower_marital_status = request.POST.get('borrower_marital_status', None)
    borrower_dependents = request.POST.get('borrower_dependents', None)
    borrower_address_type = request.POST.get('borrower_address_type', None)
    borrower_years_in_address = request.POST.get('borrower_years_in_address', None)
    borrower_street = request.POST.get('borrower_street', None)
    borrower_city = request.POST.get('borrower_city', None)
    borrower_state = request.POST.get('borrower_state', None)
    try:
        borrower_state = StateMaster.objects.get(id=borrower_state)
        borrower_state = borrower_state.id
    except:
        borrower_state = None

    borrower_zip = request.POST.get('borrower_zip', None)

    borrower_mailing_street = request.POST.get('borrower_mailing_street', None)
    borrower_mailing_city = request.POST.get('borrower_mailing_city', None)
    borrower_mailing_state = request.POST.get('borrower_mailing_state', None)
    try:
        borrower_mailing_state = StateMaster.objects.get(id=borrower_mailing_state)
        borrower_mailing_state = borrower_mailing_state.id
    except:
        borrower_mailing_state = None

    borrower_mailing_zip = request.POST.get('borrower_mailing_zip', None)

    borrower_former_street = request.POST.get('borrower_former_street', None)
    borrower_former_city = request.POST.get('borrower_former_city', None)
    borrower_former_state = request.POST.get('borrower_former_state', None)
    try:
        borrower_former_state = StateMaster.objects.get(id=borrower_former_state)
        borrower_former_state = borrower_former_state.id
    except:
        borrower_former_state = None

    borrower_former_zip = request.POST.get('borrower_former_zip', None)

    borrower_suffix = request.POST.get('borrower_suffix',None)

    FileMaster.objects.filter(id=file_id.id).update(
            borrower_first_name = borrower_first_name,
            borrower_middle_name = borrower_middle_name,
            borrower_last_name = borrower_last_name,
            borrower_dependents = borrower_dependents,
            borrower_social_security_number = borrower_social_security_number,
            borrower_date_of_birth = borrower_date_of_birth,
            borrower_years_in_school = borrower_years_in_school,
            borrower_marital_status = borrower_marital_status,
            borrower_street = borrower_street,
            borrower_city = borrower_city,
            borrower_state = borrower_state,
            borrower_zip = borrower_zip,
            borrower_address_type = borrower_address_type,
            borrower_years_in_address = borrower_years_in_address,
            borrower_mailing_address = borrower_mailing_street,
            borrower_mailing_city = borrower_mailing_city,
            borrower_mailing_state=borrower_mailing_state,
            borrower_mailing_zip=borrower_mailing_zip,
            borrower_former_address = borrower_former_street,
            borrower_former_city = borrower_former_city,
            borrower_former_state=borrower_former_state,
            borrower_former_zip=borrower_former_zip,
            borrower_suffix=borrower_suffix

    )   


    co_borrower_first_name = request.POST.getlist('co_borrower_first_name')
    co_borrower_middle_name = request.POST.getlist('co_borrower_middle_name')
    co_borrower_last_name = request.POST.getlist('co_borrower_last_name')
    co_borrower_social_security_number = request.POST.getlist('co_borrower_social_security_number')
    co_borrower_phone = request.POST.getlist('co_borrower_phone')
    co_borrower_date_of_birth = request.POST.getlist('co_borrower_date_of_birth')
    co_borrower_years_in_school = request.POST.getlist('co_borrower_years_in_school')
    co_borrower_marital_status = request.POST.getlist('co_borrower_marital_status')
    co_borrower_dependents = request.POST.getlist('co_borrower_dependents')
    co_borrower_address_type = request.POST.getlist('co_borrower_address_type')
    co_borrower_years_in_address = request.POST.getlist('co_borrower_years_in_address')
    co_borrower_street = request.POST.getlist('co_borrower_street')
    co_borrower_city = request.POST.getlist('co_borrower_city')
    co_borrower_state = request.POST.getlist('co_borrower_state')
    co_borrower_ids = request.POST.getlist('co_borrower_ids')
    co_borrower_zip = request.POST.getlist('co_borrower_zip')
    co_borrower_mailing_street = request.POST.getlist('co_borrower_mailing_street')
    co_borrower_mailing_city = request.POST.getlist('co_borrower_mailing_city')
    co_borrower_mailing_state = request.POST.getlist('co_borrower_mailing_state')
    co_borrower_mailing_zip = request.POST.getlist('co_borrower_mailing_zip')
    co_borrower_former_street = request.POST.getlist('co_borrower_former_street')
    co_borrower_former_city = request.POST.getlist('co_borrower_former_city')
    co_borrower_former_state = request.POST.getlist('co_borrower_former_state')
    co_borrower_former_zip = request.POST.getlist('co_borrower_former_zip')
    co_borrower_suffix = request.POST.getlist('co_borrower_suffix')


    co_borrowerids  = len(co_borrower_ids)
    co_borrower_count = 0
    while co_borrower_count < co_borrowerids:
        try:
            co_borrower_state_1 = StateMaster.objects.get(id=co_borrower_state[co_borrower_count])
            co_borrower_state_1 = co_borrower_state_1.id
        except:
            co_borrower_state_1 = None
        
        try:
            co_borrower_mailing_state_1 = StateMaster.objects.get(id=co_borrower_mailing_state[co_borrower_count])
            co_borrower_mailing_state_1 = co_borrower_mailing_state_1.id
        except:
            co_borrower_mailing_state_1 = None

        try:
            co_borrower_former_state_1 = StateMaster.objects.get(id=co_borrower_former_state[co_borrower_count])
            co_borrower_former_state_1 = co_borrower_former_state_1.id
        except:
            co_borrower_former_state_1 = None
        
        FileCoBorrower.objects.filter(id=co_borrower_ids[co_borrower_count]).update(
            co_borrower_first_name = co_borrower_first_name[co_borrower_count],
            co_borrower_middle_name = co_borrower_middle_name[co_borrower_count],
            co_borrower_last_name = co_borrower_last_name[co_borrower_count],
            co_borrower_dependents = co_borrower_dependents[co_borrower_count],
            co_borrower_social_security_number = co_borrower_social_security_number[co_borrower_count],
            co_borrower_date_of_birth = co_borrower_date_of_birth[co_borrower_count],
            co_borrower_years_in_school = co_borrower_years_in_school[co_borrower_count],
            co_borrower_marital_status = co_borrower_marital_status[co_borrower_count],
            co_borrower_street = co_borrower_street[co_borrower_count],
            co_borrower_city = co_borrower_city[co_borrower_count],
            co_borrower_state = co_borrower_state_1,
            co_borrower_zip = co_borrower_zip[co_borrower_count],
            co_borrower_address_type = co_borrower_address_type[co_borrower_count],
            co_borrower_years_in_address = co_borrower_years_in_address[co_borrower_count],
            co_borrower_mailing_address = co_borrower_mailing_street[co_borrower_count],
            co_borrower_mailing_city = co_borrower_mailing_city[co_borrower_count],
            co_borrower_mailing_state=co_borrower_mailing_state_1,
            co_borrower_mailing_zip=co_borrower_mailing_zip[co_borrower_count],
            co_borrower_former_address = co_borrower_former_street[co_borrower_count],
            co_borrower_former_city = co_borrower_former_city[co_borrower_count],
            co_borrower_former_state=co_borrower_former_state_1,
            co_borrower_former_zip=co_borrower_former_zip[co_borrower_count],
            co_borrower_suffix = co_borrower_suffix[co_borrower_count]
        )
        co_borrower_count += 1

    request.session['div_id'] = 'borrower_information-details'
    return JsonResponse({'is_updated': 'success'})

def assets_liabilites_details(request, file_id):
    """Add the Assets and Liabilites details"""
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)

    asset_description = None
    if 'asset_description' in request.POST:
        asset_description = request.POST['asset_description']
    
    assest_market_value = None
    if 'assest_market_value' in request.POST:
        assest_market_value = request.POST['assest_market_value']

    asset_cash_deposit = None
    if 'asset_cash_deposit' in request.POST:
        asset_cash_deposit = request.POST['asset_cash_deposit']

    FileMaster.objects.filter(id=file_id).update(
        asset_description=asset_description,
        assest_market_value=assest_market_value,
        asset_cash_deposit=asset_cash_deposit
    )

    assets_name = request.POST.getlist('asset_name[]')
    address_bank = request.POST.getlist('address_bank[]')
    s_l_credit_union = request.POST.getlist('s_l_credit_union[]')
    cash_market_value = request.POST.getlist('cash_market_value[]')
    months_left_to_pay = request.POST.getlist('months_left_to_pay[]')
    acct_no = request.POST.getlist('acct_no[]')
    asset_ids = request.POST.getlist('asset_ids[]')

    assetids  = len(asset_ids)
    asset_count = 0
    while asset_count < assetids:
        
        FileAssets.objects.filter(id=asset_ids[asset_count]).update(
            file_assets=assets_name[asset_count],
            file_address_bank=address_bank[asset_count],
            file_s_l_credit_union=s_l_credit_union[asset_count],
            file_cash_or_description_market_value=cash_market_value[asset_count],
            file_months_left_to_pay=months_left_to_pay[asset_count],
            file_acct_no=acct_no[asset_count],
        )
        asset_count += 1
    

    asset_name_1 = request.POST.getlist('asset_name_1[]')
    address_bank_1 = request.POST.getlist('address_bank_1[]')
    s_l_credit_union_1 = request.POST.getlist('s_l_credit_union_1[]')
    acct_no_1 = request.POST.getlist('acct_no_1[]')
    list_savings_ids = request.POST.getlist('list_savings_ids[]')

    listsavingsids  = len(list_savings_ids)
    list_saving = 0
    while list_saving < listsavingsids:
        
        FileSavingsAccount.objects.filter(id=list_savings_ids[list_saving]).update(
            file_name=asset_name_1[list_saving],
            file_address_bank=address_bank_1[list_saving],
            file_s_l_credit_union=s_l_credit_union_1[list_saving],
            file_acct_no=acct_no_1[list_saving],
        )
        list_saving += 1


    liabilities_name = request.POST.getlist('liabilities_name[]')
    liabilities_address_company = request.POST.getlist('liabilities_address_company[]')
    liabilities_monthly_payment = request.POST.getlist('liabilities_monthly_payment[]')
    liabilities_unpaid_balance = request.POST.getlist('liabilities_unpaid_balance[]')
    liabilities_acct_no = request.POST.getlist('liabilities_acct_no[]')
    liabilities_ids = request.POST.getlist('liabilities_ids[]')

    liabilitiesids  = len(liabilities_ids)
    liabilities_count = 0
    while liabilities_count < liabilitiesids:
        
        FileLiabilities.objects.filter(id=liabilities_ids[liabilities_count]).update(
            file_liabilities_name = liabilities_name[liabilities_count],
            file_liabilities_address_company = liabilities_address_company[liabilities_count],
            file_liabilities_monthly_payment =liabilities_monthly_payment[liabilities_count],
            file_liabilities_unpaid_balance = liabilities_unpaid_balance[liabilities_count],
            file_liabilities_acct_no = liabilities_acct_no[liabilities_count],
        )
        liabilities_count += 1

    
    liabilities_name_1 = request.POST.getlist('liabilities_name_1[]')
    liabilities_address_company_1 = request.POST.getlist('liabilities_address_company_1[]')
    liabilities_monthly_payment_1 = request.POST.getlist('liabilities_monthly_payment_1[]')
    liabilities_months_left_to_pay_1 = request.POST.getlist('liabilities_months_left_to_pay_1[]')
    liabilities_unpaid_balance_1 = request.POST.getlist('liabilities_unpaid_balance_1[]')
    liabilities_acct_no_1 = request.POST.getlist('liabilities_acct_no_1[]')
    liabilities_pledged_asset_ids = request.POST.getlist('liabilities_pledged_asset_ids[]')

    liabilitiespledgedassetids  = len(liabilities_pledged_asset_ids)
    liabilities_pledged_asset_count = 0
    while liabilities_pledged_asset_count < liabilitiespledgedassetids:
        
        FileLiabilitiesPledgedAssets.objects.filter(id=liabilities_pledged_asset_ids[liabilities_pledged_asset_count]).update(
            file_name = liabilities_name_1[liabilities_pledged_asset_count],
            file_address_company = liabilities_address_company_1[liabilities_pledged_asset_count],
            file_monthly_payment =liabilities_monthly_payment_1[liabilities_pledged_asset_count],
            file_months_left_to_pay = liabilities_months_left_to_pay_1[liabilities_pledged_asset_count],
            file_unpaid_balance = liabilities_unpaid_balance_1[liabilities_pledged_asset_count],
            file_acct_no = liabilities_acct_no_1[liabilities_pledged_asset_count],
        )
        liabilities_pledged_asset_count += 1

    request.session['div_id'] = 'assets_liabilities-details'
    return JsonResponse({'is_updated': 'success'})

def add_assets_details(request):
    """Add the Assets details"""
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)

    file_id = FileMaster.objects.get(id=request.GET.get('file_id'))

    assets_name = request.GET.get('asset_name')
    address_bank = request.GET.get('address_bank')
    s_l_credit_union = request.GET.get('s_l_credit_union')
    cash_market_value = request.GET.get('cash_market_value')
    months_left_to_pay = request.GET.get('months_left_to_pay')
    acct_no = request.GET.get('acct_no')

    file_asset = FileAssets.objects.create(
        file_id= file_id,
        file_assets=assets_name,
        file_address_bank=address_bank,
        file_s_l_credit_union=s_l_credit_union,
        file_cash_or_description_market_value=cash_market_value,
        file_months_left_to_pay=months_left_to_pay,
        file_acct_no=acct_no,
    )

    return JsonResponse({'file_asset_id': file_asset.id})

def add_liabilities_details(request):
    """Add the Liabilites details"""
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)

    file_id = FileMaster.objects.get(id=request.GET.get('file_id'))

    liabilities_name = request.GET.get('liabilities_name')
    liabilities_address_company = request.GET.get('liabilities_address_company')
    liabilities_monthly_payment = request.GET.get('liabilities_monthly_payment')
    liabilities_unpaid_balance = request.GET.get('liabilities_unpaid_balance')
    liabilities_acct_no = request.GET.get('liabilities_acct_no')

    file_liabilities = FileLiabilities.objects.create(
        file_id= file_id,
        file_liabilities_name =liabilities_name,
        file_liabilities_address_company = liabilities_address_company,
        file_liabilities_monthly_payment = liabilities_monthly_payment,
        file_liabilities_unpaid_balance = liabilities_unpaid_balance,
        file_liabilities_acct_no = liabilities_acct_no
    )

    return JsonResponse({'file_liabilities_id': file_liabilities.id})

def delete_liabilities_details(request):
    """Add the Liabilites details"""
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)

    file_id = FileMaster.objects.get(id=request.GET.get('file_id'))
    liabilities_id = request.GET.get('liabilities_id')
    FileLiabilities.objects.get(id=liabilities_id).delete()
    return JsonResponse({'is_delete': 'success'})

def delete_assests_details(request):
    """Add the assets details"""
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)

    assets_id = request.GET.get('asset_id')
    FileAssets.objects.get(id=assets_id).delete()
    return JsonResponse({'is_delete': 'success'})

@csrf_exempt
def doc_file_rename(request):
    """Rename the file name"""
    doc_file_id = request.POST.get('doc_file_id')
    new_file_name = request.POST.get('new_file_name')
    file_id = request.POST.get('file_id')

    new_file_path = 'document_{}/{}'.format(file_id, str(new_file_name))

    try:
        doc_file = DocumentsTypeMaster.objects.get(id=doc_file_id)
        os.rename(doc_file.document_file_path.path, settings.MEDIA_ROOT +'/'+ new_file_path)
        doc_file.document_file_path = new_file_path
        doc_file.document_file_name = new_file_name
        doc_file.save()
        is_updated = 'Success'
    except Exception:
        is_updated = 'File not found'

    return JsonResponse({
        'is_updated': is_updated,
        'is_file_path': new_file_path
        })


def add_list_savings_details(request):
    """Add the Assets details"""
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)

    file_id = FileMaster.objects.get(id=request.GET.get('file_id'))

    assets_name_1 = request.GET.get('asset_name_1')
    address_bank_1 = request.GET.get('address_bank_1')
    s_l_credit_union_1 = request.GET.get('s_l_credit_union_1')
    acct_no_1 = request.GET.get('acct_no_1')

    file_saving_list = FileSavingsAccount.objects.create(
        file_id= file_id,
        file_name=assets_name_1,
        file_address_bank=address_bank_1,
        file_s_l_credit_union=s_l_credit_union_1,
        file_acct_no=acct_no_1,
    )

    return JsonResponse({'file_saving_list': file_saving_list.id})

def delete_list_savings_details(request):
    """Add the assets details"""
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)

    assets_id_1 = request.GET.get('asset_id_1')
    FileSavingsAccount.objects.get(id=assets_id_1).delete()
    return JsonResponse({'is_delete': 'success'})


def add_liabilities_pledged_assets(request):
    """Add the Assets details"""
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)

    file_id = FileMaster.objects.get(id=request.GET.get('file_id'))

    liabilities_name_1 = request.GET.get('liabilities_name_1')
    liabilities_address_company_1 = request.GET.get('liabilities_address_company_1')
    liabilities_monthly_payment_1 = request.GET.get('liabilities_monthly_payment_1')
    liabilities_months_left_to_pay_1 = request.GET.get('liabilities_months_left_to_pay_1')
    liabilities_unpaid_balance_1 = request.GET.get('liabilities_unpaid_balance_1')
    liabilities_acct_no_1 = request.GET.get('liabilities_acct_no_1')

    file_liabilities_pledged_assets_list = FileLiabilitiesPledgedAssets.objects.create(
        file_id= file_id,
        file_name=liabilities_name_1,
        file_address_company=liabilities_address_company_1,
        file_monthly_payment=liabilities_monthly_payment_1,
        file_months_left_to_pay=liabilities_months_left_to_pay_1,
        file_unpaid_balance=liabilities_unpaid_balance_1,
        file_acct_no=liabilities_acct_no_1,
    )

    return JsonResponse({'file_liabilities_pledged_assets_list': file_liabilities_pledged_assets_list.id})

def delete_liabilities_pledged_assets_list_details(request):
    """delete the liabilities details"""
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)

    liabilities_pledged_assets_id = request.GET.get('liabilities_pledged_assets_id')
    FileLiabilitiesPledgedAssets.objects.get(id=liabilities_pledged_assets_id).delete()
    return JsonResponse({'is_delete': 'success'})


def add_update_manage_password(request):
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)
    file_id = FileMaster.objects.get(id=request.GET.get('file_id'))
    password_name = request.GET.get('password_name')
    password_type = request.GET.get('password_type')
    user_name = request.GET.get('user_name')
    user_password = request.GET.get('user_password')
    user_password_url = request.GET.get('user_password_url')
    
    try:
        password_type_master = PasswordTypeMaster.objects.get(id=password_type)
    except Exception:
        password_type_master = None

    file_password = FilePassword.objects.create(
        file_id=file_id,
        password_name = password_name,
        user_name = user_name,
        password =user_password,
        url = user_password_url,
        password_type = password_type_master,
        created_by = user_obj
    )

    return JsonResponse({
        'manage_password_id': file_password.id
        })


def remove_manage_password(request):
    """Add the assets details"""
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)

    remove_manage_password_id = request.GET.get('remove_manage_password_id')
    try:
        FilePassword.objects.get(id=remove_manage_password_id).delete()
        is_delete = 'success'
    except Exception:
        is_delete = 'Fail'

    return JsonResponse({'is_delete': is_delete})


def update_manage_password_details(request, file_id):
    user_id = request.session.get('user_id')
    user_obj = UserMaster.objects.get(id=user_id)
    
    user_password_ids_array = request.POST.getlist('manage_password_ids')
    user_password_name_array = request.POST.getlist('user_password_name_array[]')
    user_password_type_array = request.POST.getlist('user_password_type_array[]')
    user_name_array = request.POST.getlist('user_name_array[]')
    user_password_array = request.POST.getlist('user_password_array[]')
    user_password_url_array = request.POST.getlist('user_password_url_array[]')
    user_password_ids_length = len(user_password_ids_array)
    user_password_count = 0

    try:
        while user_password_count < user_password_ids_length:
            FilePassword.objects.filter(id=user_password_ids_array[user_password_count]).update(
                password_name=user_password_name_array[user_password_count],
                user_name=user_name_array[user_password_count],
                password=user_password_array[user_password_count],
                password_type=user_password_type_array[user_password_count],
                url=user_password_url_array[user_password_count],
                created_by=user_obj
            )
            user_password_count += 1
    except Exception:
        pass
    request.session['div_id'] = 'password-details'
    return JsonResponse({'is_update': 'success'})

@csrf_exempt
def document_sorting(request):

    file_id = request.POST.get('file_id')
    sorting_type = request.POST.get('sorting_type')


    try:
        if sorting_type == 'ascending':
            document_detail_obj = DocumentsTypeMaster.objects.filter(file_id=file_id).order_by('document_file_name')
        elif sorting_type == 'descending':
            document_detail_obj = DocumentsTypeMaster.objects.filter(file_id=file_id).order_by('document_file_name').reverse()
        elif sorting_type == 'date_wise_ascending':
            document_detail_obj = DocumentsTypeMaster.objects.filter(file_id=file_id).order_by('created_date')
        elif sorting_type == 'date_wise_descending':
            document_detail_obj = DocumentsTypeMaster.objects.filter(file_id=file_id).order_by('created_date').reverse()
        else:
            document_detail_obj = DocumentsTypeMaster.objects.filter(file_id=file_id)
    except Exception:
        document_detail_obj = None

    file_document_details = []
    for i in document_detail_obj:
        file_name_doc = i.document_file_name
        file_url = settings.MEDIA_URL+file_name_doc
        i.file_type=mimetypes.guess_type(file_url,strict = True)
        if file_name_doc.endswith('.FNM') or file_name_doc.endswith('.fnm'):
            file_document_details.append(i)

    return render(request, 'file/document_sorting.html', {
        'document_details':document_detail_obj,'file_document_details':file_document_details
        })