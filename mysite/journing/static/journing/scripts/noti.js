$(document).ready(function(){

    $('.noti-button-div').on('click',function(){
        noti_box = $('.all-noti-js')
        $('.dot').css({
            'display':'none'
        })
        if (noti_box.css('display')=== 'none'){
            noti_box.css({
                'display':'flex',
                'flex-direction':'column',
                'top':'50px'
            })
        }else{
            noti_box.css({
                'display':'none'
            })
        }   
        reset_noti()
    })
})

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

function reset_noti(){
        
        $.ajax({
            url:`/reset/notification/`,
            type:'post',
            data:{},
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            success:function(response){
                console.log(response.message)
               if (response.message === 'login_required'){
                    console.log(response,response.message,response.login_url)
                   window.location.href=response.login_url
                }
            },
            error: function(xhr, status, error) {
                console.error('Error posting data to Django server:', error);
            }
        })
}