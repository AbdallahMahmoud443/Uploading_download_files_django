
from django.db import models

# Create your models here.

class Employee(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    cvFile = models.FileField(upload_to='employee_files/cv/',blank=True,null=True)
    photoFile = models.FileField(upload_to='employee_files/photo/',blank=True,null=True)
    # New Field for pan card picture as blob
    pan_card_pic_blob = models.BinaryField(blank=True,null=True) # passport in india
    
    
    def __str__(self):
        return f'{self.id} {self.firstName}'


def certificate_upload_path(instance,fileName):
    ''' This Method responsiable for create folder for each employee inside it all certificates in spesific paht'''
    return f'employee_files/certificates/{instance.employeeid}/{fileName}'

class EmployeeCertificates(models.Model):
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    certificateFile=models.FileField(upload_to=certificate_upload_path,null =True,blank=True)
    
    def __str__(self):
        return f'{self.employee}'
    
    
