# Django
from django.utils.copycompat import deepcopy
from django.utils.safestring import mark_safe

# Django-DataTables
from utils import hungarian_to_python, lookupattr

__all__ = ['Column', 'CheckboxColumn']

class Column(object):
    """Specify options for a Column on a DataTable."""

    creation_counter = 0

    DEFAULTS = {
        'label': None,
        'model_field': None,
        'display_field': None,
        'sort_field': None,
        'search_field': None,
        #'visible': True,
        #'searchable': True,
        #'sortable': True,
        'renderer': None,
    }

    def __init__(self, **kwargs):
        self.options = {}
        for key, value in kwargs.items():
            try:
                self.options[key] = hungarian_to_python(key, value)
                kwargs.pop(key)
            except NameError:
                pass
        for key, value in self.DEFAULTS.items():
            setattr(self, key, kwargs.get(key, value))
        # Increase the creation counter, and save our local copy.
        self.creation_counter = Column.creation_counter
        Column.creation_counter += 1

class CheckboxColumn(Column):
    
    def __init__(self, **kwargs):
        kwargs.setdefault('renderer', self.render_checkbox)
        kwargs.setdefault('label', mark_safe(u'<input type="checkbox"/>'))
        kwargs.setdefault('bSortable', False)
        super(CheckboxColumn, self).__init__(**kwargs)

    def render_checkbox(self, result_row, bound_column):
        if self.model_field:
            checked = bool(lookupattr(result_row, bound_column.model_field))
        else:
            checked = False
        return mark_safe(u'<input type="checkbox"/>')

class BoundColumn(object):
    """A Column bound to a particular DataTable instance."""

    def __init__(self, data_table, column, name):
        self.data_table = data_table
        self.column = column
        self.name = name
        self.options = deepcopy(self.column.options)
        for key in self.column.DEFAULTS.keys():
            setattr(self, key, getattr(self.column, key))
        if self.label is None:
            self.label = self.name.replace('_', ' ').title()
        if self.model_field is None:
            self.model_field = self.name
        self.model_field = self.model_field.replace('.', '__')
        if self.display_field is None:
            self.display_field = self.model_field
        self.display_field = self.display_field.replace('.', '__')
        if self.sort_field is None:
            self.sort_field = self.model_field
        self.sort_field = self.sort_field.replace('.', '__')
        if self.search_field is None:
            self.search_field = self.model_field
        self.search_field = self.search_field.replace('.', '__')

    def render(self, row, include_hidden=True):
        if not include_hidden and not self.options.bVisible:
            return u''
        elif self.renderer:
            try:
                return self.renderer(row, self)
            except:
                return u''
        else:
            return unicode(lookupattr(row, self.display_field))
