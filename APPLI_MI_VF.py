#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 11:55:40 2025
Programme principal du Groupe 1 du Module intégratif Objets Connectés 2025.
Raphael, Ambre, Sofia et Gabin.


Partie permettant l'affichage de l'application du module intégratif. Permet de rentrer son identifiant, d'ajouter un arbre et d'ajouter un trajet

"""


"""Importation des bibliothèques"""
from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from time import time
from plyer import gps
from datetime import datetime
import json



"""Création de l'application"""
class MyApp(App):
 
    def build(self):
        """Création de la page générale"""
        self.title = 'Ambrasobin - Page de connexion'
        self.layout = BoxLayout(orientation='vertical')
        self.fen()
        self.id_phone = 1
        
        return self.layout
    
    def fen(self,instance=None): 
        """Création de la page permettant la connexion"""
        self.layout.clear_widgets()  
        self.nom_texte = Label(text="Quel est ton nom ?")
        self.layout.add_widget(self.nom_texte)
        self.nom_input = TextInput(text="LEMAITRE")
        self.layout.add_widget(self.nom_input)
        self.prenom_texte = Label(text="Quel est ton prénom ?")
        self.layout.add_widget(self.prenom_texte)
        self.prenom_input = TextInput(text="Ambre")
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
        
        UrlRequest('http://irioso.free.fr/Groupe_1/recup_id.php', req_body=req_body, method=req_method, on_success=self.page_principale)
                
    def page_principale(self,request, result): 
        """Page de choix de l'action : 4 possibilités"""
        if result[-1]!="}":
           result+="}"
        data = json.loads(result)
        if not data.get('id') or not data.get('id_groupe'):
         # Cas où id ou id_groupe est nul, vide, ou absent
            self.layout.clear_widgets()
            self.title = "Erreur de connexion"
            self.erreur_label = Label(text="Erreur de connexion, veuillez réessayer.")
            self.layout.add_widget(self.erreur_label)
            self.bouton_reessayer = Button(text="Réessayer")
            self.bouton_reessayer.bind(on_press=self.fen)
            self.layout.add_widget(self.bouton_reessayer)
            return
        else:
            self.id = data['id']
            self.id_grp = data['id_groupe']
           
        self.layout.clear_widgets()
        self.title = "Ambrasobin - Page principale"
        self.titre_page_principale = Label(text= "    Bienvenue sur\n la page principale !",underline = True, font_size='50sp', markup=True, color=[0.16,0.42,0.17,1])
        self.layout.add_widget(self.titre_page_principale)
        self.choix_donnees = Label(text="Que veux tu faire ?")
        self.arbre = Button(text="Ajouter un arbre", color=[1,1,1,1], background_normal = "", background_color = [0.16,0.42,0.17,1])
        self.arbre.bind(on_press=self.page_arbre)
        self.trajet = Button(text="Bonus - Demarrer un trajet et determiner \nles moyens de transport utilisés", color=[0,0,0,1], background_normal = "", background_color = [1,1,0,1])
        self.trajet.bind(on_press=self.ajout_trajet)
        self.nouveau_depart = Button(text="Demarrer un trajet et determiner \nle moyen de transport utilisé")
        self.nouveau_depart.bind(on_press=self.un_ajout_trajet)
        self.trajet_journee = Button(text="Determiner les moyens de transports \n utilisés sur une période de la journée")
        self.trajet_journee.bind(on_press=self.ajout_trajet_journee)
        self.bouton_bonus=Button(text="compter les bonus du groupe")
        self.bouton_bonus.bind(on_press=self.vers_compte_bonus)
        self.layout.add_widget(self.choix_donnees)       
        self.layout.add_widget(self.arbre)
        self.layout.add_widget(self.nouveau_depart)
        self.layout.add_widget(self.trajet_journee)
        self.layout.add_widget(self.trajet)
        self.layout.add_widget(self.bouton_bonus)
        
    def vers_compte_bonus(self, instance):
        req_body = json.dumps({'id_groupe': self.id_grp})
        req_method = 'POST'
        UrlRequest('http://irioso.free.fr/Groupe_1/compte_bonus.php', req_body=req_body, method=req_method, on_success=self.affichage_compte_bonus)

    def affichage_compte_bonus(self, request, result):
        if result[-1]!="}":
            result+="}"
        data = json.loads(result)
        self.layout.clear_widgets()
        self.title = "Ambrasobin - Compte des bonus"
        self.message = Label(text="Voici le compte des bonus du groupe :")
        self.layout.add_widget(self.message)
        self.bonus = Label(text="Nombre de bonus : " + str(data['bonus']))
        self.layout.add_widget(self.bonus)
        self.bouton_retour = Button(text="Retour à la page principale")
        self.bouton_retour.bind(on_press=self.retour_page_principale)
        self.layout.add_widget(self.bouton_retour)
        
    def page_arbre(self, instance, **kwargs):
        """Construction de la page pour ajouter un arbre"""
        self.layout.clear_widgets()
        self.title = "Ambrasobin - Page Arbre"
        # récupération de la position GPS
        gps.configure(on_location=self.recup_donnees_gps_arbre)
        gps.start()
        self.debut_gps_arbre = Button(text="Prise de position")
        self.debut_gps_arbre.bind(on_press=self.lancer_verification_arbre)
        self.layout.add_widget(self.debut_gps_arbre)
    
    def recup_donnees_gps_arbre(self, **kwargs):
        """Récupération des données GPS pour l'arbre"""
        self.lat = kwargs.get('lat')
        self.long = kwargs.get('lon')


    def lancer_verification_arbre(self, instance):
        req_body = json.dumps({'long': self.long, 'lat': self.lat})
        req_method = 'POST'
        UrlRequest('http://irioso.free.fr/Groupe_1/distance_arbre.php', req_body=req_body, method=req_method, on_success=self.verification_arbre)

    def verification_arbre(self, request, result):
        if result[-1]!="}":
            result+="}"
        booleen = json.loads(result)['booleen']
        if booleen is True:
            self.id_arbre = json.loads(result)['id']
            req_body = json.dumps({'long': self.long, 'lat': self.lat, 'id': self.id_arbre})
            UrlRequest('http://irioso.free.fr/Groupe_1/MAJ_arbre.php', req_body=req_body, method='POST', on_success=self.test_bonus)
        else:
            # pas d'arbre, on peut en ajouter un
            self.enregistrement_nv_arbre(None)

    def test_bonus(self, request, result):
        req_body = json.dumps({'id': self.id_arbre,
                                'timestamp': time()})
        req_method = 'POST'
        UrlRequest('http://irioso.free.fr/Groupe_1/insert_bonus.php', req_body=req_body, method=req_method, on_success=self.vers_recup_data_obs)
        

    def vers_recup_data_obs(self, request, result):
        if result[-1]!="}":
            result+="}"
        booleen= json.loads(result)['booleen']
        if booleen is True:
            self.recup_data_obs()
        else:
            self.recup_data_obs()

    def recup_data_obs(self):
        req_body = json.dumps({'id': self.id_arbre})
        req_method = 'POST'
        UrlRequest('http://irioso.free.fr/Groupe_1/recup_data_arbre.php', req_body=req_body, method='POST', on_success=self.affichage_arbre)

    def affichage_arbre(self, request, result):
        if result[-1]!="}":
            result+="}" # Correction pour s'assurer que le JSON est bien formé  
        data = json.loads(result)

        self.essence_val = data['essence']
        self.circonference_val = data['circonference']
        self.mort_val = data['mort']

        self.layout.clear_widgets()
        self.title = "Ambrasobin - Données de l'arbre"
        self.message = Label(text="Voici les données de l'arbre :")
        self.layout.add_widget(self.message)
        self.essence = Label(text="Essence : " + data['essence'])
        self.layout.add_widget(self.essence)
        self.circonference = Label(text="Circonférence : " + str(data['circonference']))
        self.layout.add_widget(self.circonference)
        self.mort = Label(text="État de l'arbre (0 mort, 1 vivant) : " + str(data['mort']))
        self.layout.add_widget(self.mort)

        self.bouton_diff = Button(text="Ajouter des données différentes")
        self.bouton_diff.bind(on_press=self.inser_nv_datas)
        self.layout.add_widget(self.bouton_diff)
        self.bouton_egal = Button(text="Ajouter les mêmes données")
        self.bouton_egal.bind(on_press=self.inser_mm_datas)
        self.layout.add_widget(self.bouton_egal)

    def inser_nv_datas(self, instance):

        self.layout.clear_widgets()
        self.title = "Ambrasobin - Insertion de nouvelles données"
        self.essence = Label(text="Quelle est l'essence de l'arbre ?")
        self.layout.add_widget(self.essence)
        self.demande_essence = TextInput()
        self.layout.add_widget(self.demande_essence)
        self.circonference = Label(text="Quelle est la circonférence de l'arbre ?")
        self.layout.add_widget(self.circonference)
        self.demande_circonference = TextInput()
        self.layout.add_widget(self.demande_circonference)
        self.mort = Label(text="Quel est l'état de l'arbre (0 mort, 1 vivant) ?")
        self.layout.add_widget(self.mort)
        self.demande_mort = TextInput()
        self.layout.add_widget(self.demande_mort)
        self.bouton_envoi = Button(text="Enregistrer les données")
        self.bouton_envoi.bind(on_press=self.envoi_nv_datas)
        self.layout.add_widget(self.bouton_envoi)

    def envoi_nv_datas(self, instance):
        self.time= time()
        req_body = json.dumps({'id': self.id_arbre,
                                'id_groupe': self.id_grp,
                                'lat': self.lat,
                                'long': self.long,
                                'timestamp': self.time,
                                'essence': self.demande_essence.text,
                                'circonference': self.demande_circonference.text,
                                'mort': self.demande_mort.text})
        req_method = 'POST'
        UrlRequest('http://irioso.free.fr/Groupe_1/inser_nv_obs.php', req_body=req_body, method=req_method, on_success=self.message_arbre)



    def inser_mm_datas(self, instance):
        """Insertion des mêmes données pour un arbre déjà existant"""
        self.layout.clear_widgets()
        self.title = "Ambrasobin - Insertion des mêmes données"
        self.message = Label(text="Les mêmes données seront insérées pour l'arbre.")
        self.layout.add_widget(self.message)
        self.bouton_envoi = Button(text="Enregistrer les données")
        self.bouton_envoi.bind(on_press=self.envoi_mm_datas)
        self.layout.add_widget(self.bouton_envoi)
    
    def envoi_mm_datas(self, instance):
        """Envoi des mêmes données pour un arbre déjà existant"""
        self.time = time()
        req_body = json.dumps({
        'id': self.id_arbre,
        'id_groupe': self.id_grp,
        'lat': self.lat,
        'long': self.long,
        'timestamp': self.time,
        'essence': self.essence_val,
        'circonference': self.circonference_val,
        'mort': self.mort_val})         
        req_method = 'POST'
        UrlRequest('http://irioso.free.fr/Groupe_1/inser_nv_obs.php', req_body=req_body, method=req_method, on_success=self.message_arbre)
        
    def message_arbre(self,request,result):
        """Affichage d'un message pour dire que l'arbre a été ajouté"""

        self.layout.clear_widgets()

        self.title = "Ambrasobin - Arbre ajouté"
        self.message = Label(text="Les données ont bien été ajouté !")
        self.layout.add_widget(self.message)
        # retour à la page principale
        self.bouton_retour = Button(text="Retour à la page principale")
        self.bouton_retour.bind(on_press=self.retour_page_principale)
        self.layout.add_widget(self.bouton_retour)
    
    def retour_page_principale(self, instance):
        # Tu peux rappeler la page principale sans arguments réseau
        self.page_principale(None, '{"id": %d, "id_groupe": %d}' % (self.id, self.id_grp))

    def enregistrement_nv_arbre(self, instance):
        self.layout.clear_widgets()
        self.title = "Ambrosin - Enregistrement d'un nouvel arbre"
        self.essence_arbre = Label(text="Quel est l'essence de l'arbre ?")
        self.layout.add_widget(self.essence_arbre)
        self.demande_essence_arbre = TextInput()
        self.layout.add_widget(self.demande_essence_arbre)
        

        self.circonference_arbre = Label(text="Quel est la circonference de l'arbre ?")
        self.layout.add_widget(self.circonference_arbre)
        self.demande_circonference_arbre = TextInput()
        self.layout.add_widget(self.demande_circonference_arbre)
        

        self.mort_arbre = Label(text="Quel est l'état de l'arbre (0 mort, 1 vivant) ?")
        self.layout.add_widget(self.mort_arbre)
        self.demande_mort_arbre = TextInput()
        self.layout.add_widget(self.demande_mort_arbre)
        

        self.nom_img = Label(text="nom de l'image ?")
        self.layout.add_widget(self.nom_img)
        self.demande_nom_img = TextInput()
        self.layout.add_widget(self.demande_nom_img)
        

        self.timestamp_arbre = time()
        
        self.bouton_envoi = Button(text="Enregistrer l'arbre")
        self.bouton_envoi.bind(on_press=self.envoi_arbre)
        self.layout.add_widget(self.bouton_envoi)
        

    def envoi_arbre(self, instance):
        req_body = json.dumps({
            'essence': self.demande_essence_arbre.text,
            'circonference': self.demande_circonference_arbre.text,
            'mort': self.demande_mort_arbre.text,
            'id_groupe': self.id_grp,
            'lat': self.lat,
            'long': self.long,
            'timestamp': self.timestamp_arbre,
            'nom_img': self.demande_nom_img.text,
        })

        req_method = 'POST'
        UrlRequest('http://irioso.free.fr/Groupe_1/ajout_arbre.php', req_body=req_body, method=req_method, on_success=self.message_arbre)

   
