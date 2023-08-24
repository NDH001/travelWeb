// the dimensions for the image in different zones
const LIST_IMG_HEIGHT= '75px'
const LIST_IMG_WIDTH= '120px'
const HOUR_IMG_HEIGHT= '130px'
const HOUR_IMG_WIDTH= '220px'

// the parameters unique to each collection
let activity_name = undefined
let list_name = undefined
let collection_id = undefined

function get_data(data,list,id){
    activity_name=data
    list_name=list
    collection_id = id
}

// to clear a selected hour div and return the collection back to the pool
function restore_div(index){

    // look for the clicked hour div according to the index passed in
    div = $(`#hour-div-${index}`)
    ori_list = div.find('.activity').find('img').attr('id')
    ori_list = '.' + ori_list + '-list';
    
    // return back to the pool with the preset dimension
    current_element = div.find('.drop-area').find('div')
    current_element.css({
        'height':`${LIST_IMG_HEIGHT}`,
        'width':`${LIST_IMG_WIDTH}`
    })
    div.find('.drop-area').find('div').find('img').css({
        'height':`${LIST_IMG_HEIGHT}`,
        'width':`${LIST_IMG_WIDTH}`
    })

    $(ori_list).append(current_element)
    
    // clear the rest hour sections 
    div.find('.drop-area').empty()
    div.find('.name').text('-')
    div.find('.activity').html('')

}

$(document).ready(function(){

    // records
    journal = {}

    //  the draggable and droppable elements
    let collections = $('.collection-img')
    let drop = $('.drop-area')

    collections.draggable({
        revert:'invalid',
        appendTo:'body',
        helper:'clone', 
        start:function(event,ui){
            // pass the collection parameters during drag (' simple variable reference wouldn't work ')
            ui.helper.data({'activity_name':activity_name})
            ui.helper.data({'list_name':list_name})
            ui.helper.data({'collection_id':collection_id})
            // a variable that determines if the collection is dragged from pool or within a hour div ( false means from the pool)
            ui.helper.data({'duplicate':false})
        }
        
    }) 

    drop.droppable({
        accept: ".collection-img",
        drop: function(event, ui) {

            // locate the hour div index --> time
            time = $(this).attr('id')
            
            list_name = ui.helper.data('list_name')
            activity_name= ui.helper.data('activity_name')
            console.log(ui.helper.data('collection_id'))
            console.log(collection_id,'hi')
            // if collection is dragged and dropped from hour div, duplicate it so that the collection would remain in both hour div
            let current_element = undefined
            if (ui.helper.data('duplicate')){
                current_element = ui.draggable.clone()
            // else remove the collection from the original pool and add it to the div
            }else{
                current_element = ui.draggable
            }
            
            // check if there is existing collection in a hour div
            if ($(this).children().length>0){
                // remove the existing collection to the pool 
                restore_div(time)
            }

            // add the collection to the current hour div
            $(this).append(current_element);

            // set the css of the collection in the hour div
            current_element.css({'height':`${HOUR_IMG_HEIGHT}`,'width':`${HOUR_IMG_WIDTH}`,'border-radius':'10px'}); 
            current_element.find('img').css({'height':`${HOUR_IMG_HEIGHT}`,'width':`${HOUR_IMG_WIDTH}`,'border-radius':'5px'})

            // show the activity name e.g. dong fang ming zhu 
            $(`#hour-div-${time} .name`).text(activity_name)
            
            // set the activity icon and chosen_id is used to keep track which pool did the collection came from 
            let selected_icon = undefined
            let chosen_id = undefined
            
            if (list_name === 'sight_collections'){
                selected_icon = sighticon
                chosen_id = 'sight'
            }else if (list_name==='food_collections'){
                selected_icon = foodicon 
                chosen_id = 'food'
            }else{
                selected_icon = shopicon
                chosen_id = 'shop'
            }

            $(`#hour-div-${time} .activity`).html(
                `<img id="${chosen_id}" src="${selected_icon}"/>`
            )

            // while the collection is dragged within a hour div, set the duplicate condition to true
            current_element.draggable({
                revert:'invalid',
                appendTo:'body',
                helper:'clone', 
                start:function(event,ui){
                    ui.helper.data({'activity_name':activity_name})
                    ui.helper.data({'list_name':list_name})
                    ui.helper.data({'duplicate':true})
                }

            }) 

    }
    })
    
})