import os
from django.db import models

from group.models import GroupMaster, UserGroupMap
from role.models import RoleMaster

# Create your models here.


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/document_<id>/<filename>
    return 'document_{0}/{1}'.format(instance.file_id.id, filename)


class TermMaster(models.Model):
    term = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.CharField(max_length=4, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    def __str__(self):
       return u'{0}'.format(self.term)
    class Meta:
        managed = False
        db_table = 'tbl_term_master'

class FileCoBorrower(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')
    co_borrower_name = models.CharField(max_length=255, blank=True, null=True)
    co_borrower_first_name = models.CharField(max_length=255, blank=True, null=True)
    co_borrower_middle_name = models.CharField(max_length=255, blank=True, null=True)
    co_borrower_last_name = models.CharField(max_length=255, blank=True, null=True)
    co_borrower_dependents = models.CharField(max_length=255, blank=True, null=True)
    co_borrower_phone = models.CharField(max_length=45, blank=True, null=True)
    co_borrower_email = models.CharField(max_length=155, blank=True, null=True)
    co_borrower_social_security_number = models.CharField(max_length=155,blank=True, null=True)
    co_borrower_date_of_birth = models.CharField(max_length=155,blank=True, null=True)
    co_borrower_marital_status = models.CharField(max_length=55, blank=True, null=True)
    co_borrower_street = models.CharField(max_length=55, blank=True, null=True)
    co_borrower_city = models.CharField(max_length=25, blank=True, null=True)
    co_borrower_state = models.CharField(max_length=155, blank=True, null=True)
    co_borrower_zip = models.CharField(max_length=155, blank=True, null=True)
    co_borrower_country = models.CharField(max_length=25, blank=True, null=True)
    co_borrower_address_type = models.CharField(max_length=155, blank=True, null=True)
    co_borrower_years_in_school =  models.CharField(max_length=155, blank=True, null=True)
    co_borrower_years_in_address = models.CharField(max_length=155, blank=True, null=True)
    co_borrower_mailing_address = models.CharField(max_length=155, blank=True, null=True)
    co_borrower_mailing_state = models.CharField(max_length=55, blank=True, null=True)
    co_borrower_mailing_city = models.CharField(max_length=55, blank=True, null=True)
    co_borrower_mailing_zip =  models.CharField(max_length=155, blank=True, null=True)
    co_borrower_mailing_country = models.CharField(max_length=55, blank=True, null=True)

    co_borrower_former_address = models.CharField(max_length=55, blank=True, null=True)
    co_borrower_former_city = models.CharField(max_length=25, blank=True, null=True)
    co_borrower_former_state = models.CharField(max_length=25, blank=True, null=True)
    co_borrower_former_zip = models.CharField(max_length=155,blank=True, null=True)

    co_borrower_suffix = models.CharField(max_length=155,blank=True, null=True)
    co_borrower_tax_transcript_ordered_date=models.DateField(blank=True, null=True)
    co_borrower_tax_transcript_received_date=models.DateField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name='%(class)s_created_user_id')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name='%(class)s_updated_user_id')

    class Meta:
        managed = False
        db_table = 'tbl_file_co_borrower'


class FileEscrowMap(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')   
    company_name = models.CharField(max_length=255, blank=True, null=True)
    number = models.CharField(max_length=45, blank=True, null=True)
    officer_name = models.CharField(max_length=255, blank=True, null=True)
    officer_phone = models.CharField(max_length=45, blank=True, null=True)
    officer_email = models.CharField(max_length=155, blank=True, null=True)
    opened_date = models.DateField(max_length=155,blank=True, null=True)
    is_open = models.CharField(max_length=45, blank=True, null=True)
    assistant_name = models.CharField(max_length=255, blank=True, null=True)
    assitant_phone = models.CharField(max_length=45, blank=True, null=True)
    assistant_email = models.CharField(max_length=155, blank=True, null=True)
    requested_escrow_fees = models.CharField(max_length=45, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name='%(class)s_created_user_id')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name='%(class)s_updated_user_id')

    class Meta:
        managed = False
        db_table = 'tbl_file_escrow_map'


class FileHoa(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')    
    hoa_name = models.CharField(max_length=155, blank=True, null=True)
    hoa_phone = models.CharField(max_length=45, blank=True, null=True)
    hoa_email = models.CharField(max_length=155, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name='%(class)s_created_user_id')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name='%(class)s_updated_user_id')

    class Meta:
        managed = False
        db_table = 'tbl_file_hoa'


