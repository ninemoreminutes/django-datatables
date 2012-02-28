var datatables_checkbox_columns_initialized = false;

$(function() {
    function header_has_been_clicked() {
        //FIXME: Change #checkbox_header and location to be variables
        if (($('#checkbox_header').val() == 'None') || ($('#checkbox_header').val() == 'Some')) {
            $('#checkbox_header').val('All');
            $('#my_span').css('color', 'red');
            var checked = 'checked';
        } else if ($('#checkbox_header').val() == 'All') {
            $('#checkbox_header').val('None');
            $('#my_span').css('color', 'blue');
            var checked = false;
        }
        checkboxes = $('div.dataTables_wrapper').find('input.datatables_checkbox_column[name="location"]');
        checkboxes.each(function(index) {
            if ($(this).prop('checked') != checked) {
                $(this).prop('checked', checked);
            }
        });
        $('input.datatables_checkbox_column')[0].click();
        $('input.datatables_checkbox_column')[0].click();
    }
    
    function checkbox_has_been_clicked() {
        var checked = $(this).prop('checked');
        var original_box = $(this);
        var unanimous = true;
        checkboxes = $('div.dataTables_wrapper').find('input.datatables_checkbox_column[name="location"]');
        checkboxes.each(function(index) {
            if ($(this).prop('checked') != checked) {
                unanimous = false;
            }
        });
        if (unanimous == true) {
            if (checked == true) {
                $('#my_span').css('color', 'red');
                $('#checkbox_header').val('All');
            } else {
                $('#my_span').css('color', 'blue');
                $('#checkbox_header').val('None');
            }
        } else {
            $('#my_span').css('color', 'purple');
            $('#checkbox_header').val('Some');
        }
    }
    
    if (!datatables_checkbox_columns_initialized) {
        $('a#my_span').live('click', header_has_been_clicked);
        $('input.datatables_checkbox_column').live('click', checkbox_has_been_clicked);
        datatables_checkbox_columns_initialized = true;
      }
});