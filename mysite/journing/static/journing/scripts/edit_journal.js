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

$(document).ready(function(){
    journal = {}
    journal_id_only = {}
    $.ajax({
        url: `/journal/edit/get/${journal_id}/?date=${date}`,
        method: 'GET',
        dataType: 'json',  // Expects JSON data
        success: function(response) {
        let records = response['records'];
        console.log(records)

        $('.hour-div').each(function(index,element){
            if (records[index]){
                current_record = records[index]

                let img_path = undefined
                let icon_path = undefined
                if (current_record.list_name ==='sight_collections'){
                    img_path = sightimg
                    icon_path=sighticon
                }else if(current_record.list_name ==='food_collections'){
                    img_path = foodimg
                    icon_path=foodicon
                }else{
                    img_path = shopimg
                    icon_path=shopicon
                }
                
                $(element).find('.drop-area').html(
                    `<div class="collection-img" ondragstart="get_data('${current_record.activity_name}','${current_record.list_name}','${current_record.collection_id}')" style="height:${HOUR_IMG_HEIGHT};width:${HOUR_IMG_WIDTH};border-radius:10px;">

                    <img src="${img_path}${current_record.img_local}" style="height:${HOUR_IMG_HEIGHT};width:${HOUR_IMG_WIDTH};border-radius:5px;">

                    </div>`
                )

                $(element).find('.name').text(current_record.activity_name)


                $(element).find('.activity').html(
                    `<img src=${icon_path}></img>`
                )
            }

        }) 
        },
        error: function(error) {
          console.log('Error:', error);
        }
      });

      $('.drop-area').on('mouseenter', '.collection-img', function() {
        $(this).draggable({
            revert:'invalid',
            appendTo:'body',
            helper:'clone', 
            start:function(event,ui){
                // pass the collection parameters during drag (' simple variable reference wouldn't work ')
                ui.helper.data({'activity_name':activity_name})
                ui.helper.data({'list_name':list_name})
                ui.helper.data({'collection_id':collection_id})
                // a variable that determines if the collection is dragged from pool or within a hour div ( false means from the pool)
                ui.helper.data({'duplicate':true})
            }
        });
        });

        $('.drop-area').droppable({
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


})