from django.db import models
import uuid
import qrcode
import os
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from phonenumber_field.modelfields import PhoneNumberField
from .managers import InscriptionManager,InscriptionExposantManager
from django.conf import settings

debug_logo_pdf = os.path.join(settings.STATICFILES_DIRS[0], 'images/favicon/favicon_immobfrdz.png') 
prod_logo_pdf = os.path.join(settings.STATIC_ROOT, 'images/favicon/favicon_immobfrdz.png') 

default_logo_pdf = debug_logo_pdf if settings.DEBUG else prod_logo_pdf

class Inscription(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField(max_length = 254)
    numero_tel = PhoneNumberField(blank=True)
    ville = models.CharField(max_length=255)
    id_inscription = models.CharField(
        max_length=20,  
        #unique=True,   
        editable=False,
        default='IMOBDZFR' + str(uuid.uuid4())[:8].upper()
    )
    qr_code = models.ImageField(upload_to='qr_codes',blank=True)
    date_inscription = models.DateTimeField(auto_now=True)
    logo_pdf = models.ImageField(default=default_logo_pdf)
    
    objects = InscriptionManager()
    
    def __str__(self):

        return f"{self.nom} {self.prenom} -- {self.id_inscription}"
    
    def save(self,*args,**kwargs):
        qrcode_id_inscription = qrcode.make(self.id_inscription)
        canvas= Image.new("RGB",(250,250),'white') 
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_id_inscription)
        fname = f"id_inscr{self.id_inscription}.png"
        
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname,File(buffer),save=False)        
        canvas.close()
        super().save(*args,**kwargs)
        

class ExposantInscription(models.Model):
    sect_activity = [
        ('PI','Promoteur Immobilier'),
        ('OF','Organisme financier'),
        ('BEA','Bureau d\'étude / Architecture'),
        ('EC','Entreprise de Construction'),
        ('AI','Agence immobilière'),
        ('TH','Tourisme / Hôtel'),
        ('AP','Association professionnelle'),
        ('PM','Presse / Média'),
    ]
    nom = models.CharField(max_length=255)
    raison_sociel = models.CharField(max_length=255)
    telephone = PhoneNumberField(blank=True)
    adresse = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    secteur_activite = models.CharField(max_length=100,choices=sect_activity)
    date = models.DateField(auto_now=True)
    
    objects=InscriptionExposantManager()
    

class Contact(models.Model): 
    nom = models.CharField(max_length = 255)
    email = models.EmailField(max_length=255)
    text = models.TextField()


