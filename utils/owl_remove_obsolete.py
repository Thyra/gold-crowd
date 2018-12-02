import sys
from bs4 import BeautifulSoup

# @TODO It would be better to do this with SAX (e.g. iterparse) because the file is pretty big but I don't know how
with open(sys.argv[1]) as owl_file:
  soup = BeautifulSoup(owl_file, 'lxml-xml')
  for x in soup.find_all('owl:deprecated'):
    #@TODO: add to the condition below that it's a real class with a go term (= it has a oboInOwl:id subelement)
    if x.text == 'true' and x.parent.name == 'Class':
      axiom = x.parent.next_sibling
      go_term = x.parent['rdf:about'].split('/')[-1]
      print(go_term)
      if axiom.name == 'owl:Axiom' and axiom.children[0].name == 'owl:annotatedSource' and axiom.children[0]['rdf:resource'] == "http://purl.obolibrary.org/obo/GO_0000005":
        pass



with open('out.xml', 'w') as out_file:
  out_file.write(soup.prettify())
