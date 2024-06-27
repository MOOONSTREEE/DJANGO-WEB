import urllib.parse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .models import Capteur, Donnee
from django.utils.dateparse import parse_date
import csv
import matplotlib.pyplot as plt
import io
import base64
from django.utils.timezone import localtime
import matplotlib.dates as mdates
import plotly.express as px
from datetime import datetime

def index(request):
    capteurs = Capteur.objects.all()
    donnees = Donnee.objects.all()

    capteurid = request.GET.get('capteur_id')
    date_start = request.GET.get('date_start')
    date_end = request.GET.get('date_end')

    if capteurid:
        donnees = donnees.filter(capteur_id=capteurid)
    if date_start:
        donnees = donnees.filter(timestamp__gte=parse_date(date_start))
    if date_end:
        donnees = donnees.filter(timestamp__lte=parse_date(date_end))

    return render(request, 'index.html', {'capteurs': capteurs, 'donnees': donnees})

def donnee_detail(request, donnee_id):
    donnee = get_object_or_404(Donnee, pk=donnee_id)
    return render(request, 'donnee_detail.html', {'donnee': donnee})

def add_donnee(request):
    if request.method == 'POST':
        capteur_nom = request.POST['capteur']
        valeur = request.POST['valeur']
        
        try:
            capteur = Capteur.objects.get(nom_capteur=capteur_nom)
            Donnee.objects.create(capteur=capteur, valeur=valeur)
        except Capteur.DoesNotExist:
            pass
        
        return redirect('index')
    return render(request, 'index.html')

def delete_donnee(request, donnee_id):
    donnee = get_object_or_404(Donnee, pk=donnee_id)
    donnee.delete()
    return redirect('index')

def edit_capteur_ajax(request, capteur_id):
    if request.method == 'POST':
        capteur = get_object_or_404(Capteur, pk=capteur_id)
        capteur.nom_capteur = request.POST['nom_capteur']
        capteur.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="donnees.csv"'

    writer = csv.writer(response)
    writer.writerow(['DonneeID', 'CapteurID', 'Timestamp', 'Valeur'])

    for donnee in Donnee.objects.all():
        writer.writerow([donnee.donneeid, donnee.capteur_id, localtime(donnee.timestamp).strftime("%Y-%m-%d %H:%M:%S"), donnee.valeur])

    return response


def graphique(request):
    # Définir la plage de dates
    date_start = datetime(2024, 6, 22)
    date_end = datetime(2024, 6, 30)

    # Filtrer les données par la plage de dates
    donnees = Donnee.objects.filter(timestamp__range=[date_start, date_end])
    
    data = {
        'timestamp': [localtime(donnee.timestamp) for donnee in donnees],
        'valeur': [float(donnee.valeur) for donnee in donnees],
        'capteur': [donnee.capteur.nom_capteur for donnee in donnees],
    }
    
    # Utiliser un graphique de points
    fig = px.scatter(data, y='timestamp', x='valeur', color='capteur', title='Données des Capteurs')
    
    fig.update_layout(
        yaxis_title='Date',
        xaxis_title='Valeur',
        xaxis=dict(tickmode='linear')
    )
    
    fig.update_traces(marker=dict(size=5), line=dict(width=2))
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True)

    fig_html = fig.to_html(full_html=False)
    return render(request, 'graphique.html', {'graph': fig_html})