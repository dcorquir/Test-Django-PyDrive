from django.shortcuts import render, redirect
from django.conf import settings
from pprint import pprint

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def home(request):
    gauth = GoogleAuth()
    gauth.DEFAULT_SETTINGS['client_config_file'] = settings.GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE
    gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.
    pprint(gauth)
    drive = GoogleDrive(gauth)
    file1 = drive.CreateFile({'title': 'Hello2.docx'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
    file1.SetContentString('Hello World!')  # Set content of the file from given string.
    file1.Upload()
    pprint(file1)
    return render(request, 'index.html')


def login(request):
    code = request.GET.get('code')
    print("CODE -- ", code)
    if code:
        request.session['code'] = code

    return redirect('home')
