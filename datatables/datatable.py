# Django
from django.http import HttpResponse
from django.template import Context
from django.template.loader import select_template
from django.utils.copycompat import deepcopy
from django.utils.datastructures import SortedDict
from django.utils.safestring import mark_safe
from django.db.models import Q

# Django DataTables
from columns import Column, BoundColumn
from utils import dumpjs, hungarian_to_python, lookupattr

__all__ = ['DataTable']

class DataTableOptions(object):
    """Container class for DataTable options defined via the Meta class."""

    def __init__(self, options=None):
        self.id = getattr(options, 'id', 'datatable_%d' % id(self))
        self.classes = getattr(options, 'classes', [])
        if isinstance(self.classes, basestring):
            self.classes = self.classes.split()
        self.classes = set(self.classes)
        self.width = str(getattr(options, 'width', '100%'))
        self.border = str(getattr(options, 'border', '0'))
        self.cellpadding = str(getattr(options, 'cellpadding', '0'))
        self.cellspacing = str(getattr(options, 'cellspacing', '0'))
        self.model = getattr(options, 'model', None)
        self.options = {}
        for name in dir(options):
            if name.startswith('_'):
                continue
            value = getattr(options, name)
            try:
                self.options[name] = hungarian_to_python(name, value)
            except NameError:
                pass

class DataTableDeclarativeMeta(type):
    """Metaclass for capturing declarative attributes on a DataTable class."""

    def __new__(cls, name, bases, attrs):
        columns = [(c, attrs.pop(c)) for c, obj in attrs.items() \
                  if isinstance(obj, Column)]
        columns.sort(key=lambda x: x[1].creation_counter)
        for base in reversed(bases):
            columns = getattr(base, 'base_columns', {}).items() + columns
        attrs['base_columns'] = SortedDict(columns)
        new_class = super(DataTableDeclarativeMeta, cls).__new__(cls, name, bases, attrs)
        # FIXME: Need to merge superclass Meta options, if present.
        new_class._meta = DataTableOptions(getattr(new_class, 'Meta', None))
        return new_class

class DataTable(object):
    """Base class for defining a DataTable and options."""

    __metaclass__ = DataTableDeclarativeMeta

    def __init__(self, data=None, name=''):
        self.columns = deepcopy(self.base_columns)

    @property
    def id(self):
        return self._meta.id

    @property
    def classes(self):
        return ' '.join(self._meta.classes)

    @property
    def width(self):
        return self._meta.width

    @property
    def border(self):
        return self._meta.border

    @property
    def cellpadding(self):
        return self._meta.cellpadding

    @property
    def cellspacing(self):
        return self._meta.cellspacing

    def bound_columns(self):
        if not getattr(self, '_bound_columns', None):
            self._bound_columns = SortedDict([
                (name, BoundColumn(self, column, name)) \
                for name, column in self.columns.items()])
        return self._bound_columns

    def base_queryset(self):
        """Return the base queryset to be used for this table."""
        return self._meta.model._default_manager.get_query_set()

    def get_queryset(self):
        """Method for subclasses to override to customize the queryset."""
        return self.base_queryset()

    def update_queryset(self, qs):
        self._qs = qs

    def apply_ordering(self, qs):
        #qs = qs.order_by(*sort_fields)
        return qs

    def get_results(self):
        qs = self.get_queryset()
        qs = self.apply_ordering(qs)
        return qs

    def results(self):
        if self._meta.options.get('bServerSide', False):
            return ''
        else:
            return self.get_results()

    def js_options(self):
        options = deepcopy(self._meta.options)
        columns = self.bound_columns()
        aoColumnDefs = options.setdefault('aoColumnDefs', [])
        colopts = SortedDict()
        for index, name in enumerate(columns.keys()):
            column = columns[name]
            for key, value in column.options.items():
                if not (key, str(value)) in colopts.keys():
                    colopts[(key, str(value))] = {}
                    colopts[(key, str(value))]['targets'] = []
                colopts[(key, str(value))]['targets'] = colopts[(key, str(value))]['targets'] + [index]
                colopts[(key, str(value))]['key'] = key
                colopts[(key, str(value))]['value'] = value
            if column.sort_field != column.display_field and column.sort_field in columns:
                key = 'iDataSort'
                value = columns.keys().index(column.sort_field)
                if not (key, str(value)) in colopts.keys():
                    colopts[(key, str(value))] = {}
                    colopts[(key, str(value))]['targets'] = []
                colopts[(key, str(value))]['targets'] = colopts[(key, str(value))]['targets'] + [index]
                colopts[(key, str(value))]['key'] = key
                colopts[(key, str(value))]['value'] = value
        for kv, values in colopts.items():
            aoColumnDefs.append(dict([(values['key'], values['value']), ('aTargets', values['targets'])]))
        return mark_safe(dumpjs(options))

    def process_request(self, request, name='datatable'):
        setattr(request, name, self)
        
    def process_response(self, request, response):
        if 'sEcho' in request.GET:# and request.is_ajax():
            return self.handle_ajax(request)
        else:
            return response

    def handle_ajax(self, request):
        params = {}
        for name, value in request.GET.items():
            try:
                params[name] = hungarian_to_python(name, value)
            except NameError:
                pass
        # Handle Sorting
        sorting_cols = []
        for count in range(params.get('iSortingCols', 0)):
            sort_num = params['iSortCol_'+str(count)]
            sort_dir = params['sSortDir_'+str(count)]
            if sort_dir == 'desc':
                sort_str = '-' + self.bound_columns()[self.bound_columns().keys()[sort_num]].sort_field
            else:
                sort_str = self.bound_columns()[self.bound_columns().keys()[sort_num]].sort_field
            if params.get('bSortable_'+str(count), False):
                sorting_cols.append(sort_str)
        qs = self.get_queryset()
        qs = qs.order_by(*sorting_cols)
        # Handle Global Search
        search_fields = []
        search_term = params.get('sSearch', '')
        if search_term:
            for count in range(params.get('iColumns', 0)):
                if params.get('bSearchable_'+str(count), True):
                    search_fields.append(self.bound_columns()[self.bound_columns().keys()[count]])
            qfilter = None
            for field in search_fields:
                # FIXME: Does not work for extra fields or foreignkey fields
                q = Q(**{'%s__icontains' % field.model_field: search_term})
                if qfilter is None:
                    qfilter = q
                else:
                    qfilter |= q
            if qfilter:
                qs = qs.filter(qfilter)
        # Handle Start and Length of display
        start = params.get('iDisplayStart', 0)
        end = params.get('iDisplayLength', self.get_results().count()) + start
        qs = qs[start:end]
        results = []
        for result in qs:
            row = []
            for name, bound_column in self.bound_columns().items():
                row.append(unicode(lookupattr(result, bound_column.display_field)))
            results.append(row)
        data = {
            'iTotalRecords': self.get_results().count(),
            'iTotalDisplayRecords': self.get_results().count(),
            'sEcho': request.GET['sEcho'],
            #'sColumns': ,
            'aaData': list(results)
        }
        print qs.query
        s = dumpjs(data)
        return HttpResponse(s, content_type='application/json')

    def as_html(self):
        t = select_template(['datatables/table.html'])
        return t.render(Context({'table': self}))
