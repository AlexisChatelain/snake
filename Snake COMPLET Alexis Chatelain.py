# copyright musiques : The Grid et End Credits Tron Legacy (2009), Gave Over : https://www.youtube.com/watch?v=br3OzOrARh4, sons Snake Google
# copyright images : boutons issus d'Internet, image Tron Legacy (2009)
# Principale source d'inspiration : Snake Google : https://www.google.fr/search?q=snake&rlz=1C1GCEA_enFR815FR815&oq=snake&aqs=chrome..69i57j46j0l2j46j69i59.823j1j7&sourceid=chrome&ie=UTF-8

# Problème résolus :
# - le serpent ne peut plus tourner sur lui-même
# - tête à gauche, droite, HAUT et BAS
# - la pomme ne peut plus être générée aléatoirement sous le corps
# - écran d'accueil créé et terminé
# - écran game over terminé
# - blanc de la tête maintenant inexistant
# - rafraîchissement annulé à la fermeture

'''
Liste de ce qui reste éventuellement à faire :
- nouveaux sons, musique et images libres de droits
- sous programmes
- commmenter
- Optimiser
'''

import pickle
import re
from getpass import getpass
import os
import pygame
from pygame.locals import *
from random import randint
import sys
import time
pygame.init()
pygame.font.init()

#Création de la fenetre et polices d'écritures
rep_ok=0
while rep_ok==0:
    reponse=input("Plein écran ? (O/N)")
    if reponse =="n" or reponse =="N" or reponse=="o" or reponse =="O":
        if reponse =="o" or reponse =="O":
            fenetre= pygame.display.set_mode((800,700),pygame.FULLSCREEN)
        elif reponse =="n" or reponse =="N":
            fenetre= pygame.display.set_mode((800,700))
        rep_ok=1
pygame.display.set_caption("Snake COMPLET Alexis Chatelain")
myfont = pygame.font.SysFont("Arial", 58)
myfont1 = pygame.font.SysFont("LCD5x8H", 230) #
myfont2 = pygame.font.SysFont("Arial", 25)
font = pygame.font.SysFont("Arial", 58)
pygame.key.set_repeat(400, 30)
#chargement des images
lumino=pygame.image.load(os.path.join("Snake_Files\images", 'luminosite.png')).convert_alpha()
carre_rose=pygame.image.load(os.path.join("Snake_Files\images", 'carre_rose_50x50.png')).convert()
carre_rouge=pygame.image.load(os.path.join("Snake_Files\images", 'carre_rouge_50x50.png')).convert()
serpent_corps=pygame.image.load(os.path.join("Snake_Files\images", 'serpent_corps.png')).convert()
serpent_tete_droite=pygame.image.load(os.path.join("Snake_Files\images", 'serpent_tete_droite.png')).convert_alpha()
serpent_tete_gauche=pygame.image.load(os.path.join("Snake_Files\images", 'serpent_tete_gauche.png')).convert_alpha()
serpent_tete_haut=pygame.image.load(os.path.join("Snake_Files\images", 'serpent_tete_haut.png')).convert_alpha()
serpent_tete_bas=pygame.image.load(os.path.join("Snake_Files\images", 'serpent_tete_bas.png')).convert_alpha()
rejouer=pygame.image.load(os.path.join("Snake_Files\images", 'rejouer.png')).convert_alpha()
quitter=pygame.image.load(os.path.join("Snake_Files\images", 'quitter.png')).convert_alpha()
pomme=pygame.image.load(os.path.join("Snake_Files\images", 'pomme.png')).convert_alpha()
accueil = pygame.image.load(os.path.join("Snake_Files\images", 'tron.jpg')).convert_alpha()
jouer=pygame.image.load(os.path.join("Snake_Files\images", 'jouer.png')).convert_alpha()
joueur=pygame.image.load(os.path.join("Snake_Files\images", 'joueur.png')).convert_alpha()
#fonctions
def affichage_damier(carre_rose,carre_rouge):
    for i in range(16):
        for j in range(14):
            fenetre.blit(carre_rose,(2*i*50,j*50))
            fenetre.blit(carre_rouge,((2*i+1)*50,j*50))
            carre_rose,carre_rouge=carre_rouge,carre_rose

