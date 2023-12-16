from django.shortcuts import render,redirect
from .forms import IntegrationForm,ExposantInscriptionForm,ContactForm,ExposantAllPagesForm
from .models import Inscription,ExposantInscription
from django.core.mail import EmailMultiAlternatives
from immobProject.renderers import render_to_pdf 
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail,get_connection
import os
from django.conf import settings


def inscription(request) :
    formulaire_envoyer = False

    if request.method == "POST":
        form = IntegrationForm(request.POST)
        if form.is_valid():
            # form.save()
            nom = form.cleaned_data['nom']
            prenom =form.cleaned_data['prenom']
            email =form.cleaned_data['email']
            numero_tel=form.cleaned_data['numero_tel']
            ville=form.cleaned_data['ville']
            data_inscription = Inscription.objects.createAndReturn(nom,prenom,email,numero_tel,ville)
            data = {
                'nom':nom, 
                'prenom': prenom,
                'ville': ville,
                'numero_tel' :numero_tel,
                'date' : data_inscription.date_inscription,
                'qr_code': data_inscription.qr_code.path,
                'logo_pdf' : data_inscription.logo_pdf,
            }
            pdf_content= render_to_pdf(request,'pdf_inscription.html', data)
            if pdf_content.status_code == 404:
                raise ValueError("Invoice not found")
            
            filename =f'inscription_events_paris{data_inscription.id_inscription}.pdf'
            file_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', filename)

            with open(file_path,'wb') as pdf_file :

                pdf_file.write(pdf_content.content)

            # pdf_content["Content-Disposition"] = f"attachment; filename={filename}"

            formulaire_envoyer= True

            email = form.cleaned_data['email']
            my_subject = "club-efa inscription Visiteur"

            # url to pdf
            pdf_url = os.path.join(settings.MEDIA_URL, 'pdfs', filename)
            print(f"the pdf url is ==> {pdf_url}")
            html_pdf_url = str(pdf_url)
            context ={
                'formulaire_envoyer':formulaire_envoyer,
                'pdf_url':pdf_url,
                'html_pdf_url': html_pdf_url
            }
            

            html_message = render_to_string('email_visiteur.html',data)
            plain_message = strip_tags(html_message)
            try : 
                message = EmailMultiAlternatives(
                    subject=my_subject,
                    body=plain_message,
                    from_email='visiteur.cefa@club-efa.com',
                    to=[email]
                )
                message.attach_alternative(html_message,"text/html")
                message.send()
            except Exception  as e : 
                print(f"An error occurred: {e}")
            
            
            return render(request,'inscription_visiteur.html',context)
            
        
    else : 
        form = IntegrationForm()

    context = {
        'form' : form,
        'formulaire_envoyer' : formulaire_envoyer,
    }
    return render(request,'inscription_visiteur.html',context)
        

def main_view(request):
    
    if request.method=='POST':
        form = ExposantAllPagesForm()
        nom = form.cleaned_data['nom']
        raison_sociel = form.cleaned_data['raison_sociel']
        telephone = form.cleaned_data['telephone']
        adresse = form.cleaned_data['adresse']
        email = form.cleaned_data['email']
        secteur_activite = form.cleaned_data['secteur_activite']

        exposant_data = ExposantInscription.objects.createAndReturn(nom,raison_sociel,telephone,adresse,email,secteur_activite)
        context = {
            'nom' : exposant_data.nom,
            'raison_sociel':exposant_data.raison_sociel,
            'telephone':exposant_data.telephone,
            'adresse':exposant_data.adresse,
            'email':exposant_data.email,
            'secteur_activite':exposant_data.get_secteur_activite_display(),
        }
        email = form.cleaned_data['email']  
        my_subject = "club-efa inscription exposant"
        html_message = render_to_string('exposant_email.html',context)
        plain_message = strip_tags(html_message)
        message = EmailMultiAlternatives(
            subject=my_subject,
            body=plain_message,
            from_email='exposant.cefa@club-efa.com',
            to=[email]
        )
        message.attach_alternative(html_message,"text/html")
        message.send()

        return redirect('Exposant') 
    else : 
        form = ExposantAllPagesForm()

    context={
        'form' : form
    }
    return render(request,"main.html",context)


def inscriptionExposant(request):
    if request.method == "POST":
        form = ExposantInscriptionForm(request.POST)
        if form.is_valid():
            # form.save()
            nom = form.cleaned_data['nom']
            raison_sociel = form.cleaned_data['raison_sociel']
            telephone = form.cleaned_data['telephone']
            adresse = form.cleaned_data['adresse']
            email = form.cleaned_data['email']
            secteur_activite = form.cleaned_data['secteur_activite']

            exposant_data = ExposantInscription.objects.createAndReturn(nom,raison_sociel,telephone,adresse,email,secteur_activite)
            context = {
                'nom' : exposant_data.nom,
                'raison_sociel':exposant_data.raison_sociel,
                'telephone':exposant_data.telephone,
                'adresse':exposant_data.adresse,
                'email':exposant_data.email,
                'secteur_activite':exposant_data.get_secteur_activite_display(),
            }
            email = form.cleaned_data['email']  
            my_subject = "club-efa inscription exposant"
            html_message = render_to_string('exposant_email.html',context)
            plain_message = strip_tags(html_message)
            message = EmailMultiAlternatives(
                subject=my_subject,
                body=plain_message,
                from_email='exposant.cefa@club-efa.com',
                to=[email]
            )
            message.attach_alternative(html_message,"text/html")
            message.send()
            form = ExposantInscriptionForm()
            return redirect('Exposant') 
    else : 
        form = ExposantInscriptionForm()
        
    context = {
        'form' : form,
        
    }
    return render(request,'exposant.html',context)
            
        

def conatct(request) : 
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            nom = form.cleaned_data['nom']
            email = form.cleaned_data['email']
            message_conatct = form.cleaned_data['text']
            form.save()
            subject = f'Message de {nom}'
            message= message_conatct
            from_email = email
            recipient = ['contact@club-efa.com']
            send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient)
            return redirect('main_view')
    else : 
        form = ContactForm()
    context ={
        'form' : form
    }

    return render(request,'contact.html',context)