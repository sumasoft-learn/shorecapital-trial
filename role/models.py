from django.db import models
from company.models import CompanyMaster
from user.models import UserMaster




# Create your models here.
class RoleMaster(models.Model):
    role_name = models.CharField(max_length=45, blank=True, null=True)
    role_type = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.CharField(max_length=1, blank=True, null=True)
    company_id = models.ForeignKey('company.CompanyMaster', on_delete=models.CASCADE, db_column="company_id",related_name="role_company_id")
    created_date = models.DateTimeField(auto_now_add=True)
    #created_by = models.IntegerField(blank=True, null=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name="role_created_user_id")
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name="role_updated_user_id")
	
    def __str__(self):
       return u'{0}'.format(self.role_name)
    class Meta:
        managed = False
        db_table = 'tbl_role_master'
		
class RoleTypeMaster(models.Model):
    role_type_title = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.CharField(max_length=2, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name='%(class)s_created_user_id')
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name='%(class)s_updated_user_id')
    def __str__(self):
       return u'{0}'.format(self.role_type_title)
    class Meta:
        managed = False
        db_table = 'tbl_role_type_master'
        
class FeatureMaster(models.Model):
    feature_name = models.CharField(max_length=45, blank=True, null=True)
    is_menu = models.CharField(max_length=45, blank=True, null=True)
    menu_url = models.CharField(max_length=45, blank=True, null=True)
    parent_feature_id = models.ForeignKey('role.FeatureMaster', on_delete=models.CASCADE, db_column="parent_feature_id",related_name='%(class)s_parent_feature_id')
    menu_title = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_feature_master'

class RoleFeatureMap(models.Model):
    feature_id = models.ForeignKey('role.FeatureMaster', on_delete=models.CASCADE, db_column="feature_id",related_name='%(class)s_feature_id')
    role_id = models.ForeignKey('role.RoleMaster', on_delete=models.CASCADE, db_column="role_id",related_name='%(class)s_role_id')
    class Meta:
        managed = False
        db_table = 'tbl_role_feature_map'