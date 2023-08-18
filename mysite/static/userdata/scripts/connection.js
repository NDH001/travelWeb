// the function that takes the item id and user id from the templates
let current_user = undefined
let target_user = undefined
let action = undefined
function get_data(current_user_data,target_user_data,act_data){
    current_user = current_user_data
    target_user = target_user_data
    action = act_data
}

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

function follow_unfollow(){

        $.ajax({
            url:`/accounts/connection/peek/${action}/`,
            type:'post',
            data:{
                current_user:`${current_user}`,
                target_user:`${target_user}`,
            },
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

$(document).ready(function(){
// set the redirect link based on the where the current page is

    $('.connect-js').each(function(){
        let connect_button = $(this)

        connect_button.on('click',function(){
            console.log(current_user,target_user,action)
            follow_unfollow()
            
        })
    })
})