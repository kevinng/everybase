$(document).ready((function(){function e(e){const n=document.getElementById(e),i=n.nextElementSibling;new ClipboardJS(i,{target:n,text:function(){return n.value}}).on("success",(function(n){const t=i.innerHTML;if("Copied!"!==i.innerHTML)if(i.innerHTML="Copied!",setTimeout((function(){i.innerHTML=t}),3e3),"email_clipboard"==e){var o=(new amplitude.Identify).add("num emails copied",1);amplitude.getInstance().identify(o),amplitude.getInstance().logEvent("qualification - copied email",{"contact id":"{{ contact.id }}"})}else if("phone_number_clipboard"==e){o=(new amplitude.Identify).add("num phone numbers copied",1);amplitude.getInstance().identify(o),amplitude.getInstance().logEvent("qualification - copied phone number",{"contact id":"{{ contact.id }}"})}}))}e("email_clipboard"),e("phone_number_clipboard")}));