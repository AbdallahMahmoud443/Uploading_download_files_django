from django.urls import path
from django.views.static import serve
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('createemployee',views.CreaetEmployee,name='createEmployeePage'),
    path('',views.ShowEmployees,name='ShowEmployeesPage'),
    path('employeedetails/<int:employee_id>',views.EmployeeDetails,name='EmployeeDetailsPage'),
    # THIS PATH TO ENABLE DOWNLOADING FILE 
    #path('/<path:path>/', serve, {'document_root': settings.MEDIA_ROOT})
] 