class FileListingBuyer(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')    
    listing_office = models.CharField(max_length=255, blank=True, null=True)
    listing_agent = models.CharField(max_length=255, blank=True, null=True)
    listing_agent_phone = models.CharField(max_length=45, blank=True, null=True)
    listing_agent_email = models.CharField(max_length=155, blank=True, null=True)
    buyer_re_office = models.CharField(max_length=255, blank=True, null=True)
    buyer_agent = models.CharField(max_length=255, blank=True, null=True)
    buyer_agent_phone = models.CharField(max_length=45, blank=True, null=True)
    buyer_agent_email = models.CharField(max_length=155, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name='%(class)s_created_user_id')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name='%(class)s_updated_user_id')

    class Meta:
        managed = False
        db_table = 'tbl_file_listing_buyer'


class FileMaster(models.Model):
    file_id = models.CharField(max_length=45, blank=True, null=True)
    status_id = models.ForeignKey('file.LoanStatusMaster', on_delete=models.CASCADE, db_column="status_id",related_name="loan_status_id")
    assigned_group_id = models.ForeignKey(GroupMaster, on_delete=models.CASCADE, db_column="assigned_group_id",related_name="assigned_group_id")
    assigned_user_id = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="assigned_user_id",related_name="assigned_user_id")
    brokerage = models.CharField(max_length=45, blank=True, null=True)
    company_id = models.ForeignKey('company.CompanyMaster', on_delete=models.CASCADE, db_column="company_id",related_name="company_id")
    est_closure_date = models.CharField(max_length=45, blank=True, null=True)
    loan_officer_id = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="loan_officer_id",related_name="loan_officer_id")
    nmls_id = models.CharField(max_length=45, blank=True, null=True)
    loan_officer_direct = models.CharField(max_length=155, blank=True, null=True)
    loan_officer_fax = models.CharField(max_length=45, blank=True, null=True)
    loan_officer_email = models.CharField(max_length=155, blank=True, null=True)
    lender = models.CharField(max_length=155, blank=True, null=True)
    agency_case_number = models.CharField(max_length=255, blank=True, null=True)
    lender_case_number = models.CharField(max_length=255, blank=True, null=True)
    mortgage_applied = models.CharField(max_length=255, blank=True, null=True)
    no_of_units = models.CharField(max_length=255, blank=True, null=True)
    year_built = models.CharField(max_length=255, blank=True, null=True)
    charging_processing_fees = models.CharField(max_length=45, blank=True, null=True)
    ae_name = models.CharField(max_length=255, blank=True, null=True)
    ae_direct = models.CharField(max_length=255, blank=True, null=True)
    ae_fax = models.CharField(max_length=45, blank=True, null=True)
    ae_email = models.CharField(max_length=155, blank=True, null=True)
    ae_company_id = models.CharField(max_length=255, blank=True, null=True)
    loan_purpose_id = models.ForeignKey('file.LoanPurposeMaster', on_delete=models.CASCADE, db_column="loan_purpose_id",related_name="loan_purpose_id")
    rate_type = models.ForeignKey('file.RateTypeMaster', on_delete=models.CASCADE, db_column="rate_type",related_name="rate_type")
    loan_amount = models.CharField(max_length=45, blank=True, null=True)
    subordination = models.CharField(max_length=45, blank=True, null=True)
    loan_number = models.CharField(max_length=45, blank=True, null=True)
    appraisal_value = models.CharField(max_length=45, blank=True, null=True)
    piw = models.CharField(max_length=45, blank=True, null=True)
    ltv = models.CharField(max_length=45, blank=True, null=True)
    cltv = models.CharField(max_length=45, blank=True, null=True)
    rate = models.CharField(max_length=45, blank=True, null=True)
    term = models.ForeignKey('file.TermMaster', on_delete=models.CASCADE, db_column="term",related_name="file_term")
    lock_expiration_date = models.DateField(blank=True, null=True)
    float = models.CharField(max_length=45, blank=True, null=True)
    property_type =models.ForeignKey('file.PropertyTypeMaster', on_delete=models.CASCADE, db_column="property_type",related_name="property_type")
    occupancy = models.ForeignKey('file.OccupancyMaster', on_delete=models.CASCADE, db_column="occupancy",related_name="occupancy")
    impound = models.ForeignKey('file.ImpoundMaster', on_delete=models.CASCADE, db_column="impound",related_name="impound")
    program_code = models.CharField(max_length=45, blank=True, null=True)
    compensation_pay_type = models.ForeignKey('file.CompensationPayerTypeMaster', on_delete=models.CASCADE, db_column="compensation_pay_type",related_name="compensation_pay_type")
    lender_pd_comp = models.CharField(max_length=45, blank=True, null=True)
    borrower_ysp = models.CharField(max_length=45, blank=True, null=True)
    borrower_pwd_comp = models.CharField(max_length=45, blank=True, null=True)
    borrower_name = models.CharField(max_length=255, blank=True, null=True)
    borrower_first_name = models.CharField(max_length=255, blank=True, null=True)
    borrower_middle_name = models.CharField(max_length=255, blank=True, null=True)
    borrower_last_name = models.CharField(max_length=255, blank=True, null=True)
    borrower_dependents = models.CharField(max_length=255, blank=True, null=True)
    borrower_phone = models.CharField(max_length=45, blank=True, null=True)
    borrower_email = models.CharField(max_length=155, blank=True, null=True)
    borrower_social_security_number = models.CharField(max_length=155, blank=True, null=True)
    borrower_date_of_birth = models.CharField(max_length=155,blank=True, null=True)
    borrower_years_in_school = models.CharField(max_length=155,blank=True, null=True)
    borrower_marital_status = models.CharField(max_length=55, blank=True, null=True)
    borrower_street = models.CharField(max_length=55, blank=True, null=True)
    borrower_city = models.CharField(max_length=25, blank=True, null=True)
    borrower_state = models.CharField(max_length=155, blank=True, null=True)
    borrower_zip = models.CharField(max_length=155, blank=True, null=True)
    borrower_country = models.CharField(max_length=25, blank=True, null=True)
    borrower_address_type = models.CharField(max_length=155, blank=True, null=True)
    borrower_years_in_address = models.CharField(max_length=155,blank=True, null=True)
    borrower_mailing_address = models.CharField(max_length=55, blank=True, null=True)
    borrower_mailing_city = models.CharField(max_length=25, blank=True, null=True)
    borrower_mailing_state = models.CharField(max_length=25, blank=True, null=True)
    borrower_mailing_zip = models.CharField(max_length=155,blank=True, null=True)
    borrower_mailing_country = models.CharField(max_length=25, blank=True, null=True)

    borrower_former_address = models.CharField(max_length=55, blank=True, null=True)
    borrower_former_city = models.CharField(max_length=25, blank=True, null=True)
    borrower_former_state = models.CharField(max_length=25, blank=True, null=True)
    borrower_former_zip = models.CharField(max_length=155,blank=True, null=True)
    borrower_suffix = models.CharField(max_length=155,blank=True, null=True)
    property_address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=45, blank=True, null=True)
    customer_id = models.CharField(max_length=45, blank=True, null=True)
    url = models.CharField(max_length=45, blank=True, null=True)
    state_id = models.IntegerField(blank=True, null=True)
    zip_code = models.CharField(max_length=45, blank=True, null=True)
    delievery_disclosure = models.CharField(max_length=45, blank=True, null=True)
    delievery_disclosure_type = models.CharField(max_length=45, blank=True, null=True)
    req_condition_stip_from = models.CharField(max_length=45, blank=True, null=True)
    charge_credit_report = models.CharField(max_length=45, blank=True, null=True)
    charge_appraisal = models.CharField(max_length=45, blank=True, null=True)
    loan_amount_2 = models.CharField(max_length=45, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name='%(class)s_created_user_id')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name='%(class)s_updated_user_id')
    fha_base_mip = models.CharField(max_length=255, blank=True, null=True)
    fha_base_loan = models.CharField(max_length=255, blank=True, null=True)
    va_base_ff = models.CharField(max_length=255, blank=True, null=True)
    va_base_loan = models.CharField(max_length=255, blank=True, null=True)
    refinance_cost = models.CharField(max_length=255, blank=True, null=True)
    refinance_amount = models.CharField(max_length=255, blank=True, null=True)
    refinance_original_cost = models.CharField(max_length=255, blank=True, null=True)
    refinance_describe_improvements = models.CharField(max_length=45, blank=True, null=True)
    refinance_purpose = models.CharField(max_length=255, blank=True, null=True)
    refinance_lot_year = models.CharField(max_length=255, blank=True, null=True)
    construction_total = models.CharField(max_length=255, blank=True, null=True)
    construction_amount = models.CharField(max_length=45, blank=True, null=True)
    construction_original_cost = models.CharField(max_length=255, blank=True, null=True)
    construction_present_value = models.CharField(max_length=255, blank=True, null=True)
    construction_lot_year = models.CharField(max_length=255, blank=True, null=True)
    construction_amount_existing_liens = models.CharField(max_length=255, blank=True, null=True)
    construction_cost = models.CharField(max_length=255, blank=True, null=True)
    contruction_describe_improvements = models.CharField(max_length=255, blank=True, null=True)
    source_of_down = models.CharField(max_length=255, blank=True, null=True)
    property_name = models.CharField(max_length=255, blank=True, null=True)
    property_title_will_be_held = models.CharField(max_length=255, blank=True, null=True)
    estate_will_be =  models.CharField(max_length=255, blank=True, null=True)
    subordinate_financing = models.CharField(max_length=255, blank=True, null=True)
    settlement_charges = models.CharField(max_length=255, blank=True, null=True)
    no_of_months = models.CharField(max_length=255, blank=True, null=True)
    reverse_status = models.CharField(max_length=255, blank=True, null=True)    
    tax_transcript = models.ForeignKey('file.TaxTranscriptMaster', on_delete=models.CASCADE, db_column="tax_transcript",related_name="tax_transcript")
    tax_transcript_date = models.DateField(blank=True, null=True)
    sub_status_id = models.ForeignKey('file.LoanSubStatusMaster', on_delete=models.CASCADE, db_column="sub_status_id",related_name="sub_status_id")
    closing_disclosure = models.ForeignKey('file.ClosingDisclosureMaster', on_delete=models.CASCADE, db_column="closing_disclosure",related_name="closing_disclosure")
    closing_disclosure_date = models.DateField(blank=True, null=True)
    appraisal_ordered = models.ForeignKey('file.AppraisalOrderedMaster', on_delete=models.CASCADE, db_column="appraisal_ordered",related_name="appraisal_ordered")
    appraisal_ordered_date = models.DateField(blank=True, null=True)
    payoff_exp = models.DateField(blank=True, null=True)
    note = models.CharField(max_length=5000, blank=True, null=True)
    recieved_date = models.DateField(blank=True, null=True)
    approval_expiration = models.DateField(blank=True, null=True)
    asset_expiration_date = models.DateField(blank=True, null=True)
    broker_last_upload = models.DateField(blank=True, null=True)
    cpl_expiration_date = models.DateField(blank=True, null=True)
    credit_expiration_date = models.DateField(blank=True, null=True)
    disclosure_date = models.DateField(blank=True, null=True)
    hoi_effective_date = models.DateField(blank=True, null=True)
    income_expiration_date = models.DateField(blank=True, null=True)
    oldest_document_expired = models.DateField(blank=True, null=True)
    short_sale_expiration_date = models.DateField(blank=True, null=True)
    title_expiration_date = models.DateField(blank=True, null=True)
    vvoe_ordered_date = models.DateField(blank=True, null=True)
    vvoe_receive_date = models.DateField(blank=True, null=True)
    vvoe_expiration_date = models.DateField(blank=True, null=True)
    tax_transcript_ordered_date = models.DateField(blank=True, null=True)
    tax_transcript_received_date = models.DateField(blank=True, null=True)
    generated_date = models.DateField(blank=True, null=True)
    signature_date = models.DateField(blank=True, null=True)
    submitted_to_uw = models.DateField(blank=True, null=True)
    initial_loan_estimate = models.DateField(blank=True, null=True)
    most_recent_loan_estimate = models.DateField(blank=True, null=True)
    initial_closing_disclosure = models.DateField(blank=True, null=True)
    most_recent_closing_disclosure = models.DateField(blank=True, null=True)
    cleared_to_close = models.DateField(blank=True, null=True)
    closing_datetime = models.DateField(blank=True, null=True)
    wire_ordered_date = models.DateField(blank=True, null=True)
    wire_disbursement = models.DateField(blank=True, null=True)
    wire_date = models.DateField(blank=True, null=True)
    first_payment = models.DateField(blank=True, null=True)
    date_to_avoid_epo = models.DateField(blank=True, null=True)
    appraisal_delivery_date = models.DateField(blank=True, null=True)

    asset_description = models.CharField(max_length=500, blank=True, null=True)
    assest_market_value = models.CharField(max_length=500, blank=True, null=True)
    asset_cash_deposit = models.CharField(max_length=500, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tbl_file_master'


class FilePassword(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')    
    password_name = models.CharField(max_length=255, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=155, blank=True, null=True)
    customer_id = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    password_type = models.ForeignKey('file.PasswordTypeMaster', on_delete=models.CASCADE, db_column="password_type",related_name='%(class)s_password_type')
    #created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name='%(class)s_created_user_id')
    #updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name='%(class)s_updated_user_id')

    class Meta:
        managed = False
        db_table = 'tbl_file_password'


class BorrowerEmploymentDetails(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')
    employer_name = models.CharField(max_length=255, blank=True, null=True)
    employer_street_address = models.CharField(max_length=255, blank=True, null=True)
    employer_city = models.CharField(max_length=55, blank=True, null=True)
    employer_zip = models.CharField(max_length=155, blank=True, null=True)
    employer_state = models.CharField(max_length=55, blank=True, null=True)
    self_employed = models.BooleanField(default=False)
    no_of_years_in_this_job = models.CharField(max_length=155, blank=True, null=True)
    yrs_employed_in_this_line_of_work_profession = models.CharField(max_length=155, blank=True, null=True)
    position_title_type_of_business = models.CharField(max_length=255, blank=True, null=True)
    business_phone = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_borrower_employment_details'

class BorrowerAdditionalEmploymentDetails(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')
    employer_name = models.CharField(max_length=255, blank=True, null=True)
    employer_street_address = models.CharField(max_length=255, blank=True, null=True)
    employer_city = models.CharField(max_length=55, blank=True, null=True)
    employer_zip = models.CharField(max_length=155, blank=True, null=True)
    employer_state = models.CharField(max_length=55, blank=True, null=True)
    self_employed = models.BooleanField(default=False)
    date_from = models.CharField(max_length=155,blank=True, null=True)
    date_to = models.CharField(max_length=155,blank=True, null=True)
    position_title_type_of_business = models.CharField(max_length=255, blank=True, null=True)
    business_phone = models.CharField(max_length=55, blank=True, null=True)
    monthly_income = models.CharField(max_length=155, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_borrower_additional_employment_details'

class CoBorrowerEmploymentDetails(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')
    cw_id = models.ForeignKey('file.FileCoBorrower', on_delete=models.CASCADE, db_column="cw_id",related_name='%(class)s_cw_id')
    employer_name = models.CharField(max_length=255, blank=True, null=True)
    employer_street_address = models.CharField(max_length=255, blank=True, null=True)
    employer_city = models.CharField(max_length=55, blank=True, null=True)
    employer_zip = models.CharField(max_length=55,blank=True, null=True)
    employer_state = models.CharField(max_length=55, blank=True, null=True)
    self_employed = models.BooleanField(default=False)
    no_of_years_in_this_job = models.CharField(max_length=55, blank=True, null=True)
    yrs_employed_in_this_line_of_work_profession = models.CharField(max_length=55,blank=True, null=True)
    position_title_type_of_business = models.CharField(max_length=255, blank=True, null=True)
    business_phone = models.CharField(max_length=55,blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_co_borrower_employment_details'

class CoBorrowerAdditionalEmploymentDetails(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')
    employer_name = models.CharField(max_length=255, blank=True, null=True)
    employer_street_address = models.CharField(max_length=255, blank=True, null=True)
    employer_city = models.CharField(max_length=55, blank=True, null=True)
    employer_zip = models.CharField(max_length=155, blank=True, null=True)
    employer_state = models.CharField(max_length=55, blank=True, null=True)
    self_employed = models.BooleanField(default=False)
    date_from = models.CharField(max_length=155,blank=True, null=True)
    date_to = models.CharField(max_length=155,blank=True, null=True)
    position_title_type_of_business = models.CharField(max_length=255, blank=True, null=True)
    business_phone = models.CharField(max_length=155, blank=True, null=True)
    monthly_income = models.CharField(max_length=155, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_co_borrower_additional_employment_details'

class FileTitleMap(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')    
    title_name = models.CharField(max_length=155, blank=True, null=True)
    title_order = models.CharField(max_length=45, blank=True, null=True)
    title_rep_name = models.CharField(max_length=45, blank=True, null=True)
    title_rep_email = models.CharField(max_length=155, blank=True, null=True)
    title_rep_phone = models.CharField(max_length=45, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name='%(class)s_created_user_id')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name='%(class)s_updated_user_id')

    class Meta:
        managed = False
        db_table = 'tbl_file_title_map'


class LoanPurposeMaster(models.Model):
    purpose_title = models.CharField(max_length=150, blank=True, null=True)
    is_active = models.CharField(max_length=2, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name='%(class)s_created_user_id')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name='%(class)s_updated_user_id')
    fnm_purpose_value = models.CharField(max_length=100, blank=True, null=True)
    fnm_applied_value = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
       return u'{0}'.format(self.purpose_title)
    class Meta:
        managed = False
        db_table = 'tbl_loan_purpose_master'


class LoanStatusMaster(models.Model):
    status_code = models.CharField(unique=True, max_length=15, blank=True, null=True)
    status_name = models.CharField(max_length=255, blank=True, null=True)
    workflow_id =  models.ForeignKey('file.WorkFlowTypeMaster', on_delete=models.CASCADE, db_column="workflow_id",related_name='%(class)s_workflow_id')
    is_active = models.CharField(max_length=2, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name='%(class)s_created_user_id')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name='%(class)s_updated_user_id')
    sequence = models.IntegerField(blank=True, null=True)
    is_visible_dashboard = models.CharField(max_length=1, blank=True, null=True)
    def __str__(self):
       return u'{0}'.format(self.status_name)
    class Meta:
        managed = False
        db_table = 'tbl_loan_status_master'

class PasswordTypeMaster(models.Model):
    password_type_title = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.CharField(max_length=2, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name='%(class)s_created_user_id')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name='%(class)s_updated_user_id')
    def __str__(self):
       return u'{0}'.format(self.password_type_title)
    class Meta:
        managed = False
        db_table = 'tbl_password_type_master'



class PropertyTypeMaster(models.Model):
    property_type_title = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.CharField(max_length=2, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name='%(class)s_created_user_id')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name='%(class)s_updated_user_id')
    fnm_property_value = models.CharField(max_length=155, blank=True, null=True)
    def __str__(self):
       return u'{0}'.format(self.property_type_title)
    class Meta:
        managed = False
        db_table = 'tbl_property_type_master'

class OccupancyMaster(models.Model):
    occupancy_title = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.CharField(max_length=2, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name='%(class)s_created_user_id')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name='%(class)s_updated_user_id')
    def __str__(self):
       return u'{0}'.format(self.occupancy_title)
    class Meta:
        managed = False
        db_table = 'tbl_occupancy_master'

class ImpoundMaster(models.Model):
    impund_title = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.CharField(max_length=2, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name='%(class)s_created_user_id')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name='%(class)s_updated_user_id')
    def __str__(self):
       return u'{0}'.format(self.impund_title)
    class Meta:
        managed = False
        db_table = 'tbl_impound_master'

class CompensationPayerTypeMaster(models.Model):
    compensation_payer_type_title = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.CharField(max_length=2, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name='%(class)s_created_user_id')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name='%(class)s_updated_user_id')
    def __str__(self):
       return u'{0}'.format(self.compensation_payer_type_title)
    class Meta:
        managed = False
        db_table = 'tbl_compensation_payer_type_master'

class RateTypeMaster(models.Model):
    rate_type_title = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.CharField(max_length=2, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name='%(class)s_created_user_id')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name='%(class)s_updated_user_id')
    fnm_applied_value = models.CharField(max_length=45, blank=True, null=True)
    def __str__(self):
       return u'{0}'.format(self.rate_type_title)
    class Meta:
        managed = False
        db_table = 'tbl_rate_type_master'

class StateMaster(models.Model):
    state = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.CharField(max_length=2, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name='%(class)s_created_user_id')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name='%(class)s_updated_user_id')
    fnm_state_value = models.CharField(max_length=45, blank=True, null=True)
    def __str__(self):
       return u'{0}'.format(self.state)
    class Meta:
        managed = False
        db_table = 'tbl_state_master'

