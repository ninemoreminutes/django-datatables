# Python
import imp
try:
    import json
except ImportError:
    from django.utils import simplejson as json
import sys

# Django
from django.test import TestCase
from django.test.client import Client
from django.utils.datastructures import SortedDict

# Django-FortuneCookie
from fortunecookie.models import *

# Django-DataTables
import datatables


class TestDataTables(TestCase):
    """Test cases for Django-DataTables app."""

    fixtures = ['fortunecookies']

    def setUp(self):
        super(TestDataTables, self).setUp()
        # For test coverage.
        imp.reload(sys.modules['datatables.columns'])
        # imp.reload(sys.modules['datatables.datatable'])
        imp.reload(sys.modules['datatables.decorators'])
        imp.reload(sys.modules['datatables.utils'])

    def test_hungarian_to_python(self):
        fndef = 'function(oSettings, json) { alert("Init Complete!"); }'
        result = datatables.hungarian_to_python('fnInitComplete', fndef)
        self.assertEqual(unicode(result), fndef)
        result = datatables.hungarian_to_python('bVisible', 1)
        self.assertTrue(isinstance(result, bool))
        self.assertTrue(result)
        result = datatables.hungarian_to_python('sCookiePrefix', 'my_cookie')
        self.assertTrue(isinstance(result, basestring))
        self.assertTrue(result)
        # FIXME: Test other types.

    def test_lookupattr(self):
        pass

    def _verify_meta_options(self, **kwargs):
        # Helper to test that options specified in Meta class are correctly
        # represented in the JS/JSON output from the DataTable class.
        dumps = json.dumps

        class DT(datatables.DataTable):
            Meta = type('Meta', (object,), kwargs)
        js_options = DT().js_options()
        for name, value in kwargs.items():
            if name.startswith('fn'):
                self.assertTrue(value in js_options)
            else:
                js_o = json.loads(js_options)
                self.assertEqual(js_o[name], value)

    def test_features(self):
        # Test that all DataTables features are handled by the Meta class and
        # included in the JS/JSON output from the DataTable class.
        # http://datatables.net/usage/features
        self._verify_meta_options(bAutoWidth=True)
        self._verify_meta_options(bDeferRender=True)
        self._verify_meta_options(bFilter=True)
        self._verify_meta_options(bInfo=True)
        self._verify_meta_options(bJQueryUI=True)
        self._verify_meta_options(bLengthChange=True)
        self._verify_meta_options(bPaginate=True)
        self._verify_meta_options(bProcessing=True)
        self._verify_meta_options(bScrollInfinite=True)
        self._verify_meta_options(bSort=True)
        self._verify_meta_options(bSortClasses=True)
        self._verify_meta_options(bStateSave=True)
        self._verify_meta_options(sScrollX='100%')
        self._verify_meta_options(sScrollY='100%')

    def test_options(self):
        # Test that all DataTables options are handled by the Meta class and
        # included in the JS/JSON output from the DataTable class.
        # http://datatables.net/usage/options
        aaData = [
            ['Trident', 'Internet Explorer 4.0', 'Win 95+', 4, 'X'],
            ['Trident', 'Internet Explorer 5.0', 'Win 95+', 5, 'C'],
        ]
        self._verify_meta_options(aaData=aaData)
        self._verify_meta_options(aaSorting=[[2, 'asc'], [3, 'desc']])
        self._verify_meta_options(aaSortingFixed=[[0, 'asc']])
        aLengthMenu = [[10, 25, 50, -1], [10, 25, 50, "All"]]
        self._verify_meta_options(aLengthMenu=aLengthMenu)
        aoSearchCols = [
            None,
            {'sSearch': 'My filter'},
            None,
            {'sSearch': '^[0-9]', 'bEscapeRegex': False}
        ]
        self._verify_meta_options(aoSearchCols=aoSearchCols)
        asStripClasses = ['strip1', 'strip2', 'strip3']
        self._verify_meta_options(asStripClasses=asStripClasses)
        self._verify_meta_options(bDestroy=True)
        self._verify_meta_options(bRetrieve=True)
        self._verify_meta_options(bScrollCollapse=True)
        self._verify_meta_options(bSortCellsTop=True)
        self._verify_meta_options(iCookieDuration=60*60*24)
        self._verify_meta_options(iDeferLoading=57)
        self._verify_meta_options(iDisplayLength=50)
        self._verify_meta_options(iDisplayStart=20)
        self._verify_meta_options(iScrollLoadGap=50)
        self._verify_meta_options(oSearch={'sSearch': 'Initial search'})
        self._verify_meta_options(sAjaxDataProp='data')
        sAjaxSource = 'http://www.sprymedia.co.uk/dataTables/json.php'
        self._verify_meta_options(sAjaxSource=sAjaxSource)
        self._verify_meta_options(sCookiePrefix='my_datatable_')
        self._verify_meta_options(sDom='<"top"i>rt<"bottom"flp><"clear"&lgt;')
        self._verify_meta_options(sPaginationType='full_numbers')
        self._verify_meta_options(sScrollXInner='110%')

    def test_callbacks(self):
        # Test that all DataTables callbacks are handled by the Meta class and
        # included in the JS/JSON output from the DataTable class.
        # http://datatables.net/usage/callbacks
        fnCookieCallback = '''function (sName, oData, sExpires, sPath) {
            /* Customise oData or sName or whatever else here */
            return sName + "="+JSON.stringify(oData)+"; expires=" + sExpires +
                "; path=" + sPath;
        }'''
        self._verify_meta_options(fnCookieCallback=fnCookieCallback)
        fnDrawCallback = '''function(oSettings) {
            alert('DataTables has redrawn the table');
        }'''
        self._verify_meta_options(fnDrawCallback=fnDrawCallback)
        fnFooterCallback = '''function(nFoot, aasData, iStart, iEnd,
            aiDisplay) {
            nFoot.getElementsByTagName('th')[0].innerHTML = "Starting index " +
                "is " + iStart;
        }'''
        self._verify_meta_options(fnFooterCallback=fnFooterCallback)
        fnFormatNumber = '''function (iIn) {
            return iIn;
        }'''
        self._verify_meta_options(fnFormatNumber=fnFormatNumber)
        fnHeaderCallback = '''function(nHead, aasData, iStart, iEnd,
            aiDisplay) {
            nHead.getElementsByTagName('th')[0].innerHTML = "Displaying "+
                (iEnd-iStart)+" records";
        }'''
        self._verify_meta_options(fnHeaderCallback=fnHeaderCallback)
        fnInfoCallback = '''function(oSettings, iStart, iEnd, iMax, iTotal,
            sPre) {
            return iStart +" to "+ iEnd;
        }'''
        self._verify_meta_options(fnInfoCallback=fnInfoCallback)
        fnInitComplete = '''function(oSettings, json) {
            alert('DataTables has finished its initialisation.');
        }'''
        self._verify_meta_options(fnInitComplete=fnInitComplete)
        fnPreDrawCallback = '''function(oSettings) {
            if ($('#test').val() == 1) {
                return false;
            }
        }'''
        self._verify_meta_options(fnPreDrawCallback=fnPreDrawCallback)
        fnRowCallback = '''function(nRow, aData, iDisplayIndex,
            iDisplayIndexFull) {
            /* Bold the grade for all 'A' grade browsers */
            if ( aData[4] == "A" )
            {
                $('td:eq(4)', nRow).html( '<b>A</b>' );
            }
            return nRow;
        }'''
        self._verify_meta_options(fnRowCallback=fnRowCallback)
        fnServerData = '''function (sSource, aoData, fnCallback) {
            /* Add some data to send to the source, and send as 'POST' */
            aoData.push({ "name": "my_field", "value": "my_value" });
            $.ajax({
                "dataType": 'json',
                "type": "POST",
                "url": sSource,
                "data": aoData,
                "success": fnCallback
            });
        }'''
        self._verify_meta_options(fnServerData=fnServerData)
        fnServerParams = '''function (aoData) {
            aoData.push({"name": "more_data", "value": "my_value"});
        }'''
        self._verify_meta_options(fnServerParams=fnServerParams)
        fnStateLoadCallback = '''function (oSettings, oData) {
            oData.sFilter = "";
            return true;
        }'''
        self._verify_meta_options(fnStateLoadCallback=fnStateLoadCallback)
        fnStateSaveCallback = '''function (oSettings, sValue) {
            sValue += ',"myCustomParameter": "myValue"';
            return sValue;
        }'''
        self._verify_meta_options(fnStateSaveCallback=fnStateSaveCallback)

    def _verify_column_options(self, **kwargs):
        # Helper to test that options specified to the Column class are
        # correctly represented in the JS/JSON output from the DataTable class
        # (in the aoColumnDefs list).
        dumps = json.dumps
        columns = SortedDict()
        option_values = {}
        for index, name in enumerate(kwargs.keys()):
            options = kwargs[name]
            columns[name] = datatables.Column(**options)
            # Build a dictionary of expected options, values and targets:
            # {
            #    '<option_name>': [[<expected_value>, [<target>, ...]], ...],
            #    ...
            # }
            for k, v in options.items():
                if k not in option_values:
                    option_values[k] = []
                if v not in [x[0] for x in option_values[k]]:
                    option_values[k].append([v, []])
                for x in option_values[k]:
                    if x[0] == v:
                        x[1].append(index)
        DT = type('DT', (datatables.DataTable,), columns)
        js_options = DT().js_options()
        js_o = json.loads(js_options)
        # Check that aoColumnDefs correctly includes all of the specified
        # options.
        for column_def in js_o['aoColumnDefs']:
            column_targets = column_def['aTargets']
            for column_opt, column_val in column_def.items():
                if column_opt == 'aTargets':
                    continue
                self.assertTrue(column_opt in option_values)
                ovalues = option_values[column_opt]
                val_found = False
                for ovalue, otargets in ovalues:
                    if column_val == ovalue:
                        val_found = True
                        self.assertTrue(set(column_targets) <= set(otargets))
                self.assertTrue(val_found)
            # FIXME: Checks that all options given in aoColumnDefs are valid,
            # doesn't yet check if any are missing.

    def test_columns(self):
        # Test that all DataTables column options are handled by the Column
        # class and included in the JS/JSON output from the DataTable class.
        # http://datatables.net/usage/columns
        options = {
            'fortune': {'asSorting': ['desc', 'asc', 'asc']},
            'lucky_numbers': {},
        }
        self._verify_column_options(**options)
        options = {
            'fortune': {'bSearchable': False},
            'lucky_numbers': {},
        }
        self._verify_column_options(**options)
        options = {
            'fortune': {'bSortable': False},
            'lucky_numbers': {'bSortable': True},
        }
        self._verify_column_options(**options)
        options = {
            'fortune': {'bUseRendered': False},
            'lucky_numbers': {},
        }
        self._verify_column_options(**options)
        options = {
            'fortune': {'bVisible': False},
            'lucky_numbers': {'bVisible': True},
        }
        self._verify_column_options(**options)
        options = {
            'fortune': {
                'fnRender':
                'function (oObj) { return oObj.aData[oObj.iDataColumn];}'
            },
            'lucky_numbers': {},
        }
        # FIXME: Doesn't yet handle functions.
        # self._verify_column_options(**options)
        options = {
            'fortune': {'mDataProp': 'fortune_display'},
            'lucky_numbers': {'mDataProp': 1},
        }
        self._verify_column_options(**options)
        options = {
            'fortune': {
                'mDataProp': 'function(oObj) { return oObj.aData[0]; }'
            },
            'lucky_numbers': {'mDataProp': None},
        }
        # FIXME: Doesn't yet handle functions.
        # self._verify_column_options(**options)
        options = {
            'fortune': {'sClass': 'my_class'},
            'lucky_numbers': {'sClass': 'my_other_class'},
        }
        self._verify_column_options(**options)
        options = {
            'fortune': {},
            'lucky_numbers': {'sDefaultContent': 'Edit'},
        }
        self._verify_column_options(**options)
        options = {
            'fortune': {},
            'lucky_numbers': {'sName': 'lucky_number_column'},
        }
        self._verify_column_options(**options)
        options = {
            'fortune': {'sSortDataType': 'dom-text'},
            'lucky_numbers': {'sSortDataType': 'dom-text'},
        }
        self._verify_column_options(**options)
        options = {
            'fortune': {'sTitle': 'My column title'},
            'lucky_numbers': {},
        }
        self._verify_column_options(**options)
        options = {
            'fortune': {'sType': 'string'},
            'lucky_numbers': {'sType': 'html'},
        }
        self._verify_column_options(**options)
        options = {
            'fortune': {'sWidth': '20%'},
            'lucky_numbers': {},
        }
        self._verify_column_options(**options)

    def test_column_sorting(self):
        class DT(datatables.DataTable):
            fortune = datatables.Column(sort_field="lucky_numbers")
            lucky_numbers = datatables.Column()

        dt = DT()
        js_options = dt.js_options()
        js_o = json.loads(js_options)
        self.assertTrue(js_o['aoColumnDefs'][0]['aTargets'][0] == 0)
        self.assertTrue(js_o['aoColumnDefs'][0]['iDataSort'] == 1)

    def test_server_side(self):
        args = {
            'sEcho': 1,
            'iSortingCols': 1,
            'iSortCol_0': 1,
            'sSortDir_0': 'desc'
        }
        response = self.client.get('/', args)
        data = json.loads(response.content)
        top_item = data['aaData'][0][0]
        second_item = data['aaData'][1][0]
        args['sSortDir_0'] = 'asc'
        response = self.client.get('/', args)
        data = json.loads(response.content)
        self.assertTrue(data['aaData'][len(data['aaData'])-1][0] == top_item)
        args['iDisplayStart'] = 1
        args['sSortDir_0'] = 'desc'
        args['iDisplayLength'] = 2
        response = self.client.get('/', args)
        data = json.loads(response.content)
        self.assertTrue(data['aaData'][0][0] == second_item)
        self.assertTrue(len(data['aaData']) == args['iDisplayLength'])
        del args['iDisplayLength']
        del args['iDisplayStart']
        args['iColumns'] = 4
        args['sSearch'] = 'you'
        args['bSearchable_0'] = True
        args['bSearchable_1'] = False
        args['bSearchable_2'] = False
        args['bSearchable_3'] = False
        args['bRegex'] = False
        response = self.client.get('/', args)
        data = json.loads(response.content)
        qs = FortuneCookie.objects.filter(fortune__icontains=args['sSearch'])
        self.assertTrue(qs.count() == len(data['aaData']))
        del args['sSearch']
        args['sSearch_0'] = 'you'
        args['bRegex_0'] = False
        response = self.client.get('/', args)
        data = json.loads(response.content)
        self.assertTrue(qs.count() == len(data['aaData']))
        args['sSearch_0'] = '^You.*$'
        args['bRegex_0'] = True
        qs = FortuneCookie.objects.filter(fortune__regex=args['sSearch_0'])
        response = self.client.get('/', args)
        data = json.loads(response.content)
        self.assertTrue(qs.count() == len(data['aaData']))
        del args['sSearch_0']
        del args['bRegex_0']
        args['sSearch'] = '^You.*$'
        args['bRegex'] = True
        response = self.client.get('/', args)
        data = json.loads(response.content)
        self.assertTrue(qs.count() == len(data['aaData']))
