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


// records
let journal = {}
let journal_initial = {} // a json to compare to the journal json to see if there is any changes on the page
let journal_id_only = {} // a json with only journal json id for easy setting up of dropped items on page load ( the loop )

// the dimensions for the image in different zones
const LIST_IMG_HEIGHT= '75px'
const LIST_IMG_WIDTH= '120px'
const HOUR_IMG_HEIGHT= '130px'
const HOUR_IMG_WIDTH= '220px'

// the parameters unique to each collection
let activity_name = undefined
let list_name = undefined
let collection_id = undefined

// everytime a collection is clicked, its corresponding data is sent to this javascript
function get_data(data,list,id){
    activity_name=data
    list_name=list
    collection_id = id
}

function enable_drag(target,duplicate=false){
    target.draggable({
        revert:'invalid',
        appendTo:'body',
        helper:'clone', 
        start:function(event,ui){
            // pass the collection parameters during drag (' simple variable reference wouldn't work ')
            ui.helper.data({'activity_name':activity_name})
            ui.helper.data({'list_name':list_name})
            ui.helper.data({'collection_id':collection_id})
            // a variable that determines if the collection is dragged from pool or within a hour div ( false means from the pool)
            ui.helper.data({'duplicate':duplicate})
        }
        
    }) 
}

function enable_drop(target){

    target.droppable({
        accept: ".collection-img",
        drop: function(event, ui) {
            // locate the hour div index --> time
            time = $(this).attr('id')
            list_name = ui.helper.data('list_name')
            activity_name= ui.helper.data('activity_name')
            collection_id = ui.helper.data('collection_id')
            date = $('.date').text().trim()
 
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

            // add the new item to the journal records
            journal[time] = {collection_id,list_name,activity_name,date}
            journal_id_only[time] = collection_id
            
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
            enable_drag(current_element,duplicate=true)

    }
    })

}

function redirect(redirect_date){
            window.location.href= `/journal/edit/${journal_id}/?date=${date_format(new Date(redirect_date))}`
}

function read_existing(){
    // this function gets data from the django get journal view
    $.ajax({
        url: `/journal/edit/get/${journal_id}/?date=${date}`,
        method: 'GET',
        dataType: 'json',
        success: function(response) {
        let records = response['records'];
        console.log(records)

        $('.title').val(title)

        $('.hour-div').each(function(index,element){
            if (records[index]){
                current_record = records[index]

                let img_path = undefined
                let icon_path = undefined
                let list_append_id = undefined
                if (current_record.list_name ==='sight_collections'){
                    img_path = sightimg
                    icon_path=sighticon
                    list_append_id='sight'
                }else if(current_record.list_name ==='food_collections'){
                    img_path = foodimg
                    icon_path=foodicon
                    list_append_id='food'
                }else{
                    img_path = shopimg
                    icon_path=shopicon
                    list_append_id='shop'
                }
                
                collection_id = current_record.collection_id
                list_name = current_record.list_name
                activity_name= current_record.activity_name
                date = current_record.date
                remark = current_record.remark

                // display the earlier dropped images
                $(element).find('.drop-area').html(
                    `<div class="collection-img" ondragstart="get_data('${activity_name}','${list_name}','${collection_id}')" style="height:${HOUR_IMG_HEIGHT};width:${HOUR_IMG_WIDTH};border-radius:10px;">

                    <img src="${img_path}${current_record.img_local}" style="height:${HOUR_IMG_HEIGHT};width:${HOUR_IMG_WIDTH};border-radius:5px;">

                    </div>`
                )

                $(element).find('.name').text(activity_name)
 
                $(element).find('.activity').html(
                    `<img id=${list_append_id} src=${icon_path}></img>`
                    )

                $(element).find('.remarks textarea').val(remark)

                // keep a copy of journal and journal_initial for comparison to check for any changes within a div
                journal[index+1] = {
                    collection_id,
                    list_name,
                    activity_name,
                    date,
                    remark,
                }
                journal_id_only[index+1] = collection_id


                journal_initial[index+1] = {
                    collection_id,
                    list_name,
                    activity_name,
                    date,
                    remark,
                }
            }

        }) 
        },
        error: function(error) {
          console.log('Error:', error);
        }
      });

}

// the drop area needs to be activated again after page read
function enable_drop_area_after_saved(){
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
}

// format the date to standadize
function date_format(date){

    let year = date.getFullYear();
    let month = (date.getMonth() + 1).toString().padStart(2, '0');
    let day = date.getDate().toString().padStart(2, '0');

    return year + '-' + month + '-' + day
}

// get a new date depending on the arrows clicked
function set_date(date_holder,next=true){

    date_to_be = new Date(date_holder.text())
    if (next){
        date_to_be.setDate(date_to_be.getDate() + 1);
    }
    else{
        date_to_be.setDate(date_to_be.getDate() - 1);
    }
    date_holder.text(date_format(date_to_be))
    return date_holder.text()
    

}
// arrow vanish if no more available page should be shown
function check_arrow_visibility(){

    current_date = $('.date').text()
    left_arrow = $('.left-arrow')
    right_arrow = $('.right-arrow')
    if (new Date(current_date) > new Date(start)){
        left_arrow.css({
            'display':'block'
        })
    }else{

        left_arrow.css({
            'display':'none'
        })
    }

    if (new Date(current_date) < new Date(end)){
        right_arrow.css({
            'display':'block'
        })
    }else{

        right_arrow.css({
            'display':'none'
        })
    }

}

// arrows sets the new date on the page and also save the current page
function enable_arrows(){
    
    let date_holder = $('.date').find('h2')
    $('.right-arrow').on('click',function(){
        redirect(set_date(date_holder,next=true))
        check_arrow_visibility()
    })
    
    $('.left-arrow').on('click',function(){
        redirect(set_date(date_holder,next=false))
        check_arrow_visibility()
    })
}

$(document).ready(function(){

    //  the draggable and droppable elements
    let collections = $('.collection-img')
    let drop = $('.drop-area')

    enable_drag(collections,duplicate=false)
    
    enable_drop(drop)
    
    check_arrow_visibility()

    enable_arrows()
  
    if (new_journal=='False'){
        read_existing()
        enable_drop_area_after_saved()
    }

})