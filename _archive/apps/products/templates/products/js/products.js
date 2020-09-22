<script type="text/javascript">
var ProductsTable = function() {
    var options = {

        data: {
            type: 'local',
            source: dataJSONArray,
        },

        layout: {
            scroll: false,
            footer: false,
        },

        sortable: false,
        pagination: false,

        columns: [
            {
                field: 'id',
                title: '#',
                sortable: false,
                width: 20,
                selector: {class: 'kt-checkbox--solid'},
                textAlign: 'center',
            }, {
                field: 'short_id',
                title: 'Product ID',
                width: 80,
            }, {
                field: 'description',
                title: 'Description',
                autoHide: false,
                width: 200,
            }, {
                field: 'quantity',
                title: 'Quantity',
                autoHide: false,
                width: 70,
            }],
    };

    var initProductsTable = function() {

        var enable_or_disable_submit_button = function () {
            var checkedNodes = datatable.rows('.kt-datatable__row--active').nodes();
            var count = checkedNodes.length;

            if ($('#email_txt').val().length == 0 ||
                $('#full_name_txt').val().length == 0 ||
                count == 0) {
                
                // Disable submit button
                $('.submit_btn').attr('disabled', 'true');

            } else if ($('#email_txt').val().length > 0 &&
                $('#full_name_txt').val().length > 0 &&
                count > 0) {
                
                // Enable submit button
                $('.submit_btn').removeAttr('disabled');
            }
        }

        $('#full_name_txt').keyup(function() {
            enable_or_disable_submit_button();
        });
    
        $('#email_txt').keyup(function() {
            enable_or_disable_submit_button();
        });

        var datatable = $('#products_table').KTDatatable(options);
        datatable.on(
            'kt-datatable--on-check kt-datatable--on-uncheck kt-datatable--on-layout-updated',
            function(e) {
                enable_or_disable_submit_button()

                var checkedNodes = datatable.rows('.kt-datatable__row--active').nodes();
                var count = checkedNodes.length;
                if (count > 0) {
                    var product_str = 'product'
                    if (count > 1) { product_str = 'products' }
                    $('#prompter_msg').text(count + ' ' + product_str + ' selected');
                } else {
                    $('#prompter_msg').text('Select interested products and send enquiry');
                }

                // Get selected row IDs
                var ids = datatable.rows('.kt-datatable__row--active').
                    nodes().
                    find('.kt-checkbox--single > [type="checkbox"]').
                    map(function(i, chk) {
                        return $(chk).val();
                    });
                
                // Remove all hidden inputs storing selected products IDs
                $('input[name="selected_products"]').remove()

                // Append all selected row IDs as hidden input elements to the
                // request-for-information form.
                all_selected_ids = ''
                for (var i = 0; i < ids.length; i++) {
                    all_selected_ids = ids[i] + ';' + all_selected_ids
                }

                $('#rfi_form').append('<input type="hidden" name="selected_products" value="' + all_selected_ids + '" />');
            });
    };

    return {
        init: function() {
            initProductsTable();
        },
    };
}();

jQuery(document).ready(function() {
    ProductsTable.init();
});
</script>