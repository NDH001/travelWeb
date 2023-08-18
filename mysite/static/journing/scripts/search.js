// retrieve the query string from the search bar and perform query filtering and redirect to that page
function search(cat,redirect_url){
    input = document.getElementById(cat).value
    console.log(redirect_url)
    if (input){
        window.location.href = (`${redirect_url}?q=${input}`)
    }
}

