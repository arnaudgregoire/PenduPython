import tkinter as tk

class MonBouton(tk.Button):
    def __init__(self, frame, fenetre, texte):
        self.texte  = texte
        self.master = frame
        self.fenetre = fenetre
        tk.Button.__init__(self, master = self.master, text = self.texte, command = self.cliquer)
        
    def cliquer(self):
        self.config(state="disabled")
        self.fenetre.traitement(self.texte)
