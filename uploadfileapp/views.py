import os
from django.shortcuts import redirect, render
from uploadfileapp.forms import EmployeeForm
from django.contrib import messages

from uploadfileapp.models import EmployeeCertificates
# Create your views here.

def CreaetEmployee(request):
 
    if request.method == "POST":
       employeeForm = EmployeeForm(request.POST,request.FILES)
       certificates_files = request.FILES.getlist('certificates_files')
       if employeeForm.is_valid():
           employee = employeeForm.save()
           if len(certificates_files) > 10:
               messages.error(request,'You Can Upload Maximum of 10 certificates')
               return redirect('createEmployeePage')
           
           # Create folder for the employee using employee id
           employee_folder = os.path.join('employee_files','certificates',str(employee.id))
           os.makedirs(employee_folder,exist_ok=True)
           
           # logic for uploading files
           for idx,certificate_file in enumerate(certificates_files,start=1):
               original_extension = os.path.splitext(certificate_file.name)[1]
               # Rename and save the certificate file with the desired format
               new_filename = f'{employee.id}_{employee.firstName}_{idx}{original_extension}'
               newFilePath = os.path.join(employee_folder,new_filename)
               
               # save the certificate file
               with open(newFilePath,'wb+') as destination:
                    for chunk in certificate_file.chunks():
                       destination.write(chunk)
                
               # create object of EmployeeCertificates
               EmployeeCertificates.objects.create(
                    employee= employee,
                    # save path, not file object
                    certificateFile=newFilePath
                )
                
    else:
        employeeForm = EmployeeForm()  
           
    return render(request,'uploadfileapp/create_employee.html',{
        'EmployeeForm':employeeForm
    })