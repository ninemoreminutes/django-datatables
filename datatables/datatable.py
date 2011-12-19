# Django
from django.template import Context
from django.template.loader import select_template
from django.utils.copycompat import deepcopy
from django.utils.datastructures import SortedDict
from django.utils.safestring import mark_safe

# Django DataTables
from columns import Column, BoundColumn
from utils import dumpjs, hungarian_to_python

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

    def results(self):
        qs = self.get_queryset()
        qs = self.apply_ordering(qs)
        return iter(qs)

    def js_options(self):
        options = deepcopy(self._meta.options)
        columns = self.bound_columns()
        aoColumnDefs = options.setdefault('aoColumnDefs', [])
        colopts = SortedDict()
        for index, name in enumerate(columns.keys()):
            column = columns[name]
            for key, value in column.options.items():
                colopts[(key, value)] = colopts.get((key, value), []) + [index]
            if column.sort_field != column.display_field and column.sort_field in columns:
                key = 'iDataSort'
                value = columns.keys().index(column.sort_field)
                colopts[(key, value)] = colopts.get((key, value), []) + [index]
        for kv, targets in colopts.items():
            aoColumnDefs.append(dict([kv, ('aTargets', targets)]))
        return mark_safe(dumpjs(options))

    def has_response(self):
        return False

    def get_response(self, request=None):
        pass

    def as_html(self):
        t = select_template(['datatables/table.html'])
        return t.render(Context({'table': self}))
