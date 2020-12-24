from django.db import models

# Create your models here.
class CompanyMaster(models.Model):
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
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="created_by",related_name="company_created_user_id")
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('user.UserMaster', on_delete=models.CASCADE, db_column="updated_by",related_name="company_updated_user_id")
    def __str__(self):
       return u'{0}'.format(self.company_name)
    class Meta:
        managed = False
        db_table = 'tbl_company_master'