from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# Pas de ViewSet pour l'instant, juste les URLs admin

app_name = 'perimetre_consolidation'
