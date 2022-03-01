{% comment %}
Javascript
https://codebeautify.org/minify-js

Dependences:
    JQuery

$(document).ready(function() {
    $toggle_save_user = $('#toggle_save_user')
    $toggle_save_user.click(function () {
        // Make AJAX call to save user, and update button look.
        $.ajax({
            type: 'POST',
            url: "{% url 'users:toggle_save_user' lead.author.id %}",
            dataType: 'json',
            success: function (data) {
                if (data['s'] == true) {
                    $toggle_save_user
                        .removeClass('text-slate-600 bg-slate-100 hover:bg-slate-200')
                        .addClass('text-white bg-blue-500 hover:bg-blue-600')
                        .text('Person Saved')
                } else {
                    $toggle_save_user
                        .addClass('text-slate-600 bg-slate-100 hover:bg-slate-200')
                        .removeClass('text-white bg-blue-500 hover:bg-blue-600')
                        .text('Save Person')
                }
            }
        })
    })
})
{% endcomment %}
$(document).ready((function(){$toggle_save_user=$("#toggle_save_user"),$toggle_save_user.click((function(){$.post("{% url 'users:toggle_save_user' lead.author.id %}",(function(e){1==e.s?$toggle_save_user.removeClass("text-slate-600 bg-slate-100 hover:bg-slate-200").addClass("text-white bg-blue-500 hover:bg-blue-600").text("Person Saved"):$toggle_save_user.addClass("text-slate-600 bg-slate-100 hover:bg-slate-200").removeClass("text-white bg-blue-500 hover:bg-blue-600").text("Save Person")}))}))}));