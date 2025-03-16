from django.contrib import admin
from .models import GlassDisposalEntry, RecyclingLocation

@admin.register(GlassDisposalEntry)
class GlassDisposalAdmin(admin.ModelAdmin):
    list_display = ('user', 'recycling_location', 'timestamp', 'coins_awarded')
    search_fields = ('user__username', 'recycling_location__name')
    list_filter = ('timestamp',)

@admin.register(RecyclingLocation)
class RecyclingLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')
    search_fields = ('name',)
