from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Min, Max, Q, F

from zazz import models
from zazz.models import Samples

import simplejson

from functools import reduce
from operator import getitem
from itertools import product

# Create your views here.


def index(request):
    context = {
        "include_static": True,
    }
    port = request.META['SERVER_PORT']
    if int(port) == 8000:
        print ('WARNING!!! YOU ARE RUNNING IN DEFUALT PORT!')
        print ('static files (like angular.min.js) might get confused in the cache from other projects')
    return render(request, 'zazz/index.html', context)


def has_data(f):
    '''
    Decorator that passes AJAX data to a function parameters
    '''
    def wrapper(*args, **kwargs):
            request = args[0]
            if request.method == 'POST':
                    if len(request.POST):
                            for k in request.POST:
                                    kwargs[k] = request.POST[k]
                    else:
                            POST = simplejson.loads(request.body)
                            for k in POST:
                                    kwargs[k] = POST[k]
            elif request.method == 'GET':
                    for k in request.GET:
                            kwargs[k] = request.GET[k]
                            print ("GET: {} == {}".format(k, kwargs[k]))

            return f(*args, **kwargs)

    return wrapper

def returns_json(f):
    '''
    Decorator for functions that return a JSON responce
    '''
    def wrapper(*args, **kwargs):
        ret = f(*args, **kwargs)
        
        #Is this a HttpReponse?
        if type(ret) is HttpResponse:
            return ret
        
        ret_json = simplejson.dumps(ret)
        
        return HttpResponse(ret_json, content_type='application/json')
    
    return wrapper

@has_data
@returns_json
def sample_table(request, **kwargs):

    print (kwargs)

    order = kwargs['order']

    if order == 'asc':
        order_s = ''
    elif order == 'desc':
        order_s = '-' # https://stackoverflow.com/questions/9834038/django-order-by-query-set-ascending-and-descending 
    else:
        print ('THIS SHOULD NEVER HAPPEN')
        order_s = ''

    offset = kwargs['offset']
    limit = kwargs['limit']
    from_offset = int(offset)
    to_offset = from_offset + int(limit)

    if 'sort' in kwargs:
        sort = kwargs['sort']
    else:
        sort = 'id'

    count = Samples.objects.all().count()

    if 'filter' in kwargs:
        filter_ = kwargs['filter']
        filter_ = simplejson.loads(filter_)
        filter_ = {f + '__icontains' :f_value for f, f_value in filter_.items()}
        querySet = Samples.objects.filter(**filter_).order_by(order_s + sort)
        count = querySet.count()
        querySet = querySet[from_offset:to_offset]

    else:
        querySet = Samples.objects.order_by(order_s + sort)[from_offset:to_offset]

    ret = {'total': count}
    ret['rows'] = [{'sample': entry.sample, 'Bases': entry.Bases, 'Barcode_Name': entry.Barcode_Name} for entry in querySet]

    return ret


@has_data
@returns_json
def Barcode_Name(request, **kwargs):
    '''
    This runs only once
    '''
    ret = Samples.objects.order_by('Barcode_Name').values_list('Barcode_Name', flat=True).distinct()
    ret = {x:x for x in ret}
    return ret

@has_data
@returns_json
def get_database_checkbox(request, **kwargs):
    '''
    #Get all different values

$scope.itemArray = [
        {id: 1, name: 'first'},
        {id: 2, name: 'second'},
        {id: 3, name: 'third'},
        {id: 4, name: 'fourth'},
        {id: 5, name: 'fifth'},
    ];
    
    '''
    field = kwargs['field']
    database = kwargs['database']
    table = kwargs['table'] # Default: __ZAZZ__
    filter_ = kwargs.get('filter', {})

    print ('get_database_checkbox:')
    print ('field:', field)
    print ('database:', database)
    print ('table:', table)
    print ('fiter_:', filter_)

    if database == 'none_not_none':
        ret = []
        filter_[field + '__isnull'] = True
        if Samples.objects.filter(**filter_).exists():
            ret.append('Exists')

        filter_[field + '__isnull'] = False
        if Samples.objects.filter(**filter_).exists():
            ret.append('Missing')
    elif database == 'multi_1':
        #ret = set([y for x in Samples.objects.filter(**filter_).values_list(field, flat=True).distinct() for y in x])
        #ret = set(['|'.join(x) for x in Samples.objects.filter(**filter_).values_list(field, flat=True).distinct()])

        #Get the table object
        #table_obj = getattr(models, field)
        #ret = table_obj.objects.filter(**filter_).all().values_list(field, flat=True)

        table_obj = getattr(models, table)
        ret = [x[field] for x in table_obj.objects.filter(**filter_).values(field).distinct()]

        if '' in ret or None in ret:
            ret = ['<Empty>'] + sorted([x for x in ret if x])
        else:
            ret = sorted(ret)

    else:
        ret = Samples.objects.filter(**filter_).values_list(field, flat=True).distinct()
    ret = {
       'success': True,
       #'results': [{'id':i+1, 'name': x} for i,x in enumerate(ret)],  # {x:x for x in ret}
       'results': ['ALL'] + list(ret),  # {x:x for x in ret}
    }

    #print ('get_database_checkbox RETURNS:')
    #print (ret)

    return ret

