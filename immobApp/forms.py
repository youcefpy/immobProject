from django import forms
from django.forms import ModelForm, TextInput, EmailInput
from .models import Inscription, ExposantInscription, Contact


class IntegrationForm(forms.ModelForm):
    class Meta : 
        model = Inscription
        fields = ['nom','prenom','email','numero_tel','ville']


class ExposantInscriptionForm(forms.ModelForm):
    class Meta : 
        model = ExposantInscription
        fields = ['nom','raison_sociel','telephone','adresse','email','secteur_activite']
        labels = {
            'nom': 'Nom',
            'raison_sociel': 'Raison sociale',
            'telephone': 'Téléphone',
            'adresse': 'Adresse',
            'email': 'Email',
            'secteur_activite': "Secteur d'activité",
        }
        
        
class ExposantAllPagesForm(forms.ModelForm):
    class Meta : 
        model = ExposantInscription
        fields = ['nom','raison_sociel','telephone','adresse','email','secteur_activite']
        labels = {
            'nom': 'Nom',
            'raison_sociel': 'Raison sociale',
            'telephone': 'Téléphone',
            'adresse': 'Adresse',
            'email': 'Email',
            'secteur_activite': "Secteur d'activité",
        }


class ContactForm(forms.ModelForm):
    class Meta : 
        model = Contact
        fields =['nom','email','text']