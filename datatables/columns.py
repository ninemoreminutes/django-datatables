
__all__ = ['Column']

class Column(object):
    """Specify options for a Column on a DataTable."""

    creation_counter = 0

    def __init__(self, **kwargs):
        self.label = kwargs.get('label', None)
        self.model_field = kwargs.get('model_field', None)
        self.display_field = kwargs.get('display_field', None)
        self.sort_field = kwargs.get('sort_field', None)
        self.visible = kwargs.get('visible', True)
        self.searchable = kwargs.get('searchable', True)
        self.sortable = kwargs.get('sortable', True)
        self.sclass = kwargs.get('sclass', None)
        self.renderer = kwargs.get('renderer', None)
        # Increase the creation counter, and save our local copy.
        self.creation_counter = Column.creation_counter
        Column.creation_counter += 1

class BoundColumn(object):
    """A Column bound to a particular DataTable instance."""

    def __init__(self, data_table, column, name):
        self.data_table = data_table
        self.column = column
        self.name = name
        self.visible = self.column.visible
        self.searchable = self.column.searchable
        self.sortable = self.column.sortable
        self.sclass = self.column.sclass
        if self.column.label is None:
            self.label = self.name.replace('_', ' ').title()
        else:
            self.label = self.column.label
        if self.column.model_field is None:
            self.model_field = self.name
        else:
            self.model_field = self.column.model_field
        if self.column.display_field is None:
            self.display_field = self.model_field
        else:
            self.display_field = self.column.display_field
        if self.column.sort_field is None:
            self.sort_field = self.model_field
        else:
            self.sort_field = self.column.sort_field