@has_data
@returns_json
def get_database_slider(request, **kwargs): 
    '''
    Samples.objects.filter(**{}).aggregate(Max('Bases'))
    '''
    field = kwargs['field']
    filter_ = kwargs.get('filter', {})
    table = kwargs.get('table', None)

    print ('FROM: /get_database_slider/')
    print ('field')
    print (field)
    print ('filter_')
    print (filter_)
    print ('table:')
    print (table)

    if table:
        field = table + '__' + field

    ret = Samples.objects.filter(**filter_).aggregate(Min(field) , Max(field))
    ret_min = ret[field + '__min']
    ret_max = ret[field + '__max']

    ret = {
        'results': {
            'min': ret_min,
            'max': ret_max,
        },
        'success': True,
    }

    return ret

def multi_to_django_db(f):
    '''
    Location__multi ==> Location__Location
    '''
    ret = f.replace('__multi', '')
    ret = ret + '_multi__' + ret

    return ret 


def multi_to_django_raw(f):
    '''
    Location__multi ==> Location_raw
    '''
    ret = f.replace('__multi', '')
    ret = ret + '_raw'

    return ret

def multi_to_django_simple(f):
    '''
    Location__multi ==> Location
    '''

    return f.replace('__multi', '')

def create_splitter(sep):
    def f(x):
        if not x:
            return ['']

        return x.split(sep)

    return f


def expand(results, expanders, splitter, fields_not_in_expanders):
    '''
    results = [{'a':1, 'b':2, 'c': 'k|l', 'd': 'm|n'}]
    results = [{'a':1, 'b':2, 'c': 'k|l', 'd': 'm|n', 'e': 'o|p'}]
    expanders = {'t1': ['c', 'd'], 't2': ['e']}
    expanders = {'t': ['c', 'd']}
    expanders = {'t1': ['c'], 't2': ['d']}



    results = [{'Position': 93978, 'Chromosome': 'chr10', 'VEP_SYMBOL': 'TUBB8|TUBB8|TUBB8|RP11-631M21.6|TUBB8|TUBB8', 'CLINVARZAZZ_interpretation': 'None'}]
    expanders = {'VEP_MULTI': {'VEP_SYMBOL'}, 'ZAZZ_CLINVAR': {'CLINVARZAZZ_interpretation'}} 



    results = [{**dict(zip(bv, zipx)), **{xk:xv for xk, xv in x.items() if not xk in bv }} for x in results for bk,bv in expanders.items() for zipx in zip(*map(lambda lx : splitter(getitem(x, lx)), bv))]

    '''


    '''
    results2 = [
                {**dict(zip(expander_values, zipx)), 
                 **{result_key:result_value for result_key, result_value in result.items() if not result_key in expander_values }} 
                 for result in results 
                    for expander_key, expander_values in expanders.items() 
                        for zipx in zip(*map(lambda lambda_x : splitter(getitem(result, lambda_x)), expander_values))
                ]

    '''


    # In a single line:
    # [r for r in results for expanded in [ dict([yy for k in pi for yy in k]) for pi in list(product(*[ zip(*[ [(e_field, ss) for ss in r[e_field].split('|')] for e_field in e_v]) for e_k, e_v in expanders.items() ])) ]]
    return [
        {**expanded, **{fni:r[fni] for fni in fields_not_in_expanders}} for r in results 
            for expanded in [ 
                dict(
                    [
                        yy for k in pi for 
                            yy in k
                    ]
                    ) 
                for pi in list(
                    product(*[ 
                        zip(*[ 
                            [
                                (e_field, ss) for ss in splitter(r[e_field])] 
                                    for e_field in e_v
                              ]) 
                        for e_k, e_v in expanders.items() 
                    ])
                ) 
            ]
    ]






