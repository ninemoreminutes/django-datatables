# Django
from django.utils.copycompat import deepcopy

# Django-DataTables
from utils import hungarian_to_python

__all__ = ['Column']

class Column(object):
    """Specify options for a Column on a DataTable."""

    creation_counter = 0

    DEFAULTS = {
        'label': None,
        'model_field': None,
        'display_field': None,
        'sort_field': None,
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
        if self.display_field is None:
            self.display_field = self.model_field
        if self.sort_field is None:
            self.sort_field = self.model_field
