#-*- coding: utf-8 -*-

import urllib2
from BeautifulSoup import BeautifulSoup
from lxml import etree
import time
 
class Crawler:
 
    urls = []
    urls_done = [] 
    count = 0
 
    def __init__(self, domain):
        self.domain = domain
        self.count = 0
 
 
    def getUrls(self):
        return self.urls
 
    def crawl(self, url):
          
        # On limite le script à 10000 itérations
        if self.count > 9999:
            return None
      
        # Si le domaine est différent, on stoppe le script
        if not str(url).startswith(self.domain):
            return None
      
        # On récupère/parse le code HTML
        try:
            t1 = time.time()
            html = urllib2.urlopen(url)
            if str(html.info()).find("text/html") == -1:
                return None
            t2 = time.time() - t1
            # On affiche des informations concernant le déroulement du script:
            # compteur ; code HTTPRequest ; temps exécution ; url
            print "%s;%s;%.1f;%s;" % (str(self.count).ljust(3),str(html.getcode()).ljust(4), t2, url.split(self.domain)[1], )
        except:
            print "Erreur %s" % (url,)
        else:
            soup = BeautifulSoup(html)
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
                        self.count+=1
                        self.urls_done.append(href)
 
                        # Récursif
                        self.crawl(href)
  
# On construit une liste d'url
crawler = Crawler("http://xxx")
# Point de départ
crawler.crawl("http://xxx/shop/")
 
 
# On construit le XML
urlset = etree.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" )
for u in crawler.getUrls():
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
  
# On génère le fichier sitemap.xml
f = open('sitemap.xml', 'w+')
f.write(code)