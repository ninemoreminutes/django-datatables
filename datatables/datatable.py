# Django
from django.http import HttpResponse
from django.template import Context
from django.template.loader import select_template
from django.utils.copycompat import deepcopy
from django.utils.datastructures import SortedDict
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.forms.widgets import Media, media_property

# Django DataTables
from columns import Column, BoundColumn
from utils import dumpjs, hungarian_to_python, lookupattr

__all__ = ['DataTable']

class DataTableOptions(object):
    """Container class for DataTable options defined via the Meta class."""

    def __init__(self, options=None):
        self.update(options)

    def update(self, options=None):
        self.id = getattr(options, 'id', getattr(self, 'id', 'datatable_%d' % id(self)))
        self.var = getattr(options, 'var', getattr(self, 'var', None))
        self.classes = getattr(options, 'classes', getattr(self, 'classes', []))
        if isinstance(self.classes, basestring):
            self.classes = self.classes.split()
        self.classes = set(self.classes)
        self.width = str(getattr(options, 'width', getattr(self, 'width', '100%')))
        self.border = str(getattr(options, 'border', getattr(self, 'border', '0')))
        self.cellpadding = str(getattr(options, 'cellpadding', getattr(self, 'cellpadding', '0')))
        self.cellspacing = str(getattr(options, 'cellspacing', getattr(self, 'cellspacing', '0')))
        self.model = getattr(options, 'model', getattr(self, 'model', None))
        self.options = getattr(self, 'options', {})
        self.options.update(getattr(options, 'options', {}))
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
        new_class._meta = DataTableOptions()
        for base in reversed(bases):
            new_class._meta.update(getattr(base, '_meta', None))
        new_class._meta.update(getattr(new_class, 'Meta', None))
        if 'media' not in attrs:
            new_class.media = media_property(new_class)
        return new_class

class DataTable(object):
    """Base class for defining a DataTable and options."""

    __metaclass__ = DataTableDeclarativeMeta

    def __init__(self, data=None, name=''):
        self.columns = SortedDict(self.base_columns.items())#deepcopy(self.base_columns)

    @property
    def id(self):
        return self._meta.id

    @property
    def var(self):
        return self._meta.var

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

    @property
    def bound_columns(self):
        if not getattr(self, '_bound_columns', None):
            self._bound_columns = SortedDict([
                (name, BoundColumn(self, column, name)) \
                for name, column in self.columns.items()])
        return self._bound_columns

    def get_default_queryset(self):
        """Return the default queryset to be used for this table."""
        if self._meta.model:
            return self._meta.model._default_manager.get_query_set()
        else:
            return EmptyQuerySet()

    def get_queryset(self):
        """Return the current queryset to use for this table."""
        return getattr(self, '_qs', self.get_default_queryset())

    def update_queryset(self, qs):
        """Update the queryset used for this table."""
        self._qs = qs

    def reset_queryset(self):
        """Reset the queryset to the default for this table."""
        if hasattr(self, '_qs'):
            del self._qs

    def rows(self):
        if self._meta.options.get('bServerSide', False):
            qs = self.get_queryset().none()
        else:
            qs = self.get_queryset()
        for result in qs:
            d = SortedDict()
            for bcol in self.bound_columns.values():
                d[bcol.name] = bcol.render_value(result)
            if 'id' not in d:
                d['id'] = result.id
            yield d

    def js_options(self):
        options = deepcopy(self._meta.options)
        columns = self.bound_columns
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

    @property
    def media(self):
        media = Media()
        for bound_column in self.bound_columns.values():
            media = media + bound_column.column.media
        return media

    def extra_js(self):
        columns = self.bound_columns.values()
        extra = ''
        for column in columns:
            try:
                extra += column.column.render_javascript(self.var, column)
            except Exception, e:
                #print e
                pass
        return mark_safe(extra)

    def process_request(self, request, name='datatable'):
        setattr(request, name, self)
        
    def process_response(self, request, response):
        if 'sEcho' in request.GET:# and request.is_ajax():
            return self.handle_ajax(request)
        else:
            return response

    def _handle_ajax_sorting(self, qs, params):
        bc = self.bound_columns
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

    def _handle_ajax_global_search(self, qs, params):
        bc = self.bound_columns
        search_fields = []
        sSearch = params.get('sSearch', '')
        bRegex = params.get('bRegex', False)
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
                if bRegex:
                    q = Q(**{'%s__regex' % search_field: sSearch})
                else:
                    q = Q(**{'%s__icontains' % search_field: sSearch})
                if qfilter is None:
                    qfilter = q 
                else:
                    qfilter |= q
            if qfilter:
                qs = qs.filter(qfilter)
        return qs

    def _handle_ajax_column_specific_search(self, qs, params):
        bc = self.bound_columns
        search_fields = []
        iColumns = params.get('iColumns', 0)
        for i in range(iColumns):
            bcol = bc.values()[i]
            bSearchable = params.get('bSearchable_%d' % i, True)
            bSearchable = bSearchable and bcol.options.get('bSearchable', True)
            sSearch = params.get('sSearch_%d' % i, '')
            bRegex = params.get('bRegex_%d' % i, False)
            if bSearchable and sSearch:
                search_fields.append({
                    'field': bcol.search_field,
                    'term': sSearch,
                    'regex': bRegex,
                })
        qfilter = None
        for search_field in search_fields:
            if search_field['regex']:
                q = Q(**{'%s__regex' % search_field['field']: search_field['term']})
            else:
                q = Q(**{'%s__icontains' % search_field['field']: search_field['term']})
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
        qs = self._handle_ajax_global_search(qs, params)
        qs = self._handle_ajax_column_specific_search(qs, params)
        iTotalDisplayRecords = qs.count()
        iDisplayStart = params.get('iDisplayStart', 0)
        iDisplayLength = params.get('iDisplayLength', -1)
        if iDisplayLength < 0:
            iDisplayLength = iTotalDisplayRecords
        qs = qs[iDisplayStart:(iDisplayStart + iDisplayLength)]
        aaData = []
        for result in qs:
            aData = []
            for bcol in self.bound_columns.values():
                aData.append(bcol.render_value(result, include_hidden=False))
            aaData.append(aData)
        data = {
            'iTotalRecords': iTotalRecords,
            'iTotalDisplayRecords': iTotalDisplayRecords,
            'sEcho': params.get('sEcho', ''),
            #'sColumns': ,
            'aaData': aaData,
        }
        #print qs.query
        s = dumpjs(data)
        return HttpResponse(s, content_type='application/json')

    def as_html(self):
        t = select_template(['datatables/table.html'])
        return t.render(Context({'table': self}))
