from django.contrib import admin
from django.urls import path,include
from .views import generate_qr_code, scan_code, scan_code_page

urlpatterns = [
    path('generate_qr_code/', generate_qr_code, name='generate_qr'),
    path('scan_code/', scan_code, name='scan_qr'),
    path('scanner/', scan_code_page, name='scan_qr_page'),
]