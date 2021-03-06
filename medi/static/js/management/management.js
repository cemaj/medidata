function render_permission() {
  var totalForms = parseInt($("#id_form-TOTAL_FORMS").val());
  var htmlTH = "";
  for(var i = 1; i<=totalForms; i++) {
    var children = $("#id_form-" + (i-1) + "-permissions li label");
    var html = "";
    children.map(function(index, el) {
      if(i==1){
        htmlTH += "<th>" + el.innerText + "</th>";
      }
      el.innerHTML = el.innerHTML.replace(el.innerText,"");
      html += "<td>" + el.innerHTML + "</td>";
    });
    $("#permissionTD_" + i).replaceWith(html);
  }
  $("#permissionTH").replaceWith(htmlTH);
}

function changeUserType(userType) {
  $("#bank_detail").hide();
  $(".organisations").parent().hide();
  $("#user_role").hide();
  $("#gp_user_role").hide();
  $("#client_user_role").hide();
  if(userType === "GP"){
    $("#bank_detail").show();
    $("#id_gp_organisation").parent().show();
    $("#user_role").show();
    $("#gp_user_role").show();
  }else if(userType === "CLT"){
    $("#id_gp_organisation").show();
    $("#id_client_organisation").parent().show();
    $("#user_role").show();
    $("#client_user_role").show();
  }else{
    $("#id_medi_organisation").show();
    $("#id_medi_organisation").parent().show();
  }
}

function hideOrganisation() {
  $(".organisations").parent().hide();
  $("#id_medi_organisation").parent().show();
}

function setDefaultData() {
  var userType = $("#id_user_type").val();
  var sortCode = $("#id_payment_bank_sort_code").val();
  if(userType === "GP"){
    $("input[type=checkbox][class=gp_btn][value=" + $("#id_role").val() + "]:first").attr("checked", "true");
    var length = sortCode.length;
    if(length > 3){
      var subNumber = Math.round(length / 3);
      $("#sortcode1").val(sortCode.substring(0,subNumber));
      $("#sortcode2").val(sortCode.substring(subNumber,subNumber*2));
      if(length % 3){
        $("#sortcode3").val(sortCode.substring(subNumber*2,(subNumber*3)+1));
      }else{
        $("#sortcode3").val(sortCode.substring(subNumber*2,subNumber*3));
      }
    }else{
      $("#sortcode1").val(sortCode);
    }
  }else if(userType === "CLT"){
    $("input[type=checkbox][class=client_btn][value=" + $("#id_role").val() + "]:first").attr("checked", "true");
  }
  $("#userForm").show();
}
