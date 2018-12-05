# Takes a OBO ontology file as its first argument and prints GO term ids for obsolete terms, one per line
from lib import obo_parser
import sys
with open(sys.argv[1]) as obo_fp:
  parser = obo_parser.Parser(obo_fp)
  for stanza in parser:
    if 'is_obsolete' in stanza.tags and stanza.tags['is_obsolete'][0] == 'true':
      print stanza.tags['id'][0]
