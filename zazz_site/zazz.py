
import os
import re
import json
import numpy as np
import pandas as pd
import operator
import base64

os.environ['DJANGO_SETTINGS_MODULE'] = 'zazz_site.settings'
import django
django.setup()

from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers

from zazz import models

from time import gmtime, strftime
from functools import reduce
from itertools import product
from collections import OrderedDict, defaultdict
from zazz.models import Samples

print ('OFFLINE:')

g = {
    
}

import_errors = defaultdict(int)

'''
class Mutations(models.Model):

    vep = models.ManyToManyField(to="VEP")
    name = models.CharField(null=False, max_length=100)
    alternative = models.CharField(null=True, max_length=100)
    reference = models.CharField(null=True, max_length=100)
    this_type = models.CharField(null=False, choices=[('name', 'GENERIC'), ('rs_name', 'rs'), ('hgvs_name', 'hgvs')], max_length=100)
'''

class ZazzException(Exception):
    def set_info(self, info):
        self.info = info

def convert_to_base64(s):
    return base64.b64encode(bytes(s, encoding='ascii')).decode()

def decode_base64_json(s):
    return json.loads(base64.b64decode(s.replace('_', '=')))

def print_now():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def get_model(name):
    return getattr(models, name)

def create_field_parameters(parameters):
	return ', '.join(['{k} = {v}'.format(k=k,v=v) for k,v in parameters.items()])

def create_field(field):

#    if field['type'] in ['MultiSelectField']:
#        this_models = ''
#    else:
#        this_models = 'models.'
    this_models = 'models.'

    return '    {name} = {this_models}{type_}({parameters})'.format(
        name=field['name'].replace(' ', '_'),
        this_models=this_models,
        type_ = field['type'],
        parameters = create_field_parameters(field['parameters']),
        )

def create_fields(fields):
	return '\n'.join([create_field(field) for field in fields])

def get_table_pattern():
    table_pattern = '''
class {table}(models.Model):
{meta_val}
{fields_val}
'''
    return table_pattern

def table_pattern_f(table, fields_val, meta_val=''):
    table_pattern = get_table_pattern()
    return table_pattern.format(table=table, fields_val=fields_val, meta_val=meta_val)

def create_external(external):

    #Create main
    table = external['name']
    #fields_keys = [x for x in external['fields'] if x['name'] in external['keys']]
    fields_keys = external['fields']


    fields_val = create_fields(fields_keys)
    ret = table_pattern_f(table=table, fields_val=fields_val)

    #Create secondary


    return ret

def create_externals(externals):
    '''
    externals = [
        {'name': 'Clinvar', 'filename': 'clinvar.csv', 'type': 'csv', 'fields': 
            [
                {'name': 'Chromosome', 'type': 'CharField', 'parameters': {'max_length': '100'}},
                {'name': 'Position', 'type': 'IntegerField', 'parameters': {}},
                {'name': 'Clinical Significance', 'type': 'CharField', 'parameters': {'max_length': '100'}},
            ],
         'keys': ['Chromosome', 'Position'],
        },
    ]

    '''
    return '\n'.join(map(create_external, externals))

def create_table(table, fields, externals):
    '''
    table: Name of main table
    fields: list fields that describe the database 

    '''

    Many2ManyTables = {}
    for field in fields:
        #if field.get('table', False):
        if field.get('database', False) == 'multi_1':
            f_table = field['table']
            if not f_table in Many2ManyTables:
                Many2ManyTables[f_table] = []

            Many2ManyTables[f_table].append(field)
    '''
    Many2ManyTables is a dictionary. 
    keys: are name of tables that we group fields together 
    values is a list of these fields 
    '''

    # Transform Many2ManyTables to django tables format
    Many2ManyTables_text = '\n'.join([table_pattern_f(k,create_fields(v)) for k,v in Many2ManyTables.items()])

    # Add the "normal" fields (not Many2Many)
    new_fields = [field for field in fields if field.get('database', False) != 'multi_1']

    #Add fields for ManyToMany
    #The main table needs to have a ManytoMany relationship with the Samples table     
    new_fields += [{'name': k, 'type': 'ManyToManyField', 'parameters': {'to': k}} for k,v in Many2ManyTables.items()]

    #We also need to add a "raw" field for each many2many relationship
    #We may have to remove this on the furture!
    for k,v in Many2ManyTables.items():
        for f in v:
            # f = {'name': 'Sift', 'col_name': 'sift', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 20, 'database': 'multi', 'l': <function import_annotated_vcf.<locals>.<lambda> at 0x116418488>, 'l_multi': <function splitUnique.<locals>.f at 0x116418510>, 'table': 'Transcripts', 'order': 21}
            #print (f)
            field_to_add = dict(f)

            # All raw fields should be CharFields !
            if field_to_add['type'] != 'CharField':
                field_to_add['type'] = 'CharField'
                field_to_add['parameters']['max_length'] = '200'
            field_to_add['name'] += '_raw'
            new_fields.append(field_to_add)

    # Create a multi field index 
    meta_val = '''
    class Meta:
            indexes = [
                models.Index(
                    fields=['Chromosome', 'Position', 'Reference', 'Alternative'],
                    name='sample_idx',
                ),
            ]
'''

    table_text = table_pattern_f(table=table, fields_val = create_fields(new_fields), meta_val=meta_val)
#    print (table_text)
#    a=1/0


    models_pattern = '''
from django.db import models
# from multiselectfield import MultiSelectField

# Create your models here.

{Many2ManyTables}

class Data(models.Model):
    field = models.CharField(null=True, max_length=200)

{table}

{externals}
'''

    externals_text = create_externals(externals)

    models_text = models_pattern.format(table=table_text, Many2ManyTables=Many2ManyTables_text, externals=externals_text)


    print ('NEW MODELS:')
    print (models_text)


    print ('Saving to zazz/models.py..')
    with open('zazz/models.py', 'w') as f:
        f.write(models_text)
    print ('..DONE')


    print ('Running: python manage.py makemigrations  ...')
    command = 'python manage.py makemigrations zazz'
    os.system(command)
    print ('  ..DONE')

    print ('Running: python manage.py migrate')
    command = 'python manage.py migrate'
    os.system(command)
    print(' ..DONE')


	#print (Data.objects.all())

	#df = pd.read_excel('annotations_zaganas.xlsx')
	#print (df[:3])

	#print ()
	#print ("python manage.py makemigrations")
	#print ("python manage.py migrate")


def create_js_field(field):
    '''
    IGNORE = DO NOT SHOW IN UI
    '''
    pattern = "{{'name': '{name}', 'type': '{type}', 'selected': false, 'e_order': -1, 'database': '{database}', {special}{renderer}{table}{xUnits}{order}{include} }}"

    database = field.get('database', 'normal');

    xUnits = ''

    if field.get('component') == 'freetext':
        type_ = 'freetext'
        special = "'text' : ''" # The ng-model
    elif field.get('component') == 'ignore':
        type_ = 'ignore'
        special = "'text' : ''" # The ng-model
    elif field['type'] in ['CharField', 'ManyToManyField']:
        type_ = 'checkbox'
        special = "'itemArray': [], 'selected2': ['ALL']"
    elif field['type'] in ['IntegerField', 'FloatField']:
        type_ = 'slider'
        special = ''''slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }'''
        if field['type'] == 'IntegerField':
            if not 'xUnits' in field:
                raise ZazzException('xUnit missing from IntegerField')
            xUnits = ", 'xUnits': " + str(field['xUnits'])
    elif field['type'] == 'ForeignKey':
        type_ = 'checkbox'
        special = "'itemArray': [], 'selected2': ['ALL']"

    else:
        raise ZazzException('Unknown field: {}'.format(field['type']))

    if 'renderer' in field:
        renderer = ", 'renderer': " + field['renderer']
    else:
        renderer = ''

    if 'table' in field:
        table = ", 'table': '" + field['table'] + "'"
    else:
        table = ''

    if 'order' in field:
        order = ", 'order': " + str(field['order'])
    else:
        order = ''

    if 'include' in field:
        include = ", 'include': " + str(field['include'])
    else:
        include = ''


    values = {
        'name': field['name'],
        'type': type_,
        'special': special,
        'database': database,
        'renderer': renderer,
        'table': table,
        'order': order,
        'include': include,
        'xUnits': xUnits,
    }

    return pattern.format(**values)

def create_js_fields(fields):
	return ',\n'.join([create_js_field(x) for x in fields])

def create_js(fields):
    '''
$scope.fields = [
            //{'name': 'sample', 'type': 'checkbox', 'selected': false, 'itemArray': [{id: 1, name: ''}], 'selected2': {'value': {id: 1, name: ''}} },
            {'name': 'sample', 'type': 'checkbox', 'selected': false, 'itemArray': [], 'selected2': ['ALL'], 'e_order': -1 }, 
            {'name': 'Bases', 'type': 'slider', 'selected': false, 'slider': {
                                                                                'min': 30,
                                                                                'max': 70,
                                                                                'options': {
                                                                                    'floor': 1,
                                                                                    'ceil': 100,
                                                                                    'disabled': true,
                                                                                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                                                                                        console.log('Slider changed');
                                                                                        //console.log(modelValue); // This the min
                                                                                        //console.log(highValue); // This is the max
                                                                                        $scope.update_table();
                                                                                    }
                                                                                },
                                                                            }, 
                'e_order': -1}, 
            {'name':'Barcode_Name', 'type':'checkbox', 'selected': false, 'itemArray': [], 'selected2': ['ALL'], 'e_order': -1 }
        ];

    '''


    print ('JAVASCRIPT:')
    fields_val = f'$scope.fields=[{create_js_fields(fields)}];'
    print (fields_val)

    # Add fields javascript object in angular controller 
    z_zazz_ctrl_fn = 'zazz/static/zazz/zazz_Ctrl.js'
    with open(z_zazz_ctrl_fn) as f:
        z_zazz_ctrl = f.read()
    z_zazz_ctrl_new = re.sub(
        r'// FIELDS BEGIN\n.+\n// FIELDS END\n', 
        f'// FIELDS BEGIN\n{fields_val}\n// FIELDS END\n', 
        z_zazz_ctrl, 
        flags=re.DOTALL  )

    with open(z_zazz_ctrl_fn, 'w') as f:
        f.write(z_zazz_ctrl_new + '\n')

    print ('Javed javascript at:', z_zazz_ctrl_fn)

def is_dataframe(data):
    '''
    Return true if data is a pandas dataFrame
    '''

    return type(data) is pd.DataFrame

def chromosome_unifier(chromosome):
    '''
    All chromosome input should pass from this function.
    Chromosome can be declared in multiple ways.. "1", chr1, chr01, ...
    Here we make sure that all chromosome values are in the form chr1, chr2, chrX, chrY
    '''
    
    # "15" --> chr15
    if re.match(r'^\d+$', chromosome):
        return 'chr' + chromosome

    if re.match(r'^chr[\dXY]+$', chromosome):
        return chromosome

    if chromosome.upper() in ['X', 'Y']:
        return 'chr' + chromosome.lower()

    raise ZazzException(f'Unknown Chromosome value: ->{chromosome}<-')


def get_value_from_record(field, record, line_index):
    '''

    Extract the value that is present in the record and is described in the field 

    field : Any item in fields list. field is a dictionary
    record: Any item in input data. 

    DUPLICATE CODE!!
    FIX ME!!

    '''

    if not field['col_name'] in record:
        message = '{} does not exist in record\n'.format(field['col_name'])
        message += 'Available columns:\n'
        message += '\n'.join(record.keys()) + '\n'
        raise ZazzException(message)

    try:
        if 'line_l' in field:
            value = field['line_l'](record)
        elif 'l' in field:
            value = field['l'](record[field['col_name']])
        else:
            value = record[field['col_name']]
    except ZazzException as t_exception:
        e_message = str(t_exception)
        e_info = t_exception.info
        import_errors[e_message] += 1
        value = None
    except Exception as e:
        print ('Record:')
        print (record)
        print ('Index:', line_index)
        raise e

    return value

def get_key_from_record(field):
    '''
    Get the name of the key of the record
    '''

    key = field['name']
    if field.get('database', '') == 'multi_2':
        pass
    elif field.get('database', '') == 'multi_1':
        key = field['name'] + '_raw'

    return key


def create_m2m_table(schema, table):
    '''
    Create a dictionary with all the Many2Many tables.
    Example: {'phylop', 'pfam', 'drugbank', 'go', 'dbsnp', 'omim', 'cosmic', 'Transcripts'} 

    key: multi_1 table
    values: list with all column names.
    '''

    m2m_tables = defaultdict(list)

    for field in schema:
        if field.get('database', '') == 'multi_1':
            #m2m_tables.add(field.get('table', table))
            m2m_tables[field.get('table', table)].append(field)

    return m2m_tables

