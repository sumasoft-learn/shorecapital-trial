# Generated by Django 2.1.3 on 2019-08-03 17:03

import django.core.files.storage
import django.core.validators
from django.db import migrations, models
import django_drf_filepond.models


class Migration(migrations.Migration):

    dependencies = [
        ('django_drf_filepond', '0003_add_storedupload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temporaryupload',
            name='file',
            field=models.FileField(storage=django_drf_filepond.models.FilePondUploadSystemStorage(), upload_to=django_drf_filepond.models.get_upload_path),
        ),
        migrations.AlterField(
            model_name='temporaryupload',
            name='file_id',
            field=models.CharField(max_length=22, validators=[django.core.validators.MinLengthValidator(22)]),
        ),
    ]
