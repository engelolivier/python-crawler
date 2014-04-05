#-*- coding: utf-8 -*-

# On importe Tkinter
import os
import sys
from Tkinter import *

def we_are_frozen():
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
    
    def __init__(self, window, **kwargs):
        Frame.__init__(self, window, width=768, height=576, **kwargs)
        self.pack(fill=BOTH)
        self.nb_clic = 0
        
        
        # Création de nos widgets
        self.message = Label(self, text="Veuillez indiquer la racine du site")
        self.message.pack()

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
        
        self.nb_clic += 1
        gen = CrawlerGraph(self.domain.get()).crawl(self.url.get())  


        for i in range(9999):
          
            try:
                data = gen.next() + "\n"
                print i
                self.loading.insert(INSERT, data)
                self.loading.see(END)
                self.loading.update_idletasks()

            except StopIteration:
                print "Erreur fin itération"
        

class CrawlerGraph(Crawler):
    """
    Crawler pour version graphique
    """

    def print_info(self, *args, **kwargs):

        html = kwargs["html"]
        url = kwargs["url"]
        
        try:
            print url

        except:
            print "Erreur info %s"

window = Tk()
window.title="Crawler"
interface = Interface(window)

interface.mainloop()
interface.destroy()