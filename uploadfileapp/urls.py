from django.urls import path
from . import views
urlpatterns = [
    path('',views.CreaetEmployee,name='createEmployeePage')
]
