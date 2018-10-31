import tkinter as tk
import numpy as np
class FenSecondaire(tk.Tk):
        
    """
    La classe de la fenêtre secondaire
    """
        
    def __init__(self, username):
        self.fenetre = tk.Tk.__init__(self)
        self.username = username
        self.title= "Statistiques"
        self.history_values = []
        self.history_title = tk.Label(self, text="Historique :")
        self.history_title.pack()
        self.history = tk.Label(self, text="")
        self.history.pack()
        self.statistique_title = tk.Label(self, text = "Statistiques :")
        self.statistiques = tk.Label(self, text="")
        self.statistiques.pack()
        self.clearHistoryButton =tk.Button(self, text = "Réinitialiser l'historique", command=self.clearHistory)
        self.clearHistoryButton.pack()
        self.history.config(text = str(self.getHistory()))
        self.statistiques.config(text=self.getStatistiques())
        
    def getHistory(self):
        self.bdd = []
        self.bdd = np.loadtxt("bdd.txt",
            dtype=str,
            delimiter=",")

        for i in range(self.bdd.shape[0]):
            if self.username == self.bdd[i,0] :
                self.history_values += [list(self.bdd[i])]

        return self.history_values

    def getStatistiques(self):
        bon = 0
        mauvais = 0
        if self.history_values != []:
            for i in range(len(self.history_values)):
                if self.history_values[i][2] == "True":
                    bon += 1
                else:
                    mauvais += 1
            print(str(bon + mauvais))        
            return "Nombre de parties jouées : " + str(bon + mauvais) + "\n " + "Pourcentbonage de victoire : " + str(bon * 100 /(bon + mauvais)) + " %"
        else:
            return "Aucune partie jouées"
    
    def clearHistory(self):
        with open('bdd.txt','w') as f:
            for i in range(self.bdd.shape[0]):
                if(self.bdd[i,0] != self.username):
                    f.write(self.bdd[i,0] + "," + self.bdd[i,1] + "," + self.bdd[i,2] +"\n")       

        