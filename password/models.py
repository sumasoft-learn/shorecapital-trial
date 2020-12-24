from django.db import models

# Create your models here.
class PasswordMaster(models.Model):

    current_password = models.CharField(max_length=30, blank=True, null=True)
    new_password=models.CharField(max_length=30, blank=True, null=True)
    confirm_password = models.CharField(max_length=40, blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'tbl_password_master'
    def __str__(self):
        return u'{0}'.format(self.new_password)

