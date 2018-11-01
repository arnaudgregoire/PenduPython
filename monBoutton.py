import tkinter as tk

class MonBouton(tk.Button):
    def __init__(self, frame, fenetre, texte):
        self.__texte  = texte
        self.__master = frame
        self.__fenetre = fenetre
        tk.Button.__init__(self, master = self.__master, text = self.__texte, command = self.cliquer)
        
    def cliquer(self):
        self.config(state="disabled")
        self.__fenetre.traitement(self.__texte)
