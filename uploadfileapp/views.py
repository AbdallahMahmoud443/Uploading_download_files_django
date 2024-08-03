import base64
import os
from django.shortcuts import get_object_or_404, redirect, render
from uploadfileapp.forms import EmployeeForm
from django.contrib import messages

from uploadfileapp.models import Employee, EmployeeCertificates
# Create your views here.

def CreaetEmployee(request):
    if request.method == "POST":
       employeeForm = EmployeeForm(request.POST,request.FILES)
       certificates_files = request.FILES.getlist('certificates_files')
       if employeeForm.is_valid():
           employee = employeeForm.save(commit=False) # save employee
           # before save make sure image is saved into data base (upload image inyo database)
           pan_card_pic = request.FILES.get('pan_card_pic_blob')
           if pan_card_pic:
              employee.pan_card_pic_blob = pan_card_pic.read() #! reading binary image and store it in database important step
               
           employee.save()
           
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
    

def ShowEmployees(request):
    employees = Employee.objects.all()
    # Calculate remaining certificates for each employee
    employees_data = []
    for employee in employees:
        existing_certificates = len(EmployeeCertificates.objects.filter(employee=employee))
        remaining_certificates = 10 - existing_certificates
        employees_data.append({
            'employee':employee,
            'remaining_certificates':remaining_certificates
        })
        
    return render(request,'uploadfileapp/show_employees.html',{'employees_data':employees_data})

def EmployeeDetails(request,employee_id):
    # get employee based on id 
    employee = get_object_or_404(Employee,pk=employee_id)
    certificates = EmployeeCertificates.objects.filter(employee=employee)
    # Convert Binary Image data to base64
    pan_card_pic_base64 = base64.b64encode(employee.pan_card_pic_blob).decode('utf-8') if employee.pan_card_pic_blob else None

    return render(request,'uploadfileapp/employee_details.html',{
        'employee':employee,
        'certificates':certificates,
        'pan_card_pic_base64':pan_card_pic_base64
    })