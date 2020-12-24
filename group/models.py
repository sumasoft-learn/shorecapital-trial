from django.db import models

# Create your models here.
class UserGroupMap(models.Model):
    user_id =  models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="user_id",related_name="usergroup_user_id")
    group_id =models.ForeignKey('group.GroupMaster', on_delete=models.CASCADE, db_column="group_id",related_name="usergroup_group_id")
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name="usergroup_created_user_id")
    status = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_user_group_map'

class GroupMaster(models.Model):
    company_id = models.CharField(max_length=45, blank=True, null=True)
    group_name = models.CharField(max_length=45, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name="group_created_user_id")
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name="group_updated_user_id")
    status = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_group_master'