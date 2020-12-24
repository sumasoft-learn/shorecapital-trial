# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TblCompanyMaster(models.Model):
    company_code = models.CharField(max_length=45, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_type = models.CharField(max_length=45, blank=True, null=True)
    admin_user_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    company_logo = models.CharField(max_length=255, blank=True, null=True)
    company_address_line1 = models.CharField(max_length=255, blank=True, null=True)
    company_address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=45, blank=True, null=True)
    country = models.CharField(max_length=45, blank=True, null=True)
    zip_code = models.CharField(max_length=15, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_company_master'


class TblCompensationPayerTypeMaster(models.Model):
    compensation_payer_type_title = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.CharField(max_length=45, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_compensation_payer_type_master'


class TblFileCoBorrower(models.Model):
    file_id = models.CharField(max_length=45, blank=True, null=True)
    co_borrower_name = models.CharField(max_length=255, blank=True, null=True)
    co_borrower_phone = models.CharField(max_length=45, blank=True, null=True)
    co_borrower_email = models.CharField(max_length=155, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_file_co_borrower'


class TblFileEscrowMap(models.Model):
    file_id = models.IntegerField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    number = models.CharField(max_length=45, blank=True, null=True)
    officer_name = models.CharField(max_length=255, blank=True, null=True)
    officer_phone = models.CharField(max_length=45, blank=True, null=True)
    officer_email = models.CharField(max_length=155, blank=True, null=True)
    opened_date = models.DateTimeField(blank=True, null=True)
    is_open = models.CharField(max_length=45, blank=True, null=True)
    assistant_name = models.CharField(max_length=255, blank=True, null=True)
    assitant_phone = models.CharField(max_length=45, blank=True, null=True)
    assistant_email = models.CharField(max_length=155, blank=True, null=True)
    requested_escrow_fees = models.CharField(max_length=45, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_file_escrow_map'


class TblFileHoa(models.Model):
    file_id = models.IntegerField(blank=True, null=True)
    hoa_name = models.CharField(max_length=155, blank=True, null=True)
    hoa_phone = models.CharField(max_length=45, blank=True, null=True)
    hoa_email = models.CharField(max_length=155, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_file_hoa'


class TblFileListingBuyer(models.Model):
    file_id = models.IntegerField(blank=True, null=True)
    listing_office = models.CharField(max_length=255, blank=True, null=True)
    listing_agent = models.CharField(max_length=255, blank=True, null=True)
    listing_agent_phone = models.CharField(max_length=45, blank=True, null=True)
    listing_agent_email = models.CharField(max_length=155, blank=True, null=True)
    buyer_re_office = models.CharField(max_length=255, blank=True, null=True)
    buyer_agent = models.CharField(max_length=255, blank=True, null=True)
    buyer_agent_phone = models.CharField(max_length=45, blank=True, null=True)
    buyer_agent_email = models.CharField(max_length=155, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_file_listing_buyer'


class TblFileMaster(models.Model):
    file_id = models.CharField(unique=True, max_length=45, blank=True, null=True)
    status_id = models.IntegerField(blank=True, null=True)
    brokerage = models.CharField(max_length=45, blank=True, null=True)
    company_id = models.CharField(max_length=45, blank=True, null=True)
    est_closure_date = models.CharField(max_length=45, blank=True, null=True)
    loan_officer_id = models.IntegerField(blank=True, null=True)
    nmls_id = models.CharField(max_length=45, blank=True, null=True)
    loan_officer_direct = models.CharField(max_length=155, blank=True, null=True)
    loan_officer_fax = models.CharField(max_length=45, blank=True, null=True)
    loan_officer_email = models.CharField(max_length=155, blank=True, null=True)
    lender = models.CharField(max_length=155, blank=True, null=True)
    charging_processing_fees = models.CharField(max_length=45, blank=True, null=True)
    ae_name = models.CharField(max_length=255, blank=True, null=True)
    ae_direct = models.CharField(max_length=255, blank=True, null=True)
    ae_fax = models.CharField(max_length=45, blank=True, null=True)
    ae_email = models.CharField(max_length=155, blank=True, null=True)
    ae_company_id = models.CharField(max_length=255, blank=True, null=True)
    loan_purpose_id = models.IntegerField(blank=True, null=True)
    rate_type = models.IntegerField(blank=True, null=True)
    loan_amount = models.CharField(max_length=45, blank=True, null=True)
    subordination = models.CharField(max_length=45, blank=True, null=True)
    loan_number = models.CharField(max_length=45, blank=True, null=True)
    appraisal_value = models.CharField(max_length=45, blank=True, null=True)
    piw = models.CharField(max_length=45, blank=True, null=True)
    ltv = models.CharField(max_length=45, blank=True, null=True)
    cltv = models.CharField(max_length=45, blank=True, null=True)
    rate = models.CharField(max_length=45, blank=True, null=True)
    term = models.IntegerField(blank=True, null=True)
    lock_expiration_date = models.DateTimeField(blank=True, null=True)
    float = models.CharField(max_length=45, blank=True, null=True)
    property_type = models.IntegerField(blank=True, null=True)
    occupancy = models.CharField(max_length=45, blank=True, null=True)
    impounds = models.CharField(max_length=45, blank=True, null=True)
    program_code = models.CharField(max_length=45, blank=True, null=True)
    compensation_pay_type = models.CharField(max_length=45, blank=True, null=True)
    lender_pd_comp = models.CharField(max_length=45, blank=True, null=True)
    borrower_ysp = models.CharField(max_length=45, blank=True, null=True)
    borrower_pwd_comp = models.CharField(max_length=45, blank=True, null=True)
    borrower_name = models.CharField(max_length=255, blank=True, null=True)
    borrower_phone = models.CharField(max_length=45, blank=True, null=True)
    borrower_email = models.CharField(max_length=155, blank=True, null=True)
    property_address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=45, blank=True, null=True)
    state_id = models.IntegerField(blank=True, null=True)
    zip_code = models.CharField(max_length=45, blank=True, null=True)
    delievery_disclosure = models.CharField(max_length=45, blank=True, null=True)
    delievery_disclosure_ype = models.CharField(max_length=45, blank=True, null=True)
    req_condition_stip_from = models.CharField(max_length=45, blank=True, null=True)
    charge_credit_report = models.CharField(max_length=45, blank=True, null=True)
    charge_appraisal = models.CharField(max_length=45, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    customer_id = models.CharField(max_length=45, blank=True, null=True)
    url = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_file_master'


class TblFilePassword(models.Model):
    file_id = models.IntegerField(blank=True, null=True)
    password_name = models.CharField(max_length=255, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=155, blank=True, null=True)
    customer_id = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    password_type = models.CharField(max_length=45, blank=True, null=True)
    created_by = models.CharField(max_length=45, blank=True, null=True)
    created_date = models.CharField(max_length=45, blank=True, null=True)
    updated_by = models.CharField(max_length=45, blank=True, null=True)
    updated_date = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_file_password'


class TblFilePropertyMap(models.Model):
    file_id = models.IntegerField(blank=True, null=True)
    property_address = models.CharField(max_length=255, blank=True, null=True)
    property_city = models.CharField(max_length=155, blank=True, null=True)
    property_state = models.IntegerField(blank=True, null=True)
    property_zipcode = models.CharField(max_length=45, blank=True, null=True)
    mailing_address = models.CharField(max_length=255, blank=True, null=True)
    mailing_city = models.CharField(max_length=45, blank=True, null=True)
    mailing_state = models.IntegerField(blank=True, null=True)
    mailing_zipcode = models.CharField(max_length=45, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_file_property_map'


class TblFileTitleMap(models.Model):
    file_id = models.IntegerField(blank=True, null=True)
    title_name = models.CharField(max_length=155, blank=True, null=True)
    title_order = models.CharField(max_length=45, blank=True, null=True)
    title_rep_name = models.CharField(max_length=45, blank=True, null=True)
    title_rep_email = models.CharField(max_length=155, blank=True, null=True)
    title_rep_phone = models.CharField(max_length=45, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_file_title_map'


class TblImpoundMaster(models.Model):
    impund_title = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.CharField(max_length=45, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_impound_master'


class TblLoanPurposeMaster(models.Model):
    purpose_title = models.CharField(max_length=150, blank=True, null=True)
    is_active = models.CharField(max_length=2, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_loan_purpose_master'


class TblLoanStatusMaster(models.Model):
    status_code = models.CharField(unique=True, max_length=15, blank=True, null=True)
    status_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.CharField(max_length=2, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_loan_status_master'


class TblOccupancyMaster(models.Model):
    occupancy_title = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.CharField(max_length=45, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_occupancy_master'


class TblPasswordTypeMaster(models.Model):
    password_type_title = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.CharField(max_length=45, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_password_type_master'


class TblPropertyTypeMaster(models.Model):
    property_type_title = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.CharField(max_length=45, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_property_type_master'


class TblRateTypeMaster(models.Model):
    rate_type_title = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.CharField(max_length=45, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_rate_type_master'


class TblRoleMaster(models.Model):
    role_name = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.CharField(max_length=1, blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_role_master'


class TblStateMaster(models.Model):
    state = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.CharField(max_length=45, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_state_master'


class TblTermMaster(models.Model):
    term = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.CharField(max_length=4, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_term_master'


class TblUserMaster(models.Model):
    user_id = models.CharField(max_length=45, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    user_type = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.CharField(max_length=1, blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_user_master'


class TblUserRoleMap(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    role_id = models.IntegerField(blank=True, null=True)
    is_active = models.CharField(max_length=1, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_user_role_map'
