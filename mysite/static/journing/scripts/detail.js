// check the current page to see what cat is the page at right now
function check_current_url(name){
    let current_url = window.location.href
    if (current_url.indexOf(name)!==-1){
        return true
    }
    return false
}

function setTabColor(name){
    
    $(name).css({
        'background-color':'black'
    })
}

$(document).ready(function(){
    
    // control the tab color
    if (check_current_url('shops')){
        console.log('shop')
        setTabColor('.shop-js')
    } else if (check_current_url('foods')){
        console.log('food')
        setTabColor('.food-js')
    }else{
        console.log('attraction')
        setTabColor('.attraction-js')
    }  

    })