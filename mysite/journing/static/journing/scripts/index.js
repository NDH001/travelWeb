// explore button smooth scroll to the explore section
function smooth_scroll(){
    document.querySelectorAll('a[href="#index-main-js"]').forEach(anchor =>{
        anchor.addEventListener('click',function(e){
            e.preventDefault();
            document.querySelector(this.getAttribute("href")).scrollIntoView({
                behavior:"smooth"
            });
        });
    })
}

smooth_scroll()
let first_page = document.querySelector('.index-main-first-page')
let page_nav= document.querySelector('.page_nav')

function init_page_nav(){

    if (first_page && window.innerWidth >= 1500){
        page_nav.style.display='none'
        window.addEventListener('scroll',()=>{

        if (window.scrollY >= 800){
            page_nav.style.display = 'block'
        }
        else{
            page_nav.style.display='none'
        }
        })

    }else{
        page_nav.style.display='block'
    } 
}

init_page_nav()
