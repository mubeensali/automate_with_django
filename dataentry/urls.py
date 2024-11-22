from django.urls import path
from dataentry import views 

urlpatterns = [
    
    path('import-data/', views.import_data, name='import_data'),
]
