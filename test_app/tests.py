# Django
from django.test import TestCase

# Django-DataTables
import datatables

class TestDataTables(TestCase):
    """Test cases for Django-DataTables app."""

    def test_foo(self):
        raise NotImplementedError, 'need to write tests!'

    def test_hungarian_to_python(self):
        #fndef = 'function(oSettings, json) { alert("Init Complete!"); }'
        #result = datatables.hungarian_to_python('fnInitComplete', fndef)
        #self.assertEqual(unicode(result), fndef)
        #self.assertEqual(datatables.utils.dumpjs(result), fndef)
        result = datatables.hungarian_to_python('bVisible', 1)
        self.assertTrue(isinstance(result, bool))
        self.assertTrue(result)

    def test_lookupattr(self):
        pass

    def test_class_meta_options(self):
        class DT1(datatables.DataTable):
            pass

    def test_column_options(self):
        pass