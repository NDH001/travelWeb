// function that redirects the user to either the homepage when they logged out or when they edit the profile
function button_listener(elementid,href_link){
document.getElementById(elementid).addEventListener('click',()=>{
    window.location.href= href_link
})
}

button_listener('profile-logout','/accounts/logout')
button_listener('profile-edit',`/accounts/profile/${user.username}/edit`)


function highlight(id){

// set all tabs color to transparent ( matching the box background color --> 30,30,30 in this case)
    $('.tab-js').each(function(){
        let tab = $(this)
        tab.css({
            'background-color':'rgb(30,30,30)'
        })
        
    })

    let selected_tab = '#'+id
// set the selected tab to black
    $(selected_tab).css({
        'background-color':'black'
    })

// hide all the tab details
    $('.tab-detail-js').each(function(){
        let tab_detail = $(this)
        tab_detail.css({
            'display':'none'
        })
    })
    let selected_tab_detail = '#'+id+'-detail'
// only show the selected tab details
    $(selected_tab_detail).css({
        'display':'block'
    })

}