def coord_matrice_vers_coord_graphique(t):
    return(t[1]*50,t[0]*50)            # attention les numeros de ligne * 50 deviennent les ordonnées, les numéros de colonne*50 deviennent les abscisses

def affichage_serpent_gauche(serpent): # affiche le serpent tête tournée vers la gauche
    for k in serpent:
        if k!=[serpent[len(serpent)-1][0],serpent[len(serpent)-1][1]]:
            fenetre.blit(serpent_corps,coord_matrice_vers_coord_graphique(k))
    fenetre.blit(serpent_tete_gauche,coord_matrice_vers_coord_graphique(serpent[len(serpent)-1]))
def affichage_serpent_droite(serpent): # affiche le serpent tête tournée vers la droite
    for k in serpent:
        if k!=[serpent[len(serpent)-1][0],serpent[len(serpent)-1][1]]:
            fenetre.blit(serpent_corps,coord_matrice_vers_coord_graphique(k))
    fenetre.blit(serpent_tete_droite,coord_matrice_vers_coord_graphique(serpent[len(serpent)-1]))

def affichage_serpent_haut(serpent): # affiche le serpent tête tournée vers la gauche
    for k in serpent:
        if k!=[serpent[len(serpent)-1][0],serpent[len(serpent)-1][1]]:
            fenetre.blit(serpent_corps,coord_matrice_vers_coord_graphique(k))
    fenetre.blit(serpent_tete_haut,coord_matrice_vers_coord_graphique(serpent[len(serpent)-1]))

def affichage_serpent_bas(serpent): # affiche le serpent tête tournée vers la gauche
    for k in serpent:
        if k!=[serpent[len(serpent)-1][0],serpent[len(serpent)-1][1]]:
            fenetre.blit(serpent_corps,coord_matrice_vers_coord_graphique(k))
    fenetre.blit(serpent_tete_bas,coord_matrice_vers_coord_graphique(serpent[len(serpent)-1]))

def déplacement_droite(serpent):                                                # fonction qui déplace d'une case vers la doite le serpent, le serpent étant une liste de 3 valeurs qui indiquent les numéros de colonne
    if serpent[len(serpent)-1][1]<15:                                           # Chercher la valeur actuelle en abscisse afin de ne pas sortir de la fenêtre
        serpent.append([serpent[len(serpent)-1][0],serpent[len(serpent)-1][1]]) # Ajouter la valeur des coordonées de la tête du serpent à la fin de la liste
        serpent[len(serpent)-1][1]=serpent[len(serpent)-1][1] + 1               # Ajouter 1 en abscisse à la dernière coordonnée fraichement crée de la liste
        if tete_pomme!=1:                                                       # si on n'est pas sur la pomme
            serpent.pop(0)                                                      # et supprimer la première coordonée de la liste
    else:
        perdu()

def déplacement_gauche(serpent):                                                # fonction qui déplace d'une case vers la gauche le serpent, le serpent étant une liste de 3 valeurs qui indiquent les numéros de colonne
    if serpent[len(serpent)-1][1]>0:                                            # Chercher la valeur actuelle en abscisse afin de ne pas sortir de la fenêtre
        serpent.append([serpent[len(serpent)-1][0],serpent[len(serpent)-1][1]]) # Ajouter la valeur des coordonées de la tête du serpent à la fin de la liste
        serpent[len(serpent)-1][1]=serpent[len(serpent)-1][1] - 1               # Soustraire 1 en abscisse à la dernière coordonnée fraichement crée de la liste
        if tete_pomme!=1:
            serpent.pop(0)                                                      # et supprimer la première coordonée de la liste
    else:
        perdu()

