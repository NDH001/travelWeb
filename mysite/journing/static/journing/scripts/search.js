function search(cat,redirect_url){
    input = document.getElementById(cat).value
    if (input){
        window.location.href = (`${redirect_url}?q=${input}`)
    }
}