#-------------Partie trajet-------------------------------------

#--------------1-Determiner les moyens de transports utilisés sur une période de la journée----------------
        
    def ajout_trajet_journee(self, instance):
        """Détermination des moyens de transport entre deux heures de la journée"""
        #Manque la descrition de la fonction
        #Manque le changement de titre
        self.layout.clear_widgets()
        self.horaire_donne = Label(text=" Sur quelle période voulez vous\n déterminer vos moyens de transport ?")
        self.layout.add_widget(self.horaire_donne)
        self.horaire_debut = TextInput(text="25/06/2025 11:49")
        self.layout.add_widget(self.horaire_debut)
        self.horaire_fin = TextInput(text="25/06/2025 11:50")
        self.layout.add_widget(self.horaire_fin)
        self.button=Button(text="Entrer", on_press=self.envoi_horaire)
        self.layout.add_widget(self.button)
        
    def heure_into_timestamp(self, string):
        """"Transforme heures en timestamp """
        #Manque la description de la fonction
        try:
            clean_str = string.strip().replace('\n', '').replace('\r', '')
            dt =datetime.strptime(clean_str, "%d/%m/%Y %H:%M")
            return dt
        except ValueError:
            self.error_label.text = "Format invalide : jj/mm/aaaa hh:mm attendu"
            return None
        
    def envoi_horaire(self,instance):
        """Reempli la table trajet_detecte"""
       #Description globale de la fonction ?
        # Conversion des textes en datetime
        dt_debut = self.heure_into_timestamp(self.horaire_debut.text)
        dt_fin = self.heure_into_timestamp(self.horaire_fin.text)

        # Si une date n'est pas valide, on arrête
        if dt_debut is None or dt_fin is None:
            return

        # Convertir datetime en timestamp UNIX (entier)
        self.tt_debut = int(dt_debut.timestamp())
        self.tt_fin = int(dt_fin.timestamp())
        
        data = {'tt_debut': self.tt_debut, 'tt_fin': self.tt_fin}

        headers = {'Content-Type': 'application/json'}

      
        UrlRequest(url='http://irioso.free.fr/Ambrasobin/envoi_horaire.php', req_body=json.dumps(data),  req_headers=headers, on_success=self.success_horaire)
        
    def success_horaire(self, request, result):
        """Détermine les moyens utilisés entre deux heures """
        #Descritpion à ajouter
        #Titre de la page
        self.layout.clear_widgets()
        
        
        data = {'tt_debut': self.tt_debut, 'tt_fin': self.tt_fin}
        
        headers = {'Content-Type': 'application/json'}

      
        UrlRequest(url='http://irioso.free.fr/Ambrasobin/deter_moyen_h.php', req_body=json.dumps(data),  req_headers=headers, on_success=self.on_horaire)
        
    def on_horaire(self, requete, resultat):
        """Interface dans laquelle on demande ce qu'il a utilisé comme moyens de tansport séparés par des virgules. Stocke les résultats dans des listes """
        #Description de la fonction
       
        self.moyen_donne_h = Label(text="Quels moyens de transport avez-vous utilisé ?")
        self.layout.add_widget(self.moyen_donne_h)
        self.moyen_input_h = TextInput(hint_text="Moyen 1, Moyen 2,...")
        self.layout.add_widget(self.moyen_input_h)
        self.button=Button(text="Entrer", on_press=self.envoi_moy_h)
        self.layout.add_widget(self.button)
        if resultat[-1]!="}":
            resultat+="}"
        data_h=json.loads(resultat)
        self.liste_moyens_estimes_h=[]
        
        for valeur in data_h.values():
            self.liste_moyens_estimes_h.append(valeur)
            
        self.liste_timestamp_h=[]
        for cle in data_h.keys():
            self.liste_timestamp_h.append(float(cle))
        self.liste_timestamp_h.append(self.tt_fin)
        
        for i in range (len(self.liste_moyens_estimes_h)):
            
            self.moyen_ss_trajet= self.liste_moyens_estimes_h[i]
            self.tt_debut_ss_trajet= self.liste_timestamp_h[i]
            self.tt_fin_ss_trajet=self.liste_timestamp_h[i+1]
            data = {'tt_debut': self.tt_debut,'tt_fin': self.tt_fin,'moyen_ss_trajet':self.moyen_ss_trajet, 'tt_debut_ss_trajet': self.tt_debut_ss_trajet, 'tt_fin_ss_trajet': self.tt_fin_ss_trajet}
            
            headers = {'Content-Type': 'application/json'}
            
            UrlRequest(url='http://irioso.free.fr/Ambrasobin/insert_sous_trajet_detecte', req_body=json.dumps(data),  req_headers=headers)
  
    def secondes_en_hms(self,secondes):
        """Permet de convertir un temps en secondes en heures, minutes, secondes """
        h = secondes // 3600
        m = (secondes % 3600) // 60
        s = secondes % 60
    
        bon_temps = ""
        if h > 0:
            bon_temps += f"{h}h"
        if m > 0 or h > 0:  # on affiche les minutes si heures existent
            bon_temps += f"{m}min"
        bon_temps += f"{s}sec"
        return bon_temps
        
    def envoi_moy_h(self, instance):
        """ Affichage des moyens utilisés"""
        #Description de la fonction
        #Titre
        self.layout.clear_widgets()
        
        self.label=Label(text="Voici les moyens de transport que vous avez utilisé \n du  "+str(self.horaire_debut.text)+" au "+str(self.horaire_fin.text)+" : ")
        self.layout.add_widget(self.label)
        for i in range(len(self.liste_moyens_estimes_h)):
            self.duree_h = self.liste_timestamp_h[i+1] - self.liste_timestamp_h[i]
            
            self.label = Label(text=self.liste_moyens_estimes_h[i] + " pendant " + str(self.secondes_en_hms(int(self.duree_h))) + " \n")
            self.layout.add_widget(self.label)
            
        self.label=Label(text= "\n\n Vous avez déclaré avoir utilisé les moyens suivants : \n")
        self.layout.add_widget(self.label)
        if "," in self.moyen_input_h.text :
            moyens_decl_h=self.moyen_input_h.text.split(",")
        else :
            moyens_decl_h=[self.moyen_input_h.text]
        for i in range(len(moyens_decl_h)):
            self.label=Label(text=moyens_decl_h[i])
            self.layout.add_widget(self.label)


 #--------------2-Demarrer un trajet et determiner le moyen de transport utilisé----------------       
        
    def un_ajout_trajet(self, instance):
        """"Construction de la page pour ajouter un trajet avec un moyen de transport"""
        self.layout.clear_widgets()
        self.title = "Ambrasobin - Page Trajet"
        self.un_bouton_debut = Button(text="Début")
        self.un_bouton_fin = Button(text="Fin")
        
        #Ajouter les rôles des boutons début et fin
        self.un_bouton_debut.bind(on_press = self.un_debut_gps)
        self.un_bouton_fin.bind(on_press = self.un_fin_gps)
        
        self.layout.add_widget(self.un_bouton_debut)
        self.layout.add_widget(self.un_bouton_fin)
        
    def un_debut_gps(self, instance, **kwargs):
        """Fonction permettant le début d'un enregistrement gps sans limite de temps fixe"""
        
        self.attente_gps = Label(text = "En attente des positions GPS")
        self.layout.add_widget(self.attente_gps)
        gps.configure(on_location=self.recup_donnees_gps)
        gps.start()
        self.timestamp_debut = time() 
        self.longitude=kwargs.get('lon')
        self.latitude=kwargs.get('lat')
        self.altitude=kwargs.get('altitude')
        self.speed=kwargs.get('speed')
        self.accuracy=kwargs.get('accuracy')
        self.bearing=kwargs.get('bearing')
        self.timestamp=time()
        
        req_body = json.dumps({
            'long': self.longitude,
            'lat': self.latitude,
            'id_groupe': self.id_grp,
            'timestamp': self.timestamp
           
        })

        req_method = 'POST'
        UrlRequest('http://irioso.free.fr/Groupe_1/lieu_d_interet_local.php', req_body=req_body, method=req_method)