def déplacement_haut(serpent):
    if serpent[len(serpent)-1][0]>0:                                            # Chercher la valeur actuelle en abscisse afin de ne pas sortir de la fenêtre
        serpent.append([serpent[len(serpent)-1][0],serpent[len(serpent)-1][1]]) # Ajouter la valeur des coordonées de la tête du serpent à la fin de la liste
        serpent[len(serpent)-1][0]=serpent[len(serpent)-1][0] - 1               # Soustaire 1 en ordonnée à la dernière coordonnée fraichement crée de la liste
        if tete_pomme!=1:
            serpent.pop(0)                                                      # et supprimer la première coordonée de la liste
    else:
        perdu()

def déplacement_bas(serpent):
    if serpent[len(serpent)-1][0]<13:                                           # Chercher la valeur actuelle en abscisse afin de ne pas sortir de la fenêtre
        serpent.append([serpent[len(serpent)-1][0],serpent[len(serpent)-1][1]]) # Ajouter la valeur des coordonées de la tête du serpent à la fin de la liste
        serpent[len(serpent)-1][0]=serpent[len(serpent)-1][0] + 1               # Ajouter 1 en ordonnée à la dernière coordonnée fraichement crée de la liste
        if tete_pomme!=1:
            serpent.pop(0)                                                      # et supprimer la première coordonée de la liste
    else:
        perdu()

def deplacement_et_affichage_bon_sens():
        if dir=="" :                                    # c'est l'écran de démarrage du jeu
            affichage_serpent_droite(serpent)
        elif dir=="droite":                             # partie déplacmeent auto
            déplacement_droite(serpent)
            affichage_serpent_droite(serpent)           # fonction qui affiche le serpent tourné vers la droite lors du démarrage du jeu (1ère image)
        elif dir=="gauche":
            déplacement_gauche(serpent)
            affichage_serpent_gauche(serpent)           # fonction qui affiche le serpent tourné vers la gauche
        elif dir=="haut":
            déplacement_haut(serpent)
            affichage_serpent_haut(serpent)
        elif dir=="bas":
            déplacement_bas(serpent)
            affichage_serpent_bas(serpent)

def affichage_bon_sens():
        if dir=="droite":
            affichage_serpent_droite(serpent)   # fonction qui affiche le serpent tourné vers la droite lors du démarrage du jeu (1ère image)
        elif dir=="gauche":
            affichage_serpent_gauche(serpent)   # fonction qui affiche le serpent tourné vers la gauche
        elif dir=="haut":
            affichage_serpent_haut(serpent)
        elif dir=="bas":
            affichage_serpent_bas(serpent)

