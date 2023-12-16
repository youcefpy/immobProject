from django.contrib import admin
from .models import Inscription, ExposantInscription,Contact


class InscriptionAdmin(admin.ModelAdmin):
    list_display=('nom','prenom','email','numero_tel','ville','id_inscription')
    
class ExposantInscriptionAdmin(admin.ModelAdmin):
    list_display=('nom','raison_sociel','telephone','adresse','email','secteur_activite')
    
class ConatctAdmin(admin.ModelAdmin):
    list_display=('nom','email','text')

admin.site.register(Inscription,InscriptionAdmin)
admin.site.register(ExposantInscription,ExposantInscriptionAdmin)
admin.site.register(Contact,ConatctAdmin)