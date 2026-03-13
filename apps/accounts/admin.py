# apps/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, Pecheur, Bateau


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display  = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter   = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering      = ('-date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        ('Informations pêche', {
            'fields': ('role', 'telephone', 'organisation', 'photo', 'is_verified')
        }),
    )


@admin.register(Pecheur)
class PecheurAdmin(admin.ModelAdmin):
    list_display  = ('utilisateur', 'numero_licence', 'commune', 'type_peche', 'experience_annee')
    list_filter   = ('type_peche',)
    search_fields = ('utilisateur__username', 'numero_licence', 'commune')


@admin.register(Bateau)
class BateauAdmin(admin.ModelAdmin):
    list_display  = ('nom', 'immatriculation', 'pecheur', 'type_bateau', 'longueur_m', 'is_actif')
    list_filter   = ('type_bateau', 'is_actif')
    search_fields = ('nom', 'immatriculation')