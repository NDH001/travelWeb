function search(cat,redirect_url){
    input = document.getElementById(cat).value
    console.log(redirect_url)
    if (input){
        window.location.href = (`${redirect_url}?q=${input}`)
    }
}

