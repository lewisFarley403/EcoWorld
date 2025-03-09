from django.contrib import admin
from .models import GlassDisposalEntry

@admin.register(GlassDisposalEntry)
class GlassDisposalAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'timestamp', 'coins_awarded')
    search_fields = ('user__username', 'location')
    list_filter = ('timestamp',)

