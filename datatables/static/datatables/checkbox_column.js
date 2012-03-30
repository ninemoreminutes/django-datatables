var datatables_checkbox_columns_initialized = false;

$(function() {
    function header_has_been_clicked() {
        if (($('input[name="' +  $(this).attr('name')+ '_hidden"]').val() == 'None') || ($('input[name="' +  $(this).attr('name')+ '_hidden"]').val() == 'Some')) {
            $('input[name="' +  $(this).attr('name')+ '_hidden"]').val('All');
            $(this).addClass('all_selected').removeClass('none_selected').removeClass('some_selected');
            var checked = 'checked';
        } else if ($('input[name="' +  $(this).attr('name')+ '_hidden"]').val() == 'All') {
            $('input[name="' +  $(this).attr('name')+ '_hidden"]').val('None');
            $(this).addClass('none_selected').removeClass('all_selected').removeClass('some_selected');
            var checked = false;
        }
        checkboxes = $('div.dataTables_wrapper').find('input.datatables_checkbox_column[name="' +  $(this).attr('name') + '"]');
        checkboxes.each(function(index) {
            if (checked == 'checked') {
                $(this).siblings('a').addClass('checked');
                $(this).parents('tr').addClass('row_selected');
            } else {
                $(this).siblings('a').removeClass('checked');
                $(this).parents('tr').removeClass('row_selected');
            }
            if ($(this).prop('checked') != checked) {
                $(this).prop('checked', checked);
            }
        });
        $('input.datatables_checkbox_column')[0].click();
        $('input.datatables_checkbox_column')[0].click();
    }
    
    function checkbox_has_been_clicked() {
        var checked = $(this).siblings('input').prop('checked');
        if (checked == false) {
            $(this).addClass('checked');
            $(this).parents('tr').addClass('row_selected');
            checked = 'checked';
        } else {
            $(this).removeClass('checked');
            $(this).parents('tr').removeClass('row_selected');
            checked = false;
        }
        $(this).siblings('input:first').prop('checked', checked);
        $(this).siblings('input').click();
        $(this).siblings('input:first').prop('checked', checked);
        if (checked == 'checked') {
            checked = true;
        }
        var unanimous = true;
        checkboxes = $('div.dataTables_wrapper').find('input.datatables_checkbox_column[name="' +  $(this).siblings('input:first').attr('name') + '"]');
        checkboxes.each(function(index) {
            if ($(this).prop('checked') != checked) {
                unanimous = false;
            }
        });
        if (unanimous == true) {
            if (checked == true) {
                $('a[name="' + $(this).siblings('input:first').attr('name') + '"]').addClass('all_selected').removeClass('none_selected').removeClass('some_selected');
                $('input[name="' +  $(this).siblings('input:first').attr('name')+ '_hidden"]').val('All');
            } else {
                $('a[name="' + $(this).siblings('input:first').attr('name') + '"]').addClass('none_selected').removeClass('all_selected').removeClass('some_selected');
                $('input[name="' +  $(this).siblings('input:first').attr('name')+ '_hidden"]').val('None');
            }
        } else {
            $('a[name="' + $(this).siblings('input:first').attr('name') + '"]').addClass('some_selected').removeClass('none_selected').removeClass('all_selected');
            $('input[name="' +  $(this).siblings('input:first').attr('name')+ '_hidden"]').val('Some');
        }
    }
    
    if (!datatables_checkbox_columns_initialized) {
        $('a.django_datatables_tristate_checkbox').on('click', header_has_been_clicked);
        $('a.django_datatables_bistate_checkbox').on('click', checkbox_has_been_clicked);
        datatables_checkbox_columns_initialized = true;
      }
});