@has_data
@returns_json
def update_table(request, **kwargs):
    '''
    if max_filter > 0, Then bring that many records.
    otherwise bring them all.
    '''
    filter_ = kwargs['filter']
    order = kwargs['order']
    max_filter = kwargs['max_filter']

    print ('Filter:')
    print (filter_)

    print ('Order:')
    print (order)

    print ('Max filter:')
    print (max_filter)

    #Create database filters
    database_filters = {}
    annotators = {}
    required_fields = set()

    expanders = {}

    # filter_ = {'Chromosome__in': ['ALL'], 'Location__table': 'Transcripts', 'Location__multi': ['downstream'], 'Function__table': 'Transcripts', 'Function__multi': ['ALL']}
    for filter_key, filter_values in filter_.items():

        if '__multi' in filter_key:
            multi_name = filter_key.replace('__multi', '') # Location__multi --> Location
            table = filter_[multi_name + '__table'] # Location__table --> Transcripts
            multi_field_in = table + '__' + multi_name + '__in' # Transcripts__Location__in
            multi_field_icontains = table + '__' + multi_name + '__icontains' # Transcripts__Location__in
            multi_field_name = table + '__' + multi_name # Transcripts__Location
            multi_field_raw = multi_name + '_raw' # Location_raw
            multi_field_gte = table + '__' + multi_name + '__gte' # Transcripts__Sift__gte
            multi_field_lte = table + '__' + multi_name + '__lte' # Transcripts__Sift__lte

            annotators[multi_name] = F(multi_field_raw)
            required_fields.add(multi_name)

            if not table in expanders:
                expanders[table] = set()

            if not multi_name in expanders[table]:
                expanders[table].add(multi_name)

            if type(filter_values) is list:
                # List of allowed values
                multi_values = ['' if x == '<Empty>' else x for x in filter_values]
                if 'ALL' in multi_values:
                    # We do not actually have to filter on anything..
                    continue

                database_filters[multi_field_in] = multi_values
            elif type(filter_values) is str:
                # String. Perform an icontains
                if not filter_values:
                    # This is empty. Allow everything
                    continue

                database_filters[multi_field_icontains] = filter_values
            elif type(filter_values) is dict: # Passed from multi slider. Min ,Max
                print ('filter values:')
                print (filter_values)

                if 'min' in filter_values:
                    database_filters[multi_field_gte] = filter_values['min']
                if 'max' in filter_values:
                    database_filters[multi_field_lte] = filter_values['max']

            else:
                raise Exception('Error 489. Unknown type: {}'.format(type(filter_values).__name__))

        elif '__table' in filter_key:
            continue

        elif '__in' in filter_key:
            required_fields.add(filter_key.replace('__in', ''))
            if 'ALL' in filter_values:
                # We do not actually have to filter on anything
                continue
            database_filters[filter_key] = filter_values

        else:
            required_fields.add(filter_key.split('__')[0])
            database_filters[filter_key] = filter_values

    print ('Applied database filter:')
    print (database_filters)

    print ('Required Fields:')
    print (required_fields)

    print ('Annotators')
    print (annotators)

    #Create orderers
    orderers = [x[0] for x in sorted(order.items(), key=lambda x:x[1])]
    print ('Orderers:')
    print (orderers)

    #Check if ALL in items
    #If 'ALL' exists in any filter, do *not* query it in the database
    #filter2 = {k:v for k,v in filter_.items() if not (type(v) is list and 'ALL' in v)}

    #Create Q filters for multi. APPLIES OR!!!
    # The AND is more complex :https://stackoverflow.com/questions/8618068/django-filter-queryset-in-for-every-item-in-list TODO 
    #q_filters = [multi(k, v) for k,v in filter2.items() if '__multi' in k]
    #q_filters = [Q(**{multi_to_django_db(k) + '__in':v}) for k,v in filter2.items() if '__multi' in k]

    # Separate multi from non multi filter
    # Reason: https://docs.djangoproject.com/en/2.0/topics/db/queries/ 
    # ...However, if a Q object is provided, it must precede the definition of any keyword arguments. 
    #filter2 = {k:v for k,v in filter2.items() if not '__multi' in k}

    #print ('post process q filter:')
    #print (q_filters)

    #print ('post processed filter:')
    #print (filter2)
    
    print ('Quering...')
    #querySet = Samples.objects.filter(*q_filters, **filter2)
    querySet = Samples.objects.filter(**database_filters).distinct()

    #Ordering..
    if orderers:
        querySet = querySet.order_by(*orderers)

    count = querySet.count()

    #Take only the fields that we require
    #required_fields = list(set([multi_to_django_simple(x) if '__multi' in x else (x.split('__')[0]) for x in filter_.keys()]))

    # Rename multi values to the original
    # https://stackoverflow.com/questions/10598940/how-to-rename-items-in-values-in-django
    #annotators = {multi_to_django_simple(x):F(multi_to_django_raw(x)) for x in filter_.keys() if '__multi' in x }

    #print ('required_fields:')
    #print (required_fields)

    # values and M2M does not go well together...

    #In [33]: Samples.objects.filter(Location__Location__in=['intronic'], id=2).values_list('Location')
    #Out[33]: <QuerySet [(52,)]> <--- ONE OBJECT

    #In [34]: Samples.objects.filter(Location__Location__in=['intronic'], id=2)[0].Location.all()
    #Out[34]: <QuerySet [<Location: Location object (52)>, <Location: Location object (54)>]> # <-- 2 OBJECTS...
    if max_filter>0:
        results = list(querySet[:max_filter].annotate(**annotators).values(*required_fields))
    else:
        results = list(querySet.annotate(**annotators).values(*required_fields))


    #print ('RESULTS 1')
    #print (results)

    #Expand
    print ('Expanders:')
    print (expanders)

    # Values not in expanders
    if results:
        fields_not_in_expanders = list(set(results[0].keys()) - set(y for x in expanders.values() for y in x))
    else:
        fields_not_in_expanders = [] # Does not really matter.. since results is empty

    # a = {'a':1, 'b':2, 'c': 'k|l', 'd': 'm|n'}
    # b = {'t': ['c', 'd']} # <-- expanders
    # [dict(zip(v,n)) for x in a for k,v in b.items()  for n in zip(*map(lambda y: getitem(x,y).split('|'), v))  ]  

    #print ('Results BEFORE EXPANDER:')
    #results = [x for x in results if x['Position']==1650845]
    #print (f'COUNT: {len(results)}')
    #print (results)


    if expanders and max_filter<=0:
        # We expand only on explore
        splitter = create_splitter('|')
        #splitter = create_splitter(',')
        #print ('RESULTS BEFORE EXPANDING')
        #print (results)
        # results = [{'a':1, 'b':2, 'c': 'k|l', 'd': 'm|n'}]
        # expanders = {'t': ['c', 'd']}
        # [{'c': 'k', 'd': 'm', 'a': 1, 'b': 2}, {'c': 'l', 'd': 'n', 'a': 1, 'b': 2}] 

        #results = [{**dict(zip(bv, zipx)), **{xk:xv for xk, xv in x.items() if not xk in bv }} for x in results for bk,bv in expanders.items() for zipx in zip(*map(lambda lx : splitter(getitem(x, lx)), bv))]
        
        results = expand(results, expanders, splitter, fields_not_in_expanders)

        #print ('Expanded results:')
        #results = [x for x in results if x['Position']==1650845]
        #print (f'COUNT: {len(results)}')

        #print ('RESULTS AFTER EXPANDING:')
        #print (results)
        #print ('=============')

    #Filter according to max_filter
    #THIS IS VERY SLOW!!!!
    #if max_filter>0:
    #    results = querySet[:max_filter]
    #else:
    #    results = querySet
    #
    #def key_values(result, field):
    #
    #    if '__' in field:
    #        key = field.split('__')[0]
    #        value = '|'.join(list(getattr(result, key).values_list(key, flat=True)))
    #    else:
    #        key = field
    #        value = getattr(result, key)
    #
    #    return key, value
    #
    #print ('Getting ONLY required fields..')
    #results = [dict((key_values(r, f) for f in required_fields)) for r in results]




    #{'Location__Location': 'intronic'} --> {'Location': 'intronic'}
    # https://stackoverflow.com/questions/10598940/how-to-rename-items-in-values-in-django ### FIXME
    #results = [{(k.split('__')[0] if '__' in k else k):v  for k,v in r.items()}   for r in results]

    #print ('Results 2')
    #print (results)

#    # Take only the fields that we queried
#    results = [{k:v for k,v in r.items() if k in fields} for r in results]

    #print ('Results 2:')
    #print (results)

    return {
        'success': True,
        'results': results,
        'count': count,
    }

