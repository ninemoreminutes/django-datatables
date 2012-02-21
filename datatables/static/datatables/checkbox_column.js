var datatables_checkbox_columns_initialized = false;
$(function() {
  function update_datatables_checkbox_columns() {
    var checked = $(this).prop('checked');
    var checkboxes = $(this);
    if ($(this).val() == '__ALL__') {
      checkboxes = $(this).parents('div.dataTables_wrapper').find('input.datatables_checkbox_column[name="' + $(this).attr('name') + '"]');
      checkboxes.prop('checked', checked);
    }
    checkboxes.parents('tr')[checked ? 'addClass' : 'removeClass']('row_selected');
    //console.log($(this).val() + ', ' + $(this).attr('name'));
  }
  if (!datatables_checkbox_columns_initialized) {
    //update_datatables_checkbox_columns();
    $('input.datatables_checkbox_column').live('click', update_datatables_checkbox_columns);
    datatables_checkbox_columns_initialized = true;
  }
});
