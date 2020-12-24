"""shore_capital URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('/create/', views.create, name='create_file'),
    path('/list/', views.index, name='list_view'),
    path('/view/<int:file_id>/', views.view, name='view_file'),
    path('/import/file/', views.import_file, name='import_file'),
    re_path(r'/documents/file/(?P<file_id>\w+)', views.upload_documents, name='upload_documents'),
    path('/status/filter', views.sub_status_filter, name='status_filter'),
    path('/loan/officer/filter', views.loan_officer_filter, name='loan_officer_filter'),
    path('/download/zip/', views.download_files, name='download_files'),
    re_path(r'/loan/information/update/(?P<file_id>\w+)', views.loan_information_update, name='loan_information_update'),
    re_path(r'/date_tracker_update/(?P<file_id>\w+)', views.date_tracker_update, name='date_tracker_update'),
    re_path(r'/update/file/(?P<file_id>\w+)', views.update_transaction_file, name='update_transaction_file'),
    path('/delete/co/borrower/', views.delete_co_borrower, name='delete_co_borrower'),
    path('/add/co/borrower/', views.add_co_borrower, name='add_co_borrower'),
    path('/update/mortgage/details/', views.type_of_mortgage, name='type_of_mortgage'),
    path('/update/property/details/', views.property_information, name='property_information'),
    re_path('/update/declaration/info/(?P<file_id>\w+)', views.declaration_information, name='declaration_information'),
    re_path('/update/transaction/details/(?P<file_id>\w+)', views.detail_transaction_details, name='detail_transaction_details'),
    re_path('/update/expenses/details/(?P<file_id>\w+)', views.monthly_expenses_details, name='monthly_expenses_details'),
    re_path('/update/employment/details/(?P<file_id>\w+)', views.employment_information, name='employment_information'),
    re_path('/update/borrower/details/(?P<file_id>\w+)', views.borrower_information, name='borrower_information'),
    re_path('/update/assets/liabilities/details/(?P<file_id>\w+)', views.assets_liabilites_details, name='assets_liabilites_details'),
    path('/add/assets/details/', views.add_assets_details, name='add_assets_liabilites_details'),
    path('/add/liabilities/details/', views.add_liabilities_details, name='add_liabilities_details'),
    path('/delete/liabilities/details/', views.delete_liabilities_details, name='delete_liabilities_details'),
    path('/delete/assets/details/', views.delete_assests_details, name='delete_assests_details'),
    path('/file/rename/', views.doc_file_rename, name='doc_file_rename'),
    path('/file/list/saving/', views.add_list_savings_details, name='add_list_savings_details'),
    path('/file/list/saving/delete', views.delete_list_savings_details, name='delete_list_savings_details'),
    path('/file/list/liabilities/pledged', views.add_liabilities_pledged_assets, name='add_liabilities_pledged_assets'),
    path('/file/list//liabilities/pledged/delete', views.delete_liabilities_pledged_assets_list_details, name='delete_liabilities_pledged_assets_list_details'),
    path('/file/password/add', views.add_update_manage_password, name='add_update_manage_password'),
    path('/file/password/delete', views.remove_manage_password, name='remove_manage_password'),
    re_path('/file/password/details/update/(?P<file_id>\w+)', views.update_manage_password_details, name='update_manage_password_details'),
    path('/documents/sorting/', views.document_sorting, name='document_sorting'),
    

]