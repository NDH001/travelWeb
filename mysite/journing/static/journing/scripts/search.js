function search(){
    var input = document.getElementById('search-bar-js').value
    if (input){
        window.open(`?=${input}`)
    }
}