$(document).ready(function(){
    $('.collection-img').draggable({
        revert:'invalid',
        appendTo:'body',
        helper:'clone',
    })

    $('.drop-area').droppable({
        accept: ".collection-img", // Specify the accepted draggable elements
        drop: function(event, ui) {
            $(this).append(ui.draggable);
            ui.draggable.css({'height':'100%','width':'100%','border-radius':'10px'}); // Reset the image position
    }
    })
    
})