class FilePropertyMap(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')    
    property_address = models.CharField(max_length=255, blank=True, null=True)
    property_city = models.CharField(max_length=155, blank=True, null=True)
    property_state =models.ForeignKey('file.StateMaster', on_delete=models.CASCADE, db_column="property_state",related_name='%(class)s_property_state')
    property_zipcode = models.CharField(max_length=45, blank=True, null=True)
    mailing_address_check = models.CharField(max_length=45, blank=True, null=True)
    mailing_address = models.CharField(max_length=255, blank=True, null=True)
    mailing_city = models.CharField(max_length=45, blank=True, null=True)
    mailing_state = models.ForeignKey('file.StateMaster', on_delete=models.CASCADE, db_column="mailing_state",related_name='%(class)s_mailing_state')
    mailing_zipcode = models.CharField(max_length=45, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name='%(class)s_created_user_id')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name='%(class)s_updated_user_id')

    class Meta:
        managed = False
        db_table = 'tbl_file_property_map'


class DeclarationMap(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')
    cw_id = models.ForeignKey('file.FileCoBorrower', on_delete=models.CASCADE, db_column="cw_id",related_name='%(class)s_cw_id')
    declaration_description = models.CharField(max_length=255, blank=True, null=True)
    declaration_sno = models.CharField(max_length=255, blank=True, null=True)
    value = models.CharField(max_length=55, blank=True, null=True)
    types = models.CharField(max_length=55,blank=True, null=True)
    borrower_id = models.CharField(max_length=55,blank=True, null=True)
    co_borrower_id = models.CharField(max_length=55,blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_file_declaration_map'


class DetailsTransactionMap(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')
    transaction_description = models.CharField(max_length=255, blank=True, null=True)
    value = models.CharField(max_length=55, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_file_details_transaction_map'


class FileAssets(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')
    file_assets = models.CharField(max_length=255, blank=True, null=True)
    file_address_bank = models.CharField(max_length=255, blank=True, null=True)
    file_s_l_credit_union = models.CharField(max_length=255, blank=True, null=True)
    file_cash_or_description_market_value = models.CharField(max_length=255, blank=True, null=True)
    file_months_left_to_pay = models.CharField(max_length=255, blank=True, null=True)
    file_acct_no = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_file_assets'


class FileSavingsAccount(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_address_bank = models.CharField(max_length=255, blank=True, null=True)
    file_s_l_credit_union = models.CharField(max_length=255, blank=True, null=True)
    file_acct_no = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_file_savings_account'


class FileLiabilitiesPledgedAssets(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_address_company = models.CharField(max_length=255, blank=True, null=True)
    file_monthly_payment = models.CharField(max_length=255, blank=True, null=True)
    file_months_left_to_pay = models.IntegerField(blank=True, null=True)
    file_unpaid_balance = models.CharField(max_length=100, blank=True, null=True)
    file_acct_no = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_file_liabilities_pledged_assets'


class FileLiabilities(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')
    file_liabilities_name = models.CharField(max_length=255, blank=True, null=True)
    file_liabilities_street_address = models.CharField(max_length=255, blank=True, null=True)
    file_liabilities_city = models.CharField(max_length=255, blank=True, null=True)
    file_liabilities_state = models.CharField(max_length=255, blank=True, null=True)
    file_liabilities_zip = models.CharField(max_length=255, blank=True, null=True)
    file_liabilities_address_company = models.CharField(max_length=255, blank=True, null=True)
    file_liabilities_monthly_payment = models.CharField(max_length=255, blank=True, null=True)
    file_liabilities_unpaid_balance = models.CharField(max_length=100, blank=True, null=True)
    file_liabilities_acct_no = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_file_liabilities'

class FileMortage(models.Model):
    mortage_applied_title = models.CharField(max_length=244, blank=True, null=True)
    is_active = models.CharField(max_length=4, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name='%(class)s_created_user_id')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name='%(class)s_updated_user_id')

    class Meta:
        managed = False
        db_table = 'tbl_mortage_applied_master'

class FileExpensesBorrower(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')
    monthly_income = models.CharField(max_length=244, default=0, blank=True, null=True)
    overtime = models.CharField(max_length=244, default=0, blank=True, null=True)
    bonuses = models.CharField(max_length=244, default=0, blank=True, null=True)
    commissions = models.CharField(max_length=244, default=0, blank=True, null=True)
    dividends_interest = models.CharField(max_length=244, default=0, blank=True, null=True)
    other = models.CharField(max_length=244, default=0, blank=True, null=True)
    net_rental_income = models.CharField(max_length=244, default=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_file_expenses_borrower'

class FileExpensesCoBorrower(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')
    cw_id = models.ForeignKey('file.FileCoBorrower', on_delete=models.CASCADE, db_column="cw_id",related_name='%(class)s_cw_id')
    monthly_income = models.CharField(max_length=244, default=0, blank=True, null=True)
    overtime = models.CharField(max_length=244, default=0,blank=True, null=True)
    bonuses = models.CharField(max_length=244, default=0, blank=True, null=True)
    commissions = models.CharField(max_length=244, default=0, blank=True, null=True)
    dividends_interest = models.CharField(max_length=244, default=0, blank=True, null=True)
    other = models.CharField(max_length=244, default=0, blank=True, null=True)
    net_rental_income = models.CharField(max_length=244, default=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_file_expenses_co_borrower'

class FileHouseExpensesPresent(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')
    rent = models.CharField(max_length=244, blank=True, null=True)
    first_mortgage = models.CharField(max_length=244, default=0, blank=True, null=True)
    other_financing = models.CharField(max_length=244, default=0, blank=True, null=True)
    hazard_insurance = models.CharField(max_length=244, default=0, blank=True, null=True)
    real_estate_taxes = models.CharField(max_length=244, default=0, blank=True, null=True)
    mortgage_insurance = models.CharField(max_length=244, default=0, blank=True, null=True)
    other = models.CharField(max_length=244, blank=True, default=0, null=True)
    homeowner_assn_dues = models.CharField(max_length=244, default=0, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'tbl_file_house_expenses_present'

class FileHouseExpensesProposed(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')
    rent = models.CharField(max_length=244, blank=True, null=True)
    first_mortgage = models.CharField(max_length=244, default=0, blank=True, null=True)
    other_financing = models.CharField(max_length=244, default=0, blank=True, null=True)
    hazard_insurance = models.CharField(max_length=244, default=0, blank=True, null=True)
    real_estate_taxes = models.CharField(max_length=244, default=0, blank=True, null=True)
    mortgage_insurance = models.CharField(max_length=244, default=0, blank=True, null=True)
    other = models.CharField(max_length=244, blank=True, default=0, null=True)
    homeowner_assn_dues = models.CharField(max_length=244, default=0, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'tbl_file_house_expenses_proposed'

class DocumentsType(models.Model):
    document_types = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        return u'{0}'.format(self.document_types)

    class Meta:
        managed = False
        db_table = 'tbl_document_types'


class DocumentsTypeMaster(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')
    document_type_id =  models.ForeignKey('file.DocumentsType', on_delete=models.CASCADE, db_column="document_type_id",related_name='%(class)s_document_type_id')
    document_file_path = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    document_file_name = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name='%(class)s_created_user_id')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name='%(class)s_updated_user_id')

    class Meta:
        managed = False
        db_table = 'tbl_document_type_master'
    
    def extension_check(self):
        name, extension = os.path.splitext(self.document_file_path.name)
        return extension

class DateTracker(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')

    # DOCUMENT DATE
    appraisal_delivery_date = models.DateField(blank=True, null=True)
    approval_exipration = models.DateTimeField(blank=True, null=True)
    asset_expiration_date = models.DateField(blank=True, null=True)
    broker_last_upload = models.DateTimeField(blank=True, null=True)
    cpl_expiration_date = models.DateField(blank=True, null=True)
    credit_expiration_date = models.DateField(blank=True, null=True)
    disclosure_date = models.DateField(blank=True, null=True)
    hoi_effective_date = models.DateField(blank=True, null=True)
    income_expiration_date = models.DateField(blank=True, null=True)
    oldest_document_expired = models.DateField(blank=True, null=True)
    payoff_expiration = models.DateField(blank=True, null=True)
    short_sale_expiration_date = models.DateField(blank=True, null=True)
    title_expiration_date = models.DateField(blank=True, null=True)

    # APPLICATION DATE
    application_Generated_date = models.DateField(blank=True, null=True)
    application_Signature_date = models.DateField(blank=True, null=True)
    submitted_to_uw = models.DateField(blank=True, null=True)

    # VERBAL VERIFICATION DATE
    vvoe_ordered_date = models.DateField(blank=True, null=True)
    vvoe_receive_date = models.DateField(blank=True, null=True)
    vvoe_expiration_date = models.DateField(blank=True, null=True)

    # LOCK DATE
    lock_date = models.DateField(blank=True, null=True)
    lock_expiration = models.DateField(blank=True, null=True)

    # TRID DOCUMENT DATE
    initial_loan_estimate = models.DateField(blank=True, null=True)
    most_recent_loan_estimate = models.DateField(blank=True, null=True)
    initial_closing_disclosure = models.DateField(blank=True, null=True)
    most_recent_closing_disclosure = models.DateField(blank=True, null=True)

    # CLOSING DATE
    cleared_to_close = models.DateField(blank=True, null=True)
    est_closing_date = models.DateTimeField(blank=True, null=True)
    closing_date_time = models.DateTimeField(blank=True, null=True)
    wire_ordered_date = models.DateTimeField(blank=True, null=True)
    wire_disbursement  = models.DateTimeField(blank=True, null=True)
    wire_date = models.DateField(blank=True, null=True)
    first_payment  = models.DateField(blank=True, null=True)

    # EARLY PAYOFF DATE
    date_to_avoid_epo  = models.DateField(blank=True, null=True)

    # TAX TRANSCRIPT DATE
    claire_tax_transcript_ordered_date = models.DateField(blank=True, null=True)
    claire_tax_transcript_received_date = models.DateField(blank=True, null=True)
    russel_tax_transcript_ordered_date = models.DateField(blank=True, null=True)
    russel_tax_transcript_received_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_date_tracker'
class WorkflowTypeMaster(models.Model):
    workflow_title = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_workflow_type_master'

class LoanSubStatusMaster(models.Model):
    sub_status_code = models.CharField(unique=True, max_length=15, blank=True, null=True)
    sub_status_name = models.CharField(max_length=255, blank=True, null=True)
    status_id =  models.ForeignKey('file.LoanStatusMaster', on_delete=models.CASCADE, db_column="status_id",related_name='%(class)s_status_id')
    is_active = models.CharField(max_length=2, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    sequence = models.IntegerField(blank=True, null=True)
    is_visible_dashboard = models.CharField(max_length=1, blank=True, null=True)
    def __str__(self):
       return u'{0}'.format(self.sub_status_name)
    class Meta:
        managed = False
        db_table = 'tbl_loan_sub_status_master'

class TaxTranscriptMaster(models.Model):
    tt_value = models.CharField(max_length=45, blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    def __str__(self):
       return u'{0}'.format(self.tt_value)
    class Meta:
        managed = False
        db_table = 'tbl_tax_transcript_master'

class ClosingDisclosureMaster(models.Model):
    cd_value = models.CharField(max_length=45, blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    def __str__(self):
       return u'{0}'.format(self.cd_value)
    class Meta:
        managed = False
        db_table = 'tbl_closing_disclosure_master'
    
class AppraisalOrderedMaster(models.Model):
    ad_value = models.CharField(max_length=45, blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    def __str__(self):
       return u'{0}'.format(self.ad_value)
    class Meta:
        managed = False
        db_table = 'tbl_appraisal_ordered_master'

class FileNoteMap(models.Model):
    file_id = models.ForeignKey('file.FileMaster', on_delete=models.CASCADE, db_column="file_id",related_name='%(class)s_file_id')
    note = models.CharField(max_length=5000, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name='%(class)s_created_user_id')
    def __str__(self):
       return u'{0}'.format(self.ad_value)
    class Meta:
        managed = False
        db_table = 'tbl_file_note_map'
