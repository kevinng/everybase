$(document).ready((function(){sourcing=$("#sourcing"),promoting=$("#promoting"),need_logistics=$("#need_logistics"),sourcing_agent=$("#sourcing_agent"),sales_agent=$("#sales_agent"),logistics_agent=$("#logistics_agent"),other=$("#other"),sm_sourcing=$("#sm_sourcing"),sm_promoting=$("#sm_promoting"),sm_need_logistics=$("#sm_need_logistics"),sm_sourcing_agent=$("#sm_sourcing_agent"),sm_sales_agent=$("#sm_sales_agent"),sm_logistics_agent=$("#sm_logistics_agent"),sm_other=$("#sm_other"),search_form=$("#search_form"),reduce_spams_and_scams=$("#reduce_spams_and_scams"),user_country=$("#user_country"),user_country_verified=$("#user_country_verified");var e=document.querySelector("#search_form"),s=new KTBlockUI(e);function _(){search_form.submit(),s.block()}function c(e,s){s.change((function(){e.prop("checked",this.checked),_()})),e.change((function(){s.prop("checked",this.checked),_()}))}c(sourcing,sm_sourcing),c(promoting,sm_promoting),c(need_logistics,sm_need_logistics),c(sourcing_agent,sm_sourcing_agent),c(sales_agent,sm_sales_agent),c(logistics_agent,sm_logistics_agent),c(other,sm_other),reduce_spams_and_scams.change((function(){_()})),user_country_verified.change((function(){_()})),user_country.change((function(){_()})),$(document).ready((function(){function e(){via_wechat.is(":checked")?via_wechat_id_div.show():via_wechat_id_div.hide()}via_wechat_id_div=$("#via_wechat_id_div"),via_wechat=$("#via_wechat"),e(),via_wechat.click((function(){e()}))}))}));