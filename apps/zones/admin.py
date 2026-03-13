# apps/zones/admin.py
from django.contrib.gis import admin
from .models import ZonePeche


@admin.register(ZonePeche)
class ZonePecheAdmin(admin.GISModelAdmin):
    list_display  = ('nom', 'code', 'type_zone', 'statut', 'superficie_km2', 'cree_par')
    list_filter   = ('type_zone', 'statut')
    search_fields = ('nom', 'code')
    readonly_fields = ('superficie_km2', 'date_creation')
    ordering      = ('nom',)