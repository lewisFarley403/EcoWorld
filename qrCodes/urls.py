"""
URL configuration for QR Codes app.

This module defines the URL patterns for QR code functionality,
including code generation, scanning, and water fountain management.

URL Patterns:
    - /generate_qr_code/: QR code generation endpoint
    - /scan_code/: Code scanning processing endpoint
    - /scanner/: QR code scanner interface
    - /add_water_fountain/: Water fountain registration
"""

from django.urls import path

from .views import generate_qr_code, scan_code, scan_code_page, add_water_fountain

app_name = 'qrCodes'

urlpatterns = [
    path('generate_qr_code/', generate_qr_code, name='generate_qr'),
    path('scan_code/', scan_code, name='scan_qr'),
    path('scanner/', scan_code_page, name='scan_qr_page'),
    path('add_water_fountain/', add_water_fountain, name='add_water_fountain'),
]