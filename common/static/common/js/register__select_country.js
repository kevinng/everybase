$(document).ready((function(){$("#country").change((function(){$(this).val().length>0?$("#submit").removeAttr("disabled"):$("#submit").attr("disabled",!0)}))}));