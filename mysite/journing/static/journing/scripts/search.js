function search(cat,redirect_url){
    input = document.getElementById(cat).value
    if (input){
        // already paginating
        if(redirect_url.indexOf('page')!==-1){
            
            window.location.href = (`${redirect_url}&q=${input}`)
        }else{

            window.location.href = (`${redirect_url}?q=${input}`)
        }
    }
}

