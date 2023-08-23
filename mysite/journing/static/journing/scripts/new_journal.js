let activity_name = undefined
let list_name = undefined
function get_data(data,list){
    activity_name=data
    list_name=list
}
function restore_div(index){
    div = $(`#hour-div-${index}`)
    ori_list = div.find('.activity').find('img').attr('id')
    ori_list = '.' + ori_list + '-list';
    
    current_element = div.find('.drop-area').find('div')
    current_element.css({
        'height':'75px',
        'width':'120px'
    })

    
    $(ori_list).append(current_element)

    div.find('.drop-area').empty()
    div.find('.name').text('-')
    div.find('.activity').html('')

}

$(document).ready(function(){
    let collections = $('.collection-img')
    let drop = $('.drop-area')

    collections.draggable({
        revert:'invalid',
        appendTo:'body',
        helper:'clone', 
        start:function(event,ui){
            ui.helper.data({'activity_name':activity_name})
            ui.helper.data({'list_name':list_name})
        }

    }) 

    drop.droppable({
        accept: ".collection-img",
        drop: function(event, ui) {
            time = $(this).attr('id')
            let current_element = ui.draggable
            console.log(current_element.html())
            
            if ($(this).children().length>0){
                restore_div(time)

            }
            $(this).append(current_element);

            ui.draggable.css({'height':'100%','width':'100%','border-radius':'10px'}); 
            ui.draggable.find('img').css({'height':'100%','width':'100%','border-radius':'5px'})

            $(`#hour-div-${time} .name`).text(ui.helper.data('activity_name'))
            
            let selected_icon = undefined
            let chosen_id = undefined
             
            console.log(ui.helper.data('list_name'))
            console.log(ui.helper.data('activity_name'))
            
            if (ui.helper.data('list_name') === 'sight_collections'){
                selected_icon = sighticon
                chosen_id = 'sight'
            }else if (ui.helper.data('list_name')==='food_collections'){
                selected_icon = foodicon 
                chosen_id = 'food'
            }else{
                selected_icon = shopicon
                chosen_id = 'shop'
            }

            $(`#hour-div-${time} .activity`).html(
                `<img id="${chosen_id}" src="${selected_icon}"/>`
            )




    }
    })


    
})