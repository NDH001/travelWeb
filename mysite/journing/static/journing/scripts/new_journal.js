// get the csrftoken 
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Check if the cookie name matches the requested name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                // Extract and decode the cookie value
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
        
}

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
function restore_div(index,new_collection_id=null){

    current_drop_zone_item_id = journal[index].collection_id
    // console.log(current_drop_zone_item_id,'this one')
    // console.log(journal[index].activity_name)
    delete journal[index]
    delete journal_id_only[index]

    // console.log(journal,'journal after delete')
    // console.log(journal_id_only,'after delete')
    // console.log(journal_id_only.includes(current_drop_zone_item_id))
    
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
    // console.log(current_drop_zone_item_id!=new_collection_id)

    // if the current item is not in any other hour div and current item id does not equal to the id of the newly coming in item then return it back to the pool
    if ( !Object.values(journal_id_only).includes(current_drop_zone_item_id) && current_drop_zone_item_id !=new_collection_id){
        current_element.draggable({
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

        $(ori_list).append(current_element)
    }
    
    
    // clear the rest of the hour sections 
    div.find('.drop-area').empty()
    div.find('.name').text('-')
    div.find('.activity').html('')
    div.find('.remarks textarea').val('')

}

$(document).ready(function(){

    // records
    journal = {}
    journal_id_only = {}

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
            collection_id = ui.helper.data('collection_id')
            date = $('.date').text()
 
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
                restore_div(time,collection_id)
            }

            journal[time] = {collection_id,list_name,activity_name,date}
            journal_id_only[time] = collection_id
            
            // console.log(journal)
            // console.log(journal_id_only)

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
                    ui.helper.data({'collection_id':collection_id})
                    ui.helper.data({'duplicate':true})
                }

            }) 

    }
    })

    $('.save').on('click',function(){

        let filled_hours_keys = Object.keys(journal)
        
        for (let key in filled_hours_keys){
            filled_hour = filled_hours_keys[key]
            let filled_hour_remark = $(`#hour-div-${filled_hour}`).find('.remarks textarea').val()
            
            journal[filled_hour]['remark'] = filled_hour_remark
        }
        journal['uuid'] = journal_id
        
        console.log(journal)
        $.ajax({
            url:`/journal/save/`,
            type:'post',
            data:JSON.stringify(journal),
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            success:function(response){
                if (response.message === 'login_required'){
                    console.log(response,response.message,response.login_url)
                    window.location.href=response.login_url
                }
            },
            error: function(xhr, status, error) {
                console.error('Error posting data to Django server:', error);
                // window.location.href='/accounts/login/'
            }
        })
    })
    
})