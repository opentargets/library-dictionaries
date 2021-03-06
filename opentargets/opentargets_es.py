import json
import os
from collections import OrderedDict

from elasticsearch import Elasticsearch, helpers

es = Elasticsearch('http://localhost:9200')
gene_data_file_path = 'ot_gene_data.json'
disease_data_file_path = 'ot_disease_data.json'
pathway_data_file_path = 'ot_pathway_data.json'


gene_dictionary_path= 'GENE-OPENTARGETS.json'
pathway_dictionary_path= 'PATHWAY-OPENTARGETS.json'
disease_dictionary_path= 'DISEASE-OPENTARGETS.json'



CRAP_LIST = ['duration',
 'freckles',
 'sight',
 'height',
 'vision',
 'weight',
 'abortion',
 'puberty',
 'electrocardiogram',
 'measurement',
 'aggression',
 'smoking',
 'sleep',
 'metabolism',
 'gambling',
 'hearing',
 'intuition',
 'reading',
 'exercise',
 'transport',
 'behavior',
 'antibody',
 'dose',
 'longevity',
 'excretion',
 'reasoning',
 'singles',
 'intelligence',
 'sensation',
 'behaviour',
 'antibodies',
 'time',
 'survival',
 'suntan',
 'function',
 'all']

def label_to_id(element_names, element_id, pref_name, label2id):
    '''adds all names to the dictionary with the proper id'''
    element_names = list(set(element_names))
    for name in element_names:
        if name:
            if name  and name.lower() not in CRAP_LIST:
                if name not in label2id:
                    label2id[name] = {"ids": [], "pref_name": pref_name }
                label2id[name]['ids'].append(element_id)

             
'''get data from es'''

if not os.path.exists(gene_data_file_path):
    print 'getting gene data'
    gene_data_file = open(gene_data_file_path,'w')
    res = helpers.scan(client=es,
                                query={"query": {
                                          "match_all": {}
                                        },
                                       '_source': True,
                                       'size': 100,
                                       },
                                scroll='12h',
                                index='20.06_gene-data',
                                timeout="30m",
                                )

    for i,hit in enumerate(res):
        gene_data_file.write(json.dumps(hit['_source'])+'\n')
        print i
    gene_data_file.close()

if not os.path.exists(disease_data_file_path):
    print 'getting disease data'
    disease_data_file = open(disease_data_file_path, 'w')
    res = helpers.scan(client=es,
                       query={"query": {
                           "match_all": {}
                       },
                           '_source': True,
                           'size': 100,
                       },
                       scroll='12h',
                       index='20.06_efo-data',
                       timeout="30m",
                       )

    for i, hit in enumerate(res):
        disease_data_file.write(json.dumps(hit['_source']) + '\n')
        print i
    disease_data_file.close()

if not os.path.exists(pathway_data_file_path):
    print 'getting pathway data'
    pathway_data_file = open(pathway_data_file_path, 'w')
    res = helpers.scan(client=es,
                       query={"query": {
                           "match_all": {}
                       },
                           '_source': True,
                           'size': 100,
                       },
                       scroll='12h',
                       index='20.06_reactome-data',
                       timeout="30m",
                       )

    for i, hit in enumerate(res):
        pathway_data_file.write(json.dumps(hit['_source']) + '\n')
        print i
    pathway_data_file.close()
    
'''parse data'''
             
target_dict =  OrderedDict()
for line in open(gene_data_file_path):
    element = json.loads(line)
    element_id = element['id']
    element_name = element['approved_name']
    element_names = []
    element_names.append(element['approved_symbol'])
    element_names.append(element['approved_name'])
    element_names.extend(element['alias_symbol'])
    element_names.extend(element['alias_name'])
    element_names.append(element['ensembl_description'])
    element_names.extend(element['name_synonyms'])
    element_names.extend(element['previous_names'])
    element_names.extend(element['previous_symbols'])
    element_names.extend(element['symbol_synonyms'])

    label_to_id(element_names, element_id, element_name, target_dict)

json.dump(target_dict, open(gene_dictionary_path, 'w'), indent=2)


disease_dict =  OrderedDict()
for line in open(disease_data_file_path):
    element = json.loads(line)
    element_id = element['code'].split("/")[-1]
    element_names = []

    element_name = element['label']
    element_names.append(element['label'])
    element_names.extend(element['efo_synonyms'])

    label_to_id(element_names, element_id, element_name, disease_dict)


json.dump(disease_dict, open(disease_dictionary_path, 'w'), indent=2)



pathway_dict = OrderedDict()
for line in open(pathway_data_file_path):
    element = json.loads(line)
    element_id = element['id']

    element_name = element['label']
    element_names = []
    element_names.append(element['label'])


    label_to_id(element_names, element_id, element_name, pathway_dict)


json.dump(pathway_dict, open(pathway_dictionary_path, 'w'), indent=2)
