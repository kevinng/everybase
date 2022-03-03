$(document).ready((function(){function e(){author_type_val=$author_type.val(),"direct"==author_type_val?($commission_payable_by__label.hide(),$commission_payable_by__input.hide(),$commission_payable_by__help.hide(),$commission_payable_by__errors.hide()):"broker"==author_type_val&&$need_agent.is(":checked")&&($commission_payable_by__label.show(),$commission_payable_by__input.show(),$commission_payable_by__help.show(),$commission_payable_by__errors.show())}function _(){$author_type__label.text("Are you a direct buyer or a middleman?"),$author_type__option__direct.text("Direct Buyer"),$author_type.select2(),$buy_country__label.text("Buy From This Country"),$buy_country__option__any_country.attr("disabled",!1),$buy_country__help.text("Country you'd like to buy or source from."),$sell_country__label.text("Destination Country"),$sell_country__option__any_country.attr("disabled",!0),"any_country"==$sell_country.find("option:selected").val()&&$sell_country.val(null).trigger("change"),$sell_country__help.text("Country your goods/services are imported into or needed."),$details__help.text("Describe goods/services you'd like to buy"),$need_agent__question.text("Do you need agents to help you buy or source?"),$need_agent__label.text("Yes, I need agents to help me buy"),$need_agent__help.text("Agents help you buy or source for goods/services for commissions."),$commission_payable_by__help.text("You're a middleman. Will commission be paid by you or the buyer?"),$commission_payable_by__option__counter_party.text("Buyer"),$commission_payable_by__option__counter_party.val("buyer"),$commission_payable_by__option__counter_party.select2()}function o(){$sell_country__label.text("Sell In This Country"),$sell_country__option__any_country.attr("disabled",!1),$sell_country__help.text("Country you'd like to sell your goods/services in."),$buy_country__label.text("Source Country"),$buy_country__option__any_country.attr("disabled",!0),"any_country"==$buy_country.find("option:selected").val()&&$buy_country.val(null).trigger("change"),$buy_country__help.text("Country your goods/services are exported from or based in."),$details__help.text("Describe goods/services you'd like to sell"),$author_type__label.text("Are you a direct seller or a middleman?"),$author_type__option__direct.text("Direct Seller"),$author_type.select2(),$need_agent__question.text("Do you need agents to help you sell or promote?"),$need_agent__label.text("Yes, I need agents to help me sell"),$need_agent__help.text("Agents help you sell or promote your goods/services for commissions."),$commission_payable_by__help.text("You're a middleman. Will commission be paid by you or the seller?"),$commission_payable_by__option__counter_party.text("Seller"),$commission_payable_by__option__counter_party.val("seller"),$commission_payable_by__option__counter_party.select2()}function i(){choice=$lead_type.val(),"buying"==choice?_():"selling"==choice&&o()}function a(){e(),$commission_type__label.show(),$commission_type__input.show(),$commission_type__errors.show(),"other"==$commission_type.val()&&($commission_type_other.show(),$commission_type_other__errors.show(),$commission_type_other__help.show()),"other"!=$commission_type.val()&&($commission__label.show(),$commission__input.show(),$commission__errors.show(),$commission__help.show()),"other"!=$commission_type.val()&&($avg_deal_size__label.show(),$avg_deal_size__input.show(),$avg_deal_size__errors.show(),$avg_deal_size__help.show()),"other"!=$commission_type.val()&&($avg_earnings__label.show(),$avg_earnings__value.show(),$avg_earnings__help.show()),$is_comm_negotiable__label.show(),$is_comm_negotiable__input.show(),$other_agent_details__label.show(),$other_agent_details.show(),$other_agent_details__errors.show(),$commission_payable_after__label.show(),$commission_payable_after__input.show(),$commission_payable_after__errors.show(),c()}function s(){$commission_type__label.hide(),$commission_type__input.hide(),$commission_type__errors.hide(),$commission_type_other.hide(),$commission_type_other__errors.hide(),$commission_type_other__help.hide(),$commission__label.hide(),$commission__input.hide(),$commission__errors.hide(),$commission__help.hide(),$avg_deal_size__label.hide(),$avg_deal_size__input.hide(),$avg_deal_size__errors.hide(),$avg_deal_size__help.hide(),$avg_earnings__label.hide(),$avg_earnings__value.hide(),$avg_earnings__help.hide(),$is_comm_negotiable__label.hide(),$is_comm_negotiable__input.hide(),$other_agent_details__label.hide(),$other_agent_details.hide(),$other_agent_details__errors.hide(),$commission_payable_after__label.hide(),$commission_payable_after__input.hide(),$commission_payable_after__errors.hide(),$commission_payable_by__label.hide(),$commission_payable_by__input.hide(),$commission_payable_by__help.hide(),$commission_payable_by__errors.hide(),$commission_payable_after_other.hide(),$commission_payable_after_other__errors.hide(),$commission_payable_after_other__help.hide()}function t(){$need_agent.is(":checked")?a():s()}function n(){$commission_type_other.hide(),$commission_type_other__errors.hide(),$commission_type_other__help.hide(),$commission__label.show(),$commission__input.show(),$commission__errors.show(),$commission__help.show(),$avg_deal_size__label.show(),$avg_deal_size__input.show(),$avg_deal_size__errors.show(),$avg_deal_size__help.show(),$avg_earnings__label.show(),$avg_earnings__value.show(),$avg_earnings__help.show()}function l(){$commission_type_other.show(),$commission_type_other__errors.show(),$commission_type_other__help.show(),$commission__label.hide(),$commission__input.hide(),$commission__errors.hide(),$commission__help.hide(),$avg_deal_size__label.hide(),$avg_deal_size__input.hide(),$avg_deal_size__errors.hide(),$avg_deal_size__help.hide(),$avg_earnings__label.hide(),$avg_earnings__value.hide(),$avg_earnings__help.hide()}function r(){choice=$commission_type.val(),"percentage"==choice?n():"other"==choice&&l()}function m(){if(""==$commission.val())$commission__js_errors.hide();else{if($commission.val()<.01||$commission.val()>100)return $avg_earnings__value_1.text("?"),$avg_earnings__value_2.text("?"),$commission__js_errors.text("Agent commission must be between 0.01% and 100%"),void $commission__js_errors.show();$commission__js_errors.hide()}avg_earnings=0,isNaN($avg_deal_size.val())||(avg_earnings=$commission.val()/100*$avg_deal_size.val()),avg_earnings=avg_earnings.toFixed(0),$avg_earnings__value_1.text(avg_earnings),$avg_earnings__value_2.text(avg_earnings)}function c(){"other"==$commission_payable_after.val()?($commission_payable_after_other.show(),$commission_payable_after_other__errors.show(),$commission_payable_after_other__help.show()):($commission_payable_after_other.hide(),$commission_payable_after_other__errors.hide(),$commission_payable_after_other__help.hide())}function h(){$need_logistics_agent.is(":checked")?($other_logistics_agent_details__label.show(),$other_logistics_agent_details.show(),$other_logistics_agent_details__errors.show()):($other_logistics_agent_details__label.hide(),$other_logistics_agent_details.hide(),$other_logistics_agent_details__errors.hide())}function p(){$friendly.is(":checked")?($submit.removeAttr("disabled"),$submit.addClass("bg-blue-500 hover:bg-blue-600"),$submit.removeClass("bg-blue-200")):($submit.prop("disabled",!0),$submit.removeClass("bg-blue-500 hover:bg-blue-600"),$submit.addClass("bg-blue-200"))}function g(e,_,o,i){e.find(":first-child").remove(),e.text("No image chosen"),_.length>0&&_.val("no"),o.hide(),i.show()}function y(e,_,o,i){img='<img src="'+_+'">',e.text(""),e.append(img),o.show(),i.hide()}function u(e,_,o,i,a){e.click((function(){e.val("")})),e.change((function(){g(_,o,i,a),files=e.prop("files"),files.length>0&&y(_,URL.createObjectURL(files[0]),i,a)}))}function b(e,_,o,i){e.click((function(){g(_,o,e,i)}))}function d(e,_,o,i,a){e.length>0?y(_,e.val(),i,a):g(_,o,i,a)}$lead_create=$("#lead_create"),$lead_type=$("#lead_type"),$author_type=$("#author_type"),$author_type__label=$("#author_type__label"),$author_type__option__direct=$("#author_type__option__direct"),$buy_country=$("#buy_country"),$buy_country__label=$("#buy_country__label"),$buy_country__option__any_country=$("#buy_country__option__any_country"),$buy_country__help=$("#buy_country__help"),$sell_country=$("#sell_country"),$sell_country__label=$("#sell_country__label"),$sell_country__option__any_country=$("#sell_country__option__any_country"),$sell_country__help=$("#sell_country__help"),$details__help=$("#details__help"),$image_one_input_label=$("#image_one_input_label"),$image_one_preview=$("#image_one_preview"),$image_one=$("#image_one"),$image_two_input_label=$("#image_two_input_label"),$image_two_preview=$("#image_two_preview"),$image_two=$("#image_two"),$image_three_input_label=$("#image_three_input_label"),$image_three_preview=$("#image_three_preview"),$image_three=$("#image_three"),$image_one_cache_use=$("#image_one_cache_use"),$image_one_cache_file_id=$("#image_one_cache_file_id"),$image_one_cache_url=$("#image_one_cache_url"),$image_one_remove=$("#image_one_remove"),$image_two_cache_use=$("#image_two_cache_use"),$image_two_cache_file_id=$("#image_two_cache_file_id"),$image_two_cache_url=$("#image_two_cache_url"),$image_two_remove=$("#image_two_remove"),$image_three_cache_use=$("#image_three_cache_use"),$image_three_cache_file_id=$("#image_three_cache_file_id"),$image_three_cache_url=$("#image_three_cache_url"),$image_three_remove=$("#image_three_remove"),$need_agent__question=$("#need_agent__question"),$need_agent=$("#need_agent"),$need_agent__help=$("#need_agent__help"),$need_agent__label=$("#need_agent__label"),$commission_type__label=$("#commission_type__label"),$commission_type__input=$("#commission_type__input"),$commission_type__errors=$("#commission_type__errors"),$commission_type=$("#commission_type"),$commission_type_other=$("#commission_type_other"),$commission_type_other__errors=$("#commission_type_other__errors"),$commission_type_other__help=$("#commission_type_other__help"),$commission_payable_by__label=$("#commission_payable_by__label"),$commission_payable_by__input=$("#commission_payable_by__input"),$commission_payable_by__option__counter_party=$("#commission_payable_by__option__counter_party"),$commission_payable_by__help=$("#commission_payable_by__help"),$commission_payable_by__errors=$("#commission_payable_by__errors"),$commission=$("#commission"),$commission__label=$("#commission__label"),$commission__input=$("#commission__input"),$commission__errors=$("#commission__errors"),$commission__js_errors=$("#commission__js_errors"),$commission__help=$("#commission__help"),$avg_deal_size=$("#avg_deal_size"),$avg_deal_size__label=$("#avg_deal_size__label"),$avg_deal_size__input=$("#avg_deal_size__input"),$avg_deal_size__errors=$("#avg_deal_size__errors"),$avg_deal_size__help=$("#avg_deal_size__help"),$avg_earnings__label=$("#avg_earnings__label"),$avg_earnings__value=$("#avg_earnings__value"),$avg_earnings__value_1=$("#avg_earnings__value_1"),$avg_earnings__value_2=$("#avg_earnings__value_2"),$avg_earnings__help=$("#avg_earnings__help"),$is_comm_negotiable__label=$("#is_comm_negotiable__label"),$is_comm_negotiable__input=$("#is_comm_negotiable__input"),$commission_payable_after=$("#commission_payable_after"),$commission_payable_after__label=$("#commission_payable_after__label"),$commission_payable_after__input=$("#commission_payable_after__input"),$commission_payable_after__errors=$("#commission_payable_after__errors"),$commission_payable_after_other=$("#commission_payable_after_other"),$commission_payable_after_other__errors=$("#commission_payable_after_other__errors"),$commission_payable_after_other__help=$("#commission_payable_after_other__help"),$other_agent_details=$("#other_agent_details"),$other_agent_details__label=$("#other_agent_details__label"),$other_agent_details__errors=$("#other_agent_details__errors"),$friendly=$("#friendly"),$need_logistics_agent=$("#need_logistics_agent"),$other_logistics_agent_details=$("#other_logistics_agent_details"),$other_logistics_agent_details__label=$("#other_logistics_agent_details__label"),$other_logistics_agent_details__errors=$("#other_logistics_agent_details__errors"),$submit=$("#submit"),$select2=$(".select2"),$select2.select2(),$select2.one("select2:open",(function(e){$("input.select2-search__field").prop("placeholder","Search here...")})),i(),e(),m(),c(),r(),t(),h(),p(),$lead_type.change((function(){i()})),$author_type.change((function(){e()})),$need_agent.change((function(){e(),t()})),$commission_type.change((function(){r()})),$commission.on("input",(function(){m()})),$avg_deal_size.on("input",(function(){m()})),$commission_payable_after.change((function(){c()})),$friendly.change((function(){p()})),$need_logistics_agent.change((function(){h()})),$lead_create.submit((function(){JsLoadingOverlay.show({overlayBackgroundColor:"#666666",overlayOpacity:.6,spinnerIcon:"ball-circus",spinnerColor:"#000",spinnerSize:"3x",overlayIDName:"overlay",spinnerIDName:"spinner",offsetY:0,offsetX:0,lockScroll:!1,containerID:null})})),u($image_one,$image_one_preview,$image_one_cache_use,$image_one_remove,$image_one_input_label),u($image_two,$image_two_preview,$image_two_cache_use,$image_two_remove,$image_two_input_label),u($image_three,$image_three_preview,$image_three_cache_use,$image_three_remove,$image_three_input_label),d($image_one_cache_url,$image_one_preview,$image_one_cache_use,$image_one_remove,$image_one_input_label),d($image_two_cache_url,$image_two_preview,$image_two_cache_use,$image_two_remove,$image_two_input_label),d($image_three_cache_url,$image_three_preview,$image_three_cache_use,$image_three_remove,$image_three_input_label),b($image_one_remove,$image_one_preview,$image_one_cache_use,$image_one_input_label),b($image_two_remove,$image_two_preview,$image_two_cache_use,$image_two_input_label),b($image_three_remove,$image_three_preview,$image_three_cache_use,$image_three_input_label)}));