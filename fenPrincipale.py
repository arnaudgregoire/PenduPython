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
        self.__fenetre     = tk.Tk.__init__(self)
        self.__bottomFrame = tk.Frame(self)
        self.__topFrame    = tk.Frame(self)
        self.__canvas      = tk.Canvas(self)
        self.__canvas.pack(side="top")
        self.__username = ""
        self.__pseudo = tk.Label(self, text="Pseudo : ")
        self.__pseudo.pack()
        self.__lmot        = tk.Label(self)
        self.__lmot.pack()
        self.__mot         = ""
        self.__motAffiche  = ""
        self.__nbManques   = 0
        self.__mots        = []
        self.title('jeu du pendu')
        self.initTopFrame()
        self.__lettres = self.getAlphabet()
        self.__boutons = []
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
        for i in range(len(self.__mot)):
            if self.__mot[i] == lettre:
                self.__motAffiche = self.__motAffiche[:i] + lettre + self.__motAffiche[i+1:]
                find = True
                self.__lmot.config(text=self.__motAffiche)

        if not find:
            self.__nbManques += 1
        
        if self.__motAffiche == self.__mot:
            self.__finPartie(True)

        if self.__nbManques >= 7:
            self.finPartie(False)   

        self.displayPicture(self.__nbManques +1)

    def finPartie(self, result):
        """
        Méthode appelé à la fin de la partie
        """

        for i in range(26):
            self.__boutons[i].config(state="disabled")

        if result:
            self.__lmot.config(text="Félicitations")

        else:
            self.__lmot.config(text=self.__mot)
        
        if self.__username != "":
            self.saveResult(result)
        

    def saveResult(self, result):
        with open('bdd.txt','a') as f:
            f.write(self.__username + "," +self.__mot + "," + str(result) +"\n")

    def statistique(self):
        f = FenSecondaire(self.__username)

    def initTopFrame(self):
        """
        initialise les boutons nouvelle partie et Quitter
        """
        self.__bouton_nouvelle_partie = tk.Button(self.__topFrame,
            text="Nouvelle Partie",
            command=self.nouvelle_partie)

        self.__bouton_statistiques = tk.Button(self.__topFrame,
            text="Statistiques",
            command=self.statistique)

        self.__bouton_quitter = tk.Button(self.__topFrame,
            text="Quitter",
            command=self.quit)

        self.__bouton_nouvelle_partie.pack(side="left")
        self.__bouton_quitter.pack(side="right")
        self.__bouton_statistiques.pack()
        self.__topFrame.pack(side="top")


    def nouvelle_partie(self):
        """
        Méthode qui initialise une nouvelle partie
        """
        self.displayPicture(1)
        self.__nbManques = 0
        self.__motAffiche = ""
        self.nouveauMot()

        prompt = simpledialog.askstring("Fenetre pour mettre ton pseudo :O","ton pseudo ?")
        
        if prompt is not None:
            self.__username = prompt
            self.__pseudo.config(text ="Pseudo : " + self.__username)
        
        if self.__username == "":
            self.__bouton_statistiques.config(state="disabled")

        else:
            self.__bouton_statistiques.config(state="normal")

        for k in range(len(self.__mot)):
            self.__motAffiche += "*"

        self.__lmot.config(text=self.__motAffiche)

        for k in range(26):
            self.__boutons[k].config(state="normal")

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
            bouton = MonBouton(self.__bottomFrame, self, self.__lettres[i])
            self.__boutons += [bouton]

    def displayBoutons(self):
        """
        Affiche les boutons dans l'objet self.frame
        """
        c = 0
        for i in range(4):
            for j in range(7):
                if c< 26:
                    self.__boutons[c].grid(row=i,column=j)
                    c+=1
        self.__bottomFrame.pack(side="bottom")

    def chargeMots(self):
        """
        Charge le contenu du fichier mots.txt dans une liste
        """
        with open('mots.txt','r') as f:
            self.__mots = f.read().splitlines()

    def nouveauMot(self):
        """
        Choisis un nouveau mot aléatoirement dans la liste de mots préchargés
        """
        self.__mot = self.__mots[randint(0,len(self.__mots)-1)]

    def displayPicture(self, number):
        """
        Affiche une image du pendu en fonction du nombre de mauvaises réponses
        """
        nomImage = 'img/pendu'+str(number)+'.gif'
        photo = tk.PhotoImage(master=self, file=nomImage)
        self.__canvas.image = photo
        self.__canvas.create_image(0,0, anchor="nw", image=photo)
        self.__canvas.config(height=photo.height(),width=photo.width())
