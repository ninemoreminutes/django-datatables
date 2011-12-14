# Django
from django.template import Context
from django.template.loader import select_template
from django.utils.copycompat import deepcopy
from django.utils.datastructures import SortedDict
from django.utils.safestring import mark_safe
from django.utils import simplejson

# Django DataTables
from columns import Column, BoundColumn

__all__ = ['DataTable']

class DataTableOptions(object):
    """Container class for DataTable options defined via the Meta class."""

    def __init__(self, options=None):
        self.id = getattr(options, 'id', 'datatable_%d' % id(self))
        self.model = getattr(options, 'model', None)
        self.options = {}
        for name in dir(options):
            if name.startswith('_'):
                continue
            value = getattr(options, name)
            try:
                self.options[name] = self._hungarian_to_python(name, value)
            except NameError:
                pass

    def _hungarian_to_python(self, name, value):
        """Validate DataTable Meta options in Hungarian notation."""
        if name.startswith('fn') and name[2].isupper():
            return value
        elif name.startswith('n') and name[1].isupper():
            return value
        elif name.startswith('m') and name[1].isupper():
            return value
        elif name.startswith('o') and name[1].isupper():
            d = {}
            for k, v in dict(value).iteritems():
                d[k] = self._hungarian_to_python(k, v)
            return d
        elif name.startswith('a') and name[1].isupper():
            return list(value)
        elif name.startswith('a') and name[1] in 'abfimnos' and name[2].isupper():
            a = []
            for i in list(value):
                a.append(self._hungarian_to_python(name[1:], i))
            return a
        elif name.startswith('s') and name[1].isupper():
            return unicode(value)
        elif name.startswith('b') and name[1].isupper():
            return bool(value)
        elif name.startswith('f') and name[1].isupper():
            return float(value)
        elif name.startswith('i') and name[1].isupper():
            return int(value)
        else:
            raise NameError, 'name "%s" is not in hungarian notation' % name


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

    def bound_columns(self):
        if not getattr(self, '_bound_columns', None):
            self._bound_columns = SortedDict([
                (name, BoundColumn(self, column, name)) \
                for name, column in self.columns.items()])
        return self._bound_columns

    def queryset(self):
        """Return the base queryset to be used for this table."""
        return self._meta.model._default_manager.get_query_set()

    def apply_ordering(self, qs):
        #qs = qs.order_by(*sort_fields)
        return qs

    def results(self):
        qs = self.queryset()
        qs = self.apply_ordering(qs)
        
        
        #column_names = [x[0] for x in self.columns()]
        #for row in qs:
        #    d = {}
        #    for name, bf in self.bound_fields().items():
        #        if name not in column_names:
        #            continue
        #        df = bf.display_field.replace('__', '.')
        #        d[name] = lookupattr(row, df, None)
        #    yield d
        return iter(qs)

    def json_options(self):
        return mark_safe(simplejson.dumps(self._meta.options))

    def has_response(self):
        return False

    def get_response(self, request=None):
        pass

    def as_html(self):
        t = select_template(['datatables/table.html'])
        return t.render(Context({'table': self}))
