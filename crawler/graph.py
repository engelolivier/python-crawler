#-*- coding: utf-8 -*-
"""Premier exemple avec Tkinter.

On crée une fenêtre simple qui souhaite la bienvenue à l'utilisateur.

"""

# On importe Tkinter
import os
import sys
from Tkinter import *

def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")

def module_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, encoding))
    return os.path.dirname(unicode(__file__, encoding))

#sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, module_path)

from crawler import Crawler




class Interface(Frame):
    
    """Notre fenêtre principale.
    Tous les widgets sont stockés comme attributs de cette fenêtre."""
    
    def __init__(self, window, **kwargs):
        Frame.__init__(self, window, width=768, height=576, **kwargs)
        self.pack(fill=BOTH)
        self.nb_clic = 0
        
        
        # Création de nos widgets
        self.message = Label(self, text="Veuillez indiquer la racine du site")
        self.message.pack()



        """
        # Dans Fenetre nous allons créer un objet type Canvas qui se nomme zone_dessin
        # Nous donnons des valeurs aux propriétés "width", "height", "bg", "bd", "relief"
        zone_dessin = Canvas(window,width=500,height=500,
                                bg='yellow',bd=8,relief="ridge")
        zone_dessin.pack() #Affiche le Canvas
         
        #Nous allons maintenant utiliser quelques méthodes du widget "zone_dessin"
        zone_dessin.create_line(0,0,500,500,fill='red',width=4) # Dessine une ligne
        zone_dessin.create_line(0,500,500,0,fill='red',width=4) # Dessine une ligne
        zone_dessin.create_rectangle(150,150,350,350) # Dessine un rectangle
        zone_dessin.create_oval(150,150,350,350,fill='white',width=4) # Dessine un cercle
        """

        v = StringVar()
        v.set("http://localhost:8000")
        self.domain = Entry(self, textvariable=v, width=30)
        self.domain.pack()


        # Création de nos widgets
        self.message2 = Label(self, text="Et le point de départ du crawler")
        self.message2.pack()

        v = StringVar()
        v.set("http://localhost:8000")
        self.url = Entry(self, textvariable=v, width=30)
        self.url.pack()

        self.loading = Text(self)
        self.loading.pack()

        self.bouton_quitter = Button(self, text="Quitter", command=self.quit)
        self.bouton_quitter.pack(side="left")
        
        self.bouton_cliquer = Button(self, text="Valider", fg="blue", command=self.valider)
        self.bouton_cliquer.pack(side="right")

        # self.valider()
    
    def valider(self):
        """Il y a eu un clic sur le bouton.
        On change la valeur du label message."""
        
        self.nb_clic += 1
        # self.message["text"] = "{}.".format(self.url.get())

        #self.loading.insert(INSERT, "Chargement...")

        gen = CrawlerGraph(self.domain.get()).crawl(self.url.get())  
        # print dir(crawler)
        #gen = crawler.crawl("http://localhost:8000")    

        for i in range(9999):
          
            try:
                data = gen.next() + "\n"
                print i
                self.loading.insert(INSERT, data)
                self.loading.see(END)
                self.loading.update_idletasks()
                # self.loading.pack()
                # self.loading.see(END)
            except StopIteration:
                print "Erreur fin itération"
        


        #crawler.crawl( self.url.get() )



class CrawlerGraph(Crawler):
    """
    Crawler pour version graphique
    """

    def print_info(self, *args, **kwargs):

        html = kwargs["html"]
        url = kwargs["url"]
        
        try:
            print url
            #print url
            #self.content=url

        except:
            print "Erreur info %s"

window = Tk()
window.title="Crawler"
interface = Interface(window)

interface.mainloop()
interface.destroy()