def get_multi_1_records(m2m_tables, record, ):
    '''

    example of field:
    {'name': 'ANN_GeneDetail_refGene', 'col_name': 'GeneDetail.refGene', 'type': 'CharField', 'parameters': {'max_length': '500', 'null': 'True'}, 'database': 'multi_1', 'table': 'ANN_GeneDetail_refGene', 'l_multi': lambda x : x.replace('\\x3d', '=').split('\\x3b'), 'order': 38},

    Returns:
    ret:
    {
        'nameof_m2m_tale' : {
            m2m_field_1: [list of values],
            m2m_field_2: [list of values],
        }
    }

    ret_raw:
    {
        'nameof_m2m_tale' : {
            m2m_field_1: raw_values,
            m2m_field_2: raw_values,
        }
    }        
    '''

    ret = defaultdict(dict)
    ret_raw = defaultdict(dict)
    
    for m2m_table_key, m2m_table_value in m2m_tables.items():
        for field in m2m_table_value:

            #print ('*** FIELD: ***')
            #print (field)

            unsplitted = record[field['col_name']]
            splited_values = field['l_multi'](unsplitted)

            ret[m2m_table_key][field['name']] = splited_values

            if 'l_raw_multi' in field:
                ret_raw[m2m_table_key][field['name'] + '_raw'] = field['l_raw_multi'](splited_values)
            else:
                ret_raw[m2m_table_key][field['name'] + '_raw'] = unsplitted

    #print (ret)
    #a=1/0
    return ret, ret_raw

def create_attribute_records(record_list):
    '''
    record_list:
       {'k': [1,2,3], 'l': [4,5,6]}
    RETURNS: 
       [{'k': 1, 'l': 4}, {'k': 2, 'l': 5}, {'k':3, 'l': 6}]
    '''

    return [dict(zip(record_list.keys(), x)) for x in zip(*record_list.values())]

def import_data_append(input_data, schema, table, externals, **kwargs):
    '''
    Append new data

    kwargs:
    to_append_re : Regular expression to match new field names
    '''

    # Get kwargs
    to_append_re = kwargs.get('to_append_re', None)
    assert to_append_re

    # Get table
    table_db = getattr(models, table)

    # Check type of input data
    if is_dataframe(input_data):
        data = input_data.to_dict('records')
    elif type(input_data) is dict:
        data = input_data
    else:
        raise ZazzException('input_data is not a pandas dataframe or a dictionary')

    #Get the new fields that we will add.
    print ('Selecting only fields according to regexp: {}'.format(to_append_re))
    print ('Total fields: {}'.format(len(schema)))
    fields = [field for field in schema if re.match(to_append_re, field['name'])]
    print ('Fields after selection: {}'.format(len(fields)))
    assert len(fields)
    print ('APPENDING NEW FIELDS:')
    for field in fields:
        print ('    ' + field['name'])

    # Get m2m_table:
    m2m_tables = create_m2m_table(fields, table)
    #print (m2m_tables)
    #a=1/0


    this_error = defaultdict(int)

    for line_index, record in enumerate(data):
        #print (line_index, record['# locus'])
        if (line_index+1) % 1000 == 0:
            print ('{} Imported records: {}/{}  {:.1%}'.format(print_now(), line_index+1, len(data), line_index/len(data)))

        try:
            database_record = table_db.objects.get(Position=record['Position'], Chromosome=record['Chromosome'], Reference=record['Reference'], Alternative=record['Alternative'])
        except ObjectDoesNotExist as e:
            this_error['Could not find chromosome/position in db'] += 1
            continue

        for field in fields:
            value = get_value_from_record(field, record, line_index)
            key = get_key_from_record(field)

            #print ('{}={}'.format(field['name'], value))
            setattr(database_record, key, value)

        #database_record.save()

        # Get multi_1 records:
        #print ('GeneDetail.refGene = ', record['GeneDetail.refGene'])
        multi_1_records, multi_1_records_raw = get_multi_1_records(m2m_tables, record)
        #print ('*** multi_1_records: ***')
        #print (multi_1_records)
        #print ('*** multi_1_records_raw: ***')
        #print (multi_1_records_raw)

        # Store multi records
        for m2m_table_key, m2m_table_value in m2m_tables.items():


            for field in m2m_table_value:
                # Add raw multi_1 records
                setattr(database_record, field['name'] + '_raw', multi_1_records_raw[m2m_table_key][field['name'] + '_raw'])
                #print (database_record)
                #print (field['name'] + '_raw')
                #print (multi_1_records[m2m_table_key][field['name'] + '_raw'])

            #Create attribute dictionary
            attribute_records = create_attribute_records(multi_1_records[m2m_table_key])

            #print ('*** attribute_records ***')
            #print (attribute_records)

            m2m_objects = [getattr(models, m2m_table_key).objects.get_or_create(**attribute_record)[0] for attribute_record in attribute_records]
            getattr(getattr(database_record, m2m_table_key), 'set')(m2m_objects)


        database_record.save()



    print ('IMPORT ERRORS ERRORS:')
    print (json.dumps(this_error, indent=4))


