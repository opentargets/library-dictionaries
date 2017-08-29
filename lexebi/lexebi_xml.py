

from lxml import etree
import json

url = 'ftp://ftp.ebi.ac.uk/pub/software/textmining/bootstrep/termrepository/LexEBI/geneProt70.xml.gz'
gene_dictionary_path= 'GENE-LEXEBI.json'
gene70_dictionary_path= 'GENE70-LEXEBI.json'
disease_dictionary_path= 'DISEASE-LEXEBI.json'
MAX_TERM_FREQ = 180000

#Ignore list created specifically for geneProt70.xml as it does not have mlfreq
IGNORE_LIST = ['cell',
               'but',
               'age',
               'pancreatic',
               'beta',
               'polymerase',
               'new',
               'protein',
               'domain',
               'gene',
               'fitting',
               'fittings'
               '-14',
               'but',
               'little'
               'littles']


def label_to_id(element_names, element_id, label2id):
    element_names = list(set(element_names))
    for name in element_names:
        if name and name.lower() not in IGNORE_LIST:

                if name not in label2id:
                    label2id[name] = []
                label2id[name].append(element_id)

def parse_gene_lexicon(input,output):

    '''parse a list of genes from biolexicon'''

    # TODO - clear root elements to avoid memory issues while parsing
    context = etree.iterparse(open(input),
                              tag='Cluster')  # requries geneProt.xml from LexEBI
    # ftp://ftp.ebi.ac.uk/pub/software/textmining/bootstrep/termrepository/LexEBI/


    target_dict = {}

    for action, cluster in context:
        element_names = []
        for entry in cluster.iterchildren(tag='Entry'):
            element_id = entry.attrib['entryId']
            if 'HUMAN' in element_id:
                if entry.attrib['baseForm']:
                    if input!= 'geneProt70.xml' and int(entry.attrib['mlfreq']) < MAX_TERM_FREQ:

                        element_names.append(entry.attrib['baseForm'])

                '''Synonyms'''
                for variant in entry.iterchildren(tag='Variant'):
                    if input!= 'geneProt70.xml' and int(variant.attrib['mlfreq']) < MAX_TERM_FREQ:
                        element_names.append(variant.attrib['writtenForm'])

                label_to_id(element_names, element_id, target_dict)

    json.dump(target_dict,
              open(output, 'w'),
              indent=4)

def parse_gene70_lexicon(input,output):

    '''parse a list of genes from biolexicon'''

    # TODO - clear root elements to avoid memory issues while parsing
    context = etree.iterparse(open(input),
                              tag='Cluster')  # requries geneProt.xml from LexEBI
    # ftp://ftp.ebi.ac.uk/pub/software/textmining/bootstrep/termrepository/LexEBI/


    target_dict = {}

    for action, cluster in context:
        element_names = []
        for entry in cluster.iterchildren(tag='Entry'):
            element_id = entry.attrib['entryId']
            if 'HUMAN' in element_id:
                if entry.attrib['baseForm']:


                        element_names.append(entry.attrib['baseForm'])

                '''Synonyms'''
                for variant in entry.iterchildren(tag='Variant'):

                        element_names.append(variant.attrib['writtenForm'])

                label_to_id(element_names, element_id, target_dict)

    json.dump(target_dict,
              open(output, 'w'),
              indent=4)

def parse_disease_lexicon(input,output):

    '''parse a list of genes from biolexicon'''

    # TODO - clear root elements to avoid memory issues while parsing
    context = etree.iterparse(open(input),
                              tag='Cluster')  # requries geneProt.xml from LexEBI
    # ftp://ftp.ebi.ac.uk/pub/software/textmining/bootstrep/termrepository/LexEBI/


    target_dict = {}

    for action, cluster in context:
        element_names = []
        for entry in cluster.iterchildren(tag='Entry'):
            element_id = entry.attrib['entryId']

        if entry.attrib['baseForm']:
            if int(entry.attrib['mlfreq']) < MAX_TERM_FREQ:

                element_names.append(entry.attrib['baseForm'])

        '''Synonyms'''
        for variant in entry.iterchildren(tag='Variant'):
            if int(variant.attrib['mlfreq']) < MAX_TERM_FREQ:
                element_names.append(variant.attrib['writtenForm'])

        label_to_id(element_names, element_id, target_dict)

    json.dump(target_dict,
              open(output, 'w'),
              indent=4)


if __name__ == '__main__':
    parse_gene_lexicon('geneProt.xml', gene_dictionary_path)
    parse_gene70_lexicon('geneProt70.xml', gene70_dictionary_path)
    parse_disease_lexicon('umlsDisease.xml', disease_dictionary_path)


