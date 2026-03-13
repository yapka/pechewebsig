# =============================================================================
from django.contrib.gis import admin
from apps.captures.models import DeclarationCapture, EspecePoisson


@admin.register(EspecePoisson)
class EspecePoissonAdmin(admin.ModelAdmin):
    list_display  = ('nom_commun', 'nom_latin', 'categorie', 'taille_min_cm', 'is_protege')
    list_filter   = ('categorie', 'is_protege')
    search_fields = ('nom_commun', 'nom_latin')


@admin.register(DeclarationCapture)
class DeclarationCaptureAdmin(admin.GISModelAdmin):
    list_display  = ('pecheur', 'espece', 'quantite_kg', 'zone',
                     'date_capture', 'statut', 'valide_par')
    list_filter   = ('statut', 'engin_peche')
    search_fields = ('pecheur__utilisateur__username', 'espece__nom_commun')
    readonly_fields = ('date_soumission', 'date_validation')
    ordering      = ('-date_capture',)
    actions       = ['valider_captures', 'rejeter_captures']

    def valider_captures(self, request, queryset):
        for capture in queryset.filter(statut='soumise'):
            capture.valider(request.user)
        self.message_user(request, f"{queryset.count()} capture(s) validée(s) ✅")
    valider_captures.short_description = "✅ Valider les captures sélectionnées"

    def rejeter_captures(self, request, queryset):
        for capture in queryset.filter(statut='soumise'):
            capture.rejeter(request.user, motif='Rejeté depuis l\'admin')
        self.message_user(request, f"{queryset.count()} capture(s) rejetée(s) ❌")
    rejeter_captures.short_description = "❌ Rejeter les captures sélectionnées"

