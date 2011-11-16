# Django
from django.utils.copycompat import deepcopy
from django.utils.datastructures import SortedDict

# Django DataTables
from columns import Column, BoundColumn

__all__ = ['DataTable']

class DataTableOptions(object):
    """Container class for DataTable options defined via the Meta class."""

    def __init__(self, options=None):
        self.model = getattr(options, 'model', None)

class DataTableDeclarativeMeta(type):
    """Metaclass for capturing declarative attributes on a DataTable class."""

    def __new__(cls, name, bases, attrs):
        columns = [(c, attrs.pop(c)) for c, obj in attrs.items() \
                  if isinstance(obj, Column)]
        columns.sort(key=lambda x: x[1].creation_counter)
        for base in reversed(bases):
            columns = getattr(base, 'base_columns', {}).items() + columns
        new_class = super(DataTableDeclarativeMeta, cls).__new__(cls, name, bases, attrs)
        new_class._meta = DataTableOptions(getattr(new_class, 'Meta', None))
        return new_class

class DataTable(object):
    """Base class for defining a DataTable and options."""

    __metaclass__ = DataTableDeclarativeMeta

    def __init__(self, **kwargs):
        self.columns = deepcopy(self.base_columns)

    def bound_columns(self):
        if not getattr(self, '_bound_columns', None):
            self._bound_columns = SortedDict([
                (name, BoundColumn(self, column, name)) \
                for name, column in self.columns.items()])
        return self._bound_columns

    def sort_field_choices(self):
        return [(name, bf.label) for name, bf in self.bound_fields().items() if bf.sortable]

    def display_field_choices(self):
        return [(name, bf.label) for name, bf in self.bound_fields().items() if bf.display_field]


    def queryset(self):
        """Return the base queryset to be used for this table."""
        return self._meta.model._default_manager.get_query_set()

    def apply_ordering(self, qs):
        sort_fields = []
        group_forms = self.group_forms()
        for group_name in sorted(group_forms.keys()):
            group_form = group_forms[group_name]
            if group_form.is_valid():
                field_name = group_form.cleaned_data['o']
                bf = self.bound_fields()[field_name]
                if not bf.sortable:
                    continue
                sort_field = bf.sort_field
                direction = group_form.cleaned_data['d']
                sort_field = direction + sort_field
                if sort_field not in sort_fields:
                    sort_fields.append(sort_field)
        print sort_fields
        qs = qs.order_by(*sort_fields)
        return qs

    def results(self):
        qs = self.queryset()
        qs = self.apply_ordering(qs)
        
        
        column_names = [x[0] for x in self.columns()]
        for row in qs:
            d = {}
            for name, bf in self.bound_fields().items():
                if name not in column_names:
                    continue
                df = bf.display_field.replace('__', '.')
                d[name] = lookupattr(row, df, None)
            yield d

    def as_html(self):
        pass

    def as_csv(self):
        pass
