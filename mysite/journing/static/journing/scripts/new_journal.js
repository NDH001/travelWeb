let collection = undefined
function get_data(data){
    collection=data
}

$(document).ready(function(){
    $('.collection-img').draggable({
        revert:'invalid',
        appendTo:'body',
        helper:'clone', 
        start:function(event,ui){
            ui.helper.data('data',collection)
        }
        
    })
    
    $('.drop-area').droppable({
        accept: ".collection-img", // Specify the accepted draggable elements
        drop: function(event, ui) {
            $(this).append(ui.draggable);
            ui.draggable.css({'height':'100%','width':'100%','border-radius':'10px'}); // Reset the image position
            time = $(this).attr('id')
            data = ui.helper.data('data')
            $(`#hour-div-${time} .name`).text(data)
    }
    })
    
})