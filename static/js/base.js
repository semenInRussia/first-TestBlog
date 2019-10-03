
function tagget(url){
    var val = $('#taginput').val();
    var data = {
        text: val,
    };
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'text',
        data: data,
        success: function(data){
            $('#contentpage').html(data);
        },
        beforeSend: function(){
            $('#contrentpage').html('<div class=\'mheader\'><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div>')
        }
        });
};
function articleget(url){
    var val = $('#articleinput').val();
    var data = {
        text: val,
    };
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'text',
        data: data,
        success: function(data){
            $('#contentpage').html(data);
        },
        beforeSend: function(){
            $('#contrentpage').html('<div class=\'mheader\'><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div>')
        }
        });
};
function view(){
    var but = $('#clicread'),
        div = but.parent();
    div.css({
        overflow:,
    })
}