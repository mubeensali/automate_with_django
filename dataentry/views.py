from django.shortcuts import render,redirect
from .utils import get_all_custom_models
from uploads.models import Upload
from django.conf import settings
from django.core.management import call_command
from django.contrib import messages


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

        #trigger the importdata command
        try:
            call_command('importdata',file_path,model_name)
            messages.success(request,'Data imported successfully')            
        except Exception as e:
            #raise e
            messages.error(request,str(e))
        return redirect('import_data')
    else:
        custom_models = get_all_custom_models()
        print(custom_models)
        context ={
            'custom_models':custom_models
        }
    return render(request, 'dataentry/importdata.html',context)
