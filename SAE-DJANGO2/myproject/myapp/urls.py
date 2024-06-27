from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('donnee/<int:donnee_id>/', views.donnee_detail, name='donnee_detail'),
    path('add/', views.add_donnee, name='add_donnee'),
    path('delete/<int:donnee_id>/', views.delete_donnee, name='delete_donnee'),
    path('edit/<int:capteur_id>/', views.edit_capteur_ajax, name='edit_capteur_ajax'),
    path('graphique/', views.graphique, name='graphique'),
    path('export/csv/', views.export_csv, name='export_csv'),
]
