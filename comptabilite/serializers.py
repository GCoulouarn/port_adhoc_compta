from rest_framework import serializers
from .models import (
    Societe, Stade, NatureCompte, TypeValeur, PlanCompteGroupe,
    PlanCompteLocal, Devise
)


class SocieteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Societe
        fields = '__all__'


class StadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stade
        fields = '__all__'


class NatureCompteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureCompte
        fields = '__all__'


class TypeValeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeValeur
        fields = '__all__'


class PlanCompteGroupeSerializer(serializers.ModelSerializer):
    societe_nom = serializers.CharField(source='societe.intitule', read_only=True)
    nature_compte_nom = serializers.CharField(source='nature_compte.intitule', read_only=True)
    
    class Meta:
        model = PlanCompteGroupe
        fields = '__all__'


class PlanCompteLocalSerializer(serializers.ModelSerializer):
    societe_nom = serializers.CharField(source='societe.intitule', read_only=True)
    groupe_nom = serializers.CharField(source='groupe.intitule', read_only=True)
    
    class Meta:
        model = PlanCompteLocal
        fields = '__all__'


class DeviseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devise
        fields = '__all__'


# Sérialiseurs pour les écritures comptables seront ajoutés plus tard
