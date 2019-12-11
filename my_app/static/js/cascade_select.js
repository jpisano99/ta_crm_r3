$(document).ready(function(){
    //alert("doc ready ... ");

    var tmp = $("#level1").val();
    if (tmp == null){
        var tmp1 = load_vals();
        var tmp2 = look_up(tmp1,"1");
    }

    $("#level1").change(function(){
        $("#level2").html("");
        $("#level3").html("");
        $("#level4").html("");
        $("#level5").html("");
        var tmp1 = load_vals();
        var tmp2 = look_up(tmp1,"2");
     });

    $("#level2").change(function(){
        $("#level3").html("");
        $("#level4").html("");
        $("#level5").html("");
        var tmp1 = load_vals();
        var tmp2 = look_up(tmp1,"3");
     });

    $("#level3").change(function(){
        $("#level4").html("");
        $("#level5").html("");
        var tmp1 = load_vals();
        var tmp2 = look_up(tmp1,"4");
     });

    $("#level4").change(function(){
        $("#level5").html("");
        var tmp1 = load_vals();
        var tmp2 = look_up(tmp1,"5");
     });
});

function load_vals(){
    var lev1_val = $("#level1").val();
    var lev2_val = $("#level2").val();
    var lev3_val = $("#level3").val();
    var lev4_val = $("#level4").val();
    var hierarchy = {level1:lev1_val,level2:lev2_val,level3:lev3_val,level4:lev4_val}
    return hierarchy;
}

function look_up(hierarchy,query_level){
    $.ajax({
        type: "POST",
        url: "/cascade_select",
        contentType: "text/json; charset=utf-8",
        data: JSON.stringify(hierarchy),
        success: function (data) {
            var newoptions = "";
            newoptions = '<option disabled selected value="start"> -- select an option -- </option>'
            for (var level of data.levels) {
                newoptions += '<option value="' + level + '">' + level + '</option>';
            }
            tmp99 = "#level"+query_level
            $(tmp99).html(newoptions);
            $(tmp99).prop('disabled', false);
        }
    });
}
