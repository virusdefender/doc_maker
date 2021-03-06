
function get_response_data(){
    $.ajax({
        type: "post",
        url: "/request_api/",
        data: $("form#api_object").serialize(),
        success: function(data){
            var response_json = JSON.parse(data);
            if(response_json.status == "success") {
                $("#response_data")[0].value = response_json.data;
                $("#response_status").html("<code>response status code:" + response_json.response_status_code + "</code>");
                Process("request_data", "formatted_request_data");
                Process("response_data", "formatted_response_data");
            }else{
                alert("Failed to get data, reaponse status code is" + response_json.response_status_code);
            }
        },
        error: function(data){
            alert("Failed to get data");
        }
    });
}


function submit_form(){
    $.ajax({
        type: "post",
        url: $("form#api_object").attr("action"),
        data: $("form#api_object").serialize(),
        success: function(data){
            var response_json = JSON.parse(data);
            if(response_json.status == "success"){
                window.location.href = response_json.redirect
            }
            else{
                alert("Invalid form");
            }
        },
        error:function(data) {
            alert("Failed to submit data");
        }
    });
}