#!/usr/bin/python

import requests
import re
import translators.server as ts
import sys
import time
from bs4 import BeautifulSoup, SoupStrainer

def main():
  site_name = 'https://www.classcentral.com'
  #agent = {"User-Agent":"Mozilla/5.0"}
  agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}


  lab = ['p','h1','h2','h3','h4','a','span','title','strong','i','div']
  #lab = ['p','h1','h2','h3','h4','a','span','title','strong','i']
  
  content = requests.get(site_name, headers=agent).content
  
  links = []
  for link in BeautifulSoup(content, parse_only=SoupStrainer('a'), features='lxml'):
    if hasattr(link, "href"):
      links.append(link['href'])
  
  links = list(set([site_name+l for l in links if not re.search('http', l)]))
  links = links[links.index(site_name+'/')]

  #for link in links:
  #  print(link)
  
  for link in links:
    # test_link = links[links.index(site_name+'/')]
    # print(test_link)

    text = requests.get(link, headers=agent).text
    par = BeautifulSoup(text, 'html.parser')
    
    # html = '''
    # <html>
    # <head>
    # <title>That is the display section.</title>
    # </head>
    # <body>
    # <p>So got the stairs. <span>Hi dog</span> Crazy</p>
    # <p></p>
    # <p>Yes, said Arthur, yes I did. It was displayed at the bottom of the locked filing cabinet stuck in a dormant toilet with a sign on the door saying 'Be wary of the leopard'</p></body>
    # </html>
    # '''
    #par = BeautifulSoup(html, 'html.parser')

    for i in par.findAll(lab):
      if i.string is not None and len(str(chi.string).strip()) > 0:
        sys.stdout.write('\x1b[2K')
        print("\rTranslating: {0}".format(i.string), end="")
        i.string.replace_with(ts.google(i.string, from_language='en', to_language='es'))
      else:
        for chi in i.children:
          if chi.string is not None and len(str(chi.string).strip()) > 0:
            sys.stdout.write('\x1b[2K')
            print("\rTranslating: {0}".format(chi.string), end="")
            time.sleep(0.5)
            ns = ts.google(chi.string, from_language='en', to_language='es')
            chi.string.replace_with(ns)

    res = link.replace(site_name, "home_")
    res = "_".join(res.split('/'))
    par = str(par)
    f = open('./paginas/'+res, 'w+')
    f.write(par)
    f.close()

if __name__ == '__main__':
  main()
