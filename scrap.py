#!/usr/bin/python

import requests
import re
import translators.server as ts
import sys
import time
import os
from bs4 import BeautifulSoup, SoupStrainer

def main():
  site_name = 'https://www.classcentral.com'
  #agent = {"User-Agent":"Mozilla/5.0"}
  agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}


  #lab = ['p','h1','h2','h3','h4','a','span','title','strong','i','div']
  lab = ['p','h1','h2','h3','h4','a','span','title','strong','i']
  
  content = requests.get(site_name, headers=agent).content
  
  links = []
  for link in BeautifulSoup(content, parse_only=SoupStrainer('a'), features='lxml'):
    if hasattr(link, "href"):
      links.append(link['href'])
  
  links = list(set([site_name+l for l in links if not re.search('http', l)]))
  links = sorted(links, key=len)
  #ind = links.index(site_name+'/')
  #links = [links[ind]] + links[ind+21:ind+50]
  links = links[121:]
  
  #for link in links:
  #  print(link)
  
  for link in links:
    print("\nProcessing page: {0} ({1} of {2})".format(link, links.index(link)+1, len(links)))

    text = requests.get(link, headers=agent).text
    par = BeautifulSoup(text, 'html.parser')
    
    for i in par.findAll(lab):
      if i.string is not None and len(str(i.string).strip()) > 0 and i.string != '\n':
        sys.stdout.write('\x1b[2K')
        print("\r\tTranslating: {0}".format(i.string), end="")
        i.string.replace_with(ts.google(i.string, from_language='en', to_language='es'))
      else:
        for chi in i.children:
          if chi.string is not None and len(str(chi.string).strip()) > 0 and chi.string != '\n':
            sys.stdout.write('\x1b[2K')
            print("\r\tTranslating: {0}".format(chi.string), end="")
            ns = ts.google(chi.string, from_language='en', to_language='hi')
            chi.string.replace_with(ns)

    if link == site_name+'/':
      res = './index.html'
    else:
      res = link.replace(site_name, ".")
      res = res+'/'+res.split('/')[-1]+'.html'
   
    par = str(par)

    dir = os.path.dirname(res)
    if not os.path.exists(dir):
        os.makedirs(dir)
    f = open(res, 'w+')
    f.write(par)
    f.close()

if __name__ == '__main__':
  main()