def import_data(input_data, schema, table, externals, delete=True, **kwargs):
    '''
    model_instances = [MyModel(
    field_1=record['field_1'],
    field_2=record['field_2'],
) for record in df_records]

    '''

    # Make sure that there is one and only one of the basic keys
    chromosome_field = [x for x in schema if x['name'] == 'Chromosome']
    position_field = [x for x in schema if x['name'] == 'Position']
    reference_field = [x for x in schema if x['name'] == 'Reference']
    alternative_field = [x for x in schema if x['name'] == 'Alternative']
    assert len(chromosome_field) == 1
    assert len(position_field) == 1
    assert len(reference_field) == 1
    assert len(alternative_field) == 1

    chromosome_field = chromosome_field[0]
    position_field = position_field[0]
    reference_field = reference_field[0]
    alternative_field = alternative_field[0]

    errors_1 = 0

    print ('Importing externals..')

    if delete:
        print ('Deleting external --> internal')
        for external in externals:
            if external['type'] == 'internal':
                print ('   Deleting external --> internal table: {}'.format(external['name']))
                get_model(external['name']).objects.all().delete()
                print ('   Done')

        print ('Deleting externals')
        for external in externals:
            if external['type'] == 'csv':
                print ('   Deleting external table: {}'.format(external['name']))
                get_model(external['name']).objects.all().delete()
                print ('   Done')

    if False:
        '''
        This is an initial effort. It is too slow.
        It stores all info in DB. This is inefficient if we only need a fraction of information 
        '''
        print ('Importing External Data')
        for external in externals:
            if external['type'] == 'csv':
                print ('   Name: {}'.format(external['name']))
                print ('   Loading file: {}'.format(external['filename']))
                csv = pd.read_csv(external['filename'])
                csv_dict = csv.to_dict('index')
                print ('   Length: {}'.format(len(csv_dict)))
                c = 0
                for index, d in csv_dict.items():
                    c += 1
                    if c % 1000 == 0: 
                        print ('      {}, Records: {}'.format(print_now(), c))
                        if c > 1000:
                            break

                    #Build a dictionary with the fields. NO M2M                
                    item_fields_no_m2m = {field['name']:field['l'](d) for field in external['fields'] if not field['type'] == 'ManyToManyField'}
                    new_item = get_model(external['name']).objects.get_or_create(**item_fields_no_m2m)[0]
                    #new_item.save()

                    # Build a dictionary with fields. WITH M2M
                    for field in external['fields']:
                        if field['type'] != 'ManyToManyField':
                            continue
                    
                    item_fields_m2m = {field['name']:field['l'](d) for field in external['fields'] if field['type'] == 'ManyToManyField'}
                    for m2m_k, m2m_v in item_fields_m2m.items():
                        getattr(new_item, m2m_k).add(m2m_v)
                    new_item.save()


            elif external['type'] == 'internal':
                continue
            print ('   Done')
    
    if is_dataframe(input_data):
        df = input_data
    elif type(input_data) is str:
        input_data_ext = os.path.splitext(input_data)[1]
        if input_data_ext == '.xlsx':
            print ('Reading MAIN Excel: {}'.format(input_filename))
            df = pd.read_excel(input_filename)
        else:
            raise Exception('Unknown file type: ', input_data_ext )
    else:
        raise Exception('Unknown input type', type(input_data).__name__)


    if False:
        print ('Keeping only 1000 records')
        df = df[:1000]

    data = df.to_dict('records')

    table_db = getattr(models, table)

    if delete:
        print ('Deleting all..')
        print ('Deleting table.. ', table)
        table_db.objects.all().delete()

    
    # Get the new fields that we will add.
    to_append_re = kwargs.get('to_append_re')
    if to_append_re:
        print ('Adding only fields that match regexp: {}'.format(to_append_re))
        print ('Total fields: {}'.format(len(schema)))
        schema = [field for field in schema if re.match(to_append_re, field['name'])]

        # Add basic fields as well
        schema.extend([chromosome_field, position_field, reference_field, alternative_field])
        print ('After regexp: {}'.format(len(schema)))


    m2m_tables = set()

    for field in schema:
        if field.get('database', '') == 'multi_1':
            m2m_tables.add(field.get('table', table))

    if delete:
        for m2m_table in m2m_tables:
            print ('Deleting table.. ', m2m_table)
            mm_db = getattr(models, m2m_table)
            mm_db.objects.all().delete()

    #(field['line_l'](record)) if 'line_l' in field else (field.get('l', lambda l:l)(record[field['col_name']]))

    print ('Building instances..')
    if False:
        instances = [
            table_db(**{
                field['name'] + ('_raw' if field.get('table', table) != table else ''):
                (field['line_l'](record)) if 'line_l' in field else (field.get('l', lambda l:l)(record[field['col_name']]))   #(field['l'] if 'l' in field else lambda x:x)(record[field['col_name']]) 
                    for field in schema if 'col_name' in field # Add only fields that have col_name. 
                    }) for record in data] #  for field in schema if not field['type'] == 'ManyToManyField'}) for record in data]

    def create_multi_dictionary():
        '''
        Create multi dictionary for multi_2
        '''

        multi_dictionary = defaultdict(list)
        for field in schema:
            if field.get('database', False) == 'multi_2':
                multi_dictionary[field['table']].append(field)

        return multi_dictionary

    multi_dictionary = create_multi_dictionary()

    def create_multi_record(index, record):

        all_multi_value_lists = []
        for multi_key, multi_fields in multi_dictionary.items():
            #Get the values of each multi field

            multi_values_values = []
            multi_values_keys = []
            for multi_field in multi_fields:
                field_value = record[multi_field['col_name']]
                field_value_splitted = multi_field['l_multi'](field_value)

                multi_values_keys.append(multi_field['name'])
                multi_values_values.append(field_value_splitted)

            
            # Make sure that all lists has the same number of values
            set_of_the_length_of_all_values = set(map(len, multi_values_values))
            if len(set_of_the_length_of_all_values) != 1:
                #error_message = 'Index: {} . Fields do not have the same size..'.format(index)
                error_message = 'Multi fields do not have the same size..'
                import_errors[error_message] += 1
                print (error_message)
                return None

            #print ('multi_values_values:')
            #print (multi_values_values)

            #print ('multi_values_keys')
            #print (multi_values_keys)
            multi_values_list_of_dicts = [dict(zip(multi_values_keys,x)) for x in zip(*multi_values_values)]
            
            # [{'gene': 'NBPF9', 'transcript': 'NM_001037675.3', 'location': 'exonic', 'function': 'missense', 'codon': 'CGC', 'exon': '7', 'protein': 'p.His295Arg', 'coding': 'c.885A>G', 'sift': None}, {'gene': 'NBPF8', 'transcript': 'NM_001037501.2', 'location': 'exonic', 'function': 'missense', 'codon': 'CGC', 'exon': '6', 'protein': 'p.His295Arg', 'coding': 'c.885A>G', 'sift': None}, {'gene': 'NBPF8', 'transcript': 'NR_102404.1', 'location': 'exonic_nc', 'function': None, 'codon': None, 'exon': '6', 'protein': None, 'coding': None, 'sift': None}, {'gene': 'NBPF8', 'transcript': 'NR_102405.1', 'location': 'exonic_nc', 'function': None, 'codon': None, 'exon': '5', 'protein': None, 'coding': None, 'sift': None}, {'gene': 'NBPF9', 'transcript': 'NM_001277444.1', 'location': 'exonic', 'function': 'missense', 'codon': 'CGC', 'exon': '7', 'protein': 'p.His295Arg', 'coding': 'c.885A>G', 'sift': None}]
            #print (multi_values_list_of_dicts)
            all_multi_value_lists.append(multi_values_list_of_dicts)

        # Combine multiple values
        #print (reduce(lambda x,y: x*y, all_multi_value_lists))
        if not all_multi_value_lists:
            return None

        ret = [dict(reduce(operator.or_, [y.items() for y in x])) for x in product(*all_multi_value_lists)]
        #print ('Multivalues:', len(ret))
        #print (ret)
        return ret



    if True:
        instances = []

        for line_index, record in enumerate(data):
            #print (line_index, record['# locus'])
            if (line_index+1) % 1000 == 0:
                print ('{} Imported records: {}/{}  {:.1%}'.format(print_now(), line_index+1, len(data), line_index/len(data)))

            table_db_options = {}
            for field in schema:
                if not 'col_name' in field: # Add only fields that have col_name. 
                    continue

                key = field['name']
                if field.get('database', '') == 'multi_2':
                    continue # Later add multi_2 fields
                elif field.get('database', '') == 'multi_1':
                    key = field['name'] + '_raw'

                try:
                    if 'line_l' in field:
                        value = field['line_l'](record)
                    elif 'l' in field:
                        # col_name might not exist in record! Data is not supposed to contain all fields!
                        if not field['col_name'] in record:
                            continue

                        value = field['l'](record[field['col_name']])
                    else:
                        # col_name might not exist in record! Data is not supposed to contain all fields!
                        if not field['col_name'] in record:
                            continue
                        value = record[field['col_name']]
                except ZazzException as t_exception:
                    e_message = str(t_exception)
                    e_info = t_exception.info
                    import_errors[e_message] += 1
                    value = None
                except Exception as e:
                    print ('Record:')
                    print (record)
                    print ('Index:', line_index)
                    raise e
                
                if pd.isnull(value):
                    value = None # np.nan confuses django when attempting: int(np.nan)
                table_db_options[key] = value
            multi_records = create_multi_record(line_index, record)
            if multi_records:
                for multi_record in multi_records:
                    table_db_options = {**table_db_options, **multi_record}
                    instances.append(table_db(**table_db_options))
            else:
                #print (table_db_options)
                instances.append(table_db(**table_db_options))


    count = len(instances)

    print ('Adding IDs..')
    for i, instance in enumerate(instances):
        instance.id = i

    print ('{} Bulk creating main objects..'.format(print_now()))
    # bulk_create does not work with many-to-many relationships. ..sniff...
    # https://docs.djangoproject.com/en/2.0/ref/models/querysets/

    if False:
        '''
        For testing
        '''
        print (serializers.serialize("json", instances, indent=4))

        for inst in instances:
            inst.save()
            print (inst.pk)
    if True:
        table_db.objects.bulk_create(instances) 
        print ('    {} Done'.format(print_now()))


    print ('Indexing main objects..')
    querySet = table_db.objects.filter(id__gte=0, id__lt=count)
    assert querySet.count() == count
    
    index = {x.id:x for x in querySet}

    m2m_index = {}



    print ('Creating many to many relationships..')
    #errors_1 = 0
    def process_multi_1(store):
        errors_1 = 0

        # m2m_objects: store in memory ALL m2m object, so that we can bulk import them later 
        m2m_objects = defaultdict(list)

        # For each record store which many to many has
        m2m_object_references = defaultdict(dict)


        for id_, record in enumerate(data):

            instance = index[id_]
            if id_ % 1000 == 0:
                print ('{} Entries: {}/{}'.format(print_now(), id_+1, count))

            #l_multi is obligatory
            for m2m_table in m2m_tables:

                try:
                    # field['col_name'] in record : col_name does not have to be present in record!
                    m2m_fields = OrderedDict({field['name']: field['l_multi'](record[field['col_name']]) for field in schema if field.get('table', None) == m2m_table and field['col_name'] in record})
                except ZazzException as e:
                    import_errors[str(e)] += 1
                    print (str(e))
                    m2m_fields = {}

                #assert that all have the same length
                if not len(set(len(x) for x in m2m_fields.values())) == 1:
                    print ('Index: {} . Fields do not have the same size..'.format(id_))
                    debug = {field['name']: record[field['col_name']] for field in schema if field.get('table', None) == m2m_table and field['col_name'] in record}
                    #print (debug)
                    #print (m2m_fields)
                    errors_1 += 1
                    m2m_fields = {}
                    #raise Exception()

                #Create database objects
                # {a: [1,2]  , b: [3,4]} --> [{a:1, b:3} , {a:2, b:4}]. See also create_attribute_records() 
                m2m_fields = [dict(zip(m2m_fields.keys(), x)) for x in zip(*m2m_fields.values())]

                current_length = len(m2m_objects[m2m_table])
                m2m_objects[m2m_table].extend(m2m_fields)

                m2m_object_references[id_][m2m_table] = (current_length, current_length+len(m2m_fields))

                # m2m_fields: [{'Gene': 'CLCNKB', 'Transcript': 'NM_000085.4'}, {'Gene': 'CLCNKB', 'Transcript': 'NM_001165945.2'}] 

                if not m2m_fields:
                    # Do nothing. 
                    #getattr(getattr(instance, m2m_table), 'set')(None)
                    #instance.save()
                    continue


                if False:
                    '''
                    Always create new multi object
                    '''
                    m2m_objects = [getattr(models, m2m_table)(**m2m_field) for m2m_field in m2m_fields]
                    
                    #Save objects
                    for o in m2m_objects:
                        o.save()
                if False:
                    '''
                    Create only if they don't exist
                    '''
                    m2m_objects = [getattr(models, m2m_table).objects.get_or_create(**m2m_field)[0] for m2m_field in m2m_fields]

                if store:
                    '''
                    Create only if they don't exist
                    '''
                    m2m_objects = [getattr(models, m2m_table).objects.get(**m2m_field)[0] for m2m_field in m2m_fields]


                #print (m2m_table, m2m_fields)

                #Add it to the main instance
                if False:
                    getattr(getattr(instance, m2m_table), 'set')(m2m_objects)

            if store:
                #Save instance
                instance.save()

        return m2m_objects, m2m_object_references

    m2m_objects, m2m_object_references = process_multi_1(store=False)

    print ('Bulk creating Many2Many Objects')
    table_insance_objects = {}
    for m2m_table, m2m_values in m2m_objects.items():
        print ('   Bulk creating:', m2m_table)

        table_instance = getattr(models, m2m_table)
        table_insance_objects[m2m_table]= [table_instance(**x) for x in m2m_values]
        getattr(models, m2m_table).objects.bulk_create(table_insance_objects[m2m_table]) 

        print ('   Getting Primary Key of:', m2m_table)
        table_insance_objects[m2m_table] = table_instance.objects.all().order_by('pk')

    print ('Connecting main instance with m2m..')

    #Create through objects
    through_objects = {m2m_table: getattr(Samples, m2m_table).through for m2m_table in m2m_tables}

    for id_, record in enumerate(data):

        if id_ % 1000 == 0:
            print ('{} {}/{}'.format(print_now(), id_, len(data)))

        instance = index[id_]

        #
        if not id_ in m2m_object_references:
            continue

        for table_name, table_indexes in m2m_object_references[id_].items():
            #print (table_insance_objects[table_name][table_indexes[0]: table_indexes[1]+1])
            if True:
                '''
                2019-04-18 16:09:42 0/10000
                2019-04-18 16:10:15 1000/10000 --> 33
                2019-04-18 16:10:48 2000/10000 --> 33
                2019-04-18 16:11:22 3000/10000 --> 34
                2019-04-18 16:11:57 4000/10000 --> 35
                2019-04-18 16:12:33 5000/10000 --> 36
                '''
                getattr(getattr(instance, table_name), 'set')(table_insance_objects[table_name][table_indexes[0]: table_indexes[1]+1])

            if False:
                '''
                2019-04-18 16:05:47 0/10000
                2019-04-18 16:06:14 1000/10000 --> 27
                2019-04-18 16:06:43 2000/10000 --> 29
                2019-04-18 16:07:13 3000/10000 --> 30
                2019-04-18 16:07:48 4000/10000 --> 35
                2019-04-18 16:08:27 5000/10000 --> 39

                '''
                tmp1 = [{table_name.lower() + '_id': table_insance_objects[table_name][i].pk, 'samples_id': instance.pk} for i in range(table_indexes[0], table_indexes[1]+1)]
                #print (tmp1)
                tmp2 = [through_objects[table_name](**x) for x in tmp1]
                #print (tmp2)
                through_objects[table_name].objects.bulk_create(tmp2)

        instance.save()
    

    #a=1/0

    print ('Errors 1:', errors_1)

    print ('Annotating with external CSVs')


    #Index external_internals
    external_internals = {external['name']:external for external in externals if external['type'] == 'internal'}

    for external in externals:
        if external['type'] == 'csv':
            external_name = external['name']
            print ('   Name: {}'.format(external_name))
            print ('   Loading file: {}'.format(external['filename']))
            csv = pd.read_csv(external['filename'], **external['read_csv_options'])
            csv_dict = csv.to_dict('index')
            print ('   DONE. Length: {}'.format(len(csv_dict)))

            #Take the central table object
            all_objects = table_db.objects.all()
            print ('   Annotating {} main records'.format(all_objects.count()))

            o_counter = 0
            o_annotated = 0
            for o in all_objects:

                o_counter += 1

                if o_counter % 100 == 0:
                    print ('      {}. Objects: {}  Annotated: {}'.format(print_now(), o_counter, o_annotated))

                matched = external['matcher'](csv, o) # THIS IS VERY SLOW!!
                if matched.empty:
                    continue

                o_annotated += 1

                # This is not empty
                
                # Create foreign object
                
                # Create not M2M
                not_m2m = {field['name']:fields['l'](matched) for field in external['fields'] if not field['type'] == 'ManyToManyField'}
                foreign_object = get_model(external_name)(**not_m2m)

                # Save model
                foreign_object.save()

                # Create M2M objects
                m2m = {field['name']: field['l_m2m'](matched) for field in external['fields'] if field['type'] == 'ManyToManyField'}
                #print (m2m) # {'Clinical_Significance': [{'Clinical Significance': 'Benign'}]}
                m2m_objects = {k: [get_model(k).objects.get_or_create(**x)[0] for x in v] for k,v in m2m.items()}
                #print (m2m_objects)

                #Connect with foreign_object
                for k, v in m2m_objects.items():
                    getattr(foreign_object, k).set(v)

                #Save foreign_object
                foreign_object.save()

                #Now that we have the foreign_object stored, we can connect it with the foreign key of the main object
                setattr(o, external_name, foreign_object) # o.external_name = foreign_object

                #Update main object
                o.save()

            print ('Annotated {} out of {} records'.format(o_annotated, o_counter))




    print ('DONE!')


    if False: # This is legacy code. To be removed...
        for field in schema:

            if not field['type'] == 'ManyToManyField':
                continue

            if instance is None:
                instance = index[id_]

            values = field['l_multi'](record[field['col_name']])
            #Store the values
            m2m_db = getattr(models, field['name'])

            if not field['name'] in m2m_index:
                m2m_index[field['name']] = {}

            #Perform as little as possible queries to the database
            for value in values:
                if not value in m2m_index[field['name']]:
                    m2m_index[field['name']][value] = m2m_db.objects.get_or_create(**{field['name']:value})[0]

            values_obj = [m2m_index[field['name']][value] for value in values]

            #Create M2M relationship
            getattr(getattr(instance, field['name']+'_multi'), 'set')(values_obj)
            instance.save()


    print ('IMPORT ERRROS')
    print (json.dumps(import_errors, indent=4))
    print ('DONE')

def comma_int(x):
	return int(x.replace(',', ''))

def isNone(x):
    return None if pd.isnull(x) else x

def splitUnique(field_name, sep, t=str):
    '''
    t = type
    '''

    def f(x):
        if pd.isnull(x):
                return [None]

        if not hasattr(x, 'split'):

            if t == str:
                return [str(x)]
            elif t == int:
                return [int(x)]
            elif t == float:
                return [float(x)]
            raise ZazzException(f'Invalid type: {type(x).__name__} in field: {field_name}')

        return [y if y else None for y in x.split(sep)]

    return f

def join_set_sep(sep):
    def f(x):
        if pd.isnull(x):
            return None

        return sep.join(sorted(list(set(x.split('|')))))

    return f


def parse_vcf(fn):
    '''
    '''

    print ('Parsing VCF:', fn)
    ret = {}
    c=0
    with open(fn) as f:
        for l in f:
            if l[0] == '#':
                continue
            c += 1
            if c%10000 == 0:
                print ('VCF LINES READ:', c)


            ls = l.strip().split()
            chromosome = ls[0].replace('chr', '')
            position = int(ls[1])

            reference = ls[3]
            alternative = ls[4]

            genotype = ls[9].split(':')[0]
            #print (genotype)



            #print (chromosome)
            #print (position)
            #print (reference)
            #print (alternative)
            
            if len(reference) != 1:
                continue

            if len(alternative) != 1:
                continue

            if genotype == '0/1':
                geno = 'HET'
            elif genotype == '1/1':
                geno = 'HOM'
            else:
                print (genotype)
                a=1/0


            ret[(chromosome, position)] = (reference, alternative, geno)

        print ('VCF LINES TOTAL:', c)

    return ret


