$(document).ready((function(){function e(){$("#status").val().length>0&&(a=parseInt(numFilesProcessing.val())-parseInt(numFilesRemoved.val()),b=parseInt(numFilesProcessing.val())-parseInt(numFilesSuccess.val())-parseInt(numFilesError.val()),(a>b?b:a)<=0)?$("#save").removeAttr("disabled"):(console.log(""),$("#save").attr("disabled",!0))}new Dropzone("#status_dropzone",{url:uploadStatusImageURL,params:{form_uuid:formUUID},paramName:"file",acceptedFiles:"image/*",maxFiles:maxFiles,maxFilesize:maxFileSize,addRemoveLinks:!0,renameFile:function(e){return uuid=([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g,(e=>(e^crypto.getRandomValues(new Uint8Array(1))[0]&15>>e/4).toString(16))),uuid},init:function(){this.on("processing",(function(n){e(),numFilesProcessing.val(parseInt(numFilesProcessing.val())+1)})),this.on("success",(function(n,s){numFilesSuccess.val(parseInt(numFilesSuccess.val())+1),e()})),this.on("error",(function(n,s,a){numFilesError.val(parseInt(numFilesError.val())+1),e()})),this.on("removedfile",(function(n,s,a){let i=new Headers;i.append("Accept","application/json"),i.append("Content-Type","application/json"),fetch(deleteStatusImageURL,{method:"POST",mode:"same-origin",credentials:"include",redirect:"follow",headers:i,body:JSON.stringify({file_uuid:n.upload.filename,form_uuid:formUUID})}),numFilesRemoved.val(parseInt(numFilesRemoved.val())+1),e()}))}})}));