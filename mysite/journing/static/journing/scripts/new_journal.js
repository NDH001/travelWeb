let collection = undefined
let list_name = undefined
function get_data(data,list){
    collection=data
    list_name=list
}
function restore_div(index){
    div = $(`#hour-div-${index}`)
    div.find('.drop-area').empty()
    div.find('.name').text('-')
    original.css({'height':'80px','width':'120px'})
    $('.sight-list').append(original)
    original=null

}

$(document).ready(function(){
    let collections = $('.collection-img')
    let drop = $('.drop-area')

    collections.draggable({
        revert:'invalid',
        appendTo:'body',
        helper:'clone', 
        start:function(event,ui){
            ui.helper.data({'data':collection})
            ui.helper.data({'list_name':list_name})
            original = $(this)

        }
        
    })
    
    drop.droppable({
        accept: ".collection-img",
        drop: function(event, ui) {
            if ($(this).children().length===0){
                $(this).append(ui.draggable);
                ui.draggable.css({'height':'100%','width':'100%','border-radius':'10px'}); // Reset the image position
                ui.draggable.find('img').css({'height':'100%','width':'100%','border-radius':'5px'})
                time = $(this).attr('id')
                $(`#hour-div-${time} .name`).text(ui.helper.data('data'))
                $(`#hour-div-${time} .activity`).html(
                    `<img src="${sighticon}"/>`
                )
            }
    }
    })


    
})