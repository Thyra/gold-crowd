import requests
import csv
import os
import glob
from bs4 import BeautifulSoup
# Download GNormPlus results for each PMID and extract abstract and gene annotations
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
    with open('data/brat-input/'+pmid.rstrip()+'.ann', 'w') as ann_file:
      for a in soup.find_all('annotation'):
        gene_name = a.find("text").string
        gene_start = int(a.location['offset'])
        gene_end = int(a.location['offset']) + int(a.location["length"])
        gene_id = a.find(key="NCBI Gene").string + '.' + str(gene_start) # We have to append start offset to make sure ids stay unique.
        ann_file.write("TG"+gene_id+ "\tGene " + str(gene_start) + " " + str(gene_end) + "\t" + gene_name + "\n")



# Run Noble-Coder on the abstracts
os.system("java -jar tools/NobleCoder-1.0.jar -terminology go -input data/abstracts/ -output data/noble-coder-output/ -search 'precise-match'")

# Append results from Noble-Coder to .ann files, save number of functions for later
# Skip obsolete GO terms
function_counts = {} # pmid->n_functions
with open('resources/obsolete_go_terms.txt') as f:
  obsolete_terms = f.read().split("\n")
with open('data/noble-coder-output/RESULTS.tsv', 'rb') as nc_file:
  csv_reader = csv.DictReader(nc_file, delimiter="\t")
  for line in csv_reader:
    pmid = line["Document"].split('.')[0]
    filename = pmid + '.ann'
    ann_id = line["Code"][3:]
    if 'GO:'+ann_id in obsolete_terms:
      continue
    ann_names = []
    ann_offsets = []
    for a in line["Annotations"].split(', '):
      word, start = a.split('/')
      ann_names.append(word)
      end = int(start) + len(word)
      ann_offsets.append(start + ' ' + str(end))
    with open('data/brat-input/'+filename, 'a') as ann_file: #@TODO performance -don't reopen file for every single line
      unique_ann_id = 'TF' + ann_id+'.'+ann_offsets[0].split(' ')[0]
      ann_file.write(unique_ann_id + "\tFunction " + ';'.join(ann_offsets) + "\t" + ' '.join(ann_names)+"\n")
    #@TODO filter out duplicates(maybe by offset?)
    if pmid in function_counts:
      function_counts[pmid] += 1
    else:
      function_counts[pmid] = 1

# Create statistics file
with open('data/statistics.tsv', 'wb') as statistics_file:
  csv_writer = csv.writer(statistics_file, delimiter="\t")
  csv_writer.writerow(['pmid', 'genes', 'functions', 'words'])
  for abstract_file in glob.glob('data/abstracts/*.txt'):
    print(abstract_file)
    pmid = os.path.split(abstract_file)[1].split('.')[0]
    print(pmid)
    with open(abstract_file) as fp:
      words = len(fp.read().split())
    genes = len(BeautifulSoup(open('data/gnormplus-output/'+pmid+'.xml'), 'lxml-xml').find_all('annotation'))
    csv_writer.writerow([pmid, genes, function_counts[pmid], words])
