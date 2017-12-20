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
        pprint(type(gauth))
        request.session['gauth'] = gauth
        return redirect('home')


def loggued(request, code):
    request.session['code'] = code
    return redirect('home')


def create(request):
    gauth = GoogleAuth()
    gauth.DEFAULT_SETTINGS[
        'client_config_file'] = settings.GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE
    # Creates local webserver and auto handles authentication.
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    # Create GoogleDriveFile instance with title 'Hello.txt'.
    # 'mimeType' : 'application/vnd.google-apps.folder'
    # 'mimeType' : 'application/vnd.google-apps.audio'
    # 'mimeType' : 'application/vnd.google-apps.document' | Google Docs
    # 'mimeType' : 'application/vnd.google-apps.drawing' | Google Drawing
    # 'mimeType' : 'application/vnd.google-apps.file' | Google Drive file
    # 'mimeType' : 'application/vnd.google-apps.presentation' | Google Slides
    # 'mimeType' : 'application/vnd.google-apps.script' | Google Apps Scripts
    # 'mimeType' : 'application/vnd.google-apps.site' | Google Sites
    # 'mimeType' : 'application/vnd.google-apps.spreadsheet' | Google Sheets

    file1 = drive.CreateFile({
        'title': request.POST.get('name'),
        'mimeType': request.POST.get('type')
    })
    # Set content of the file from given string.
    file1.Upload()
    messages.warning(request, "Se ha creado el archivo.")
    return redirect('home')


def list(request):
    gauth = GoogleAuth()
    gauth.DEFAULT_SETTINGS[
        'client_config_file'] = settings.GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE
    # Creates local webserver and auto handles authentication.
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    file_list = drive.ListFile(
        {'q': "'root' in parents and trashed=false"}).GetList()
    pprint(file_list)
    return render(request, 'list.html', {'files': file_list})