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

/*
function hey(){
    
    alert(x,'LIAM NEESON')
    
}
*/