// confirm delete
function pop_up_confirmation(id,pk,slug){

    confirmation = confirm('Confirm delete?')
    if (confirmation) {
        window.open(`/sights/info/${pk}/${slug}/comments/delete/?id=${id}`)
      }
}