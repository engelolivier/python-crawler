#-*- coding: utf-8 -*-

import urllib2
from BeautifulSoup import BeautifulSoup
from lxml import etree
import time
 
class Crawler:
 

 
    def __init__(self, domain):
        self.domain = domain
        self.count = 0
        self.urls = []
        self.urls_done = [] 

 
    def getUrls(self):
        """
        Retourne les URLS trouvé par le crawler
        """
        return self.urls

    def print_info(self, *args, **kwargs):
        """
        Affiche les informations lors de l'execution du script
        """
        pass

    def run(self, url):

        self.gen = self.crawl(url)      
        for i in range(9999):
            try:
                self.gen.next()
            except:
                pass

    def crawl(self, urls):
        """
        Parcours les pages du site en suivant les liens
        """  
        if not type(urls) is list:
            urls = [urls]
              
        for url in urls:
            # Si le domaine est différent, on stoppe le script
            if str(url).startswith(self.domain):
                
          
                # On récupère/parse le code HTML
                try:
                    t1 = time.time()
                    html = urllib2.urlopen(url)
                    if str(html.info()).find("text/html") == -1:
                        raise
                    t2 = time.time() - t1
    
                    # On écrit les informations que l'on souhaite
                    data = { "html" : html, "url" : url, "time" : t2  }
                    self.count+=1
                    self.print_info(**data)
                    #print data
                    
                except:
                    print "Erreur %s" % (url,)
                    
            
                else:
                    soup = BeautifulSoup(html)
                    new_urls = []
                    for link in soup.findAll('a'):
                        href = link.get('href')
                        if href and href <> "#" and not href in self.urls:
                            
                            # On ajoute http si manquant
                            if href.startswith("/"):
                                href = self.domain + href
                            elif not href.startswith("http"):
                                try:
                                    string_to_delete = url.split("/")[-1:][0]
                                    href = url.split(string_to_delete)[0] + href
                                except:
                                    pass
                            
                            # Récursif si l'adresse n'a pas encore été traité
                            if not href in self.urls_done:
                            
                                # On ajoute l'adresse à la liste
                                self.urls.append( href )
                                
                                self.urls_done.append(href)
                                new_urls.append(href)
                                
                    yield url
                    for u in self.crawl(new_urls):
                        yield u



class CrawlerSiteMap(Crawler):
    """
    Construit le siteMap du site
    """

    def print_info(self, *args, **kwargs):

        html = kwargs["html"]
        url = kwargs["url"]
        time = kwargs["time"]

        try:
            print "%s;%s;%.1f;%s;" % (str(self.count).ljust(3),str(html.getcode()).ljust(4), time, url.split(self.domain)[1], )  

        except:
            print "Erreur info %s"


    def run(self, url):

        Crawler.run(self, url)

        """
        Construction du sitemap.xml
        """
        print "Construction du XML..."
        urlset = etree.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" )
        for u in self.getUrls():
            url = etree.Element('url')
            urlset.append(url)
            # loc
            loc = etree.Element('loc')
            loc.text = str(u)
            url.append(loc)
            # changefreq
            changefreq = etree.Element('changefreq')
            changefreq.text = 'hourly'
            url.append(changefreq)
          
        code = etree.tostring(urlset, pretty_print=True)
          
        # On génère le fichier sitemap.xml dans le meme dossier
        try:
            f = open('sitemap.xml', 'w+')
            f.write(code)
        except:
            print "Erreur lors de la création du sitemap.xml"
        else:
            print "Sitemap.xml crée avec succès!"


class CrawlerInfo(Crawler):
    """
    Affiche les informations de base de chaque page
    """

    def print_info(self, *args, **kwargs):

        html = kwargs["html"]
        url = kwargs["url"]
        time = kwargs["time"]

        try:
            print "%s;%s;%.1f;%s;" % (str(self.count).ljust(3),str(html.getcode()).ljust(4), time, url.split(self.domain)[1], )  

        except:
            print "Erreur info %s"


class Crawler404(Crawler):
    """
    Affiche uniquement les codes de retour différent de 200
    """
    def print_info(self, *args, **kwargs):

        html = kwargs["html"]
        url = kwargs["url"]
        code = html.getcode()
        
        try:
            if str(code) <> "200":
                print "%s;%s;%s;" % (str(self.count).ljust(3),str(html.getcode()), url )  

        except:
            print "Erreur info %s"