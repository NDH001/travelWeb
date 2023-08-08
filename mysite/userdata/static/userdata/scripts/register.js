// a js function that modify the reg/login page values (helper function)
function insert_content(){
    
    let welcome = document.getElementById('welcome-js')
    welcome.innerText='Welcome!'

    let form = document.getElementById('sub-button-js')
    form.value = 'Register'

    let member = document.getElementById('member-js')
    member.innerText = 'Already a member ?'

    let action = document.getElementById('action-js')
    action.innerText = 'Sign in !'

    let link = document.getElementById('action-link-js')
    link.href = '/accounts/login'


}

insert_content()