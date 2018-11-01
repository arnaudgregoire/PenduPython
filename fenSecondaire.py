import tkinter as tk
import numpy as np
class FenSecondaire(tk.Tk):
        
    """
    La classe de la fenêtre secondaire
    """
        
    def __init__(self, username):
        self.__fenetre = tk.Tk.__init__(self)
        self.__username = username
        self.__title= "Statistiques"
        self.__history_values = []
        self.__history_title = tk.Label(self, text="Historique :")
        self.__history_title.pack()
        self.__history = tk.Label(self, text="")
        self.__history.pack()
        self.__statistique_title = tk.Label(self, text = "Statistiques :")
        self.__statistiques = tk.Label(self, text="")
        self.__statistiques.pack()
        self.__clearHistoryButton =tk.Button(self, text = "Réinitialiser l'historique", command=self.clearHistory)
        self.__clearHistoryButton.pack()
        self.__history.config(text = str(self.getHistory()))
        self.__statistiques.config(text=self.getStatistiques())
        
    def getHistory(self):
        self.__bdd = []
        self.__bdd = np.loadtxt("bdd.txt",
            dtype=str,
            delimiter=",")

        for i in range(self.__bdd.shape[0]):
            if self.__username == self.__bdd[i,0] :
                self.__history_values += [list(self.__bdd[i])]

        return self.__history_values

    def getStatistiques(self):
        bon = 0
        mauvais = 0
        if self.__history_values != []:
            for i in range(len(self.__history_values)):
                if self.__history_values[i][2] == "True":
                    bon += 1
                else:
                    mauvais += 1
            print(str(bon + mauvais))        
            return "Nombre de parties jouées : " + str(bon + mauvais) + "\n " + "Pourcentbonage de victoire : " + str(bon * 100 /(bon + mauvais)) + " %"
        else:
            return "Aucune partie jouées"
    
    def clearHistory(self):
        with open('bdd.txt','w') as f:
            for i in range(self.__bdd.shape[0]):
                if(self.__bdd[i,0] != self.__username):
                    f.write(self.__bdd[i,0] + "," + self.__bdd[i,1] + "," + self.__bdd[i,2] +"\n")       

        