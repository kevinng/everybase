// Dependencies
//  JQuery
$(document).ready(function() {
    $(".growing").keyup(function(e) {
        while($(this).outerHeight() < this.scrollHeight + parseFloat($(this).css("borderTopWidth")) + parseFloat($(this).css("borderBottomWidth"))) {
            $(this).height($(this).height()+1)
        }
    })
})