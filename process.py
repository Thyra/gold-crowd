import requests
import lxml
import os
from bs4 import BeautifulSoup
# Download GNormPlus results for each PMID and extract abstract
with open('data/pmid_list.txt') as pmid_list:
  for pmid in pmid_list:
    r = requests.get('https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/Gene/'+pmid.rstrip()+'/BioC/')
    soup = BeautifulSoup(r.text, 'lxml-xml')
    # We don't need to do anything with abstracts that don't contain gnormplus annotations --> no genes, no use
    if len(soup.find_all('annotation')) == 0:
      continue
    with open('data/gnormplus-output/'+pmid.rstrip()+'.xml', 'w') as gnormplus_outfile:
      gnormplus_outfile.write(r.text)
    with open('data/abstracts/'+pmid.rstrip()+'.txt', 'w') as abstract:
      #@TODO this could be done a bit nicer
      for t in soup.select('passage > text'):
        abstract.write(t.string+"\n")

# Run Noble-Coder on the abstracts
os.system("java -jar 3rd-party-tools/NobleCoder-1.0.jar -terminology go -input data/abstracts/ -output data/noble-coder-output/ -search 'precise-match'")
