// get the csrftoken 
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Check if the cookie name matches the requested name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                // Extract and decode the cookie value
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
        
}

$(document).ready(function(){



    $('#connect-js').on('click',function(){
        $.ajax({
            url:'/accounts/connection/peek/follow/',
            type:'post',
            data:{
            },
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            success: function(response){
                console.log(response)
            },
            error:function(xhr,errmsg,err){
                console.log(errmsg)
            }

        })
    })
})