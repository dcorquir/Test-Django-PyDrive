from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from pprint import pprint

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def home(request):
    return render(request, 'index.html', {})


def login(request):
    gauth = request.session.get('gauth')
    if gauth:
        messages.warning(request, "Ya se encuentra logueado.")
        return redirect('home')
    else:
        gauth = GoogleAuth()
        gauth.DEFAULT_SETTINGS[
            'client_config_file'] = settings.GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE
        # Creates local webserver and auto handles authentication.
        gauth.LocalWebserverAuth()
        pprint(gauth)
        request.session['gauth'] = gauth
        return redirect('home')



def create_file(request):
    gauth = request.session.get('gauth')
    drive = GoogleDrive(gauth)
    # Create GoogleDriveFile instance with title 'Hello.txt'.
    file1 = drive.CreateFile({
        'title': 'Hello2.docx',
        'mimeType': 'application/vnd.google-apps.folder'
    })
    # Set content of the file from given string.
    file1.SetContentString('Hello World!')
    file1.Upload()
    pprint(file1)


def list_files(request):
    pass