#Ne fonctionne pas
 #   def affiche_lieu(self, requete, resultat):
 #       self.affichage_lieu = Label(text=resultat)
#        self.layout.add_widget(self.affichage_lieu)
               
    
    def un_fin_gps(self, instance):
        """Fonction permettant la fin d'un enregistrement gps sans limite de temps fixe"""
        #A construire/ Doit permettre d'afficher les sous-transports et de comparer avec ceux rentrer par l'utilisateur
        gps.stop()
        self.layout.clear_widgets()
        self.title = "Voila le moyen de transport que vous avez utilisé"
        self.timestamp_fin=time()
        
        data = {'timestamp_debut': self.timestamp_debut, 'timestamp_fin': self.timestamp_fin}
        
        headers = {'Content-Type': 'application/json'}

      
        UrlRequest(url='http://irioso.free.fr/Ambrasobin/deter_un_moyen.php', req_body=json.dumps(data),  req_headers=headers, on_success=self.un_get_result)
        
    def un_get_result(self, requete, resultat):
        """" """
        self.moyen_donne = Label(text="Quel moyen de transport avez-vous utilisé ?")
        self.layout.add_widget(self.moyen_donne)
        self.nom_dec = TextInput(hint_text="Moyen 1")
        self.layout.add_widget(self.nom_dec)
        self.button=Button(text="Entrer", on_press=self.un_envoi_moy)
        self.layout.add_widget(self.button)
        self.nom_est=resultat
        
    def un_envoi_moy(self, instance):
        """ """
        #Titre
        self.layout.clear_widgets()
        
        self.label=Label(text="Nous avons estimé que vous avez utilisé le \n moyen de transport suivant : ")
        self.layout.add_widget(self.label)
        self.label=Label(text=self.nom_est)
        self.layout.add_widget(self.label)
            
        self.label=Label(text= "\n\n Vous avez déclaré avoir utilisé le moyen suivant : \n")
        self.layout.add_widget(self.label)
        self.label=Label(text=self.nom_dec.text)
        self.layout.add_widget(self.label)  
        
        data = {'timestamp_debut': self.timestamp_debut, 'timestamp_fin': self.timestamp_fin, 'nom_est': self.nom_est,'nom_dec': self.nom_dec.text}

        headers = {'Content-Type': 'application/json'}

      
        UrlRequest(url='http://irioso.free.fr/Ambrasobin/insert_trajet.php', req_body=json.dumps(data),  req_headers=headers)
        if self.nom_est.strip() == self.nom_dec.text.strip():
            self.timestamp_bonus = time()
            data = {'timestamp_bonus': self.timestamp_bonus}
            UrlRequest(
                url='http://irioso.free.fr/Ambrasobin/insert_bonus.php',
                req_body=json.dumps(data),
                req_headers=headers
            )
            self.label=Label(text="bravo, vous avez un bonus !")
            self.layout.add_widget(self.label)
        self.button=Button(text="Retour sur la page principale", on_press=self.retour_page_principale)
        self.layout.add_widget(self.button)


        
        
 
 #------------3-Bonus - Demarrer un trajet et determiner les moyens de transport utilisés----------------          
        
    def ajout_trajet(self, instance):
        """"Construction de la page pour ajouter un trajet avec plusieurs moyens de transport """
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
        
        self.attente_gps = Label(text = "En attente des positions GPS")
        self.layout.add_widget(self.attente_gps)
        gps.configure(on_location=self.recup_donnees_gps)
        gps.start()
        self.timestamp_debut = time() 
        
    def recup_donnees_gps(self, **kwargs):
        self.attente_gps.text = '\n'.join(['{}={}'.format(k, v) for k, v in kwargs.items()])
        self.longitude=kwargs.get('lon')
        self.latitude=kwargs.get('lat')
        self.altitude=kwargs.get('altitude')
        self.speed=kwargs.get('speed')
        self.accuracy=kwargs.get('accuracy')
        self.bearing=kwargs.get('bearing')
        self.timestamp=time()
        
        data = {'longitude': self.longitude, 'latitude': self.latitude, 'altitude': self.altitude,'timestamp': self.timestamp, 'speed': self.speed, 'bearing': self.bearing, 'accuracy' : self.accuracy}

        headers = {'Content-Type': 'application/json'}

      
        UrlRequest(url='http://irioso.free.fr/Ambrasobin/recup_donnees.php', req_body=json.dumps(data),  req_headers=headers)
        
  
        
        
    
    def fin_gps(self, instance):
        """Fonction permettant la fin d'un enregistrement gps sans limite de temps fixe"""
        #A construire/ Doit permettre d'afficher les sous-transports et de comparer avec ceux rentrer par l'utilisateur
        gps.stop()
        self.layout.clear_widgets()
        self.title = "Voila les moyens de transport que vous avez utilisé"
        self.timestamp_fin=time()
        
        data = {'timestamp_debut': self.timestamp_debut, 'timestamp_fin': self.timestamp_fin}
        
        headers = {'Content-Type': 'application/json'}

      
        UrlRequest(url='http://irioso.free.fr/Ambrasobin/deter_moyen.php', req_body=json.dumps(data),  req_headers=headers, on_success=self.get_result)
        
    def get_result(self, requete, resultat):
       
        self.moyen_donne = Label(text="Quels moyens de transport avez-vous utilisé ?")
        self.layout.add_widget(self.moyen_donne)
        self.moyen_input = TextInput(hint_text="Moyen 1, Moyen 2,...")
        self.layout.add_widget(self.moyen_input)
        self.button=Button(text="Entrer", on_press=self.envoi_moy)
        self.layout.add_widget(self.button)
        if resultat[-1]!="}":
            resultat+="}"
        data=json.loads(resultat)
        self.liste_moyens_estimes=[]
        for valeur in data.values():
            self.liste_moyens_estimes.append(valeur)
            
        self.liste_timestamp=[]
        for cle in data.keys():
            self.liste_timestamp.append(float(cle))
        self.liste_timestamp.append(self.timestamp_fin)
        
        
    def envoi_moy(self, instance):
        self.layout.clear_widgets()
        
        self.label=Label(text="Nous avons estimé que vous avez utilisé les \n moyens de transport suivants : ")
        self.layout.add_widget(self.label)
        for i in range(len(self.liste_moyens_estimes)):
            self.duree = self.liste_timestamp[i+1] - self.liste_timestamp[i]
            self.label = Label(text=self.liste_moyens_estimes[i] + " pendant " + str(int(self.duree)) + " secondes\n")

            self.layout.add_widget(self.label)
            
        self.label=Label(text= "\n\n Vous avez déclaré avoir utilisé les moyens suivants : \n")
        self.layout.add_widget(self.label)
        if "," in self.moyen_input.text :
            moyens_decl=self.moyen_input.text.split(",")
        else :
            moyens_decl=[self.moyen_input.text]
        for i in range(len(moyens_decl)):
            self.label=Label(text=moyens_decl[i])
            self.layout.add_widget(self.label)
        self.button=Button(text="Retour sur la page principale", on_press=self.retour_page_principale)
        self.layout.add_widget(self.button)
        
        
