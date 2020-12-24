from django.db import models

# Create your models here.
class UserMaster(models.Model):
    user_id = models.CharField(max_length=45, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    user_type = models.CharField(max_length=30, blank=True, null=True)
    nmls_id = models.CharField(max_length=30, blank=True, null=True)
    fax = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    officer_company = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.CharField(max_length=1, blank=True, null=True)
    company_id = models.ForeignKey('company.CompanyMaster', on_delete=models.CASCADE, db_column="company_id")
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name="created_user_id")
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name="updated_user_id")

    class Meta:
        managed = True
        db_table = 'tbl_user_master'
    def __str__(self):
       return u'{0}'.format(self.user_name)

class UserRoleMap(models.Model):
    user_id = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="user_id")
    role_id = models.ForeignKey('role.RoleMaster', on_delete=models.CASCADE, db_column="role_id")
    is_active = models.CharField(max_length=1, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name="userrole_created_user_id")
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name="userrole_updated_user_id")

    class Meta:
        managed = True
        db_table = 'tbl_user_role_map'
		
