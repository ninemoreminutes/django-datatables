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
        return mark_safe(dumpjs(options, indent=4, sort_keys=True))

    def process_request(self, request, name='datatable'):
        setattr(request, name, self)
        
    def process_response(self, request, response):
        if 'sEcho' in request.GET:# and request.is_ajax():
            return self.handle_ajax(request)
        else:
            return response

    def _handle_ajax_sorting(self, qs, params):
        bc = self.bound_columns()
        sort_fields = []
        iSortingCols = params.get('iSortingCols', 0)
        for i in range(iSortingCols):
            iSortCol = params.get('iSortCol_%d' % i, 0)
            bcol = bc.values()[iSortCol]
            sSortDir = params.get('sSortDir_%d' % i, '')
            bSortable = params.get('bSortable_%d' % i, True)
            bSortable = bSortable and bcol.options.get('bSortable', True)
            if not bSortable:
                continue
            sort_field = bcol.sort_field
            if sSortDir == 'desc':
                sort_field = '-%s' % sort_field
            sort_fields.append(sort_field)
        if sort_fields:
            qs = qs.order_by(*sort_fields)
        return qs

    def _handle_ajax_search(self, qs, params):
        bc = self.bound_columns()
        search_fields = []
        sSearch = params.get('sSearch', '')
        if sSearch:
            iColumns = params.get('iColumns', 0)
            for i in range(iColumns):
                bcol = bc.values()[i]
                bSearchable = params.get('bSearchable_%d' % i, True)
                bSearchable = bSearchable and bcol.options.get('bSearchable', True)
                if bSearchable:
                    search_fields.append(bcol.search_field)
            qfilter = None
            for search_field in search_fields:
                # FIXME: Does not work for extra fields or foreignkey fields
                q = Q(**{'%s__icontains' % search_field: sSearch})
                if qfilter is None:
                    qfilter = q 
                else:
                    qfilter |= q
            if qfilter:
                qs = qs.filter(qfilter)
        return qs

    def handle_ajax(self, request):
        params = {}
        for name, value in request.GET.items():
            try:
                params[name] = hungarian_to_python(name, value)
            except NameError:
                pass
        qs = self.get_queryset()
        iTotalRecords = qs.count()
        qs = self._handle_ajax_sorting(qs, params)
        qs = self._handle_ajax_search(qs, params)
        iTotalDisplayRecords = qs.count()
        iDisplayStart = params.get('iDisplayStart', 0)
        iDisplayLength = params.get('iDisplayLength', -1)
        if iDisplayLength < 0:
            iDisplayLength = iTotalDisplayRecords
        qs = qs[iDisplayStart:(iDisplayStart + iDisplayLength)]
        aaData = []
        for result in qs:
            aData = []
            for bcol in self.bound_columns().values():
                if bcol.options.get('bVisible', True):
                    aData.append(unicode(lookupattr(result, bcol.display_field)))
                else:
                    aData.append(u'')
            aaData.append(aData)
        data = {
            'iTotalRecords': iTotalRecords,
            'iTotalDisplayRecords': iTotalDisplayRecords,
            'sEcho': params.get('sEcho', ''),
            #'sColumns': ,
            'aaData': aaData,
        }
        print qs.query
        s = dumpjs(data)
        return HttpResponse(s, content_type='application/json')

    def as_html(self):
        t = select_template(['datatables/table.html'])
        return t.render(Context({'table': self}))
