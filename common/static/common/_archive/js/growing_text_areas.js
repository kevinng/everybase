// Dependencies
//  JQuery
$(document).ready(function() {
    // Run on load
    $('.growing').each(function() {
        while ($(this).outerHeight() < this.scrollHeight +
            parseFloat($(this).css("borderTopWidth")) +
            parseFloat($(this).css("borderBottomWidth"))) {
            $(this).height($(this).height() + 1)
        }
    })

    // Run on key up
    $('.growing').keyup(function() {
        while ($(this).outerHeight() < this.scrollHeight +
            parseFloat($(this).css("borderTopWidth")) +
            parseFloat($(this).css("borderBottomWidth"))) {
            $(this).height($(this).height() + 1)
        }
    })
})