from django.contrib import admin
from django.urls import path,include
from .views import makeQrCode, scanCode,scanCodePage

urlpatterns = [
    path('makeQrCode/', makeQrCode, name='generate_qr'),
    path('scanCode/', scanCode, name='scan_qr'),
    path('scanner/', scanCodePage, name='scan_qr_page'),
]