from django.db import models


class InscriptionManager(models.Manager):
    
    def createAndReturn(self,nom,prenom,email,ville,numero_tel):

        return self.create(nom = nom,prenom=prenom,email=email,numero_tel=numero_tel,ville=ville)

class InscriptionExposantManager(models.Manager):
    
    def createAndReturn(self,nom, raison_sociel, telephone, adresse, email, secteur_activite):
        
        return self.create(nom = nom, raison_sociel=raison_sociel,telephone=telephone,adresse=adresse,email=email,secteur_activite=secteur_activite)