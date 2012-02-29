# Django
from django.utils.copycompat import deepcopy
from django.utils.safestring import mark_safe
from django.forms.widgets import media_property
from django.template import Context
from django.template.loader import select_template

# Django-DataTables
from utils import hungarian_to_python, lookupattr

__all__ = ['Column', 'CheckboxColumn', 'ExpandableColumn']

class ColumnMeta(type):
    """Metaclass for Column class and subclass creation."""

    def __new__(cls, name, bases, attrs):
        new_class = super(ColumnMeta, cls).__new__(cls, name, bases, attrs)
        if 'media' not in attrs:
            new_class.media = media_property(new_class)
        return new_class

class Column(object):
    """Specify options for a Column on a DataTable."""

    __metaclass__ = ColumnMeta

    creation_counter = 0

    DEFAULTS = {
        'id': None,
        'classes': None,
        'label': None,
        'model_field': None,
        'display_field': None,
        'sort_field': None,
        'search_field': None,
        'value_renderer': None,
        'label_renderer': None,
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
        self.classes = set(self.classes or [])
        if self.value_renderer is None:
            self.value_renderer = getattr(self, 'render_value', None)
        if self.label_renderer is None:
            self.label_renderer = getattr(self, 'render_label', None)
        # Increase the creation counter, and save our local copy.
        self.creation_counter = Column.creation_counter
        Column.creation_counter += 1

class CheckboxColumn(Column):

    class Media:
        js = ('datatables/checkbox_column.js',)
        css = {'all': ('datatables/checkbox_column.css',)}

    def __init__(self, **kwargs):
        kwargs.setdefault('bSortable', False)
        self.name = kwargs.get('name', None)
        super(CheckboxColumn, self).__init__(**kwargs)
        self.classes.add('datatables_checkbox_column')
        self.template = select_template(['datatables/checkbox_column.html'])

    def render_label(self, bc):
        c = Context({
            'classes': ' '.join(self.classes),
            'name': self.name or bc.name,
            'value': '__ALL__',
        })
        #return mark_safe(self.template.render(c))
        return mark_safe(select_template(['datatables/checkbox_column_label.html']).render(c))

    def render_value(self, row, bc):
        c = Context({
            'classes': ' '.join(self.classes),
            'name': self.name or bc.name,
            'value': getattr(row, 'id', ''),
            'checked': bool(bc.model_field and lookupattr(row, bc.model_field)),
        })
        return mark_safe(self.template.render(c))

class ExpandableColumn(Column):

    #class Media:
    #    js = ('datatables/expandablecolumn.js',)

    def __init__(self, **kwargs):
        self.close_image = kwargs.pop('close_image', None)
        self.open_image = kwargs.pop('open_image', None)
        kwargs.setdefault('bSortable', False)
        self.function = kwargs.pop('function', None)
        super(ExpandableColumn, self).__init__(**kwargs)

    def render_label(self, bound_column):
        return ''#mark_safe(u'<img class="datatables_expand" src="%s" />' % (self.open_image))

    def render_value(self, row, bound_column):
        return mark_safe('<img class="datatables_expand" src="%s" />' % (self.open_image))

    def render_javascript(self, var, bound_column):
        javascript = '''
$(document).ready(function() {
  $('#%(id)s img.datatables_expand').live( 'click', function () {
    var nTr = $(this).parents('tr')[0];
    if ( %(var)s.fnIsOpen(nTr) ) {
      /* This row is already open - close it */
      this.src = '%(open_image)s';
      %(var)s.fnClose( nTr );
    } else {
      /* Open this row */
      this.src = '%(close_image)s';
      %(var)s.fnOpen( nTr, %(function)s, 'details' );
    }
  });
});
        ''' % {'var': var, 'open_image': self.open_image, 'close_image': self.close_image,
               'function': self.function, 'id': bound_column.datatable.id}
        return javascript

class BoundColumn(object):
    """A Column bound to a particular DataTable instance."""

    def __init__(self, datatable, column, name):
        self.datatable = datatable
        self.column = column
        self.name = name
        self.options = deepcopy(self.column.options)
        for key in self.column.DEFAULTS.keys():
            setattr(self, key, getattr(self.column, key))
        if self.id is None:
            self.id = '%s-%s' % (self.datatable.id, self.name)
        self.classes = set(self.classes)
        self.classes.add('datatable_col_%s' % self.name)
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

    @property
    def class_value(self):
        return ' '.join(self.classes)

    def render_label(self):
        if self.label_renderer:
            try:
                return self.label_renderer(self)
            except Exception, e:
                print e
                return self.label
        else:
            return self.label

    def render_value(self, row, include_hidden=True):
        if not include_hidden and not self.options.bVisible:
            return u''
        elif self.value_renderer:
            try:
                value = self.value_renderer(row, self)
            except Exception, e:
                print e
                value = u''
        else:
            value = unicode(lookupattr(row, self.display_field))
        return value
