from django.shortcuts import render,redirect
from .utils import check_csv_errors, get_all_custom_models
from uploads.models import Upload
from django.conf import settings
from django.contrib import messages
from .tasks import import_data_task,export_data_task
from django.core.management import call_command


def import_data(request):
    print(request.method)
    if request.method == 'POST':
        
        file_path =request.FILES.get('file_path')
        model_name = request.POST.get('model_name')
        
        print('file_path=',file_path)
        print('model_name=', model_name)

        #Store this file inside the upload model
        upload=Upload.objects.create(file=file_path,model_name=model_name)

        #construct fullpath
        relative_path=str(upload.file.url)
        base_url= str(settings.BASE_DIR)
        print(relative_path,base_url)

        file_path= base_url+relative_path

        #check for csv error
        try:
            check_csv_errors(file_path, model_name)
        except Exception as e:
            messages.error(request,str(e))
            return redirect('import_data')

        # Handle the import task here

        import_data_task.delay(file_path,model_name)
        

        #Show message to the user
        messages.success(request,'You data is being imported, you will be notified once it is done')
        return redirect('import_data')
    else:
        custom_models = get_all_custom_models()
        print(custom_models)
        context ={
            'custom_models':custom_models
        }
    return render(request, 'dataentry/importdata.html',context)

def export_data(request):
    if request.method == 'POST':
        model_name = request.POST.get('model_name')

        #call the export data task
        export_data_task.delay(model_name)

        #Show message to the user
        messages.success(request,'You data is being exported, you will be notified once it is done')
        return redirect('export_data')

        
    else:
        custom_models = get_all_custom_models()
        context ={
            'custom_models':custom_models
        }
    return render(request,'dataentry/exportdata.html',context)