def perdu():
    global arret, continuer, recommencer, commencer, jeu
    f = open(os.path.join("Snake_Files\scores", pseudo_choisi), "r")
    t = f.readline()
    if points > int(t):
        g = open(os.path.join("Snake_Files\scores", pseudo_choisi), "w")
        g.write(str(points))
        g.close()
    h = open(os.path.join("Snake_Files\scores", pseudo_choisi), "r")
    t = h.readline()
    record_absolu=int(t)
    f.close()
    pygame.mixer.music.stop()
    son = pygame.mixer.Sound(os.path.join("Snake_Files\sound", 'perdu.wav'))
    son.play()
    time.sleep(1)
    pygame.mixer.music.load(os.path.join("Snake_Files\sound", 'Game Over.mp3'))
    pygame.mixer.music.play(0)                                                                       # programme quand on a perdu (sorti de la fenêtre ou collision)
    affichage_bon_sens()
    if parties<10 :
        label0 = myfont.render("Partie n°0" + str(parties) + " :", 1, (0,0,0))
    else:
        label0 = myfont.render("Partie n°" + str(parties) + " :", 1, (0,0,0))
    label = myfont.render("GAME OVER !!!", 1, (0,0,0)) # render text, cad le transformer en image
    if points <2:
        label2 = myfont.render(str(points) + " point", 1, (0,0,0))
    elif points <10:
        label2 = myfont.render(str(points) + " points", 1, (0,0,0))
    else:
        label2 = myfont.render(str(points) + " points", 1, (0,0,0))
    if record_absolu <2:
        label1 = myfont.render("Votre record : " + str(record_absolu)+" point", 1, (0,0,0))
    else:
        label1 = myfont.render("Votre record : " + str(record_absolu)+" points", 1, (0,0,0))
    label3 = myfont.render("Que voulez-vous faire ?", 1, (0,0,0))
    label4 = myfont.render("Rejouer     Pseudo       Quitter", 1, (0,0,0))
    fenetre.blit(lumino,(0,0))
    fenetre.blit(rejouer, (50, 500))
    fenetre.blit(joueur, (350, 500))
    fenetre.blit(quitter, (650, 500))
    fenetre.blit(label0, (125, 100))
    fenetre.blit(label, (200, 0))
    fenetre.blit(label1, (100, 200))
    fenetre.blit(label2, (475, 100))
    fenetre.blit(label3, (75, 300))
    fenetre.blit(label4, (10, 400))
    pygame.display.flip()
    continuer1 = 0
    while continuer1 == 0:
        for event in pygame.event.get():# pour chaque événement de la bibliothèque pygame détecté
            if event.type == MOUSEBUTTONDOWN:
                if (event.pos[0]<770 and event.pos[0] >650 and event.pos[1] <670 and event.pos[1] >500): #event.pos[0] --> hauteur     #event.pos[1] --> largeur
                    arret = 1
                    continuer = 0
                    continuer1 = 1
                    recommencer = 0
                    commencer = 1
                    jeu=0
                elif event.pos[0]<470 and event.pos[0] >350 and event.pos[1] <620 and event.pos[1] >500:
                    arret = 1
                    pygame.mixer.music.stop()
                    continuer = 0
                    continuer1 = 1
                    commencer=0
                    recommencer = 0
                elif event.pos[0]<170 and event.pos[0] >50 and event.pos[1] <620 and event.pos[1] >500:
                    print("coucou")
                    arret = 1
                    pygame.mixer.music.stop()
                    continuer = 0
                    continuer1 = 1
                    commencer=0
                    recommencer = 1
            elif event.type == QUIT:
                    arret = 1
                    continuer = 0
                    continuer1 = 1
                    recommencer = 0
                    commencer = 1
                    jeu=0

# main prog
def recharge():
    global parties
    fenetre.blit(accueil,(0,0))
    fenetre.blit(msg,(10,10))
    fenetre.blit(msg2,(450,225))
    fenetre.blit(msg3,(50, 250))
    fenetre.blit(msg4,(100, 400))
    fenetre.blit(msg5,(100, 450))
    fenetre.blit(msg2_2,(450, 275))
    fenetre.blit(msg2_3,(450, 312))
    fenetre.blit(jouer,(75, 550))
    fenetre.blit(quitter,(200, 550))
    place=350
    for i in range(len(liste)):
        msg6=myfont2.render(liste[i], 1, (0,255,0)) # render text, cad le transformer en image
        fenetre.blit(msg6, (450, place))
        place=place+50
    pygame.display.flip()
