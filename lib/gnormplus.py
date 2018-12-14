from bs4 import BeautifulSoup
import requests
from collections import namedtuple
import io
import os

def get_xml(pmid):
  if os.path.isfile('data/gnormplus-output/'+pmid+'.xml'):
    with io.open('data/gnormplus-output/'+pmid+'.xml', 'r', encoding='utf-8') as f:
      return f.read()
  else:
    r = requests.get('https://www.ncbi.nlm.nih.gov/research/bionlp/pubtator2/api/v1/publications/export/biocxml?pmids='+pmid+'&concepts=gene')
    r.encoding = 'utf-8'
    with io.open('data/gnormplus-output/'+pmid+'.xml', 'w', encoding='utf-8') as gnormplus_outfile:
      gnormplus_outfile.write(r.text)
    return r.text

Gene = namedtuple('Gene', ['name', 'id', 'start', 'end'])
def extract_genes(xml):
  soup = BeautifulSoup(xml, 'lxml-xml')
  genes = []
  for a in soup.find_all('annotation'):
    infon_type = a.find('infon', key='type')
    infon_id = a.find('infon', key='identifier')
    if infon_type and infon_id and infon_type.string == 'Gene':
      ncbi_id = infon_id.string
      name = a.find('text').string
      location = a.find('location')
      genes.append(Gene(name, ncbi_id, int(location['offset']), int(location['offset']) + int(location['length'])))
  return genes

def extract_text(xml):
  soup = BeautifulSoup(xml, 'lxml-xml')
  text = ""
  #@TODO there might be a nicer way to do this
  for t in soup.select('passage > text'):
    text = text + t.string +"\n"
  return text
