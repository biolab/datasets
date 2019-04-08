import os
import sys
import json
import concurrent.futures

from plumbum.cmd import gzip
from plumbum.path.utils import move

from GEOparse import GDS, get_GEO, GEOTypes
from Orange.data import Table, Domain, ContinuousVariable, StringVariable

from orangecontrib.bioinformatics.ncbi.gene import GeneMatcher
from orangecontrib.bioinformatics.ncbi import taxonomy
from orangecontrib.bioinformatics.widgets.utils.data import (
    GENE_AS_ATTRIBUTE_NAME, TAX_ID, GENE_ID_ATTRIBUTE
)

gds_soft_folder = 'GDS/'

def get_subsets(gds: GDS):
    subsets = []

    for sub_id, sub in gds.subsets.items():
        subsets.append(
            {
                'dataset_id': sub.get_metadata_attribute('dataset_id'),
                'description': sub.get_metadata_attribute('description'),
                'sample_id': sub.get_metadata_attribute('sample_id').split(','),
                'type': sub.get_metadata_attribute('type'),
                'id': sub_id
            }
        )
    return subsets


def get_metadata(gds: GDS):
    pubmed_id = ''

    try:
        pubmed_id = gds.get_metadata_attribute('pubmed_id')
    except GEOTypes.NoMetadataException:
        # Ignore this exception. If there is no value, leave empty
        pass

    return {
        'title': gds.get_metadata_attribute('title'),
        'description': gds.get_metadata_attribute('description'),
        'type': gds.get_metadata_attribute('type'),
        'pubmed_id': pubmed_id,
        'platform': gds.get_metadata_attribute('platform'),
        'platform_organism': gds.get_metadata_attribute('platform_organism'),
        'platform_technology_type': gds.get_metadata_attribute('platform_technology_type'),
        'feature_count': gds.get_metadata_attribute('feature_count'),
        'sample_organism': gds.get_metadata_attribute('sample_organism'),
        'sample_type': gds.get_metadata_attribute('sample_type'),
        'channel_count': gds.get_metadata_attribute('channel_count'),
        'sample_count': gds.get_metadata_attribute('sample_count'),
        'value_type': gds.get_metadata_attribute('value_type'),
        'reference_series': gds.get_metadata_attribute('reference_series'),
        'order': gds.get_metadata_attribute('order'),
        'update_date': gds.get_metadata_attribute('update_date'),
        'subsets': get_subsets(gds)
    }

def prepare_geo_data(file_name: str):
    gds = get_GEO(filepath=os.path.join(gds_soft_folder, file_name))
    gds_id, _, _ = file_name.split('.')
    

    # create dict with all the metadata
    gds_info = get_metadata(gds)

    # skip gds that have more than one organism listed.
    if isinstance(gds_info['sample_organism'], list):
        with open('excluded.txt', 'a+') as fp:
            print(gds_id, 'More then one organism listed -> {}.'.format(gds_info['sample_organism']), sep='\t', file=fp)
        return 
        
    taxid = taxonomy.search(gds_info['sample_organism'], exact=True)

    try:
        taxid = str(taxid[0])
    except IndexError:
        with open('excluded.txt', 'a+') as fp:
            print(gds_id, 'Organism not provided', sep='\t', file=fp)
        return

    # skip if taxonomy not supported
    if taxid not in taxonomy.common_taxids():
        with open('excluded.txt', 'a+') as fp:
            print(gds_id, 'Taxonomy id is not supported -> {}'.format(taxid), sep='\t', file=fp)
        return

    gene_matcher = GeneMatcher(taxid)
    gds_info['taxid'] = taxid

    samples = gds.columns
    samples = samples.drop(['description'], axis=1)
    sample_types = [samp_type for samp_type in samples.columns]
    samples.index = samples.index.set_names('sample_id')
    samples = samples.reset_index()

    table = gds.table
    # Group genes of same spots (use mean)
    table = table.groupby(['IDENTIFIER']).mean().round(3)
    try:
        table = table.drop(['ID_REF'], axis=1)
    except KeyError:
        pass
    table = table.T

    # update feature count after groupby is applied
    _, columns = table.shape
    gds_info['genes'] = columns
    # add info on aggregation
    gds_info['aggregation_function'] = 'mean'
    # mandatory fields to pass linter
    gds_info['name'] = gds_id
    gds_info['version'] = 1.0
    # instances is the same as sample_count
    gds_info['instances'] = gds_info['sample_count']
    # variables is the same as feature_count + samples
    gds_info['variables'] = len(table.columns) + len(samples.columns)
    # no target value
    gds_info['target'] = ''

    # to orange table
    attrs = [ContinuousVariable(name) for name in table.columns]
    metas = [StringVariable(name) for name in samples.columns]

    domain = Domain(attrs, metas=metas)
    orange_table = Table.from_numpy(domain, table.values, metas=samples.values)
    gene_matcher.match_table_attributes(orange_table)
    
    # used to annotate table to work with bioinformatics
    gds_info[GENE_AS_ATTRIBUTE_NAME] = True
    gds_info[GENE_ID_ATTRIBUTE] = 'Entrez ID'

    # store files
    file_name = '{}.tab'.format(gds_id)
    orange_table.save(file_name)
    gzip(file_name)
    move(file_name + '.gz', file_name)

    # os.rename(file_name + '.gz', file_name)

    gds_info['url'] = 'http://file.biolab.si/geo/{}'.format(file_name)
    gds_info['compression'] = 'gz'
    with open('{}.info'.format(file_name), 'w') as fp:
        json.dump(gds_info, fp)

    with open('included.txt', 'a+') as fp:
        print(gds_id, file=fp)

if __name__ == '__main__':
    soft_files = [f for f in os.listdir(gds_soft_folder) if f.endswith('.soft.gz')]

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        executor.map(prepare_geo_data, soft_files)

    # for enum, soft in enumerate(soft_files):
    #     prepare_geo_data(soft)
    #     print('Done:', enum, 'Total:', len(soft_files))
