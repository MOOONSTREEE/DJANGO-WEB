# models.py
from django.db import models

class Capteur(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    nom_capteur = models.CharField(max_length=255, db_column='NomCapteur', unique=True)
    piece = models.CharField(max_length=255, db_column='Piece')
    emplacement = models.CharField(max_length=255, db_column='Emplacement', null=True, blank=True)

    class Meta:
        db_table = 'Capteurs'

class Donnee(models.Model):
    donneeid = models.AutoField(primary_key=True, db_column='DonneeID')
    capteur = models.ForeignKey(Capteur, on_delete=models.CASCADE, db_column='CapteurID')
    timestamp = models.DateTimeField(auto_now_add=True, db_column='Timestamp')
    valeur = models.DecimalField(max_digits=5, decimal_places=2, db_column='Valeur')

    class Meta:
        db_table = 'Donnees'
