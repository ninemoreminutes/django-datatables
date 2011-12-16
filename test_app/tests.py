# Django
from django.test import TestCase

# Django-DataTables
import datatables

class TestDataTables(TestCase):
    """Test cases for Django-DataTables app."""

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

    fixtures = ['fortunecookies',]

    # Test Features

    def test_bAutoWidth(self):
        class DT(datatables.DataTable):
            class Meta:
                bAutoWidth = True
        
        dt = DT()
        js_options = dt.js_options()
        
        self.assertTrue('"bAutoWidth": true' in js_options)

    def test_bDeferRender(self):
        class DT(datatables.DataTable):
            class Meta:
                bDeferRender = True
        
        dt = DT()
        js_options = dt.js_options()
        
        self.assertTrue('"bDeferRender": true' in js_options)

    def test_bFilter(self):
        class DT(datatables.DataTable):
            class Meta:
                bFilter = True

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"bFilter": true' in js_options)

    def test_bInfo(self):
        class DT(datatables.DataTable):
            class Meta:
                bInfo = True

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"bInfo": true' in js_options)
        
    def test_bJQueryUI(self):
        class DT(datatables.DataTable):
            class Meta:
                bJQueryUI = True

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"bJQueryUI": true' in js_options)

    def test_bLengthChange(self):
        class DT(datatables.DataTable):
            class Meta:
                bLengthChange = True

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"bLengthChange": true' in js_options)

    def test_bPaginate(self):
        class DT(datatables.DataTable):
            class Meta:
                bPaginate = True

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"bPaginate": true' in js_options)

    def test_bProcessing(self):
        class DT(datatables.DataTable):
            class Meta:
                bProcessing = True

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"bProcessing": true' in js_options)
        
    def test_bScrollInfinite(self):
        class DT(datatables.DataTable):
            class Meta:
                bScrollInfinite = True

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"bScrollInfinite": true' in js_options)
        
    def test_bSort(self):
        class DT(datatables.DataTable):
            class Meta:
                bSort = True

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"bSort": true' in js_options)
        
    def test_bSortClasses(self):
        class DT(datatables.DataTable):
            class Meta:
                bSortClasses = True

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"bSortClasses": true' in js_options)
        
    def test_bStateSave(self):
        class DT(datatables.DataTable):
            class Meta:
                bStateSave = True

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"bStateSave": true' in js_options)

    def test_sScrollX(self):
        class DT(datatables.DataTable):
            class Meta:
                sScrollX = '100%'

        dt = DT()
        js_options = dt.js_options()
        
        self.assertTrue('"sScrollX": "100%"' in js_options)

    def test_sScrollY(self):
        class DT(datatables.DataTable):
            class Meta:
                sScrollY = '100%'

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"sScrollY": "100%"' in js_options)

    # Test Options
    
    def test_aaData(self):
        class DT(datatables.DataTable):
            class Meta:
                aaData = [
                            ['Trident', 'Internet Explorer 4.0', 'Win 95+', 4, 'X'],
                            ['Trident', 'Internet Explorer 5.0', 'Win 95+', 5, 'C'],
                         ]

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"aaData": [["Trident", "Internet Explorer 4.0", "Win 95+", 4, "X"], ["Trident", "Internet Explorer 5.0", "Win 95+", 5, "C"]]' in js_options)
        
    def test_aaSorting(self):
        class DT(datatables.DataTable):
            class Meta:
                aaSorting = [[2,'asc'], [3,'desc']]

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"aaSorting": [[2, "asc"], [3, "desc"]]' in js_options)
        
    def test_aaSortingFixed(self):
        class DT(datatables.DataTable):
            class Meta:
                aaSortingFixed = [[0,'asc']]

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"aaSortingFixed": [[0, "asc"]]' in js_options)

    def test_aLengthMenu(self):
        class DT(datatables.DataTable):
            class Meta:
                aLengthMenu = [[10, 25, 50, -1], [10, 25, 50, "All"]]

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"aLengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]]' in js_options)
        
    def test_aoSearchCols(self):
        class DT(datatables.DataTable):
            class Meta:
                aoSearchCols = [
                                    None,
                                    { "sSearch": "My filter" },
                                    None,
                                    { "sSearch": "^[0-9]", "bEscapeRegex": False }
                               ]

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"aoSearchCols": [null, {"sSearch": "My filter"}, null, {"bEscapeRegex": false, "sSearch": "^[0-9]"}]' in js_options)

    def test_asStripClasses(self):
        class DT(datatables.DataTable):
            class Meta:
                asStripClasses = [ 'strip1', 'strip2', 'strip3' ]

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"asStripClasses": ["strip1", "strip2", "strip3"]' in js_options)

    def test_bDestroy(self):
        class DT(datatables.DataTable):
            class Meta:
                bDestroy = True

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"bDestroy": true' in js_options)

    def test_bRetrieve(self):
        class DT(datatables.DataTable):
            class Meta:
                bRetrieve = True

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"bRetrieve": true' in js_options)
    
    def test_bScrollCollapse(self):
        class DT(datatables.DataTable):
            class Meta:
                bScrollCollapse = True

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"bScrollCollapse": true' in js_options)
        
    def test_bSortCellsTop(self):
        class DT(datatables.DataTable):
            class Meta:
                bSortCellsTop = True

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"bSortCellsTop": true' in js_options)
        
    def test_iCookieDuration(self):
        class DT(datatables.DataTable):
            class Meta:
                iCookieDuration = 60*60*24

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"iCookieDuration": 86400' in js_options)

    def test_iDeferLoading(self):
        class DT(datatables.DataTable):
            class Meta:
                iDeferLoading = 57

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"iDeferLoading": 57' in js_options)
        
    def test_iDisplayLength(self):
        class DT(datatables.DataTable):
            class Meta:
                iDisplayLength = 50

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"iDisplayLength": 50' in js_options)

    def test_iDisplayStart(self):
        class DT(datatables.DataTable):
            class Meta:
                iDisplayStart = 20

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"iDisplayStart": 20' in js_options)

    def test_iScrollLoadGap(self):
        class DT(datatables.DataTable):
            class Meta:
                iScrollLoadGap = 50

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"iScrollLoadGap": 50' in js_options)

    def test_oSearch(self):
        class DT(datatables.DataTable):
            class Meta:
                oSearch = {"sSearch": "Initial search"}

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"oSearch": {"sSearch": "Initial search"}' in js_options)

    def test_sAjaxDataProp(self):
        class DT(datatables.DataTable):
            class Meta:
                sAjaxDataProp = "data"

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"sAjaxDataProp": "data"' in js_options)

    def test_sAjaxSource(self):
        class DT(datatables.DataTable):
            class Meta:
                sAjaxSource = "http://www.sprymedia.co.uk/dataTables/json.php"

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"sAjaxSource": "http://www.sprymedia.co.uk/dataTables/json.php"' in js_options)

    def test_sCookiePrefix(self):
        class DT(datatables.DataTable):
            class Meta:
                sCookiePrefix = "my_datatable_"

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"sCookiePrefix": "my_datatable_"' in js_options)

    def test_sDom(self):
        class DT(datatables.DataTable):
            class Meta:
                sDom = '<"top"i>rt<"bottom"flp><"clear"&lgt;'

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"sDom": "<\\"top\\"i>rt<\\"bottom\\"flp><\\"clear\\"&lgt;"' in js_options)

    def test_sPaginationType(self):
        class DT(datatables.DataTable):
            class Meta:
                sPaginationType = "full_numbers"

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"sPaginationType": "full_numbers"' in js_options)

    def test_sScrollXInner(self):
        class DT(datatables.DataTable):
            class Meta:
                sScrollXInner = "110%"

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"sScrollXInner": "110%"' in js_options)

    # Test Callbacks
    
    # Test Columns

    def test_asSorting(self):
        class DT(datatables.DataTable):
            fortune = datatables.Column(asSorting=[ "desc", "asc", "asc" ])
            lucky_numbers = datatables.Column()

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"asSorting": ["desc", "asc", "asc"]' in js_options)

    def test_bSearchable(self):
        class DT(datatables.DataTable):
            fortune = datatables.Column(bSearchable=False)
            lucky_numbers = datatables.Column()

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"aTargets": [0], "bSearchable": false' in js_options)

    def test_bSortable(self):
        class DT(datatables.DataTable):
            fortune = datatables.Column(bSortable=False)
            lucky_numbers = datatables.Column(bSortable=False)

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"aTargets": [0, 1], "bSortable": false' in js_options)
        
    def test_bUseRendered(self):
        class DT(datatables.DataTable):
            fortune = datatables.Column(bUseRendered=False)
            lucky_numbers = datatables.Column()

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"aTargets": [0], "bUseRendered": false' in js_options)
        
    def test_bVisible(self):
        class DT(datatables.DataTable):
            fortune = datatables.Column(bVisible=False)
            lucky_numbers = datatables.Column(bVisible=False)

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"aTargets": [0, 1], "bVisible": false' in js_options)

    def test_fnRender(self):
        class DT(datatables.DataTable):
            fortune = datatables.Column(fnRender=REPLACEME)
            lucky_numbers = datatables.Column()

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"fnRender": REPLACEME, "aTargets": [0]' in js_options)
        
    def test_iDataSort(self):
        class DT(datatables.DataTable):
            fortune = datatables.Column(sort_field="lucky_numbers")
            lucky_numbers = datatables.Column()

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"aTargets": [0], "iDataSort": 1' in js_options)

    def test_mDataProp(self):
        class DT(datatables.DataTable):
            fortune = datatables.Column(mDataProp=REPLACEME)
            lucky_numbers = datatables.Column()

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"mDataProp": REPLACEME, "aTargets": REPLACEME' in js_options)

    def test_sClass(self):
        class DT(datatables.DataTable):
            fortune = datatables.Column(sClass="my_class")
            lucky_numbers = datatables.Column(sClass="my_class")

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"aTargets": [0, 1], "sClass": "my_class"' in js_options)

    def test_sDefaultContent(self):
        class DT(datatables.DataTable):
            fortune = datatables.Column(sDefaultContent="Edit")
            lucky_numbers = datatables.Column()

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"aTargets": [0], "sDefaultContent": "Edit"' in js_options)

    def test_sName(self):
        class DT(datatables.DataTable):
            fortune = datatables.Column()
            lucky_numbers = datatables.Column(sName="lucky_number_column")

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"aTargets": [1], "sName": "lucky_number_column"' in js_options)

    def test_sSortDataType(self):
        class DT(datatables.DataTable):
            fortune = datatables.Column(sSortDataType="dom-text")
            lucky_numbers = datatables.Column(sSortDataType="dom-text")

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"aTargets": [0, 1], "sSortDataType": "dom-text"' in js_options)

    def test_sTitle(self):
        class DT(datatables.DataTable):
            fortune = datatables.Column(sTitle="My column title")
            lucky_numbers = datatables.Column()

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"aTargets": [0], "sTitle": "My column title"' in js_options)
        
    def test_sType(self):
        class DT(datatables.DataTable):
            fortune = datatables.Column(sType="html")
            lucky_numbers = datatables.Column(sType="html")

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"aTargets": [0, 1], "sType": "html"' in js_options)
        
    def test_sWidth(self):
        class DT(datatables.DataTable):
            fortune = datatables.Column(sWidth="20%")
            lucky_numbers = datatables.Column()

        dt = DT()
        js_options = dt.js_options()

        self.assertTrue('"aTargets": [0], "sWidth": "20%"' in js_options)