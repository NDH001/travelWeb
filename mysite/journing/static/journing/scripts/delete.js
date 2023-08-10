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

// confirm delete
function pop_up_confirmation(id,pk,slug){
    console.log(id)
    confirmation = confirm('Confirm delete?')
    // if (confirmation) {
    //     window.location.href=`/sights/info/${pk}/${slug}/comments/delete/?id=${id}`;
    //   }
    if (confirmation){

    $.ajax({
      url:`/sights/info/${pk}/${slug}/comments/delete/?id=${id}`,
      type:'post',
      data:{
        'id':id
      },
        beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success:function(response){
          console.log(response.message) 
          if (response.message === 'login'){
              window.location.href='/accounts/login'
            }
          // location.reload()
        },
        error: function(xhr, status, error) {
            console.error('Error posting data to Django server:', error);
        }

    })










    } 
}