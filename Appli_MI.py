#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 11:55:40 2025

@author: gabinalvarezsilva

Partie permettant l'affichage de l'application du module intégratif. Permet de rentrer son identifiant, d'ajouter un arbre et d'ajouter un trajet

"""
"""Importation des bibliothèques"""
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.network.urlrequest import UrlRequest
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from random import randint
from kivy.network.urlrequest import UrlRequest
import json
from time import time
from plyer import gps



"""Création de l'application"""
class MyApp(App):
 
    def build(self):
        """Création de la page générale"""
        self.title = 'Ambrasobin - Page de connexion'
        self.layout = BoxLayout(orientation='vertical')
        self.fen()
        
        return self.layout
    
    def fen(self): 
        """Création de la page permettant la connexion"""
        self.layout.clear_widgets()  
        self.nom_texte = Label(text="Quel est ton nom ?")
        self.layout.add_widget(self.nom_texte)
        self.nom_input = TextInput(text="NOM")
        self.layout.add_widget(self.nom_input)
        self.prenom_texte = Label(text="Quel est ton prénom ?")
        self.layout.add_widget(self.prenom_texte)
        self.prenom_input = TextInput(text="Prénom")

        self.layout.add_widget(self.prenom_input)
        self.bouton_valid = Button(text="S'identifier")
        self.bouton_valid.bind(on_press=self.identification)
        self.layout.add_widget(self.bouton_valid)
        
    def identification(self, instance): 
        """Envoie des données d'identification à la base de données"""
        nom = self.nom_input.text.upper()
        prenom = self.prenom_input.text.lower()
        
        #encodage des informations à transmettre
        req_body = json.dumps({'nom':nom, 'prenom':prenom})
        req_method = 'POST'
        
        UrlRequest('http://localhost:8888/src/index.php', req_body = req_body,method=req_method,  on_success = self.page_principale)
        
        #récupération de l'id_élève, de l'id_groupe
        
        
    def page_principale(self,request, result): 
        """Page de choix de l'action : enregistrement d'un arbre ou d'un trajet"""
        self.layout.clear_widgets()
        self.title = "Ambrasobin - Page principale"
        self.titre_page_principale = Label(text= "Bienvenue sur la page principale !",underline = True, font_size='50sp', markup=True, color=[0.16,0.42,0.17,1])
        self.layout.add_widget(self.titre_page_principale)
        self.choix_donnees = Label(text="Veux-tu ajouter un arbre ou un trajet ?")
        self.arbre = Button(text="Ajouter un arbre", color=[1,1,1,1], background_normal = "", background_color = [0.16,0.42,0.17,1])
        self.arbre.bind(on_press=self.ajout_arbre)
        self.trajet = Button(text="Ajouter un trajet", color=[1,1,1,1], background_normal = "", background_color = [0.16,0.42,0.17,1])
        self.trajet.bind(on_press=self.ajout_trajet)
        self.layout.add_widget(self.choix_donnees)       
        self.layout.add_widget(self.arbre)
        self.layout.add_widget(self.trajet)
        
    def ajout_arbre(self, instance):
        """Construction de la page pour ajouter un arbre"""
        self.layout.clear_widgets()
        self.title = "Ambrasobin - Page Arbre"
        
        self.debut_gps_arbre = Button(text="Prise de position")
        self.debut_gps_arbre.bind(on_press=self.enregistrement_arbre)
        self.layout.add_widget(self.debut_gps_arbre)
    
    def enregistrement_arbre(self, instance):
        """Récupération  de la position GPS de l'arbre"""
        #récupération de la position GPS
        
        #parcour de la base de données pour savoir s'il existe 
        
        #s'il existe afficher les données dessus et ajouter une observation de l'arbre dans la BD
        
        #s'il n'existe pas permettre d'en ajouter un 
        self.layout.clear_widgets()
        self.title = "Ambrosin - Enregistrement d'un nouvel arbre"
        self.essence_arbre = Label(text="Quel est l'essence de l'arbre ?")
        self.layout.add_widget(self.essence_arbre)
        self.demande_essence_arbre = TextInput()
        self.layout.add_widget(self.demande_essence_arbre)
        timestamp_arbre = time()
        #Manque l'envoie à la BD
        
        
    def ajout_trajet(self, instance):
        """"Construction de la page pour ajouter un trajet"""
        self.layout.clear_widgets()
        self.title = "Ambrasobin - Page Trajet"
        self.bouton_debut = Button(text="Début")
        self.bouton_fin = Button(text="Fin")
        
        #Ajouter les rôles des boutons début et fin
        self.bouton_debut.bind(on_press = self.debut_gps)
        self.bouton_fin.bind(on_press = self.fin_gps)
        
        self.layout.add_widget(self.bouton_debut)
        self.layout.add_widget(self.bouton_fin)

       
    def debut_gps(self, instance):
        """Fonction permettant le début d'un enregistrement gps sans limite de temps fixe"""
        self.layout.clear_widgets()
        self.attente_gps = Label(text = "En attente des positions GPS")
        self.layout.add_widget(self.attente_gps)
        gps.configure(on_location=self.on_location)
        gps.start()
     #Manque la connexion à la BD

         
    def recup_donnees_gps(self, **kwargs):
        self.attente_gps.text = '\n'.join(['{}={}'.format(k, v) for k, v in kwargs.items()])
    
    def fin_gps(self, instance):
        """Fonction permettant la fin d'un enregistrement gps sans limite de temps fixe"""
        #A construire/ Doit permettre d'afficher les sous-transports et de comparer avec ceux rentrer par l'utilisateur
        gps.stop()

    def lieux_interet (self, **kwargs) : 
        """Fonction permettant d'enregistrer les points d'intérêts traverser sur un trajet donné"""
        #récupérer les données GPS des lieux d'intérêt avec leur nom de la BD 
        #Comparer la dernière valeur de donnée avec chacune des données des points d'intérêts
        #Si on est à moins de 100m du point d'intéret l'enregistrer dans une liste
        #afficher la liste des lieux à proximité de notre trajet
if __name__ == '__main__':
    
    MyApp().run()
