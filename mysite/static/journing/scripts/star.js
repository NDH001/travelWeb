// the function that takes the item id and user id from the templates
let item_data = undefined
let user_data = undefined
function get_data(item_id,user_id){
    item_data = item_id 
    user_data = user_id
}


function check_current_url(name){

    let current_url = window.location.href
    if (current_url.indexOf(name)!==-1){
        return true
    }
    return false
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

function starry(redirect_link,action){

        $.ajax({
            url:`/collections/${redirect_link}/${action}/${item_data}/`,
            type:'post',
            data:{
                user:`${user_data}`,
                item:`${item_data}`,
            },
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            success:function(response){
               if (response.message === 'login_required'){
                    console.log(response,response.message,response.login_url)
                   window.location.href=response.login_url
                }
            },
            error: function(xhr, status, error) {
                console.error('Error posting data to Django server:', error);
                window.location.href='/accounts/login/'
            }
        })
}

$(document).ready(function(){
// set the redirect link based on the where the current page is
    let redirect_link = undefined
    if(check_current_url('sight')){
        redirect_link = 'sights'
    }else if(check_current_url('food')){
        redirect_link = 'foods'
    }else{
        redirect_link='shops'
    }

    // control the stars
    $('.select-star-js').each(function(){
    let star = $(this);
  
    star.on('click', function(){
        console.log(item_data)
        let img = star.find('img');
        let link = img.attr('src')
        if (link === lit) {
            img.attr('src', unlit);
            // delete the collection
            starry(redirect_link,'delete')
            
            // add collection
        } else {
            img.attr('src', lit);
            starry(redirect_link,'create')    
        }
        location.reload()
    })
})
})