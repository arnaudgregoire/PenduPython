import tkinter as tk
from tkinter import simpledialog
from monBoutton import MonBouton
from random import randint
from fenSecondaire import FenSecondaire

class FenPrincipale(tk.Tk):
        
    """
    La classe de la fenêtre principale
    """
        
    def __init__(self):
        self.fenetre     = tk.Tk.__init__(self)
        self.bottomFrame = tk.Frame(self)
        self.topFrame    = tk.Frame(self)
        self.canvas      = tk.Canvas(self)
        self.canvas.pack(side="top")
        self.username = ""
        self.pseudo = tk.Label(self, text="Pseudo : ")
        self.pseudo.pack()
        self.lmot        = tk.Label(self)
        self.lmot.pack()
        self.mot         = ""
        self.motAffiche  = ""
        self.nbManques   = 0
        self.mots        = []
        self.title('jeu du pendu')
        self.initTopFrame()
        self.lettres = self.getAlphabet()
        self.boutons = []
        self.initBoutons()
        self.displayBoutons()
        self.chargeMots()
        self.nouveauMot()
        self.nouvelle_partie()

    def traitement(self, lettre):
        """
        Méthode appelée à chaque fois que l'utilisateur tape sur une lettre
        """
        find = False
        for i in range(len(self.mot)):
            if self.mot[i] == lettre:
                self.motAffiche = self.motAffiche[:i] + lettre + self.motAffiche[i+1:]
                find = True
                self.lmot.config(text=self.motAffiche)

        if not find:
            self.nbManques += 1
        
        if self.motAffiche == self.mot:
            self.finPartie(True)

        if self.nbManques >= 7:
            self.finPartie(False)   

        self.displayPicture(self.nbManques +1)

    def finPartie(self, result):
        """
        Méthode appelé à la fin de la partie
        """

        for i in range(26):
            self.boutons[i].config(state="disabled")

        if result:
            self.lmot.config(text="Félicitations")

        else:
            self.lmot.config(text=self.mot)
        
        if self.username != "":
            self.saveResult(result)
        

    def saveResult(self, result):
        with open('bdd.txt','a') as f:
            f.write(self.username + "," +self.mot + "," + str(result) +"\n")

    def statistique(self):
        f = FenSecondaire(self.username)

    def initTopFrame(self):
        """
        initialise les boutons nouvelle partie et Quitter
        """
        self.bouton_nouvelle_partie = tk.Button(self.topFrame,
            text="Nouvelle Partie",
            command=self.nouvelle_partie)

        self.bouton_statistiques = tk.Button(self.topFrame,
            text="Statistiques",
            command=self.statistique)

        self.bouton_quitter = tk.Button(self.topFrame,
            text="Quitter",
            command=self.quit)

        self.bouton_nouvelle_partie.pack(side="left")
        self.bouton_quitter.pack(side="right")
        self.bouton_statistiques.pack()
        self.topFrame.pack(side="top")


    def nouvelle_partie(self):
        """
        Méthode qui initialise une nouvelle partie
        """
        self.displayPicture(1)
        self.nbManques = 0
        self.motAffiche = ""
        self.nouveauMot()

        prompt = simpledialog.askstring("Fenetre pour mettre ton pseudo :O","ton pseudo ?")
        
        if prompt is not None:
            self.username = prompt
            self.pseudo.config(text ="Pseudo : " + self.username)
        
        if self.username == "":
            self.bouton_statistiques.config(state="disabled")

        else:
            self.bouton_statistiques.config(state="normal")

        for k in range(len(self.mot)):
            self.motAffiche += "*"

        self.lmot.config(text=self.motAffiche)

        for k in range(26):
            self.boutons[k].config(state="normal")

    def getAlphabet(self):
        """
        Renvoie une liste contenant les lettres de l'alphabet
        """
        lettres = []
        for i in range(26):
            lettres.append(chr(ord('A')+i))    
        return lettres
    
    def initBoutons(self):
        """
        Remplit la liste self.boutons d'objets MonBouton
        """
        for i in range(26):
            bouton = MonBouton(self.bottomFrame, self, self.lettres[i])
            self.boutons += [bouton]

    def displayBoutons(self):
        """
        Affiche les boutons dans l'objet self.frame
        """
        c = 0
        for i in range(4):
            for j in range(7):
                if c< 26:
                    self.boutons[c].grid(row=i,column=j)
                    c+=1
        self.bottomFrame.pack(side="bottom")

    def chargeMots(self):
        """
        Charge le contenu du fichier mots.txt dans une liste
        """
        with open('mots.txt','r') as f:
            self.mots = f.read().splitlines()

    def nouveauMot(self):
        """
        Choisis un nouveau mot aléatoirement dans la liste de mots préchargés
        """
        self.mot = self.mots[randint(0,len(self.mots)-1)]

    def displayPicture(self, number):
        """
        Affiche une image du pendu en fonction du nombre de mauvaises réponses
        """
        nomImage = 'img/pendu'+str(number)+'.gif'
        photo = tk.PhotoImage(master=self, file=nomImage)
        self.canvas.image = photo
        self.canvas.create_image(0,0, anchor="nw", image=photo)
        self.canvas.config(height=photo.height(),width=photo.width())
