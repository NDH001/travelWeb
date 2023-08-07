function search(){
    let input = document.getElementById('search-bar-js').value
    if (input){
        window.location.href = (`${index_url}?q=${input}`)
    }
}