#------------------Ne fonctionne pas----------------------------------------------   
  
        
    # def lieux_interet (self, **kwargs) : 
    #     """Fonction permettant d'enregistrer les points d'intérêts traverser sur un trajet donné"""
    #     liste_lieux_visités = []
    #     #récupérer les données GPS des lieux d'intérêt avec leur nom de la BD 
    #     UrlRequest('http://localhost:8888/lieu_d_interet_local.php', on_success = self.recup_lieux)
    #     #Comparer la dernière valeur de donnée avec chacune des données des points d'intérêts
    #     #->Fonction distance entre deux points php et comparaison au rayon de chaque point
    #     for i in range(0, len(self.tableau_lieux_interet)): 
    #         #if distance(point_actuel, tableau_lieux_interet[i])< rayon : 
    #             liste_lieux_visités.append(self.tableau_lieux_interet[i])
    #     #Si on est dans le rayon d'un point d'intérêt 

    
    # def recup_lieux (self, request, result):
    #     """Fonction de récupération des points d'intérêt, chaque données les concernant est stockées sous forme de tableaux"""
    #     self.tableau_lieux_interet = json.loads(result)['noms_lieux']
    #     self.tableau_id_lieux = json.loads(result)['id_lieux']
    #     self.tableau_latitudes = json.loads(result)['latitudes']
    #     self.tableau_longitudes= json.loads(result)['longitudes']
    #     print(self.tableau_lieux_interet)

    # def data_consolidees(self, requete, resultat):
    #     data = {'id_phone': self.id_phone, 'long': self.longitude, 'lat' : self.latitude, 'speed': self.speed, 'acc': self.accuracy, 'bearing': self.bearing, 'time': self.timestamp, 'alt': self.altitude}
        
    #     headers = {'Content-Type': 'application/json'}
    #     UrlRequest(url='http://irioso.free.fr/Groupe_1/base_data_consolidees.php', req_body=json.dumps(data),  req_headers=headers)
       
    
if __name__ == '__main__':
    
    MyApp().run()
