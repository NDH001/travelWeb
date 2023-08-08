// function that redirects the user to either the homepage when they logged out or when they edit the profile
function button_listener(elementid,href_link){
document.getElementById(elementid).addEventListener('click',()=>{
    window.location.href= href_link
})
}

button_listener('profile-logout','/accounts/logout')
button_listener('profile-edit',`/accounts/profile/${user}/edit`)