<script type="text/javascript">
    // Initialize select picker
    var document__selectpicker = function () {
        var init_selectpicker = function () {
            $('.kt-selectpicker').selectpicker();
        }

        return {
            run: function () {
                init_selectpicker(); 
            }
        };
    }();

    // Hide/show batch code field
    var document__hide_show_batch_code = function () {

        var document_types = [
            {% for document_type in document_types %}
                {
                    id: '{{ document_type.id }}',
                    name: '{{ document_type.name }}',
                    acronym: '{{ document_type.acronym }}',
                    level: '{{ document_type.level }}'
                }{% if not forloop.last %},{% endif %}
            {% endfor %}
        ];

        var hide_show = function () {
            var selected_dt_id = $('#document__document_type')
                .children("option:selected")
                .val();

            var dt = document_types.filter(t => t['id'] == selected_dt_id)[0];
            if (dt === undefined) {
                return;
            }

            var element = $('#document__batch_code_span');
            if (dt.level == 'batch') {
                element.removeClass('kt-hidden');
            } else if (dt.level == 'material') {
                element.addClass('kt-hidden');
            }
        }

        var hide_show_on_change = function () {
            $('#document__document_type').change(function () {
                hide_show();
            });
        }

        return {
            run: function () {
                hide_show();
            },
            run_on_change: function () {
                hide_show_on_change();
            }
        }
    }();

    // Select the right material code on selected material name, vice versa
    var document__select_material = function () {

        // We're triggering change on 'code' when 'name' changes and vice
        // versa. This variable prevents both elements from calling each
        // other in an infinite loop.
        var stop = false;

        var mirror_selection = function (selected) {
            mirror = '#document__material_name'
            if (selected == '#document__material_name') {
                mirror = '#document__material_code'
            }

            if (stop == true) { 
                stop = false;
                return;
            }

            var material_id = $(selected)
                .children("option:selected")
                .val();

            $(mirror).val(material_id);
            $('#document__material_id').val(material_id);
            stop = true
            $(mirror).trigger('change');
        }

        var select_on_change = function () {
            $('#document__material_name').change(function () {
                mirror_selection('#document__material_name');
            });

            $('#document__material_code').change(function () {
                mirror_selection('#document__material_code');
            });
        }

        var select_with_set_material_id = function () {
            var material_id = $('#document__material_id').val();
            $('#document__material_name').val(material_id);
            $('#document__material_code').val(material_id);
            stop = true // Prevent recursive trigger
            $('#document__material_name').trigger('change');
            stop = true // Prevent recursive trigger
            $('#document__material_code').trigger('change');
        }

        return {
            init: function () {
                select_with_set_material_id();
            },
            run: function () {
                select_code();
                stop = false;
            },
            run_on_change: function () {
                select_on_change();
            }
        }
    }();

    var document__refresh_file = function () {
        
        var render_file = function (url) {
            var options = {height: "1200px"};
            PDFObject.embed(url, "#document__document_file", options);
        }

        var read_file_presigned_url = function (file_id) {
            $.ajax({
                type: 'POST',
                headers: { "X-CSRFToken": '{{ csrf_token }}' },
                url: '{% url 'documents:read_file' %}',
                data: {'file_id': file_id},
                dataType: 'json',
                success: function (response) {
                    render_file(response.url);
                }
            });
        }

        var trigger_once = function () {
            var file_id = $('#document__file_id').val()
            if (file_id) {
                read_file_presigned_url(file_id);
            }
        }

        var trigger_on_change = function () {
            $('#document__file_id').change(function () {
                trigger_once()
            })
        }

        return {
            run: function () {
                trigger_once();
            },
            run_on_change: function () {
                trigger_on_change();
            }
        }
    }();

    var document__upload_file = function () {

        var upload_file = function (temp_file, file) {
            var res = temp_file.presigned_url_response;
            var post_data = new FormData();
            for (key in res.fields) {
                post_data.append(key, res.fields[key]);
            }
            post_data.append('file', file);

            var xhr = new XMLHttpRequest();
            xhr.open('POST', res.url);
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200 || xhr.status === 204) {
                        // Hide error messages - if any
                        $('#document__document_file_input').removeClass('is-invalid');
                        $('#document__document_file_input_error_pdf_only').addClass('kt-hidden');
                        $('#document__document_file_input_error_cannot_upload').addClass('kt-hidden');
                        
                        $('#document__file_id')
                            .val(temp_file.id)
                            .trigger('change');
                    } else {
                        // Show error messages
                        $('#document__document_file_input').addClass('is-invalid');
                        $('#document__document_file_input_error_cannot_upload').removeClass('kt-hidden');
                    }

                    // Unlock portlet
                    KTApp.unblock('#document__file_input_portlet');

                    // Enable button
                    $('#document__create_document_button')
                        .attr("disabled", false);
                }
            };

            // Block portlet
            KTApp.block('#document__file_input_portlet', {
                type: 'v2',
                state: 'primary',
                message: 'Uploading...'
            });

            // Disable submit button
            $('#document__create_document_button')
                .attr("disabled", true);

            xhr.send(post_data);
        }

        var create_file_presigned_url = function (file) {
            $.ajax({
                type: 'POST',
                headers: { "X-CSRFToken": '{{ csrf_token }}' },
                url: '{% url 'documents:temp_file' %}',
                data: {
                    'filetype': file.type
                },
                dataType: 'json',
                success: function (temp_file) {
                    upload_file(temp_file, file);
                }
            });
        }

        var trigger_on_change = function () {
            var file_input = $('#document__document_file_input')
            file_input.change(function () {
                var file = file_input.prop('files')[0];

                if (file.type != 'application/pdf') {
                    $('#document__document_file_input').addClass('is-invalid');
                    $('#document__document_file_input_error_pdf_only').removeClass('kt-hidden');
                    return;
                } else {
                    $('#document__document_file_input').removeClass('is-invalid');
                    $('#document__document_file_input_error_pdf_only').addClass('kt-hidden');
                }

                create_file_presigned_url(file);
            });
        }

        return {
            run_on_change: function () {
                trigger_on_change();
            }
        }
    }();

    // Call all functions on document ready
    jQuery(document).ready(function () {
        document__selectpicker.run();
        document__hide_show_batch_code.run(); // Run once on load
        document__hide_show_batch_code.run_on_change();
        document__select_material.run_on_change();
        document__select_material.init();
        document__refresh_file.run();
        document__refresh_file.run_on_change();
        document__upload_file.run_on_change();
    });
</script>