######### BED ##########

'''
http://genome.ucsc.edu/FAQ/FAQformat#format1
 The first three required BED fields are:

    chrom - The name of the chromosome (e.g. chr3, chrY, chr2_random) or scaffold (e.g. scaffold10671).
    chromStart - The starting position of the feature in the chromosome or scaffold. The first base in a chromosome is numbered 0.
    chromEnd - The ending position of the feature in the chromosome or scaffold. The chromEnd base is not included in the display of the feature. For example, the first 100 bases of a chromosome are defined as chromStart=0, chromEnd=100, and span the bases numbered 0-99.


====A====
chr1    5   6   K
chr1    10  20  L
chr1    25  26  M

====B====
chr1    7   9   A   AA
chr1    8   10  B   BB
chr1    9   12  C   CC
chr1    10  11  D   DD  
chr1    10  20  E   EE
chr1    12  14  F   FF
chr1    17  25  G   GG
chr1    18  20  H   HH

a = BedTool('a.bed')
b = BedTool('b.bed')

#print (a.intersect(b, loj=True))
a.intersect(b, loj=True).saveas('c.bed')

chr1    5   6   K   .   -1  -1  .   .
chr1    10  20  L   chr1    9   12  C   CC
chr1    10  20  L   chr1    10  11  D   DD
chr1    10  20  L   chr1    10  20  E   EE
chr1    10  20  L   chr1    12  14  F   FF
chr1    10  20  L   chr1    17  25  G   GG
chr1    10  20  L   chr1    18  20  H   HH
chr1    25  26  M   .   -1  -1  .   .


'''


def bed_create_from_db(querySet, filename):
    '''
    QuerySet must be ordered, According to position!
    '''
    print ('Saving DB objects in BED format in: {}'.format(filename))

    with open(filename, 'w') as f:
        c = 0
        for o in querySet:

            c += 1
            if c % 1000 == 0:
                print ('   Saved: {} records'.format(c))

            record = [
                o.Chromosome,
                str(o.Position),
                str(o.Position+1), ## FIX ME !!!!
                str(o.id),
            ]
            f.write('\t'.join(record) + '\n')

    print ('   Done')

def bed_loj(filename_1, filename_2, output_filename):
    '''
    https://daler.github.io/pybedtools/autodocs/pybedtools.bedtool.BedTool.intersect.html
    '''

    print ('   Intersecting LOJ with BedTools..')
    a = BedTool(filename_1)
    b = BedTool(filename_2)

    a.intersect(b, loj=True).saveas(output_filename)
    print ('   DONE')


######### END OF BED ###

def chromosome_sizes_hg19():
    '''
    http://hgdownload.cse.ucsc.edu/goldenPath/hg19/bigZips/hg19.chrom.sizes
    '''
    return {

        'chr1':    249250621,
        'chr2':    243199373,
        'chr3':    198022430,
        'chr4':    191154276,
        'chr5':    180915260,
        'chr6':    171115067,
        'chr7':    159138663,
        'chrX':    155270560,
        'chr8':    146364022,
        'chr9':    141213431,
        'chr10':   135534747,
        'chr11':   135006516,
        'chr12':   133851895,
        'chr13':   115169878,
        'chr14':   107349540,
        'chr15':   102531392,
        'chr16':   90354753,
        'chr17':   81195210,
        'chr18':   78077248,
        'chr20':   63025520,
        'chrY' :   59373566,
        'chr19':   59128983,
        'chr22':   51304566,
        'chr21':   48129895,
        'chrM' :   16571,
    }

def list_of_chromosomes():
    return list(map(lambda x : 'chr' + x, list(map(str, range(1,23)) ) + ['X', 'Y', 'M']))

def accumulate_chromosome_sizes_hg19():
    s = chromosome_sizes_hg19()
    m = list_of_chromosomes()
    
    offset = 0
    ret = {}
    for chromosome in m:
        ret[chromosome] = offset
        offset += s[chromosome]

    return ret

def accumulative_position(chromosome, position):

    chr_index = g['list_of_chromosomes'].index(chromosome)

    if chr_index == 0:
        return int(position)

    return g['accumulate_chromosome_sizes_hg19'][g['list_of_chromosomes'][chr_index]] + int(position)

def pandas_to_vcf(df, chromosome_f, position_f, reference_f, alternative_f, vcf_filename):
    print ('Converting pandas to VCF')
    input_data = df.to_dict('records')

    f = open(vcf_filename, 'w')
    f.write('##fileformat=VCFv4.0\n')
    f.write('\t'.join(['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO']) + '\n')

    for line_index, record in enumerate(input_data):
        #print (record)

        if line_index%10000 == 0:
            print ('Lines: {}/{}'.format(line_index, len(input_data)))

        chromosome = chromosome_f(record)
        if 'chr' in chromosome.lower():
            chromosome = chromosome.replace('chr', '')

        position = position_f(record)
        reference = reference_f(record)
        alternative = alternative_f(record)

        try:
            #savoura = convert_to_base64(json.dumps(record))
            savoura = '.'

        except TypeError as e:
            if str(e) == "Object of type Timestamp is not JSON serializable":
                print ('Error:', str(e), '  ignoring..')
                continue
            else:
                raise e

        to_print = [chromosome, position, '.', reference, alternative, '.', savoura, '.']

        to_print_str = '\t'.join(map(str, to_print)) + '\n'
        f.write(to_print_str)

    f.close()
    print (f'Created file: {vcf_filename}')


def setup_1():
    '''
    Setups DB + Javascript
    '''



    #print ('Adding accumulative_position..')
    #df['accumulative_position'] = df.apply(lambda x: accumulative_position(*x['# locus'].split(':')), axis=1)
    #print ('    ..DONE')


    def split_location(x):
        #print (x)
        if pd.isnull(x):
            return 'UNKNOWN'
        return x.split('|')[0]

    def log_f(x):

        #print (x)

        if str(x)=='0.0':
            return None

        return int(-np.log10(float(x)))

    def allele_coverage(x):

        #print (x)

        if '.' in x:
            sp = x.split('.')
        elif ',' in x:
            sp = x.split(',')

        if not len(sp) == 2:
            error_message = 'More than 2 values in allele coverage'
            import_errors[error_message] += 1
            #print (x)
            #assert False
            return [None, None]

        return list(map(int, sp))

    def allele_coverage_2(x):
        ac = x['allele_coverage']
        #print ('Allele Coverage:', ac)

        if not ',' in str(ac) and not '.' in str(ac):
            int_ac = int(ac)
            str_ac = str(ac)
            coverage = int(x['coverage'])
            for i in range(1,len(str_ac)):
                part1 = int(str_ac[:i])
                part2 = int(str_ac[i:])

                if part1 + part2 == int(coverage):
                    ret = [part1, part2]
                    #print (f'Allele Coverage: {ac}  Coverage: {coverage}  Coverage: {ret}')
                    return ret
            #print (f'Allele Coverage: {ac}')
            #print ('Coverage:', coverage)
            e = ZazzException('Invalid Coverage value')
            e.set_info({'coverage': coverage, 'allele_coverage': ac})
            raise e

        else:
            return allele_coverage(ac)

    def maf_f(x):

        if type(x).__name__ in ['int', 'float']:
            ret = x
        else:
            ret = float(x.split(':')[0])

        return ret

    def sift_raw_f(x):
        #return ','.join(str(x).split('|'))
        return x

    def f5000Exomes_AMAF(name):
        def f(x):
            if pd.isnull(x):
                return None
            if x.count(':') != 2:
                e = ZazzException('Invalid 5000Exomes values')
                e.set_info({'value': x})
                raise e
            values = dict(y.split('=') for y in x.split(':'))
            return float(values[name])


        return f

    def cosmic_multi_f(x):

#        print (x)
#        print (type(x))
        if str(x) == 'nan':
            return ['NaN']


        if pd.isnull(x):
            return ['NaN']

        if not str(x):
            return ['NaN']

        return str(x).split(':')

    def dbsnp_multi_f(x):
        if not 'rs' in str(x):
            return ['NaN']

        return x.split(':')

    def go_f(x):
        if not 'GO' in str(x):
            return ['NaN']

        return re.findall(r'GO:[\d]+', x)

    def omim_f(x):
        if not re.search(r'\d', str(x)):
            return ['NaN']

        return str(x).split(':')

    def phylop_f(x):
        if not re.search(r'\d', str(x)):
            return [None]

        return list(map(float, str(x).split(',')))

    def alternative_f(x):
        return ','.join(list(set(x['genotype'].split('/')) - set(x['ref'])))

    def ANN_AAChange_refGene_columns(index):

        def ret(s):

            #print ('ANN_AAChange_refGene_exon:', s)

            if s in ['.', 'UNKNOWN']:
                return [None]

            splitted = [x.split(':') for x in s.split(',')]
            return [x[index] if index<len(x) else None for x in splitted]

            #return [x.split(':')[index] for x in s.split(',')]

        return ret

    def VEP_DOMAINS_f(line):
        '''
Superfamily_domains:SSF54277&SMART_domains:SM00666&PIRSF_domain:PIRSF000554&Gene3D:3.10.20.240&Pfam_domain:PF00564&hmmpanther:PTHR24357&hmmpanther:PTHR24357:SF60|||||Superfamily_domains:SSF54277&Pfam_domain:PF00564&Gene3D:3.10.20.240&hmmpanther:PTHR24357&hmmpanther:PTHR24357:SF59
        '''

        ret = line.split('|')

        #b = [len(list(filter(lambda t: 'hmmpanther' in t, x.split('&')))) for x in ret]

        s2 = [x.split('&') for x in ret]
        s3 = [dict([(y.split(':')[0] if y.count(':')==1 else "hmmpanter2", ':'.join(y.split(':')[1:])) for y in x if y]) for x in s2]
        s4 = defaultdict(set)
        for x in s3:
            for k,v in x.items():
                s4[k].add(v)

        s5 = set(list(map(len, s4.values())))
        if s5 == set():
            pass
        elif s5 == set([1]):
            pass
        elif s5 == set([0]):
            pass
        else:
            print (line)
            print (s4)
            print (s5)
            assert False


        return ret


