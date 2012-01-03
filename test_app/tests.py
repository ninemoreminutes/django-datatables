# Python
import json

# Django
from django.test import TestCase
from django.utils.datastructures import SortedDict

# Django-DataTables
import datatables

class TestDataTables(TestCase):
    """Test cases for Django-DataTables app."""

    fixtures = ['fortunecookies']

    def test_hungarian_to_python(self):
        fndef = 'function(oSettings, json) { alert("Init Complete!"); }'
        result = datatables.hungarian_to_python('fnInitComplete', fndef)
        self.assertEqual(unicode(result), fndef)
        #self.assertEqual(datatables.utils.dumpjs(result), fndef)
        result = datatables.hungarian_to_python('bVisible', 1)
        self.assertTrue(isinstance(result, bool))
        self.assertTrue(result)

    def test_lookupattr(self):
        pass

    def _test_meta_options(self, **kwargs):
        dumps = json.dumps
        class DT(datatables.DataTable):
            Meta = type('Meta', (object,), kwargs)
        js_options = DT().js_options()
        for name, value in kwargs.items():
            expected_js = value
            if 'fn' != name[0:2]:
                expected_js = dumps(name) + ': ' + dumps(value, sort_keys=True)
            self.assertTrue(expected_js in js_options)

    def test_features(self):
        # Test that all DataTables features are handled by the Meta class and
        # included in the JS/JSON output from the DataTable class.
        # http://datatables.net/usage/features
        self._test_meta_options(bAutoWidth=True)
        self._test_meta_options(bDeferRender=True)
        self._test_meta_options(bFilter=True)
        self._test_meta_options(bInfo=True)
        self._test_meta_options(bJQueryUI=True)
        self._test_meta_options(bLengthChange=True)
        self._test_meta_options(bPaginate=True)
        self._test_meta_options(bProcessing=True)
        self._test_meta_options(bScrollInfinite=True)
        self._test_meta_options(bSort=True)
        self._test_meta_options(bSortClasses=True)
        self._test_meta_options(bStateSave=True)
        self._test_meta_options(sScrollX='100%')
        self._test_meta_options(sScrollY='100%')

    def test_options(self):
        # Test that all DataTables options are handled by the Meta class and
        # included in the JS/JSON output from the DataTable class.
        # http://datatables.net/usage/options
        aaData = [
            ['Trident', 'Internet Explorer 4.0', 'Win 95+', 4, 'X'],
            ['Trident', 'Internet Explorer 5.0', 'Win 95+', 5, 'C'],
        ]
        self._test_meta_options(aaData=aaData)
        self._test_meta_options(aaSorting=[[2, 'asc'], [3, 'desc']])
        self._test_meta_options(aaSortingFixed=[[0, 'asc']])
        aLengthMenu = [[10, 25, 50, -1], [10, 25, 50, "All"]]
        self._test_meta_options(aLengthMenu=aLengthMenu)
        aoSearchCols = [
            None,
            {'sSearch': 'My filter'},
            None,
            {'sSearch': '^[0-9]', 'bEscapeRegex': False}
        ]
        self._test_meta_options(aoSearchCols=aoSearchCols)
        asStripClasses = ['strip1', 'strip2', 'strip3']
        self._test_meta_options(asStripClasses=asStripClasses)
        self._test_meta_options(bDestroy=True)
        self._test_meta_options(bRetrieve=True)
        self._test_meta_options(bScrollCollapse=True)
        self._test_meta_options(bSortCellsTop=True)
        self._test_meta_options(iCookieDuration=60*60*24)
        self._test_meta_options(iDeferLoading=57)
        self._test_meta_options(iDisplayLength=50)
        self._test_meta_options(iDisplayStart=20)
        self._test_meta_options(iScrollLoadGap=50)
        self._test_meta_options(oSearch={'sSearch': 'Initial search'})
        self._test_meta_options(sAjaxDataProp='data')
        sAjaxSource = 'http://www.sprymedia.co.uk/dataTables/json.php'
        self._test_meta_options(sAjaxSource=sAjaxSource)
        self._test_meta_options(sCookiePrefix='my_datatable_')
        self._test_meta_options(sDom='<"top"i>rt<"bottom"flp><"clear"&lgt;')
        self._test_meta_options(sPaginationType='full_numbers')
        self._test_meta_options(sScrollXInner='110%')

    def test_callbacks(self):
        # Test that all DataTables callbacks are handled by the Meta class and
        # included in the JS/JSON output from the DataTable class.
        # http://datatables.net/usage/callbacks
        fnCookieCallback = '''function (sName, oData, sExpires, sPath) {
            /* Customise oData or sName or whatever else here */
            return sName + "="+JSON.stringify(oData)+"; expires=" + sExpires +"; path=" + sPath;
        }'''
        self._test_meta_options(fnCookieCallback=fnCookieCallback)
        fnDrawCallback = '''function(oSettings) {
            alert('DataTables has redrawn the table');
        }'''
        self._test_meta_options(fnDrawCallback=fnDrawCallback)
        fnFooterCallback = '''function(nFoot, aasData, iStart, iEnd, aiDisplay) {
            nFoot.getElementsByTagName('th')[0].innerHTML = "Starting index is "+iStart;
        }'''
        self._test_meta_options(fnFooterCallback=fnFooterCallback)
        fnFormatNumber = '''function (iIn) {
            return iIn;
        }'''
        self._test_meta_options(fnFormatNumber=fnFormatNumber)
        fnHeaderCallback = '''function(nHead, aasData, iStart, iEnd, aiDisplay) {
            nHead.getElementsByTagName('th')[0].innerHTML = "Displaying "+(iEnd-iStart)+" records";
        }'''
        self._test_meta_options(fnHeaderCallback=fnHeaderCallback)
        fnInfoCallback = '''function(oSettings, iStart, iEnd, iMax, iTotal, sPre) {
            return iStart +" to "+ iEnd;
        }'''
        self._test_meta_options(fnInfoCallback=fnInfoCallback)
        fnInitComplete = '''function(oSettings, json) {
            alert('DataTables has finished its initialisation.');
        }'''
        self._test_meta_options(fnInitComplete=fnInitComplete)
        fnPreDrawCallback = '''function(oSettings) {
            if ($('#test').val() == 1) {
                return false;
            }
        }'''
        self._test_meta_options(fnPreDrawCallback=fnPreDrawCallback)
        fnRowCallback = '''function(nRow, aData, iDisplayIndex, iDisplayIndexFull) {
            /* Bold the grade for all 'A' grade browsers */
            if ( aData[4] == "A" )
            {
                $('td:eq(4)', nRow).html( '<b>A</b>' );
            }
            return nRow;
        }'''
        self._test_meta_options(fnRowCallback=fnRowCallback)
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
        self._test_meta_options(fnServerData=fnServerData)
        fnServerParams = '''function (aoData) {
            aoData.push({"name": "more_data", "value": "my_value"});
        }'''
        self._test_meta_options(fnServerParams=fnServerParams)
        fnStateLoadCallback = '''function (oSettings, oData) {
            oData.sFilter = "";
            return true;
        }'''
        self._test_meta_options(fnStateLoadCallback=fnStateLoadCallback)
        fnStateSaveCallback = '''function (oSettings, sValue) {
            sValue += ',"myCustomParameter": "myValue"';
            return sValue;
        }'''
        self._test_meta_options(fnStateSaveCallback=fnStateSaveCallback)

    def _test_column_options(self, **kwargs):
        dumps = json.dumps
        columns = SortedDict()
        option_values = {}
        for index, name in enumerate(kwargs.keys()):
            options = kwargs[name]
            columns[name] = datatables.Column(**options)
            for k,v in options.items():
                if k not in option_values:
                    option_values[k] = []
                if v not in [x[0] for x in option_values[k]]:
                    option_values[k].append([v, []])
                for x in option_values[k]:
                    if x[0] == v:
                        x[1].append(index)
        DT = type('DT', (datatables.DataTable,), columns)
        js_options = DT().js_options()
        for oname, ovalues in option_values.items():
            for ovalue, otargets in ovalues:
                expected_js = dumps({
                    'aTargets': otargets,
                    oname: ovalue,
                }, sort_keys=True).lstrip('{').rstrip('}').strip()
            #print js_options, expected_js
            self.assertTrue(expected_js in js_options)

    def test_columns(self):
        # Test that all DataTables column options are handled by the Column
        # class and included in the JS/JSON output from the DataTable class.
        # http://datatables.net/usage/columns
        options = {
            'fortune': {'asSorting': ['desc', 'asc', 'asc']},
            'lucky_numbers': {},
        }
        # FIXME: self._test_column_options(**options)
        options = {
            'fortune': {'bSearchable': False},
            'lucky_numbers': {},
        }
        self._test_column_options(**options)
        options = {
            'fortune': {'bSortable': False},
            'lucky_numbers': {'bSortable': False},
        }
        self._test_column_options(**options)
        options = {
            'fortune': {'bUseRendered': False},
            'lucky_numbers': {},
        }
        self._test_column_options(**options)
        options = {
            'fortune': {'bVisible': False},
            'lucky_numbers': {'bVisible': False},
        }
        self._test_column_options(**options)
        options = {
            'fortune': {'fnRender': 'function (oObj) { return oObj.aData[oObj.iDataColumn]; }'},
            'lucky_numbers': {},
        }
        # FIXME: self._test_column_options(**options)
        options = {
            'fortune': {'mDataProp': 'fortune_display'},
            'lucky_numbers': {'mDataProp': 1},
        }
        self._test_column_options(**options)
        options = {
            'fortune': {'mDataProp': 'function(oObj) { return oObj.aData[0]; }'},
            'lucky_numbers': {'mDataProp': None},
        }
        # FIXME: self._test_column_options(**options)
        options = {
            'fortune': {'sClass': 'my_class'},
            'lucky_numbers': {'sClass': 'my_class'},
        }
        self._test_column_options(**options)
        options = {
            'fortune': {},
            'lucky_numbers': {'sDefaultContent': 'Edit'},
        }
        self._test_column_options(**options)
        options = {
            'fortune': {},
            'lucky_numbers': {'sName': 'lucky_number_column'},
        }
        self._test_column_options(**options)
        options = {
            'fortune': {'sSortDataType': 'dom-text'},
            'lucky_numbers': {'sSortDataType': 'dom-text'},
        }
        self._test_column_options(**options)
        options = {
            'fortune': {'sTitle': 'My column title'},
            'lucky_numbers': {},
        }
        self._test_column_options(**options)
        options = {
            'fortune': {'sType': 'html'},
            'lucky_numbers': {'sType': 'html'},
        }
        self._test_column_options(**options)
        options = {
            'fortune': {'sWidth': '20%'},
            'lucky_numbers': {},
        }
        self._test_column_options(**options)

    def test_column_sorting(self):
        class DT(datatables.DataTable):
            fortune = datatables.Column(sort_field="lucky_numbers")
            lucky_numbers = datatables.Column()

        dt = DT()
        js_options = dt.js_options()
        self.assertTrue('"aTargets": [0], "iDataSort": 1' in js_options)
