from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.network.urlrequest import UrlRequest
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from random import randint
from kivy.clock import Clock
from time import time
from plyer import gps
import json

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
        req_body = json.dumps({'nom': nom, 'prenom': prenom})
        req_method = 'POST'
        UrlRequest('http://irioso.free.fr/Groupe_1/recup_id.php', req_body=req_body, method=req_method, on_success=self.page_principale)

    def page_principale(self, request, result): 
        """Page de choix de l'action : enregistrement d'un arbre ou d'un trajet"""
        if result[-1]!="}":
            result+="}"
        data = json.loads(result)
        if 'id' in data and 'id_groupe' in data:
            self.id = data['id']
            self.id_grp = data['id_groupe']
        else:
            self.layout.clear_widgets()
            self.title = "Erreur de connexion"
            self.erreur_label = Label(text="Erreur de connexion, veuillez réessayer.")
            self.layout.add_widget(self.erreur_label)
            self.bouton_reessayer = Button(text="Réessayer")
            self.bouton_reessayer.bind(on_press=self.fen)
            self.layout.add_widget(self.bouton_reessayer)

        self.layout.clear_widgets()
        self.title = "Ambrasobin - Page principale"
        self.titre_page_principale = Label(text="Bienvenue sur la page principale !", underline=True, font_size='50sp', markup=True, color=[0.16, 0.42, 0.17, 1])
        self.layout.add_widget(self.titre_page_principale)
        self.choix_donnees = Label(text="Veux-tu ajouter un arbre ou un trajet ?")
        self.arbre = Button(text="Ajouter un arbre", color=[1, 1, 1, 1], background_normal="", background_color=[0.16, 0.42, 0.17, 1])
        self.arbre.bind(on_press=self.page_arbre)
        self.trajet = Button(text="Ajouter un trajet", color=[1, 1, 1, 1], background_normal="", background_color=[0.16, 0.42, 0.17, 1])
        self.trajet.bind(on_press=self.ajout_trajet)
        self.layout.add_widget(self.choix_donnees)
        self.layout.add_widget(self.arbre)
        self.layout.add_widget(self.trajet)

        

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
            id_arbre = json.loads(result)['id']
            req_body = json.dumps({'long': self.long, 'lat': self.lat, 'id': id_arbre})
            req_method = 'POST'
            UrlRequest('http://irioso.free.fr/Groupe_1/MAJ_arbre.php', req_body=json.dumps({'id': id_arbre}), method='POST', on_success=self.message_arbre)
        else:
            # pas d'arbre, on peut en ajouter un
            self.enregistrement_nv_arbre(None)

    def message_arbre(self, *args):
        """Affichage d'un message pour dire que l'arbre a été ajouté"""
        self.layout.clear_widgets()
        self.title = "Ambrasobin - Arbre ajouté"
        self.message = Label(text="L'arbre a bien été ajouté !")
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
        self.essence_arbre = self.demande_essence_arbre.text

        self.circonference_arbre = Label(text="Quel est la circonference de l'arbre ?")
        self.layout.add_widget(self.circonference_arbre)
        self.demande_circonference_arbre = TextInput()
        self.layout.add_widget(self.demande_circonference_arbre)
        self.circonference_arbre = self.demande_circonference_arbre.text

        self.mort_arbre = Label(text="Quel est l'état de l'arbre (0 mort, 1 vivant) ?")
        self.layout.add_widget(self.mort_arbre)
        self.demande_mort_arbre = TextInput()
        self.layout.add_widget(self.demande_mort_arbre)
        self.mort_arbre = self.demande_mort_arbre.text

        self.nom_img = Label(text="nom de l'image ?")
        self.layout.add_widget(self.nom_img)
        self.demande_nom_img = TextInput()
        self.layout.add_widget(self.demande_nom_img)
        self.nom_img = self.demande_nom_img.text

        self.timestamp_arbre = time()
        
        self.bouton_envoi = Button(text="Enregistrer l'arbre")
        self.bouton_envoi.bind(on_press=self.envoi_arbre)
        self.layout.add_widget(self.bouton_envoi)
        

    def envoi_arbre(self, instance):
        req_body = json.dumps({
            'essence': self.essence_arbre,
            'circonference': self.circonference_arbre,
            'mort': self.mort_arbre,
            'id_groupe': self.id_grp,
            'lat': self.lat,
            'long': self.long,
            'timestamp': self.timestamp_arbre,
            'nom_img': self.nom_img
        })

        req_method = 'POST'
        UrlRequest('http://irioso.free.fr/Groupe_1/ajout_arbre.php', req_body=req_body, method=req_method, on_success=self.message_arbre)

    def ajout_trajet(self, instance):
        """Construction de la page pour ajouter un trajet"""
        self.layout.clear_widgets()
        self.title = "Ambrasobin - Page Trajet"
        self.bouton_debut = Button(text="Début")
        self.bouton_fin = Button(text="Fin")
        self.bouton_debut.bind(on_press=self.debut_gps)
        self.bouton_fin.bind(on_press=self.fin_gps)
        self.layout.add_widget(self.bouton_debut)
        self.layout.add_widget(self.bouton_fin)

    def debut_gps(self, instance):
        """Début d'un enregistrement gps sans limite de temps fixe"""
        self.attente_gps = Label(text="En attente des positions GPS")
        self.layout.add_widget(self.attente_gps)
        gps.configure(on_location=self.recup_donnees_gps)
        gps.start()
        self.timestamp_debut = time()

    def recup_donnees_gps(self, **kwargs):
        self.attente_gps.text = '\n'.join(['{}={}'.format(k, v) for k, v in kwargs.items()])
        longitude = kwargs.get('lon')
        latitude = kwargs.get('lat')
        altitude = kwargs.get('altitude')
        speed = kwargs.get('speed')
        accuracy = kwargs.get('accuracy')
        bearing = kwargs.get('bearing')
        timestamp = time()
        data = {
            'longitude': longitude,
            'latitude': latitude,
            'altitude': altitude,
            'timestamp': timestamp,
            'speed': speed,
            'bearing': bearing,
            'accuracy': accuracy
        }
        headers = {'Content-Type': 'application/json'}
        UrlRequest(url='http://irioso.free.fr/Ambrasobin/recup_donnees.php', req_body=json.dumps(data), req_headers=headers, on_success=self.on_success)

    def on_success(self, request, result):
        pass

    def fin_gps(self, instance):
        """Fin d'un enregistrement gps sans limite de temps fixe"""
        gps.stop()
        self.layout.clear_widgets()
        self.title = "Voila les moyens de transport que vous avez utilisé"
        self.timestamp_fin = time()
        data = {'timestamp_debut': self.timestamp_debut, 'timestamp_fin': self.timestamp_fin}
        headers = {'Content-Type': 'application/json'}
        UrlRequest(url='http://irioso.free.fr/Ambrasobin/deter_moyen.php', req_body=json.dumps(data), req_headers=headers, on_success=self.get_result)

    def get_result(self, requete, resultat):
        self.label = Label(text=resultat)
        self.layout.add_widget(self.label)

    def lieux_interet(self, **kwargs):
        """Enregistre les points d'intérêts traversés sur un trajet donné"""
        liste_lieux_visites = []
        UrlRequest('http://irioso.free.fr/Groupe_1/lieu_d_interet_local.php', on_success=self.recup_lieux)
        for i in range(0, len(self.tableau_lieux_interet)):
            # if distance(point_actuel, tableau_lieux_interet[i]) < rayon:
            liste_lieux_visites.append(self.tableau_lieux_interet[i])
        print('Bonjour')

    def recup_lieux(self, request, result):
        """Récupère les points d'intérêt, chaque donnée est stockée sous forme de tableau"""
        self.tableau_lieux_interet = json.loads(result)['noms_lieux']
        self.tableau_id_lieux = json.loads(result)['id_lieux']
        self.tableau_latitudes = json.loads(result)['latitudes']
        self.tableau_longitudes = json.loads(result)['longitudes']
        self.label_lieux_interet = Label(text=str(self.tableau_lieux_interet))
        self.layout.add_widget(self.label_lieux_interet)
        latitude1 = 18
        longitude1 = 21
        latitude2 = 32
        longitude2 = 44
        req_body = json.dumps({'lat1': latitude1, 'long1': longitude1, 'lat2': latitude2, 'long2': longitude2})
        req_method = 'POST'
        UrlRequest(url='http://localhost:8888/distance.php', req_body=req_body, method=req_method, on_success=self.distance_interet)

    def distance_interet(self, request, result):
        self.label_distance = Label(text=result)
        self.layout.add_widget(self.label_distance)

if __name__ == '__main__':
    MyApp().run()