#    def zazz_clinvar_f(s):
#
#        print ('=====1====')
#        print (s)
#        print ('=====2====')
#        return 'kostas'


    def zazz_clinvarzazz_f(clinvar_field):
        def f(s):
            '''

            '''


            s_splited = s.split('|')
            different = set(s_splited)
            assert len(different) == 1
            first = s_splited[0]
            if first == '':
                return [None]

            #print ('==1==')
            #print (first)
            #print ('==2==')
            decoded = decode_base64_json(first)
            #print ('==3==')
            #print (json.dumps(decoded, indent=4))
            
            # zazz_clinvarzazz_f Clinical Significance 
            ret = []
            for rcv_code, rcv_value in decoded['RCV'].items():
                scv_dictionary = rcv_value['SCV']
                rcv_data = rcv_value['RCV_data']

                Clinical_significance = rcv_data['Clinical significance']
                condition_name = '/'.join(rcv_data['Condition name'])
                rcv_review_status = rcv_data['Review status'] # "criteria provided, single submitter", 
                Review_status_stars = str(rcv_data['Review status stars'])


                for scv_data, scv_value in scv_dictionary.items():
                    scv_data = scv_value['SCV_data']

                    interpretation = scv_data['interpretation']
                    scv_review_status = scv_data['Review status']

                    if clinvar_field == 'interpretation':
                        ret.append(interpretation)
                    elif clinvar_field == 'scv_review_status':
                        ret.append(scv_review_status)
                    elif clinvar_field == 'clinical_significance':
                        ret.append(Clinical_significance)
                    elif clinvar_field == 'condition_name':
                        ret.append(condition_name)
                    elif clinvar_field == 'rcv_review_status':
                        ret.append(rcv_review_status)
                    elif clinvar_field == 'review_status_stars':
                        ret.append(Review_status_stars)
                    else:
                        raise ZazzException('Unknown clinvar field: {}'.format(clinvar_field))

            #print ('==4===')
            #print (ret)
            #a=1/0

            return ret

        return f

    fields = [

        # Main entries
        {'name': 'Chromosome', 'col_name': 'Chromosome', 'type': 'CharField', 'parameters': {'max_length': '5'}, 'l': lambda x: x, 'order': 1},
        {'name': 'Position', 'col_name': 'Position', 'type': 'IntegerField', 'parameters': {}, 'l': lambda x:x, 'xUnits':20, 'order': 2},
        {'name': 'Reference', 'col_name': 'Reference', 'type': 'CharField', 'parameters': {'max_length': '255'}, 'component': 'freetext', 'l': lambda x:x, 'order': 3},
        {'name': 'Alternative', 'col_name': 'Alternative', 'type': 'CharField', 'parameters': {'max_length': '255'}, 'component': 'freetext', 'l': lambda x:x, 'order': 4},


        # FIELDS FROM RAW VCF
        {'name':'RAW_NS', 'col_name': 'NS', 'type': 'IntegerField', 'parameters': {'null': True}, 'l': lambda x:x, 'xUnits': 10, 'order': 11 },
        {'name':'RAW_HS', 'col_name': 'HS', 'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'l': lambda x:x, 'order': 12 },
        {'name':'RAW_DP', 'col_name': 'DP', 'type': 'IntegerField', 'parameters': {}, 'l': lambda x:x, 'xUnits': 10, 'order': 13 },
        {'name':'RAW_RO', 'col_name': 'RO', 'type': 'IntegerField', 'parameters': {}, 'l': lambda x:x, 'xUnits': 10, 'order': 14 },
        {'name':'RAW_AO', 'col_name': 'AO', 'type': 'IntegerField', 'parameters': {}, 'l': lambda x:x, 'xUnits': 10, 'order': 15 },
        {'name':'RAW_SRF', 'col_name': 'SRF', 'type': 'IntegerField', 'parameters': {}, 'l': lambda x:x, 'xUnits': 10, 'order': 16 },
        {'name':'RAW_SRR', 'col_name': 'SRR', 'type': 'IntegerField', 'parameters': {}, 'l': lambda x:x, 'xUnits': 10, 'order': 17 },
        {'name':'RAW_SAF', 'col_name': 'SAF', 'type': 'IntegerField', 'parameters': {}, 'l': lambda x:x, 'xUnits': 10, 'order': 18 },
        {'name':'RAW_SAR', 'col_name': 'SAR', 'type': 'IntegerField', 'parameters': {}, 'l': lambda x:x, 'xUnits': 10, 'order': 19 },
        {'name':'RAW_FDP', 'col_name': 'FDP', 'type': 'IntegerField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'xUnits': 10, 'order': 20 },
        {'name':'RAW_FRO', 'col_name': 'FRO', 'type': 'IntegerField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'xUnits': 10, 'order': 21 },
        {'name':'RAW_FAO', 'col_name': 'FAO', 'type': 'IntegerField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'xUnits': 10, 'order': 22 },
        {'name':'RAW_AF', 'col_name': 'AF', 'type': 'FloatField', 'parameters': {}, 'l': lambda x:x, 'order': 23 },
        {'name':'RAW_QD', 'col_name': 'QD', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'order': 24 },
        {'name':'RAW_FSRF', 'col_name': 'FSRF', 'type': 'IntegerField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'xUnits': 10, 'order': 25 },
        {'name':'RAW_FSRR', 'col_name': 'FSRR', 'type': 'IntegerField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'xUnits': 10, 'order': 26 },
        {'name':'RAW_FSAF', 'col_name': 'FSAF', 'type': 'IntegerField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'xUnits': 10, 'order': 27 },
        {'name':'RAW_FSAR', 'col_name': 'FSAR', 'type': 'IntegerField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'xUnits': 10, 'order': 28 },
        {'name':'RAW_FXX', 'col_name': 'FXX', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'order': 29 },
        {'name':'RAW_TYPE', 'col_name': 'TYPE', 'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'l': lambda x:x, 'order': 30 },
        {'name':'RAW_LEN', 'col_name': 'LEN', 'type': 'IntegerField', 'parameters': {}, 'l': lambda x:x, 'xUnits': 10, 'order': 31 },
        {'name':'RAW_HRUN', 'col_name': 'HRUN', 'type': 'IntegerField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'xUnits': 10, 'order': 32 },
        {'name':'RAW_FR', 'col_name': 'FR', 'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'l': lambda x:x, 'order': 33 },
        {'name':'RAW_RBI', 'col_name': 'RBI', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'order': 34 },
        {'name':'RAW_FWDB', 'col_name': 'FWDB', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'order': 35 },
        {'name':'RAW_REVB', 'col_name': 'REVB', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'order': 36 },
        {'name':'RAW_REFB', 'col_name': 'REFB', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'order': 37 },
        {'name':'RAW_VARB', 'col_name': 'VARB', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'order': 38 },
        {'name':'RAW_SSSB', 'col_name': 'SSSB', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'order': 39 },
        {'name':'RAW_SSEN', 'col_name': 'SSEN', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'order': 40 },
        {'name':'RAW_SSEP', 'col_name': 'SSEP', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'order': 41 },
        {'name':'RAW_STB', 'col_name': 'STB', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'order': 42 },
        {'name':'RAW_STBP', 'col_name': 'STBP', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'order': 43 },
        {'name':'RAW_PB', 'col_name': 'PB', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'order': 44 },
        {'name':'RAW_PBP', 'col_name': 'PBP', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'order': 45 },
        {'name':'RAW_MLLD', 'col_name': 'MLLD', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'order': 46 },
        {'name':'RAW_OID', 'col_name': 'OID', 'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'l': lambda x:x, 'order': 47 },
        {'name':'RAW_OPOS', 'col_name': 'OPOS', 'type': 'IntegerField', 'parameters': {}, 'l': lambda x:x, 'xUnits': 10, 'order': 48 },
        {'name':'RAW_OREF', 'col_name': 'OREF', 'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'l': lambda x:x, 'order': 49 },
        {'name':'RAW_OALT', 'col_name': 'OALT', 'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'l': lambda x:x, 'order': 50 },
        {'name':'RAW_OMAPALT', 'col_name': 'OMAPALT', 'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'l': lambda x:x, 'order': 51 },
        {'name':'RAW_GT_GT', 'col_name': 'GT_GT', 'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'l': lambda x:x, 'order': 52 },
        {'name':'RAW_GT_GQ', 'col_name': 'GT_GQ', 'type': 'IntegerField', 'parameters': {}, 'l': lambda x:x, 'xUnits': 10, 'order': 53 },
        {'name':'RAW_GT_DP', 'col_name': 'GT_DP', 'type': 'IntegerField', 'parameters': {}, 'l': lambda x:x, 'xUnits': 10, 'order': 54 },
        {'name':'RAW_GT_RO', 'col_name': 'GT_RO', 'type': 'IntegerField', 'parameters': {}, 'l': lambda x:x, 'xUnits': 10, 'order': 55 },
        {'name':'RAW_GT_AO', 'col_name': 'GT_AO', 'type': 'IntegerField', 'parameters': {}, 'l': lambda x:x, 'xUnits': 10, 'order': 56 },
        {'name':'RAW_GT_SRF', 'col_name': 'GT_SRF', 'type': 'IntegerField', 'parameters': {}, 'l': lambda x:x, 'xUnits': 10, 'order': 57 },
        {'name':'RAW_GT_SRR', 'col_name': 'GT_SRR', 'type': 'IntegerField', 'parameters': {}, 'l': lambda x:x, 'xUnits': 10, 'order': 58 },
        {'name':'RAW_GT_SAF', 'col_name': 'GT_SAF', 'type': 'IntegerField', 'parameters': {}, 'l': lambda x:x, 'xUnits': 10, 'order': 59 },
        {'name':'RAW_GT_SAR', 'col_name': 'GT_SAR', 'type': 'IntegerField', 'parameters': {}, 'l': lambda x:x, 'xUnits': 10, 'order': 60 },
        {'name':'RAW_GT_FDP', 'col_name': 'GT_FDP', 'type': 'IntegerField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'xUnits': 10, 'order': 61 },
        {'name':'RAW_GT_FRO', 'col_name': 'GT_FRO', 'type': 'IntegerField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'xUnits': 10, 'order': 62 },
        {'name':'RAW_GT_FAO', 'col_name': 'GT_FAO', 'type': 'IntegerField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'xUnits': 10, 'order': 63 },
        {'name':'RAW_GT_AF', 'col_name': 'GT_AF', 'type': 'FloatField', 'parameters': {}, 'l': lambda x:x, 'order': 64 },
        {'name':'RAW_GT_FSRF', 'col_name': 'GT_FSRF', 'type': 'IntegerField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'xUnits': 10, 'order': 65 },
        {'name':'RAW_GT_FSRR', 'col_name': 'GT_FSRR', 'type': 'IntegerField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'xUnits': 10, 'order': 66 },
        {'name':'RAW_GT_FSAF', 'col_name': 'GT_FSAF', 'type': 'IntegerField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'xUnits': 10, 'order': 67 },
        {'name':'RAW_GT_FSAR', 'col_name': 'GT_FSAR', 'type': 'IntegerField', 'parameters': {'null': 'True'}, 'l': lambda x:x, 'xUnits': 10, 'order': 68 },


        # FIELDS FROM IONTORRENT
        {'name': 'ION_Type', 'col_name': 'type', 'type': 'CharField', 'parameters': {'max_length': '100'}, 'order': 102},
        #{'name': 'Position', 'col_name': 'accumulative_position', 'type': 'IntegerField', 'parameters': {}, 'l': lambda x: x, 'order': 2},
        {'name': 'ION_Reference', 'col_name': 'ref', 'type': 'CharField', 'parameters': {'max_length': '255'}, 'component': 'freetext', 'l': lambda x:x, 'order': 105},
        {'name': 'ION_Length', 'col_name': 'length', 'type': 'IntegerField', 'parameters': {'null': 'True'}, 'l':lambda x: int(x), 'xUnits': 20, 'order': 106, },
        {'name': 'ION_Genotype', 'col_name': 'genotype', 'type': 'CharField', 'parameters': {'max_length': '255'}, 'component': 'freetext', 'l': lambda x:x, 'order': 107},
        {'name': 'ION_PValue', 'col_name': 'pvalue', 'type': 'IntegerField', 'parameters': {'null': True}, 'l': log_f, 'xUnits': 20, 'order': 108, },
        {'name': 'ION_Coverage', 'col_name': 'coverage', 'type': 'IntegerField', 'parameters': {'null': 'True'}, 'l': lambda x: int(x), 'xUnits': 20, 'order': 109, },
        {'name': 'ION_Allele_Coverage_1', 'col_name': 'allele_coverage', 'type': 'IntegerField', 'parameters': {'null': True}, 'line_l': lambda x: allele_coverage_2(x)[0], 'xUnits': 20, 'order': 110, },
        {'name': 'ION_Allele_Coverage_2', 'col_name': 'allele_coverage', 'type': 'IntegerField', 'parameters': {'null': True}, 'line_l': lambda x: allele_coverage_2(x)[1], 'xUnits': 20, 'order': 111, },
        {'name': 'ION_MAF', 'col_name': 'maf', 'type': 'FloatField', 'parameters': {'null': True}, 'l': lambda x : maf_f(x), 'xUnits': 20, 'order': 112, },
        {'name': 'ION_Gene', 'col_name': 'gene', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'database': 'multi_1', 'l': lambda x:x, 'l_multi': splitUnique('Gene', '|'), 'table': 'ION_Transcripts', 'order': 113},
        {'name': 'ION_Transcript', 'col_name': 'transcript', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'database': 'multi_1', 'l': lambda x:x, 'l_multi': splitUnique('Transcript', '|'), 'table': 'ION_Transcripts', 'order': 114},
        {'name': 'ION_Location', 'col_name': 'location', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'database': 'multi_1', 'l': lambda x:x, 'l_multi': splitUnique('Transcript', '|'), 'table': 'ION_Transcripts', 'order': 115},
        {'name': 'ION_Function', 'col_name': 'function', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'database': 'multi_1', 'l': lambda x:x, 'l_multi': splitUnique('Transcript', '|'), 'table': 'ION_Transcripts', 'order': 116}, ## Prosuces 10/2000 errors!
        {'name': 'ION_Codon', 'col_name': 'codon', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'database': 'multi_1', 'l': lambda x:x, 'l_multi': splitUnique('Transcript', '|'), 'table': 'ION_Transcripts', 'order': 117},
        {'name': 'ION_Exon', 'col_name': 'exon', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'database': 'multi_1', 'l': lambda x:x, 'l_multi': splitUnique('Transcript', '|'), 'table': 'ION_Transcripts', 'order': 118},
        {'name': 'ION_Protein', 'col_name': 'protein', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'database': 'multi_1', 'l': lambda x:x, 'l_multi': splitUnique('Transcript', '|'), 'table': 'ION_Transcripts', 'order': 119},
        {'name': 'ION_Coding', 'col_name': 'coding', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'database': 'multi_1', 'l': lambda x:x, 'l_multi': splitUnique('Transcript', '|'), 'table': 'ION_Transcripts', 'order': 120},
        {'name': 'ION_Sift', 'col_name': 'sift', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 20, 'database': 'multi_1', 'l': sift_raw_f, 'l_multi': splitUnique('Transcript', '|', float), 'table': 'ION_Transcripts', 'order': 121},
        {'name': 'ION_Polyphen', 'col_name': 'polyphen', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 20, 'database': 'multi_1', 'l': sift_raw_f, 'l_multi': splitUnique('Transcript', '|', float), 'table': 'ION_Transcripts', 'order': 122},
        {'name': 'ION_Grantham', 'col_name': 'grantham', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 20, 'database': 'multi_1', 'l': sift_raw_f, 'l_multi': splitUnique('Transcript', '|', float), 'table': 'ION_Transcripts', 'order': 123},
        {'name': 'ION_NormalizedAlt', 'col_name': 'normalizedAlt', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'database': 'multi_1', 'l_multi': splitUnique('Transcript', '|'), 'table': 'ION_Transcripts', 'order': 124},
        {'name': 'ION_F5000Exomes_AMAF', 'col_name': '5000Exomes', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': f5000Exomes_AMAF('AMAF'), 'order': 125},
        {'name': 'ION_F5000Exomes_EMAF', 'col_name': '5000Exomes', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': f5000Exomes_AMAF('EMAF'), 'order': 126},
        {'name': 'ION_F5000Exomes_GMAF', 'col_name': '5000Exomes', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': f5000Exomes_AMAF('GMAF'), 'order': 127},
        {'name': 'ION_Clinvar', 'col_name': 'clinvar', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'l': lambda x:x, 'order': 128},
        {'name': 'ION_COSMIC', 'col_name': 'cosmic', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'database': 'multi_1', 'l_multi': cosmic_multi_f, 'table': 'ION_cosmic', 'order': 129,
            'renderer': '''
                        function(x) {
                            if (x.ION_COSMIC != 'NaN') {
                                return "<a href=https://cancer.sanger.ac.uk/cosmic/search?q=" + x.ION_COSMIC + ">" + x.ION_COSMIC + "</a>";
                            }
                            return 'NaN';
                        }
                        '''},
        {'name': 'ION_DbSNP', 'col_name': 'dbsnp', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'database': 'multi_1', 'l_multi': dbsnp_multi_f, 'table': 'ION_dbsnp', 'order': 130,
            'renderer': '''
                        function(x) {
                            if (x.ION_DbSNP != 'NaN') {
                                return "<a href=https://www.ncbi.nlm.nih.gov/snp/" + x.ION_DbSNP + ">" + x.ION_DbSNP + "</a>";
                            }
                            return 'NaN';
                        }

                        '''},
        {'name': 'ION_Drugbank', 'col_name': 'drugbank', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'database': 'multi_1', 'l_multi': cosmic_multi_f, 'table': 'ION_drugbank', 'order': 131},
        {'name': 'ION_GO', 'col_name': 'go', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'database': 'multi_1', 'l_multi': go_f, 'table': 'ION_go', 'order': 132},
        {'name': 'ION_OMIM', 'col_name': 'omim', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'database': 'multi_1', 'l_multi': omim_f, 'table': 'ION_omim', 'order': 133,
            'renderer': '''
                function(x) {
                    if (x.ION_OMIM != 'NaN') {
                        return "<a href=https://www.omim.org/entry/" + x.ION_OMIM + ">" + x.ION_OMIM + "</a>";
                    }
                    return 'NaN';
                }
            '''
             },
        {'name': 'ION_Pfam', 'col_name': 'pfam', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'database': 'multi_1', 'l_multi': omim_f, 'table': 'ION_pfam', 'order': 134,
            'renderer': '''
                function(x) {
                    if (x.ION_Pfam != 'NaN') {
                        return "<a href=https://pfam.xfam.org/family/" + x.ION_Pfam + ">" + x.ION_Pfam + "</a>";
                    }
                    return 'NaN';
                }
            '''
            },
        {'name': 'ION_Phylop', 'col_name': 'phylop', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'database': 'multi_1', 'l_multi': phylop_f, 'table': 'ION_phylop', 'order': 135},

        ########## FIELDS FROM ANNOVAR #########
        {'name': 'ANN_Func_refGene', 'col_name': 'Func.refGene', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'order': 201},
        {'name': 'ANN_Gene_refGene', 'col_name': 'Gene.refGene', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'order': 202},
        {'name': 'ANN_GENEDETAIL_REFGENE', 'col_name': 'GeneDetail.refGene', 'type': 'CharField', 'parameters': {'max_length': '500', 'null': 'True'}, 'database': 'multi_1', 'table': 'ANN_GeneDetail_refGene', 'l_multi': lambda x : x.replace('\\x3d', '=').split('\\x3b'), 'order': 203},
        {'name': 'ANN_ExonicFunc_refGene', 'col_name': 'ExonicFunc.refGene', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'order': 204},

        {'name': 'ANN_AAChange_refGene_gene', 'col_name': 'AAChange.refGene', 'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'ANN_AAChange_refGene', 'l_multi': ANN_AAChange_refGene_columns(0), 'order': 205},
        {'name': 'ANN_AAChange_refGene_transcript', 'col_name': 'AAChange.refGene', 'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'ANN_AAChange_refGene', 'l_multi': ANN_AAChange_refGene_columns(1), 'order': 206},
        {'name': 'ANN_AAChange_refGene_exon', 'col_name': 'AAChange.refGene', 'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'ANN_AAChange_refGene', 'l_multi': ANN_AAChange_refGene_columns(2), 'order': 207},
        {'name': 'ANN_AAChange_refGene_coding', 'col_name': 'AAChange.refGene', 'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'ANN_AAChange_refGene', 'l_multi': ANN_AAChange_refGene_columns(3), 'order': 208},
        {'name': 'ANN_AAChange_refGene_protein', 'col_name': 'AAChange.refGene', 'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'ANN_AAChange_refGene', 'l_multi': ANN_AAChange_refGene_columns(4), 'order': 209},
        {'name': 'ANN_cytoBand', 'col_name': 'cytoBand', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'order': 210},

        {'name': 'ANN_ExAC_ALL', 'col_name': 'ExAC_ALL', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 211},
        {'name': 'ANN_ExAC_AFR', 'col_name': 'ExAC_AFR', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 212},
        {'name': 'ANN_ExAC_AMR', 'col_name': 'ExAC_AMR', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 213},
        {'name': 'ANN_ExAC_EAS', 'col_name': 'ExAC_EAS', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 214},
        {'name': 'ANN_ExAC_FIN', 'col_name': 'ExAC_FIN', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 215},
        {'name': 'ANN_ExAC_NFE', 'col_name': 'ExAC_NFE', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 216},
        {'name': 'ANN_ExAC_OTH', 'col_name': 'ExAC_OTH', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 217},
        {'name': 'ANN_ExAC_SAS', 'col_name': 'ExAC_SAS', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 218},

        {'name': 'ANN_avsnp147', 'col_name': 'avsnp147', 'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'component': 'freetext', 'order': 219},

        {'name': 'ANN_SIFT_score', 'col_name': 'SIFT_score', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 220},
        {'name': 'ANN_SIFT_pred', 'col_name': 'SIFT_pred', 'type': 'CharField', 'parameters': {'max_length': '10', 'null': 'True'}, 'order': 221},

        {'name': 'ANN_Polyphen2_HDIV_score', 'col_name': 'Polyphen2_HDIV_score', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 222},
        {'name': 'ANN_Polyphen2_HDIV_pred', 'col_name': 'Polyphen2_HDIV_pred', 'type': 'CharField', 'parameters': {'max_length': '10', 'null': 'True'}, 'order': 223},
        {'name': 'ANN_Polyphen2_HVAR_score', 'col_name': 'Polyphen2_HVAR_score', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 224},
        {'name': 'ANN_Polyphen2_HVAR_pred', 'col_name': 'Polyphen2_HVAR_pred', 'type': 'CharField', 'parameters': {'max_length': '10', 'null': 'True'}, 'order': 225},

        {'name': 'ANN_LRT_score', 'col_name': 'LRT_score', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 226},
        {'name': 'ANN_LRT_pred', 'col_name': 'LRT_pred', 'type': 'CharField', 'parameters': {'max_length': '10', 'null': 'True'}, 'order': 228},

        {'name': 'ANN_MutationTaster_score', 'col_name': 'MutationTaster_score', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 229},
        {'name': 'ANN_MutationTaster_pred', 'col_name': 'MutationTaster_pred', 'type': 'CharField', 'parameters': {'max_length': '10', 'null': 'True'}, 'order': 230},
        {'name': 'ANN_MutationAssessor_score', 'col_name': 'MutationAssessor_score', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 231},
        {'name': 'ANN_MutationAssessor_pred', 'col_name': 'MutationAssessor_pred', 'type': 'CharField', 'parameters': {'max_length': '10', 'null': 'True'}, 'order': 232},

        {'name': 'ANN_FATHMM_score', 'col_name': 'FATHMM_score', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 233},
        {'name': 'ANN_FATHMM_pred', 'col_name': 'FATHMM_pred', 'type': 'CharField', 'parameters': {'max_length': '10', 'null': 'True'}, 'order': 234},

        {'name': 'ANN_PROVEAN_score', 'col_name': 'PROVEAN_score', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 235},
        {'name': 'ANN_PROVEAN_pred', 'col_name': 'PROVEAN_pred', 'type': 'CharField', 'parameters': {'max_length': '10', 'null': 'True'}, 'order': 236},

        {'name': 'ANN_VEST3_score', 'col_name': 'VEST3_score', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 237},

        {'name': 'ANN_CADD_raw', 'col_name': 'CADD_raw', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 238},
        {'name': 'ANN_CADD_phred', 'col_name': 'CADD_phred', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 239},
        {'name': 'ANN_DANN_score', 'col_name': 'DANN_score', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 240},
        
        {'name': 'ANN_fathmm_MKL_coding_score', 'col_name': 'fathmm-MKL_coding_score', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 241},
        {'name': 'ANN_fathmm_MKL_coding_pred', 'col_name': 'fathmm-MKL_coding_pred', 'type': 'CharField', 'parameters': {'max_length': '10', 'null': 'True'}, 'order': 242},
        
        {'name': 'ANN_MetaSVM_score', 'col_name': 'MetaSVM_score', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 243},
        {'name': 'ANN_MetaSVM_pred', 'col_name': 'MetaSVM_pred', 'type': 'CharField', 'parameters': {'max_length': '10', 'null': 'True'}, 'order': 244},
        {'name': 'ANN_MetaLR_score', 'col_name': 'MetaLR_score', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 245},
        {'name': 'ANN_MetaLR_pred', 'col_name': 'MetaLR_pred', 'type': 'CharField', 'parameters': {'max_length': '10', 'null': 'True'}, 'order': 246},
        
        {'name': 'ANN_integrated_fitCons_score', 'col_name': 'integrated_fitCons_score', 'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 247},
        {'name': 'ANN_integrated_confidence_value', 'col_name': 'integrated_confidence_value',  'type': 'IntegerField', 'parameters': {'null': True}, 'xUnits': 10, 'l': lambda x: None if x == '.' else int(x) , 'order': 248},

        {'name': 'ANN_GERP', 'col_name': 'GERP++_RS',  'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 249},

        {'name': 'ANN_phyloP7way_vertebrate', 'col_name': 'phyloP7way_vertebrate',  'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 250},
        {'name': 'ANN_phyloP20way_mammalian', 'col_name': 'phyloP20way_mammalian',  'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 251},
        {'name': 'ANN_phastCons7way_vertebrate', 'col_name': 'phastCons7way_vertebrate',  'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 252},
        {'name': 'ANN_phastCons20way_mammalian', 'col_name': 'phastCons20way_mammalian',  'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 253},

        {'name': 'ANN_SiPhy_29way_logOdds', 'col_name': 'SiPhy_29way_logOdds',  'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'l': lambda x: None if x == '.' else float(x) , 'order': 254},

        {'name': 'ANN_CLNALLELEID', 'col_name': 'CLNALLELEID', 'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'component': 'freetext', 'order': 255},

        {'name': 'ANN_CLNDN', 'col_name': 'CLNDN', 'type': 'CharField', 'parameters': {'max_length': '10', 'null': 'True'}, 'database': 'multi_1', 'table': 'ANN_CLINVAR', 'l_multi': lambda x : x.split('|'), 'order': 256},
        {'name': 'ANN_CLNDISDB', 'col_name': 'CLNDISDB', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'database': 'multi_1', 'table': 'ANN_CLINVAR', 'l_multi': lambda x : x.split('|'), 'component': 'freetext', 'order': 257},
        
        {'name': 'ANN_CLNREVSTAT', 'col_name': 'CLNREVSTAT', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'order': 258},
        {'name': 'ANN_CLNSIG', 'col_name': 'CLNSIG', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'order': 259},

        ########## FIELDS FROM VEP #########
        #{'name': 'VEP_Feature', 'col_name': 'Feature', 'type': 'CharField', 'parameters': {'max_length': '200', 'null': 'True'}, 'l': lambda x:x.split('|')[0], 'order': 94},      
        {'name': 'VEP_Allele', 'col_name': 'Allele',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 301},
        {'name': 'VEP_Consequence', 'col_name': 'Consequence',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 302},
        {'name': 'VEP_IMPACT', 'col_name': 'IMPACT',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 302},
        {'name': 'VEP_SYMBOL', 'col_name': 'SYMBOL',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 303},
        {'name': 'VEP_Gene', 'col_name': 'Gene',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 303},
        {'name': 'VEP_Feature_type', 'col_name': 'Feature_type',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 304},
        {'name': 'VEP_Feature', 'col_name': 'Feature',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 305},
        {'name': 'VEP_BIOTYPE', 'col_name': 'BIOTYPE',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 306},
        {'name': 'VEP_EXON', 'col_name': 'EXON',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 307},
        {'name': 'VEP_INTRON', 'col_name': 'INTRON',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 308},
        {'name': 'VEP_HGVSc', 'col_name': 'HGVSc',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 309},
        {'name': 'VEP_HGVSp', 'col_name': 'HGVSp',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 310},
        
        {'name': 'VEP_cDNA_position', 'col_name': 'cDNA_position',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 311},
        {'name': 'VEP_CDS_position', 'col_name': 'CDS_position',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 312},
        {'name': 'VEP_Amino_acids', 'col_name': 'Amino_acids',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 313},
        {'name': 'VEP_Codons', 'col_name': 'Codons',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 314},
        {'name': 'VEP_Existing_variation', 'col_name': 'Existing_variation',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'compoent': 'freetext', 'l_multi': lambda x : x.split('|'), 'order': 315},
        {'name': 'VEP_DISTANCE', 'col_name': 'DISTANCE',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 316},
        {'name': 'VEP_STRAND', 'col_name': 'STRAND',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 317},
        {'name': 'VEP_FLAGS', 'col_name': 'FLAGS',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 318},
        {'name': 'VEP_VARIANT_CLASS', 'col_name': 'VARIANT_CLASS',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 319},
        {'name': 'VEP_SYMBOL_SOURCE', 'col_name': 'SYMBOL_SOURCE',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 320},
        {'name': 'VEP_HGNC_ID', 'col_name': 'HGNC_ID',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 321},
        {'name': 'VEP_CANONICAL', 'col_name': 'CANONICAL',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 322},
        {'name': 'VEP_TSL', 'col_name': 'TSL',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 323},

        {'name': 'VEP_APPRIS', 'col_name': 'APPRIS',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 324},
        {'name': 'VEP_CCDS', 'col_name': 'CCDS',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 325},
        {'name': 'VEP_ENSP', 'col_name': 'ENSP',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 326},
        {'name': 'VEP_SWISSPROT', 'col_name': 'SWISSPROT',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 327},
        {'name': 'VEP_TREMBL', 'col_name': 'TREMBL',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 328},
        {'name': 'VEP_UNIPARC', 'col_name': 'UNIPARC',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 329},
        {'name': 'VEP_GENE_PHENO', 'col_name': 'GENE_PHENO',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 330},
        {'name': 'VEP_SIFT', 'col_name': 'SIFT',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 331},
        {'name': 'VEP_PolyPhen', 'col_name': 'PolyPhen',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 332},
       # {'name': 'VEP_DOMAINS', 'col_name': 'DOMAINS',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': VEP_DOMAINS_f, 'order': 333}, # This is problematic. FIXME
        {'name': 'VEP_miRNA', 'col_name': 'miRNA',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 334},

        {'name': 'VEP_HGVS_OFFSET', 'col_name': 'HGVS_OFFSET',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 335},
        {'name': 'VEP_AF', 'col_name': 'AF',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 336},
        {'name': 'VEP_AFR_AF', 'col_name': 'AFR_AF',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 337},
        {'name': 'VEP_AMR_AF', 'col_name': 'AMR_AF',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 338},
        {'name': 'VEP_EAS_AF', 'col_name': 'EAS_AF',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 339},
        {'name': 'VEP_EUR_AF', 'col_name': 'EUR_AF',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 340},
        {'name': 'VEP_SAS_AF', 'col_name': 'SAS_AF',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 341},
        {'name': 'VEP_AA_AF', 'col_name': 'AA_AF',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 342},
        {'name': 'VEP_EA_AF', 'col_name': 'EA_AF',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 343},
        {'name': 'VEP_gnomAD_AF', 'col_name': 'gnomAD_AF',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 344},

        {'name': 'VEP_gnomAD_AFR_AF', 'col_name': 'gnomAD_AFR_AF',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 345},
        {'name': 'VEP_gnomAD_AMR_AF', 'col_name': 'gnomAD_AMR_AF',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 346},
        {'name': 'VEP_gnomAD_ASJ_AF', 'col_name': 'gnomAD_ASJ_AF',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 347},
        {'name': 'VEP_gnomAD_EAS_AF', 'col_name': 'gnomAD_EAS_AF',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 348},
        {'name': 'VEP_gnomAD_FIN_AF', 'col_name': 'gnomAD_FIN_AF',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 349},
        {'name': 'VEP_gnomAD_NFE_AF', 'col_name': 'gnomAD_NFE_AF',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 350},
        {'name': 'VEP_gnomAD_OTH_AF', 'col_name': 'gnomAD_OTH_AF',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 351},
        {'name': 'VEP_gnomAD_SAS_AF', 'col_name': 'gnomAD_SAS_AF',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 352},
        {'name': 'VEP_MAX_AF', 'col_name': 'MAX_AF',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 353},
        {'name': 'VEP_MAX_AF_POPS', 'col_name': 'MAX_AF_POPS',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 354},

        {'name': 'VEP_CLIN_SIG', 'col_name': 'CLIN_SIG',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 355},
        {'name': 'VEP_SOMATIC', 'col_name': 'SOMATIC',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 356},
        {'name': 'VEP_PHENO', 'col_name': 'PHENO',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 357},
        {'name': 'VEP_PUBMED', 'col_name': 'PUBMED',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 358},
        {'name': 'VEP_MOTIF_NAME', 'col_name': 'MOTIF_NAME',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 359},
        {'name': 'VEP_MOTIF_POS', 'col_name': 'MOTIF_POS',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 360},
        {'name': 'VEP_HIGH_INF_POS', 'col_name': 'HIGH_INF_POS',  'type': 'CharField', 'parameters': {'max_length': '100', 'null': 'True'}, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : x.split('|'), 'order': 361},
        {'name': 'VEP_MOTIF_SCORE_CHANGE', 'col_name': 'MOTIF_SCORE_CHANGE',  'type': 'FloatField', 'parameters': {'null': 'True'}, 'xUnits': 10, 'database': 'multi_1', 'table': 'VEP_MULTI', 'l_multi': lambda x : [(None if y=='' else float(y)) for y in x.split('|')], 'order': 362},

        # Custom Clinvar parser
        {'name': 'CLINVARZAZZ_interpretation', 'col_name': 'ClinVar_ZAZZCLINVAR', 'type': 'CharField', 'parameters': {'max_length': '255', 'null': 'True'}, 'database': 'multi_1', 'table': 'ZAZZ_CLINVAR', 'l_multi': zazz_clinvarzazz_f('interpretation'), 'l_raw_multi': lambda x : '|'.join(map(str, x)), 'order': 401},
        {'name': 'CLINVARZAZZ_scv_review_status', 'col_name': 'ClinVar_ZAZZCLINVAR', 'type': 'CharField', 'parameters': {'max_length': '255', 'null': 'True'}, 'database': 'multi_1', 'table': 'ZAZZ_CLINVAR', 'l_multi': zazz_clinvarzazz_f('scv_review_status'), 'l_raw_multi': lambda x : '|'.join(map(str, x)), 'order': 402},
        {'name': 'CLINVARZAZZ_clinical_significance', 'col_name': 'ClinVar_ZAZZCLINVAR', 'type': 'CharField', 'parameters': {'max_length': '255', 'null': 'True'}, 'database': 'multi_1', 'table': 'ZAZZ_CLINVAR', 'l_multi': zazz_clinvarzazz_f('clinical_significance'), 'l_raw_multi': lambda x : '|'.join(map(str, x)), 'order': 403},
        {'name': 'CLINVARZAZZ_condition_name', 'col_name': 'ClinVar_ZAZZCLINVAR', 'type': 'CharField', 'parameters': {'max_length': '255', 'null': 'True'}, 'database': 'multi_1', 'table': 'ZAZZ_CLINVAR', 'l_multi': zazz_clinvarzazz_f('condition_name'), 'l_raw_multi': lambda x : '|'.join(map(str, x)), 'order': 404},
        {'name': 'CLINVARZAZZ_rcv_review_status', 'col_name': 'ClinVar_ZAZZCLINVAR', 'type': 'CharField', 'parameters': {'max_length': '255', 'null': 'True'}, 'database': 'multi_1', 'table': 'ZAZZ_CLINVAR', 'l_multi': zazz_clinvarzazz_f('rcv_review_status'), 'l_raw_multi': lambda x : '|'.join(map(str, x)), 'order': 405},
        {'name': 'CLINVARZAZZ_review_status_stars', 'col_name': 'ClinVar_ZAZZCLINVAR', 'type': 'CharField', 'parameters': {'max_length': '255', 'null': 'True'}, 'database': 'multi_1', 'table': 'ZAZZ_CLINVAR', 'l_multi': zazz_clinvarzazz_f('review_status_stars'), 'l_raw_multi': lambda x : '|'.join(map(str, x)), 'order': 406},
    ]    

    print ('TOTAL FIELDS: {}'.format(len(fields)))
    
    externals = []
    create_table('Samples', fields, externals)
    create_js(fields)

    return fields

def import_annotated_vcf(filename, fields):
    '''
    '''
    

    # Loading annotated VCF
    print (f'Import annotated VCF: {filename}')
    print ('Loading..')
    df = pd.read_excel(filename)
    print ('    DONE')
        

    print ('Importing:', filename)
    externals = []
    import_data(df, fields, 'Samples', externals)



def init_globals():
    g['list_of_chromosomes'] = list_of_chromosomes()
    g['accumulate_chromosome_sizes_hg19'] = accumulate_chromosome_sizes_hg19()

def vep(vcf_input, vcf_output):
    '''
    Create a potential VEP command
    '''

    command = r'''
time ./ensembl-vep-release-96/vep \
    -i {vcf_input} \
    --fork 6  \
    --cache --dir_cache /home/kantale/VEP/homo_sapiens_vep_96_GRCh37/ \
    --force_overwrite \
    --offline \
    --everything \
    --fasta /home/kantale/VEP/fasta/Homo_sapiens.GRCh37.dna.primary_assembly.fa.gz --assembly GRCh37 \
    --vcf  \
    -o {vcf_output}
'''.format(vcf_input=vcf_input, vcf_output=vcf_output)

    return command

def clinvar_vep(vcf_input, vcf_output):
    command = r'''
time ./ensembl-vep-release-96/vep \
    -i {vcf_input} \
    --fork 6 \
    --species homo_sapiens \
    --cache \
    --offline \
    --assembly GRCh37\
     --vcf \
     --custom /home/kantale/VEP/clinvar.vcf.gz,ClinVar,vcf,exact,0,ZAZZCLINVAR \
     -o {vcf_output}
'''.format(vcf_input=vcf_input, vcf_output=vcf_output)

    return command

def iontorrent_raw_vcf_parser(filename):
    '''
    '''

    def create_zazz_field(name, type_, order):
        '''
        {'name': 'ION_Chromosome', 'col_name': '# locus', 'type': 'CharField', 'parameters': {'max_length': '100'}, 'l': lambda x: x.split(':')[0], 'order': 1},
        '''

        #print ('name={}, type={}, order={}'.format(name, type_, order))

        zazz_db_dict = {
            'Float' : 'FloatField',
            'Integer': 'IntegerField',
            'String': 'CharField',
            'Flag': 'CharField',
        }

        zazz_db_params = {
            'Float' : "{}",
            'Integer': "{}",
            'String': "{'max_length': '100', 'null': 'True'}",
            'Flag': "{'max_length': '100', 'null': 'True'}",
        }

        ret = "{{'name':'RAW_{name}', 'col_name': '{name}', 'type': '{type_}', 'parameters': {parameters}, 'l': lambda x:x, 'order': {order} }},".format(
            name=name,
            type_=zazz_db_dict[type_],
            parameters=zazz_db_params[type_],
            order=order,
            )

        return ret


    def parse_vcf_info_header(l):
        '''
        ##INFO=<ID=NS,Number=1,Type=Integer,Description="Number of samples with data">
        '''

        m = re.search(r'##INFO=<ID=([\w]+),Number=[\w\.],Type=([\w]+)', l)
        if not m:
            raise ZazzException('Could not parse INFO header: {}'.format(l))

        return {
            'id': m.group(1),
            'type': m.group(2),
        }

    def parse_vcf_format_header(l):
        '''
        ##FORMAT=<ID=FRO,Number=1,Type=Integer,Description="Flow Evaluator Reference allele observation count">
        '''
        m = re.search(r'##FORMAT=<ID=([\w]+),Number=[\w\.],Type=([\w]+)', l)
        if not m:
            raise ZazzException('Could not parse FORMAT header: {}'.format(l))
        return {
            'id': m.group(1),
            'type': m.group(2),
        }

    def vcf_type_converter(type_name, v):
        if type_name == 'Float':
            return float(v)
        elif type_name == 'Integer':
            return int(v)
        elif type_name == 'String':
            return v
        else:
            raise ZazzException('Do not know how to convert info type: {}'.format(type_name))


    print ('Parsing RAW IonTorrent file:', filename)

    info_data = {}
    format_data = {}
    errors = defaultdict(int)

    c = 0
    with open(filename) as f:
        for l in f:
            c += 1

            if c%10000 == 0:
                print ('Lines: {}'.format(c))

            if l.startswith('##INFO'):
                info_dict = parse_vcf_info_header(l)
                info_data[info_dict['id']] = info_dict
                continue

            if l.startswith('##FORMAT'):
                format_dict = parse_vcf_format_header(l)
                format_data[format_dict['id']] = format_dict

            if l[0] == '#':
                continue
    
            #print (info_data) 
            #print (format_data)
            #a=1/0          

            if False:
                '''
                Create fields
                '''
                order = 0
                for k,v in info_data.items():
                    order+=1
                    r = create_zazz_field(k, v['type'], order)
                    print (r)
                for k,v in format_data.items():
                    order+=1
                    r = create_zazz_field('GT_' + k, v['type'], order)
                    print (r)

                a=1/0


            ls = l.strip().split()
            record = {}

            record['Chromosome'] = chromosome_unifier(ls[0])
            record['Position'] = int(ls[1])
            record['Reference'] = ls[3]
            record['Alternative'] = ls[4]

            if ',' in record['Alternative']:
                errors['When allele_1 <> allele_2 <> reference. The variant is removed. TO BE FIXED!'] += 1
                continue

            record['QUAL'] = float(ls[5])
            info = ls[7]

            try:
                info_dict = dict(x.split('=') for x in info.split(';'))
                for k,v in info_dict.items():
                    this_type = info_data[k]['type']
                    record[k] = vcf_type_converter(this_type, v)

                for k,v in info_data.items():
                    if not k in record:
                        record[k] = None

                format_ = ls[8].split(':')
                gt = ls[9].split(':')

                gt_dict = dict(zip(format_, gt))
                for k, v in gt_dict.items():
                    this_type = format_data[k]['type']
                    record['GT_' + k] = vcf_type_converter(this_type, v)

                for k,v in format_data.items():
                    if not 'GT_' + k in record:
                        record['GT_' + k] = None

            except ValueError as e:
                message = 'Could not convert {}={} to type {}\n'.format(k, v, this_type)
                message += 'Line:\n'
                message += l
                raise ZazzException(message)


            yield (record)
            #a=1/0


    print ('Errors:')
    print (json.dumps(errors, indent=4))

    print ('Done parsing RAW Iontorret file:', filename)

def annovar_vcf_parser(filename):
    '''
    http://annovar.openbioinformatics.org/en/latest/misc/accessory/
    The ANNOVAR_DATE marks the start of ANNOVAR annotation, whereas ALLELE_END marks the end of ANNOVAR annotation for this variant.

    dist\x3d35 ?? 
    '''

    print ('Parsing ANNOVAR VCF FILE:', filename)

    c = 0
    error_1 = 0
    error_2 = 0
    fields = None
    with open(filename) as f:
        for l in f:
            c += 1
            if l[0] == '#':
                continue
            
                if c % 10000 == 0:
                    print ('Lines: ', c)

            ls = l.strip().split()
            chromosome = ls[0]
            try: 
                position = int(ls[1])
            except ValueError as e:
                print ('Could not parse position in line:', c)
                error_1 += 1
                continue

            reference = ls[3]
            alternative = ls[4]
            annovar_s = ls[7]

            if annovar_s.count('ALLELE_END') != 1:
                print ('More than one ALLELE_END in line:', c)
                error_2 += 1

            s = re.search(r'ANNOVAR_DATE.*ALLELE_END', l)
            record = dict([x.split('=') for x in s.group(0).split(';') if '=' in x])

            # Make sure that all variants have the same fields
            if fields is None:
                fields = set(record.keys())
            else:
                assert set(record.keys()) == fields
        
            #Create record to add
            record['Chromosome'] = chromosome_unifier(chromosome)
            record['Position'] = position
            record['Reference'] = reference
            record['Alternative'] = alternative

            yield record

    
    print ('FINISHED PARSING ', filename)
    print ('Errors:')
    print ('Could not parse chromosome:', error_1)
    print ('Greater than 2 alleles:', error_2) # FIX ME

def vep_vcf_parser(filename):
    print ('Parsing VEP VCF FILE:', filename)

    def parse_info(line):
        description_s = re.search(r'Description="(.+)"', line)
        description = description_s.group(1)
        #print ('description:')
        #print (description)
        format_s = re.search(r'Format: (.+)', description)
        if not format_s:
            return None
        format_ = format_s.group(1)
        #print (format_)
        ret = format_.split('|')
        #print (ret)
        return ret


    c = 0
    field_names = None
    with open(filename) as f:

        record_counter = defaultdict(list)

        for l in f:

            c += 1
            if l[0] == '#':
                if re.match(r'^##INFO', l):
                    field_names_temp = parse_info(l)
                    if field_names_temp:
                        if field_names:
                            assert False
                        field_names = field_names_temp
                continue
            
            if c % 10000 == 0:
                print (print_now(), 'Lines: ', c)

            ls = l.strip().split()
            chromosome = ls[0]
            position = int(ls[1])
            reference =  ls[3]
            alternative = ls[4]
            info_field = ls[7]
            if info_field == '.':
                continue

            info_multi = info_field.split(',')
            #print ('INFO MULTIS:', len(info_multi))

            record_all = defaultdict(set)
            record_to_yield = {}

            for info in info_multi:
                info_s = info.split('|')
                #print ('INFO LEN:')
                #print (len(info_s))
                #print ('INFO:')
                #print (info)
                #print ('INFO SPLITTED:')
                #print (info_s)
                #print (len(field_names))
                #print (field_names)

                if len(info_s) != len(field_names):
                    print ('ERROR!! MISMATCHING FIELDS / VALUES')
                    print ('LINE:')
                    print (l)
                    print ('INFO LEN:')
                    print (len(info_s))
                    print ('INFO:')
                    print (info)
                    print ('INFO SPLITTED:')
                    print (info_s)
                    print (len(field_names))
                    print (field_names)
                    assert False


                record = dict(zip(field_names, info_s))
                #print ('record:')
                #print (record)

                for record_key, record_value in record.items():
                    record_all[record_key].add(record_value)

                    # record_to_yield is not a defaultdict(list), because at the end of the day it will contain strings
                    if record_key in record_to_yield:
                        record_to_yield[record_key].append(record_value)
                    else:
                        record_to_yield[record_key] = [record_value]

            # Convert to strings
            for field_name in field_names:
                record_to_yield[field_name] = '|'.join(record_to_yield[field_name])

            # Add standard fields
            record_to_yield['Chromosome'] = chromosome_unifier(chromosome)
            record_to_yield['Position'] = position
            record_to_yield['Reference'] = reference
            record_to_yield['Alternative'] = alternative

            #print ('record_to_yield:')
            #print (record_to_yield)
            yield record_to_yield
            #a=1/0



                #print ('===========================================')
                #print ('===========================================')

            #print ('record all:')
            #print (record_all)

            for record_key, record_item in record_all.items():
                record_counter[record_key].append(len(record_item))

            #print ('record counter:')
            #print (record_counter)

        print ('AVERAGE COUNTS:')
        for record_key, record_item in record_counter.items():
            print ('{} --> {}'.format(record_key, np.mean(record_item)))

        



def import_file_as_pandas(filename, fields, first, filetype, **kwargs):
    '''
    import_data accepts a pandas dataframe.
    So, we convert VCF to pandas dataframe

    if first is True then create chromosome,Position entries
    '''

    print ('Creating pandas object from: ', filename)
    vcf_parser = kwargs.get('vcf_parser')

    if filetype == 'vcf':
        record_generator = vcf_parser(filename)
        d = defaultdict(list)

        for record in record_generator:
            for k,v in record.items():
                d[k].append(v)

        df = pd.DataFrame(d)
    elif filetype == 'excel':
        print ('Reading excel file:', filename)
        df = pd.read_excel(filename)
        # Add Chromosome, Position, Reference, Alternative
        chr_pos_ref_alt_getter = kwargs.get('chr_pos_ref_alt_getter')
        if not chr_pos_ref_alt_getter:
            raise ZazzException('chr_pos_ref_alt_getter is not declared')

        print ('Adding chromosome, position, reference, alternative columns..')
        df['Chromosome'] = df.apply(chr_pos_ref_alt_getter['Chromosome'], axis=1)
        df['Position'] = df.apply(chr_pos_ref_alt_getter['Position'], axis=1)
        df['Reference'] = df.apply(chr_pos_ref_alt_getter['Reference'], axis=1)
        df['Alternative'] = df.apply(chr_pos_ref_alt_getter['Alternative'], axis=1)
        print ('   ...Done')
    else:
        raise ZazzException('Unknown filetype: {}'.format(filetype))

    #Converting pandas to VCF
    save_to_vep_vcf = kwargs.get('save_to_vep_vcf')
    if save_to_vep_vcf:
        '''
        Convert a pandas to VCF. This can be the input to VEP
        '''
        fields_dict = {field['name']: field for field in fields}

        def alternative_f(x):
            return ','.join(list(set(x['genotype'].split('/')) - set(x['ref'])))

        pandas_to_vcf(
            df, 
            lambda x : x['Chromosome'],
            lambda x : x['Position'],
            lambda x : x['Reference'],
            lambda x : x['Alternative'],
            save_to_vep_vcf)

        print ('Possible VEP command:')
        print (vep(save_to_vep_vcf,  os.path.splitext(save_to_vep_vcf)[0] + '_vep_output.vcf'))
        print ('Possible ANNOVAR command:')
        print (annovar(save_to_vep_vcf, os.path.splitext(save_to_vep_vcf)[0] + '_annovar_output'))
        print ('Possible CLINVAR custom annotatiom with VEP command:')
        print (clinvar_vep(save_to_vep_vcf, os.path.splitext(save_to_vep_vcf)[0] + '_vep_clinvar_output.vcf'))

    print ('Done creating pandas object from filename:', filename)
    
    externals = []
    if first:
        import_data(df, fields, 'Samples', externals, **kwargs)
    else:
        import_data_append(df, fields, 'Samples', externals, **kwargs)


def annovar(vcf_input, vcf_output):
    '''
    Create a potential annovar command 
    '''
    
    command = r'''
    time ./table_annovar.pl {vcf_input} humandb/ \
    -buildver hg19 \
    -remove \
    -protocol refGene,cytoBand,exac03,avsnp147,dbnsfp30a,clinvar_20190305 -operation g,r,f,f,f,f \
    -nastring . \
    -vcfinput \
    -out {vcf_output} 
'''.format(vcf_input=vcf_input, vcf_output=vcf_output)

    return command

def ionreporter_excel_get_chr_pos_ref_alt():
    return {
        'Chromosome' : lambda x : chromosome_unifier(x['# locus'].split(':')[0]),
        'Position' : lambda x : int(x['# locus'].split(':')[1]),
        'Reference' : lambda x : x['ref'],
        'Alternative' : lambda x : list(set(x['genotype'].split('/')) - set([x['ref']]))[0],
    }

if __name__ == '__main__':
    '''
    '''

    init_globals()


    fields = setup_1()

    # Raw
    import_file_as_pandas('data/iontorrent_raw.vcf', fields, True, 'vcf', to_append_re = r'^RAW_', vcf_parser = iontorrent_raw_vcf_parser, save_to_vep_vcf='data/iontorrent_raw_vep_input.vcf')
    # Ion Reporter
    import_file_as_pandas('data/ionreporter.xlsx', fields, False, 'excel', to_append_re = r'^ION_', chr_pos_ref_alt_getter = ionreporter_excel_get_chr_pos_ref_alt())
    # Annovar
    import_file_as_pandas('data/annovar.vcf', fields, False, 'vcf', to_append_re = r'^ANN_', vcf_parser = annovar_vcf_parser)
    # VEP
    import_file_as_pandas('data/vep.vcf', fields, False, 'vcf', to_append_re=r'VEP_', vcf_parser=vep_vcf_parser)
    # Custom ClinVar 
    import_file_as_pandas('data/clinvar.vcf', fields, False, 'vcf', to_append_re=r'CLINVARZAZZ_', vcf_parser=vep_vcf_parser)






