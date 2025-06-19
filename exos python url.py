# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 10:55:11 2025

@author: rapha
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest
from kivy.uix.label import Label

from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
import json


'EXERCICE 1'
# class MyApp(App):
 
#     def build(self):
#         self.my_box = BoxLayout()
#         self.my_button=Button(text='SE CONNECTER')
#         self.my_button.bind(on_press=self.press)
#         self.my_box.add_widget(self.my_button)
#         return self.my_box
    
#     def press(self, touch):
#         UrlRequest('http://localhost/liste_eleves.php', on_success = self.get_result)
       

#     def get_result(self, request, result):
#         self.text = result
#         print(self.text)
#         self.my_box.add_widget(Label(text=self.text))
#         self.my_box.remove_widget(self.my_button)
 
# if __name__ == '__main__':
#     MyApp().run()
    
"EXERCICXE 2"
    
class MyGridLayout(GridLayout):
    
    def __init__(self, **kwargs):
        #appel au constructeur de GridLayout
        super(MyGridLayout, self).__init__(**kwargs)
        
        #nombre de colonnes
        self.cols = 1
        self.add_widget(Label(text=''))
        #ajout des éléments texte
        self.label = Label(text='Nom : ')
        self.add_widget(self.label)
        #ajout d'un champ texte
        self.nom = TextInput(multiline=False)
        self.add_widget(self.nom)
        

        #bouton de validation
        self.bouton_valider = Button(text="Valider")
        self.bouton_valider.bind(on_press=self.press)
        self.add_widget(self.bouton_valider) 
        
    def press(self, instance):
        nom = self.nom.text
        self.remove_widget(self.nom)
        self.remove_widget(self.label)
        self.remove_widget(self.bouton_valider)
        
        
        #encodage des informations à transmettre
        nom=self.nom.text
        req_body = json.dumps({'nom':nom})
        req_method = 'POST'
        
        #envoie de la requête URL avec les données encodées au serveur Web
        UrlRequest('http://irioso.free.fr/liste_eleves.php',req_body = req_body,method=req_method,  on_success = self.got_json)
        

    def got_json(self, request, result):
        nb = json.loads(result)['reponse']
        
        self.rep=Label(text="Bonjour votre id est {} !".format(nb))
        self.add_widget(self.rep)
        
        self.bouton_again= Button(text="relancer une requête")
        self.add_widget(self.bouton_again)
        self.bouton_again.bind(on_press=self.press_again)
    
    def press_again(self,instance):
        self.remove_widget(self.bouton_again)
        self.remove_widget(self.rep)
        self.add_widget(self.label)
        self.nom = TextInput(multiline=False)
        self.add_widget(self.nom)
        self.add_widget(self.bouton_valider)
        
        
        

class MyApp(App):
    def build(self):
        return MyGridLayout()
    
    
if __name__ == '__main__':
    MyApp().run()    

    
# from kivy.app import App
# from kivy.core.window import Window
# from kivy.graphics import Color,Ellipse
# from kivy.uix.widget import Widget
# from kivy.network.urlrequest import UrlRequest
# import random
 
 
# class Balle(Widget):
#     def __init__(self,canvas):
#         self.x=random.randint(50,500)
#         self.y=random.randint(50,500)
#         self.pos = (self.x, self.y)
#         self.canvas=canvas
#         self.size=(50,50)
#         self.color=[1,0,0,0.5]#Rouge
#         with self.canvas:
#             Color(self.color[0],self.color[1],self.color[2],0.5)
#             self.disque=Ellipse(pos=self.pos, size=self.size)
        
#         #On associe les modifications de position a une fonction update:
#         self.bind(pos=self.update_disque)

#     def update_disque(self, *args):
#         #On redefinie les position du disque sur le canvas:
#         self.disque.pos = self.pos
 
# class Jeu(GridLayout):
    
#     def menu(self,**kwargs):
#         #appel au constructeur de GridLayout
#         super(Jeu, self).__init__(**kwargs)
        
#         #nombre de colonnes
#         self.cols = 1
#         self.add_widget(Label(text=''))
#         #ajout des éléments texte
#         self.label = Label(text='ID de joueur : ')
#         self.add_widget(self.label)
#         #ajout d'un champ texte
#         self.id = TextInput(multiline=False)
#         self.add_widget(self.id)
        

#         #bouton de validation
#         self.bouton_valider = Button(text="Valider")
#         self.bouton_valider.bind(on_press=self.press)
#         self.add_widget(self.bouton_valider) 
        
#     def press(self, instance):
#         self.num=self.id.text
#         self.remove_widget(self.id)
#         self.remove_widget(self.label)
#         self.remove_widget(self.bouton_valider)
        
#         self.message=Label(text="Vous pouvez commencer à jouer en cliquant sur le bouton !")
#         self.add_widget(self.message)
        
#         self.bouton_jouer= Button(text="JOUER")
#         self.add_widget(self.bouton_jouer)
#         self.bouton_jouer.bind(on_press=self.press_play)
    
#     def press_play(self,instance):
#         self.remove_widget(self.bouton_jouer)
#         self.remove_widget(self.message)
        
        
        
#     def debut(self):
#         #On cree la première balle:
#         self.balles=[Balle(self.canvas)]
                
     
#     def on_touch_up(self, touch):
#         for balle in self.balles :
            
#             #On teste si le point de l'ecran relache est sur la balle: 
#             if balle.collide_point(touch.x,touch.y):
                
#                 #On change les coordonnees de la balle par des valeurs aléatoires
#                 balle.pos=(random.randint(0,500),random.randint(0,500))
                
#                 #encodage des informations à transmettre
#                 req_body = json.dumps({'id':self.num , 'x':balle.pos[0], 'y':balle.pos[1]})
#                 req_method = 'POST'
                
#                 #envoie de la requête URL avec les données encodées au serveur Web
#                 UrlRequest('pos.free.fr',req_body = req_body,method=req_method,  on_success = self.got_json)
            
#     def got_json(self, request, result):
#         print('La balle a bougé !')

 
# class MyApp(App):
 
#     def build(self):
#         jeu=Jeu()
#         jeu.menu()
#         jeu.debut()
#         return jeu
 
# if __name__ == '__main__':
#     Window.size = (500, 500)
#     MyApp().run()