arret = 0
recommencer = 1
parties=0
record_absolu=0
commencer=0
pseudo_choisi=""
saisie=""
pygame.mixer.music.load(os.path.join("Snake_Files\sound", 'accueil_tron.mp3'))
pygame.mixer.music.play(-1)
jeu=1
while jeu == 1:
    pygame.mixer.music.load(os.path.join("Snake_Files\sound", 'accueil_tron.mp3'))
    pygame.mixer.music.play(-1)
    while commencer == 0:
        parties=0
        msg = myfont1.render("SNAKE", 1, (0,255,0))
        msg2 = myfont2.render("Cliquez sur votre pseudo :", 1, (0,255,0))
        msg2_2 = myfont2.render("Nouveau ... éviter \ /  : ? '' < > |", 1, (0,255,0))
        msg2_3 = myfont2.render("et pour valider : ENTREE", 1, (0,255,0))
        msg3 = myfont.render("Bienvenue !", 1, (0,255,0))
        msg4 = myfont2.render("Votre pseudo : ", 1, (0,255,0)) # render text, cad le transformer en image
        msg5 = myfont.render(pseudo_choisi, 1, (0,255,0)) # render text, cad le transformer en image
        liste=os.listdir("Snake_Files\scores")
        recharge()
        for event in pygame.event.get():# pour chaque événement de la bibliothèque pygame détecté
            if event.type == MOUSEBUTTONDOWN:
                for j in range(len(liste)):
                    if (event.pos[0]<800 and event.pos[0] >450 and event.pos[1] <(350+50*(j+1)) and event.pos[1] >(350+50*j) ):
                        pseudo_choisi = liste[j]
                if (event.pos[0]<195 and event.pos[0] >75 and event.pos[1] <670  and event.pos[1] >550):
                    print("coucou")
                    if pseudo_choisi!="":
                        commencer = 1
                elif event.pos[0]<320 and event.pos[0] >200 and event.pos[1] <670 and event.pos[1] >550:
                    if pseudo_choisi!="":
                        ok=0
                        while ok==0:
                            msg6 = myfont2.render("Suppr "+ pseudo_choisi +' ? (O/N)', 1, (0,255,0)) # render text, cad le transformer en image
                            fenetre.blit(msg6,(10,330))
                            pygame.display.flip()
                            for event in pygame.event.get():
                                if event.type == KEYDOWN :
                                    if event.key == K_o:
                                        os.remove("Snake_Files\scores\\" + pseudo_choisi)
                                        pseudo_choisi=""
                                        ok=1
                                    elif event.key == K_n:
                                        ok=1
                elif event.pos[0]<800 and event.pos[0] >450 and event.pos[1] <350 and event.pos[1] >275:
                    ok1=0
                    pseudo_choisi=""
                    msg5 = myfont.render(pseudo_choisi, 1, (0,255,0)) # render text, cad le transformer en image
                    recharge()
                    saisie = "Tapez pseudo ..."
                    saisie_surface = font.render(saisie, True, (0,255,0))
                    fenetre.blit(saisie_surface, (10,450))
                    pygame.display.flip()
                    while ok1==0:
                            #new_pseudo=input("Renseignez votre pseudo ...")
                        for event in pygame.event.get():
                            if event.type == KEYDOWN :
                                if saisie == "Tapez pseudo ...":
                                        saisie=""
                                        recharge()
                                if event.key == K_RETURN  or event.key == K_KP_ENTER :
                                    if saisie == "" or saisie == "Tapez pseudo ..." :
                                        saisie = "Tapez pseudo ..."
                                        recharge()
                                    else:
                                        ok1 = 1
                                elif event.key == K_BACKSPACE:
                                    recharge()
                                    saisie = saisie[:len(saisie)-1]
                                    saisie_surface = font.render(saisie, True, (0,255,0))
                                    fenetre.blit(saisie_surface, (10,450))
                                    pygame.display.flip()
                                else:
                                    if saisie == "Tapez pseudo ...":
                                        saisie=""
                                        recharge()
                                    # \/:*?"<>|
                                    # \/:?"<>|
                                    else:
                                        sa = event.unicode
                                        saisie = saisie + event.unicode
                                        print(sa)
                                        saisie_surface = font.render(saisie, True, (0,255,0))
                                        fenetre.blit(saisie_surface, (10,450))
                                        pygame.display.flip()

                    new_pseudo=saisie
                    e = open(os.path.join("Snake_Files\scores", new_pseudo), "w")
                    e.write("0")
                    e.close()
                    pseudo_choisi=new_pseudo

            elif event.type == QUIT:
                commencer=1
                jeu=1
                arret=1
    if arret == 1:
        break
    recommencer=1
    while recommencer == 1 :
            pygame.mixer.music.load(os.path.join("Snake_Files\sound", 'tron.mp3'))
            pygame.mixer.music.play(-1)
            serpent=[[6,0],[6,1],[6,2]]   # le serpent est modélisé par une liste de 3 couples de coordonnées autrement dit une matrice 3 lignes par 2 colonnes
            tete_pomme=0                                                                    # quand la tête est sur la pomme
            dir=""                                                                          # direction auto
            points=0                                                                        # nombre de points
            parties=parties + 1
            coord_pomme = randint(0,15)*50                                                  #position aléatoire
            coord2_pomme = randint(0,13)*50
            continuer=1
            while continuer==1: # boucle infinie , qui s arrêtera si la variable continuer prend une valeur autre que 1
                affichage_damier(carre_rose,carre_rouge)
                maj = myfont2.render(pseudo_choisi + " : Partie n° " + str(parties) + "   Points : " + str(points) , 1, (0,0,0))
                fenetre.blit(maj,(0,0))
                for i in range(len(serpent)-1): # partie anti-collision
                    if serpent[len(serpent)-1][0]==serpent[i][0] and serpent[len(serpent)-1][1]==serpent[i][1]:
                        perdu()
                if serpent[len(serpent)-1][0] *50  == coord2_pomme:                         # partie comptage des points
                    if serpent[len(serpent)-1][1] *50 == coord_pomme:
                        points=points + 1
                        son = pygame.mixer.Sound(os.path.join("Snake_Files\sound", 'point.wav'))
                        son.play()
                        tete_pomme=1
                pomme_ok=0                                                                  # partie place aléatoire de la pomme en faissant attention de ne pas être sur un bout du corps
                if tete_pomme==1:
                    while pomme_ok != 1:
                        pomme_ok=0
                        coord_pomme = randint(0,15)*50
                        coord2_pomme = randint(0,13)*50
                        for i in range(len(serpent)):
                            if coord_pomme/50==serpent[i][0] and coord2_pomme/50==serpent[i][1]:
                                pomme_ok=2
                        if pomme_ok==0:
                            pomme_ok=1
                fenetre.blit(pomme,(coord_pomme,coord2_pomme))
                deplacement_et_affichage_bon_sens()
                tete_pomme=0
                time.sleep(0.15)        # pause de 0.15 seconde
                if arret!=1:
                    pygame.display.flip()  # actualiser l'affichage de la fenêtre graphique
                arret=0

                for event in pygame.event.get():# pour chaque événement de la bibliothèque pygame détecté
                    if event.type == QUIT:      # si clic sur la croix rouge dans le coin supérieur droit de la fenêtre graphique
                        continuer = 0           # arrêter la boucle infinie while
                        recommencer = 0
                        jeu=0

                    if event.type == KEYDOWN :  # si l'utilisateur appuie sur une touche alors
                        if event.key==K_RIGHT:  # si la touche est la fleche dirigée vers la droite
                            if dir!="gauche" and dir!="droite":
                                son = pygame.mixer.Sound(os.path.join("Snake_Files\sound", 'droite.wav'))
                                son.play()
                                dir="droite"

                        if event.key==K_LEFT:   # si la touche est la fleche dirigée vers la gauche
                            if dir!="droite"and dir!="" and dir!="gauche":
                                son = pygame.mixer.Sound(os.path.join("Snake_Files\sound", 'gauche.wav'))
                                son.play()
                                dir="gauche"

                        if event.key==K_UP:   # si la touche est la fleche dirigée vers lE HAUT
                            if dir!="bas" and dir!="haut":
                                son = pygame.mixer.Sound(os.path.join("Snake_Files\sound", 'haut.wav'))
                                son.play()
                                dir="haut"

                        if event.key==K_DOWN:   # si la touche est la fleche dirigée vers lE BAS
                            if dir!="haut"and dir!="bas":
                                son = pygame.mixer.Sound(os.path.join("Snake_Files\sound", 'bas.wav'))
                                son.play()
                                dir="bas"
sys.exit
pygame.quit()