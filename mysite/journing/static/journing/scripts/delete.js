function pop_up_confirmation(id,pk,slug){
    confirmation = confirm('Confirm delete?')
    if (confirmation) {
        window.open(`delete/?id=${id}`);
      }
}